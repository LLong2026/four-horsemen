from pathlib import Path
import json,hashlib
from contract_validator import validate
r=Path(__file__).resolve().parent
i=json.loads((r/'instrument.json').read_text());f=json.loads((r/'PRETEST_FREEZE.json').read_text())
for n in ['instrument.json','frozen_prompt_v2.txt','contract_validator.py']:
 assert hashlib.sha256((r/n).read_bytes()).hexdigest()==f['files'][n],n
files=sorted((r/'captures').glob('*/*.txt'));assert len(files)==8
for p in files:
 v=validate(p.read_text(),i);assert v['accepted'],(str(p),v)
 print(p.relative_to(r),v['decision_count'],v['canonical_sha256'])
print('8/8 published response captures match the 12-case canonical target. No live execution performed.')
