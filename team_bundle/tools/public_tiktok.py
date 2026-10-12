import argparse,json,re,time,urllib.request,os
from pathlib import Path
import yt_dlp
from yt_dlp.extractor.tiktok import TikTokBaseIE
from metrics import calculate
ORIGINAL=TikTokBaseIE._parse_aweme_video_web

def patched(self,detail,*args,**kwargs):
    row=ORIGINAL(self,detail,*args,**kwargs);row['is_pinned']=bool(detail.get('isPinnedItem'));return row
TikTokBaseIE._parse_aweme_video_web=patched

def collect(handle):
    handle=handle.lower().lstrip('@')
    if not re.fullmatch(r'[a-z0-9_.]+',handle):raise ValueError('无效公开handle。')
    result={'handle':handle,'canonical_url':f'https://www.tiktok.com/@{handle}','checked_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'decision':'review'}
    request=urllib.request.Request(result['canonical_url'],headers={'User-Agent':'Mozilla/5.0','Accept-Language':'en-US,en;q=0.9'})
    try:
        with urllib.request.urlopen(request,timeout=30)as response:body=response.read().decode()
        match=re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>',body,re.S)
        info=json.loads(match.group(1))['__DEFAULT_SCOPE__']['webapp.user-detail']['userInfo']
        user,stats=info['user'],info['stats'];actual=user['uniqueId'].lower()
        if actual!=handle:raise ValueError('公开handle发生变化，需重新排重和核验。')
        bio=user.get('signature','');result.update(followers=stats.get('followerCount'),bio=bio,
            public_bio_emails=sorted(set(re.findall(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}',bio,re.I))),bio_link=(user.get('bioLink')or{}).get('link',''))
    except Exception:result['public_profile_status']='unknown';result['public_bio_emails']=[]
    options={'quiet':True,'no_warnings':True,'skip_download':True,'extract_flat':'in_playlist','playlistend':30,'socket_timeout':25,'retries':0}
    proxy=os.environ.get('HTTPS_PROXY')or os.environ.get('HTTP_PROXY')
    if proxy:options['proxy']=proxy
    with yt_dlp.YoutubeDL(options)as ydl:payload=ydl.extract_info(result['canonical_url'],download=False)
    entries=list(payload.get('entries')or[])
    unpinned=[v for v in entries if not v.get('is_pinned')]
    if any(not isinstance(v.get('timestamp'),(int,float))for v in unpinned):
        raise ValueError('视频发布时间未知，无法证明最新窗口；禁止跳过并用更旧视频补齐。')
    entries=sorted(unpinned,key=lambda v:v['timestamp'],reverse=True)[:12]
    result['videos']=[{'id':str(v.get('id')or''),'timestamp':v.get('timestamp'),'views':v.get('view_count'),
        'likes':v.get('like_count'),'comments':v.get('comment_count'),'is_pinned':False,
        'url':f'https://www.tiktok.com/@{handle}/video/{v.get("id")}', 'title':v.get('title') or v.get('description')or'',
        'track':v.get('track'),'artists':v.get('artists')or[]}for v in entries]
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('handle');p.add_argument('--output',required=True);p.add_argument('--mean-views-min',required=True,type=float);p.add_argument('--engagement-min',required=True,type=float);p.add_argument('--per-video-min',type=float);a=p.parse_args()
    try:
        d=collect(a.handle);d['metrics']=calculate(d['videos'],a.mean_views_min,a.engagement_min,a.per_video_min)
        d['latest_age_days']=(time.time()-max(v['timestamp']for v in d['videos']))/86400
    except Exception as e:d={'handle':a.handle,'decision':'review','error_class':type(e).__name__,'reason':'公开证据不完整或访问失败，未知不算通过。'}
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'handle':a.handle,'decision':d.get('decision'),'numeric_pass':(d.get('metrics')or{}).get('numeric_pass'),'output':str(out)},ensure_ascii=False))
if __name__=='__main__':main()
