import json, re, os
BASE = os.path.dirname(os.path.abspath(__file__))

def load(fn, kind):
    out = []
    for line in open(os.path.join(BASE, fn), encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip(): continue
        t, year, rating, genre, desc = line.split('|')
        out.append(dict(t=t, y=year, r=float(rating), g=genre, d=desc, kind=kind))
    return out

def load_queue():
    out = []
    for line in open(os.path.join(BASE, 'queue.psv'), encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip(): continue
        kind, t, year, genre, desc = line.split('|')
        out.append(dict(t=t, y=year, r=None, g=genre, d=desc,
                        kind='TV' if kind == 'TV' else 'MOVIE'))
    return out

def wiki_query2(it):
    base = re.sub(r',\s*seasons?\s.*$', '', it['t']).strip().strip('"')
    if it['kind'] == 'MOVIE':
        return f'{base} film'
    return base

def wiki_query(it):
    base = re.sub(r',\s*seasons?\s.*$', '', it['t']).strip().strip('"')
    if it['kind'] == 'MOVIE':
        if it['t'].startswith('Bourne'): return 'The Bourne Identity 2002 film'
        yr = it['y']
        if re.fullmatch(r'\d{4}', yr or ''): return f'{base} {yr} film'
        return f'{base} film'
    return f'{base} television series'

movies = load('movies.psv', 'MOVIE')
tv = load('tv.psv', 'TV')
queue = load_queue()
for it in movies + tv + queue:
    it['q'] = wiki_query(it)
    it['q2'] = wiki_query2(it)

GENRE_ORDER = ['Spy / Espionage', 'Action / Thriller', 'Crime', 'War', 'Sci-Fi',
               'Superhero', 'Fantasy', 'Horror', 'Comedy', 'Drama',
               'Animation / Family', 'Reality / Docu']

def groups(items):
    seen = sorted({i['g'] for i in items}, key=lambda g: GENRE_ORDER.index(g) if g in GENRE_ORDER else 99)
    out = []
    for g in seen:
        rows = [i for i in items if i['g'] == g]
        rows.sort(key=lambda i: (-i['r'], i['t'].lower().lstrip('"')))
        out.append({'g': g, 'items': rows})
    return out

data = {
    'movies': groups(movies),
    'tv': groups(tv),
    'queue': queue,
    'counts': {'movies': len(movies), 'tv': len(tv), 'queue': len(queue)},
}
json.dump(data, open(os.path.join(BASE, 'data.json'), 'w'), ensure_ascii=False)

def avg(items): return round(sum(i['r'] for i in items) / len(items), 2)
print('movies', len(movies), 'avg', avg(movies))
print('tv', len(tv), 'avg', avg(tv))
print('genres movies:', [(g['g'], len(g['items'])) for g in data['movies']])
print('genres tv:', [(g['g'], len(g['items'])) for g in data['tv']])
print('top movie rating', max(i['r'] for i in movies), 'min', min(i['r'] for i in movies))
