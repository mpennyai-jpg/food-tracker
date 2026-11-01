head=open('page_head.html',encoding='utf-8').read()
body=open('body.html',encoding='utf-8').read()
js=open('script.js',encoding='utf-8').read()
data=open('data.json',encoding='utf-8').read().replace('</','<\\/')
import os
posters = ''
if os.path.exists('posters.json'):
    posters = open('posters.json',encoding='utf-8').read().replace('</','<\\/')

NOTE = ('Poster artwork comes from Wikipedia and is built into this page, so it needs '
        'no connection to show. Eleven titles keep a monogram: nine have no matching '
        'Wikipedia article under the name used here, and two are the unresolved '
        'fragments from the source notes.')
ART_NOTE = STD_NOTE = NOTE

def page(note):
    blocks = "\n<script>\nwindow.__WATCHLOG__ = " + data + ";\n</script>\n"
    if posters:
        blocks += "<script>\nwindow.__POSTERS__ = " + posters + ";\n</script>\n"
    return body.replace('__POSTERNOTE__', note) + blocks + "<script>\n" + js + "\n</script>\n"

open('watch-log.html','w',encoding='utf-8').write(head + "\n" + page(ART_NOTE))

doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
 '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
 '<style>:root{color-scheme:light dark}body{margin:0;font:14px system-ui,sans-serif}'
 'img{max-width:100%}[hidden]{display:none!important}</style>\n'
 + head + '\n</head>\n<body>\n' + page(STD_NOTE) + '</body>\n</html>\n')
open('todd-watch-log.html','w',encoding='utf-8').write(doc)

skel=('<!doctype html><html><head><meta charset="utf-8">'
 '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
 '<style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}'
 '[hidden]{display:none!important}</style></head><body>'
 + head + "\n" + page(ART_NOTE) + '</body></html>')
open('preview.html','w',encoding='utf-8').write(skel)
print('built')
