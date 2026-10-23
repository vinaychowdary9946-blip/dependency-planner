"""Validated dependency planning, earliest starts, slack and impact analysis."""
import heapq
import json
import math


def plan(tasks):
    if not isinstance(tasks,list) or not tasks or len(tasks)>1000:
        raise ValueError('Provide 1–1000 tasks')
    graph={}
    for task in tasks:
        if not isinstance(task,dict):
            raise ValueError('Each task must be an object')
        ident=task.get('id'); duration=task.get('duration'); deps=task.get('deps',[])
        if not isinstance(ident,str) or not ident.strip() or ident in graph:
            raise ValueError('Task IDs must be unique nonempty strings')
        if type(duration) not in (int,float) or not 0 < duration <= 1_000_000_000:
            raise ValueError('Duration must be positive and at most 1,000,000,000')
        if not isinstance(deps,list) or any(not isinstance(d,str) for d in deps) or len(set(deps))!=len(deps):
            raise ValueError('Dependencies must be unique task IDs')
        graph[ident]={'duration':duration,'deps':deps}
    children={k:[] for k in graph}; degree={k:len(v['deps']) for k,v in graph.items()}
    for k,v in graph.items():
        for d in v['deps']:
            if d not in graph: raise ValueError('Unknown dependency: '+d)
            children[d].append(k)
    ready=[k for k in graph if not degree[k]]; heapq.heapify(ready)
    order=[]; starts={}; ends={}
    while ready:
        k=heapq.heappop(ready); order.append(k)
        starts[k]=max((ends[d] for d in graph[k]['deps']),default=0)
        ends[k]=starts[k]+graph[k]['duration']
        for c in children[k]:
            degree[c]-=1
            if degree[c]==0: heapq.heappush(ready,c)
    if len(order)!=len(graph):
        raise ValueError('Cycle blocks tasks: '+', '.join(sorted(k for k in degree if degree[k])))
    total=max(ends.values()); latest={}
    for k in reversed(order):
        latest[k]=min((latest[c] for c in children[k]),default=total)-graph[k]['duration']
    return {'duration':total,'order':order,'tasks':[{'id':k,'start':starts[k],'finish':ends[k],'slack':round(latest[k]-starts[k],10),'critical':math.isclose(latest[k],starts[k],rel_tol=0,abs_tol=1e-9)} for k in order]}


def impacted(tasks, changed):
    plan(tasks)
    ids={t['id'] for t in tasks}
    if changed not in ids: raise ValueError('Unknown task')
    seen={changed}
    while True:
        more={t['id'] for t in tasks if any(d in seen for d in t.get('deps',[]))}
        if more<=seen: return sorted(seen)
        seen|=more


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('file'); p.add_argument('--impact')
    a=p.parse_args()
    with open(a.file,encoding='utf-8') as f: tasks=json.load(f)
    print(json.dumps(impacted(tasks,a.impact) if a.impact else plan(tasks),indent=2))
