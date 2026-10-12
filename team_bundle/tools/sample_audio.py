"""Collect public audio evidence; automatic transcripts are never final decisions."""
import argparse,json,subprocess,os
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('public_json');p.add_argument('--samples',required=True,type=int);p.add_argument('--output-dir',required=True);a=p.parse_args()
    d=json.loads(Path(a.public_json).read_text());out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True);results=[]
    for v in d['videos'][:a.samples]:
        prefix=out/v['id'];row={'video_id':v['id'],'url':v['url'],'track':v.get('track'),'artists':v.get('artists'),'semantic_decision':'pending_review'}
        try:
            c=subprocess.run(['yt-dlp','--no-playlist','--quiet','--no-warnings','--socket-timeout','20','--retries','0',
                '-f','bestaudio/best','-o',str(prefix)+'.%(ext)s',v['url']],capture_output=True,text=True,timeout=90)
            files=list(out.glob(v['id']+'.*'))
            if c.returncode or not files:raise RuntimeError('download_failed')
            audio=prefix.with_suffix('.wav');subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(files[0]),'-t','120','-vn','-ac','1','-ar','16000',str(audio)],check=True,capture_output=True,timeout=60)
            row['audio_file']=str(audio)
            try:
                import mlx_whisper
                t=mlx_whisper.transcribe(str(audio),path_or_hf_repo='mlx-community/whisper-tiny',verbose=None,temperature=0.0,condition_on_previous_text=False)
                row.update(automatic_language=t.get('language'),transcript=t.get('text'))
            except ImportError:row['transcript_status']='需要Agent或人工听音核验；未安装本地转录引擎'
        except Exception:row['evidence_status']='unavailable'
        results.append(row);(out/'samples.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'samples':len(results),'final_semantic_decision':'pending_review'},ensure_ascii=False))
if __name__=='__main__':main()
