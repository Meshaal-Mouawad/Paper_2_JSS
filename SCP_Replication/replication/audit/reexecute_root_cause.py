from pathlib import Path
import ast,re,html,hashlib,json
B=Path(__file__).resolve().parents[1]
p=B/'generator_source/main.py'
expected='e4a26797c6c7dccb49603745720e4dce7b85bd27e2c2c86f8292183b4b2188c5'
assert hashlib.sha256(p.read_bytes()).hexdigest()==expected
nodes=[n for n in ast.walk(ast.parse(p.read_text())) if isinstance(n,ast.FunctionDef) and n.name in ['_code_role_for_line','_walkthrough_safeguards_html']]
env={'re':re,'escape':html.escape,'formula_mismatch':False,'has_any_conflict':False}
exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),str(p),'exec'),env)
details=json.loads((B/'evidence/primary/audit/lineage_defect_details_r3.json').read_text())
r=[]
for doc in details:
 for entry in doc['errors']:
  observed=env['_code_role_for_line'](entry['code'])
  r.append({'document':doc['dossier'],'source':entry['code'],'published':entry['description'],'regenerated':observed,'exact_match':observed==entry['description']})
for name in ['control_no_conflict_yield.py','conflict_formula_margin.py']:
 source=B/'evidence/detailed_cases'/name
 env['kpi_data']={'code_context':source.read_text()}
 r.append({'source_file':str(source.relative_to(B)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'regenerated_safeguards':env['_walkthrough_safeguards_html']()})
print(json.dumps({'generator_sha256':expected,'method':'Reexecution of two unchanged functions, not complete generator regeneration','results':r},indent=2))
