"""Focal ENEM: site e API SQLite no mesmo domínio (sem CORS)."""
from __future__ import annotations

import json
import os
import sqlite3
import unicodedata
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent
DB = ROOT / 'enem_questions.db'
AREAS = {
    'mat': ('matemat',),
    'ling': ('linguagen',),
    'nat': ('natureza',),
    'hum': ('humanas',),
}


def normalized(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', str(s).casefold()) if not unicodedata.combining(c))


def connection():
    if not DB.exists():
        raise FileNotFoundError('Banco de questões não instalado: execute python build.py')
    conn = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def safe_int(value, default, low, high):
    try:
        return min(high, max(low, int(value)))
    except (ValueError, TypeError):
        return default


def get_years():
    with connection() as con:
        years = [int(r['year']) for r in con.execute('SELECT DISTINCT year FROM questions WHERE year IS NOT NULL ORDER BY year DESC')]
        counts = {str(r['year']): int(r['n']) for r in con.execute('SELECT year, COUNT(*) n FROM questions GROUP BY year')}
    return {'years': years, 'counts': counts, 'source': 'ardotheedu/api-enem'}


def get_questions(params):
    year = safe_int(params.get('year', [2023])[0], 2023, 2009, 2100)
    area = params.get('area', ['mat'])[0]
    if area not in AREAS:
        return {'error': 'Área inválida. Use mat, ling, hum ou nat.'}, 400
    limit = safe_int(params.get('limit', ['200'])[0], 200, 1, 200)
    page = safe_int(params.get('page', ['1'])[0], 1, 1, 1000)
    with connection() as con:
        ds = list(con.execute('SELECT value,label FROM disciplines'))
        chosen = [r['value'] for r in ds if any(key in normalized(r['value']) or key in normalized(r['label']) for key in AREAS[area])]
        if not chosen:
            return {'data': [], 'total': 0, 'year': year, 'area': area, 'message': 'Nenhuma disciplina corresponde à área selecionada.'}, 200
        placeholders = ','.join('?' for _ in chosen)
        where = 'q.year = ? AND d.value IN (' + placeholders + ')'
        values = [year, *chosen]
        total = con.execute('SELECT COUNT(*) FROM questions q LEFT JOIN disciplines d ON q.discipline_id=d.id WHERE ' + where, values).fetchone()[0]
        rows = con.execute('''SELECT q.id,q.title,q.index_number,q.year,q.context,
                            q.alternatives_introduction,q.correct_alternative,
                            d.label discipline_label,d.value discipline_value
                            FROM questions q LEFT JOIN disciplines d ON q.discipline_id=d.id
                            WHERE ''' + where + ' ORDER BY q.index_number ASC LIMIT ? OFFSET ?', [*values, limit, (page - 1) * limit]).fetchall()
        data = []
        for r in rows:
            alts = con.execute('SELECT letter, text, file_path, is_correct FROM alternatives WHERE question_id=? ORDER BY letter', (r['id'],)).fetchall()
            images = con.execute('SELECT file_path FROM question_files WHERE question_id=?', (r['id'],)).fetchall()
            data.append({
                'id': r['id'], 'title': r['title'], 'index': r['index_number'], 'year': r['year'],
                'context': r['context'], 'alternativesIntroduction': r['alternatives_introduction'],
                'correctAlternative': r['correct_alternative'],
                'discipline': {'label': r['discipline_label'], 'value': r['discipline_value']},
                'alternatives': [{'letter': a['letter'], 'text': a['text'],
                                  'file': a['file_path'] if str(a['file_path'] or '').startswith('https://') else None,
                                  'isCorrect': bool(a['is_correct'])} for a in alts],
                'files': [img['file_path'] for img in images if str(img['file_path'] or '').startswith('https://')],
            })
    return {'data': data, 'total': total, 'page': page, 'limit': limit,
            'totalPages': (total + limit - 1) // limit, 'source': 'ardotheedu/api-enem'}, 200


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_json(self, body, status=200):
        content = json.dumps(body, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        parts = urlsplit(self.path)
        if parts.path == '/health':
            self.send_json({'ok': True, 'database': DB.exists()})
            return
        if parts.path.startswith('/api/'):
            try:
                if parts.path == '/api/years':
                    self.send_json(get_years())
                elif parts.path == '/api/questions':
                    body, code = get_questions(parse_qs(parts.query))
                    self.send_json(body, code)
                else:
                    self.send_json({'error': 'Rota não encontrada'}, 404)
            except Exception as ex:
                print('Erro interno API:', repr(ex), flush=True)
                self.send_json({'error': 'Não foi possível consultar o banco hospedado.'}, 503)
            return
        if parts.path in ('/', '/index.html'):
            self.path = '/index.html'
        elif parts.path.startswith('/enem_questions.db') or parts.path.startswith('/server.py') or parts.path.startswith('/build.py'):
            self.send_error(404)
            return
        else:
            self.path = parts.path
        return super().do_GET()

    def end_headers(self):
        if self.path == '/index.html':
            self.send_header('Cache-Control', 'no-cache')
        super().end_headers()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '10000'))
    print(f'FOCAL iniciado na porta {port}. Banco presente: {DB.exists()}', flush=True)
    ThreadingHTTPServer(('0.0.0.0', port), Handler).serve_forever()