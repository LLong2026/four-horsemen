"""Offline, fail-closed synthetic contract checker. NO execution or external effects."""
from pathlib import Path
from decimal import Decimal
import json,hashlib
KEYS=['position','anomaly_type','playbook','playbook_id','match_type','steps_executed','status']
STEPS='isolation,healing,verification'
def derive(instrument):
 out=[]
 for a in instrument['stream']:
  choices=sorted((p for p in instrument['roster'] if p['anomaly_type']==a['anomaly_type']),key=lambda p:p['record_id'])
  p=choices[0] if choices else None
  held=p is not None and Decimal(str(a['confidence_score']))<Decimal(str(p['confidence_threshold']))
  out.append(dict(zip(KEYS,[a['position'],a['anomaly_type'],p['playbook'] if p else None,p['record_id'] if p else None,'exact' if p else 'none',STEPS if p and not held else None,'escalated' if not p else 'detected' if held else 'resolved'])))
 return out
def canonical(data):
 return json.dumps(data,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('utf-8')
def reject_constant(value):raise ValueError('Nonfinite JSON value: '+value)
def unique_pairs(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('Duplicate JSON key: '+k)
  d[k]=v
 return d
def validate(text,instrument):
 try:
  if not isinstance(text,str):raise ValueError('Text required')
  data=json.loads(text,object_pairs_hook=unique_pairs,parse_constant=reject_constant)
  expected=derive(instrument)
  if not isinstance(data,list) or len(data)!=len(expected):raise ValueError('Wrong array length/type')
  for idx,(a,b) in enumerate(zip(data,expected)):
   if not isinstance(a,dict) or list(a)!=KEYS:raise ValueError('Wrong keys/order at '+str(idx))
   if type(a['position']) is not int:raise ValueError('Position must be a JSON integer')
   for key in KEYS[1:]:
    if type(a[key]) is not type(b[key]):raise ValueError('Field type mismatch: '+key)
   if a!=b:raise ValueError('Tuple content mismatch at '+str(idx))
  return {'accepted':True,'canonical_sha256':hashlib.sha256(canonical(data)).hexdigest(),'decision_count':len(data),'execution_performed':False}
 except (ValueError,TypeError,KeyError) as e:return {'accepted':False,'error':str(e),'execution_performed':False}
if __name__=='__main__':
 import sys
 root=Path(__file__).resolve().parent
 instrument=json.loads((root/'instrument.json').read_text())
 result=validate(Path(sys.argv[1]).read_text(),instrument)
 print(json.dumps(result,indent=2));sys.exit(0 if result['accepted'] else 1)
