#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys, shutil, tempfile, hashlib
B=Path(__file__).resolve().parent; O=B/'audit'; results=[]
def hashes(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
def run(command,cwd,log):
    cmd=[sys.executable]+command[1:] if command[0]=='python' else command
    p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True)
    (O/log).write_text(p.stdout+p.stderr)
    results.append({'command':command,'cwd':str(cwd.relative_to(B)) if cwd.is_relative_to(B) else 'temporary copy','exit_code':p.returncode,'log':log})
    if p.returncode:raise RuntimeError('Failed '+str(command)+'; see '+log)
for script in ['independent_recompute.py','build_source_role_ledger.py','reexecute_root_cause.py']:
    run(['python','audit/'+script],B,'packaged_'+script+'.log')
ev=Path('evaluation_r15/LEAP_Paper2_IST_R15_REVISION_PACKAGE/Independent_Evaluation_R15/independent_evaluation')
with tempfile.TemporaryDirectory(prefix='leap_paper2_audit_') as temp:
    for name,source,commands in [('technical',B/'evidence',json.loads((O/'rerun_commands.json').read_text())),('statistical',B/ev,json.loads((O/'evaluation_rerun_commands.json').read_text())['commands'])]:
        work=Path(temp)/name;shutil.copytree(source,work);before=hashes(work)
        for i,item in enumerate(commands):run(item['command'],work,'packaged_'+name+f'_{i+1:02}.log')
        after=hashes(work); changed=[k for k in before if before[k]!=after.get(k)]
        results.append({'corpus':name,'changed_existing_files':changed})
        assert not changed, changed
summary=json.loads((O/'independent_recompute.json').read_text())
assert summary['original_reconciliation']['checked_labels']==summary['original_reconciliation']['equal']==336
assert all(not v['bad'] for v in summary['manifest_integrity'].values())
(O/'packaged_rerun.json').write_text(json.dumps({'status':'PASS','commands_and_integrity':results},indent=2)+'\n')
print('PASS: independent statistics, 18-document ledger, generator functions, 10 technical and 4 statistical commands; preserved manifests unchanged.')
