"""Pinned official CLI; one task ledger, conservative reservation and no automatic key fallback."""
import argparse, json, os, re, subprocess, sys
from decimal import Decimal
from pathlib import Path
from datetime import datetime, timezone
from credentials import load_keys
ROOT=Path(__file__).resolve().parents[1]

def atomic(path,data):
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');os.chmod(tmp,0o600);os.replace(tmp,path)

def sanitize(value,keys):
    if isinstance(value,dict):
        return {k:('[REDACTED]' if re.search(r'api.?key|token|password|secret|authorization',k,re.I) else sanitize(v,keys))for k,v in value.items()}
    if isinstance(value,list):return [sanitize(v,keys)for v in value]
    if isinstance(value,str):
        for key in keys:value=value.replace(key,'[REDACTED]')
        return re.sub(r'nox_[A-Za-z0-9._-]+','[REDACTED]',value)
    return value

def plan(args):
    if not args:raise RuntimeError('缺少Nox命令。')
    forbidden=['--api-key','--config','--env','--server','--verbose','--trace-json','--plain']
    if any(any(x==f or x.startswith(f+'=')for f in forbidden)or x.startswith('nox_') for x in args):raise RuntimeError('禁止凭证参数、环境覆盖或调试输出。')
    if args==['quota']or args[:2]==['quota','usage']:return Decimal('0')
    if args[:2]==['creator','profile']:return Decimal('5')
    if args[:2]==['creator','search']:
        if '--page_size' in args and int(args[args.index('--page_size')+1])>100:raise RuntimeError('page_size必须<=100。')
        return Decimal('5')
    raise RuntimeError('本工具仅允许quota、creator search/profile，不允许外联、联系人导出或写操作。')

def perform(directory,args,slot=1,runner=subprocess.run,key_loader=load_keys):
    directory=Path(directory);file=directory/'state.json';lock=directory/'.call.lock'
    fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.close(fd)
    try:
        state=json.loads(file.read_text());reserve=plan(args)
        if state.get('blocked'):raise RuntimeError('已有扣费不明调用，先对账；不可自动续跑。')
        consumed=Decimal(str(state['consumed']));budget=Decimal(str(state['budget']))
        if consumed+reserve>budget:raise RuntimeError('预算不足以保守预留本次最多5 credits，停止付费调用。')
        keys=key_loader()
        if not 1<=slot<=len(keys):raise RuntimeError('key槽位不存在。')
        entry=ROOT/'node_modules/@noxinfluencer/cli/dist/main.js'
        if runner is subprocess.run and not entry.is_file():raise RuntimeError('先在team_bundle目录执行npm install --ignore-scripts。')
        env=os.environ.copy();env['NOXINFLUENCER_API_KEY']=keys[slot-1]
        entry_args=['node',str(entry),'--env','online',*args]
        # Persist uncertainty before network I/O; interruption cannot silently erase billable work.
        state['blocked']=True;state['inflight']={'command':args,'slot':slot,'reserved':float(reserve)};atomic(file,state)
        try:
            completed=runner(entry_args,env=env,capture_output=True,text=True,timeout=120)
            payload=json.loads(completed.stdout)
        except Exception:raise RuntimeError('请求中断或响应丢失：消耗unavailable；已锁住付费续跑。')from None
        used=(payload.get('credits')or{}).get('used')
        if reserve==0 and payload.get('success') and used is None:used=0
        if isinstance(used,bool)or not isinstance(used,(int,float))or used<0:raise RuntimeError('返回缺少明确单次用量；已停止续跑，不能按0计费。')
        request_id=(payload.get('meta')or{}).get('request_id')
        known={x.get('request_id')for x in state['calls']if x.get('request_id')}
        if request_id and request_id in known:raise RuntimeError('重复request_id，先对账；禁止重复累加。')
        state['calls'].append({'observed_at':datetime.now(timezone.utc).isoformat(),'command':args,'key_slot':slot,'used':used,'request_id':request_id,'success':payload.get('success')})
        state['consumed']=float(consumed+Decimal(str(used)))
        state['blocked']=state['consumed']>state['budget'] or Decimal(str(used))>reserve
        state.pop('inflight',None);atomic(file,state)
        clean=sanitize(payload,keys)
        atomic(directory/f'response-{len(state["calls"]):04d}.json',clean)
        if state['blocked']:raise RuntimeError('实际扣费超过本次预留/总预算；已停止续跑。')
        return clean
    finally:lock.unlink(missing_ok=True)

def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
    i=s.add_parser('init');i.add_argument('--root',required=True);i.add_argument('--task-id',required=True);i.add_argument('--budget',required=True,type=float)
    c=s.add_parser('call');c.add_argument('--root',required=True);c.add_argument('--slot',type=int,default=1);c.add_argument('nox_args',nargs=argparse.REMAINDER)
    t=s.add_parser('status');t.add_argument('--root',required=True);a=p.parse_args();r=Path(a.root)
    if a.command=='init':
        if a.budget<0:raise RuntimeError('预算不能为负。')
        r.mkdir(parents=True,exist_ok=True)
        if(r/'state.json').exists():raise RuntimeError('任务状态已存在，禁止重置消耗。')
        atomic(r/'state.json',{'task_id':a.task_id,'budget':a.budget,'consumed':0,'calls':[],'blocked':False});print('任务预算已初始化。')
    elif a.command=='status':
        d=json.loads((r/'state.json').read_text());print(json.dumps({'task_id':d['task_id'],'budget':d['budget'],'consumed':('unavailable' if d['blocked'] else d['consumed']),'confirmed_consumed':d['consumed'],'calls':len(d['calls']),'blocked':d['blocked'],'account_balance':'unavailable'},ensure_ascii=False))
    else:
        args=a.nox_args;args=args[1:]if args[:1]==['--']else args;print(json.dumps(perform(r,args,a.slot),ensure_ascii=False))
if __name__=='__main__':
    try:main()
    except Exception as e:print(str(e)if isinstance(e,RuntimeError)else'操作失败；敏感诊断不输出。',file=sys.stderr);sys.exit(1)
