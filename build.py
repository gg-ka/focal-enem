"""Baixa a base pública do projeto ardotheedu/api-enem durante o deploy.
Nenhuma dependência externa necessária (Python padrão)."""
import sqlite3
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / 'enem_questions.db'
URL = 'https://raw.githubusercontent.com/ardotheedu/api-enem/main/enem_questions.db'

print('FOCAL: obtendo base de questões SQLite...', flush=True)
req = urllib.request.Request(URL, headers={'User-Agent': 'Focal-ENEM/1.0 (deploy)'})
with urllib.request.urlopen(req, timeout=90) as stream:
    with TARGET.with_suffix('.db.tmp').open('wb') as f:
        while data := stream.read(262144):
            f.write(data)
tmp = TARGET.with_suffix('.db.tmp')
if tmp.stat().st_size < 100_000 or tmp.open('rb').read(16) != b'SQLite format 3\x00':
    tmp.unlink(missing_ok=True)
    raise RuntimeError('Arquivo baixado não é um banco SQLite válido.')
tmp.replace(TARGET)
with sqlite3.connect(f'file:{TARGET}?mode=ro', uri=True) as con:
    tables = {t[0] for t in con.execute('SELECT name FROM sqlite_master WHERE type="table"')}
    required = {'questions', 'alternatives', 'question_files', 'disciplines', 'languages'}
    if not required.issubset(tables):
        raise RuntimeError(f'Estrutura de banco inesperada: {sorted(tables)}')
    count = con.execute('SELECT COUNT(*) FROM questions').fetchone()[0]
    years = [r[0] for r in con.execute('SELECT DISTINCT year FROM questions ORDER BY year DESC')]
    if count == 0:
        raise RuntimeError('O arquivo veio sem questões')
    print(f'FOCAL: {count} questões, anos {years}, banco pronto.', flush=True)