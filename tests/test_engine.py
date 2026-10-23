import unittest,random
from graphlib import TopologicalSorter
from planner import plan,impacted
class PlannerTests(unittest.TestCase):
 def setUp(self): self.tasks=[{'id':'A','duration':2,'deps':[]},{'id':'B','duration':5,'deps':['A']},{'id':'C','duration':1,'deps':['A']},{'id':'D','duration':1,'deps':['B','C']}]
 def test_critical_and_slack(self):
  p=plan(self.tasks); self.assertEqual(p['duration'],8); self.assertEqual(next(t for t in p['tasks'] if t['id']=='C')['slack'],4)
 def test_impact(self): self.assertEqual(impacted(self.tasks,'C'),['C','D'])
 def test_cycle(self):
  self.tasks[0]['deps']=['D']
  with self.assertRaisesRegex(ValueError,'Cycle'): plan(self.tasks)
 def test_unknown(self):
  self.tasks[0]['deps']=['missing']
  with self.assertRaisesRegex(ValueError,'Unknown'): plan(self.tasks)
 def test_validation(self):
  for t in [[],[{'id':'x','duration':float('nan')}],[{'id':'x','duration':True}],self.tasks+[self.tasks[0]]]:
   with self.assertRaises(ValueError): plan(t)
 def test_disconnected(self): self.assertEqual(plan([{'id':'a','duration':1},{'id':'b','duration':3}])['duration'],3)
 def test_random_dags_against_graphlib(self):
  rng=random.Random(7)
  for _ in range(30):
   ts=[{'id':str(i),'duration':rng.randint(1,10),'deps':[str(j) for j in range(i) if rng.random()<.2]} for i in range(40)]
   p=plan(ts); canonical=list(TopologicalSorter({t['id']:t['deps'] for t in ts}).static_order())
   self.assertEqual(set(p['order']),set(canonical)); positions={k:i for i,k in enumerate(p['order'])}
   for t in ts:
    for d in t['deps']: self.assertLess(positions[d],positions[t['id']])
 def test_large_timestamp_slack_is_not_critical(self):
  tasks=[{'id':'a','duration':1000000000}, {'id':'b','duration':1,'deps':['a']}, {'id':'c','duration':1.5,'deps':['a']}]
  b=next(t for t in plan(tasks)['tasks'] if t['id']=='b')
  self.assertEqual(b['slack'],.5)
  self.assertFalse(b['critical'])
 def test_extreme_durations_rejected(self):
  for duration in [float('inf'),10**1000,1000000001]:
   with self.assertRaises(ValueError): plan([{'id':'a','duration':duration}])
if __name__=='__main__': unittest.main()
