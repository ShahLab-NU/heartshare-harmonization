"""Validate the published notebook set against its compatibility record."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
record = json.loads((root / 'notebook_compatibility.json').read_text())
expected = record['notebooks']
actual = {p.name for p in (root / 'notebooks').glob('*.ipynb')}
if actual != set(expected):
    raise ValueError('Notebook inventory differs from notebook_compatibility.json')
for name, asset in expected.items():
    path = root / 'notebooks' / name
    if hashlib.sha256(path.read_bytes()).hexdigest() != asset['sha256']:
        raise ValueError(f'{name}: checksum differs from the validated release record')
    document = json.loads(path.read_text())
    for index, cell in enumerate(document['cells']):
        if cell['cell_type'] != 'code':
            continue
        if cell.get('outputs') or cell.get('execution_count') is not None:
            raise ValueError(f'{name} cell {index}: clear outputs before publishing')
        compile(''.join(cell['source']), f'{name}:cell-{index}', 'exec')
    print(f'PASS {name}: checksum, syntax, and cleared outputs')
print('Runtime execution must also be validated against the matching BDC release before publishing.')
