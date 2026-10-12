"""Metric definitions must come from the brief, not a previous project."""
def calculate(videos, mean_views_min, engagement_min, per_video_min=None):
    if mean_views_min<0 or not 0<=engagement_min<1 or(per_video_min is not None and per_video_min<0):raise ValueError('无效需求门槛。')
    if len(videos)!=12:raise ValueError('必须取得最新12条非置顶视频。')
    for v in videos:
        if v.get('is_pinned'):raise ValueError('置顶视频不进入窗口。')
        for key in ['views','likes','comments','timestamp']:
            if isinstance(v.get(key),bool)or not isinstance(v.get(key),(int,float))or v[key]<0:
                raise ValueError(f'必需指标{key}未知或无效；不能当0。')
    ordered=sorted(videos,key=lambda v:v['timestamp'],reverse=True)
    lo=min(range(12),key=lambda i:ordered[i]['views'])
    hi=max((i for i in range(12)if i!=lo),key=lambda i:ordered[i]['views'])
    kept=[v for i,v in enumerate(ordered)if i not in {lo,hi}]
    total=sum(v['views']for v in kept)
    if total<=0:raise ValueError('保留视频总播放为0，互动率不可计算。')
    mean=total/10;rate=sum(v['likes']+v['comments']for v in kept)/total
    return {'retained_mean_views':mean,'aggregate_engagement_rate':rate,'retained_ids':[v['id']for v in kept],
            'removed_low_id':ordered[lo]['id'],'removed_high_id':ordered[hi]['id'],
            'numeric_pass':mean>mean_views_min and rate>engagement_min and(per_video_min is None or all(v['views']>per_video_min for v in kept)),
            'semantic_review':'pending','email_ownership':'pending','historical_dedupe':'pending'}
