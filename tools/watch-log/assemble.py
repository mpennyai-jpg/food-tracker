head=open('page_head.html',encoding='utf-8').read()
body=open('body.html',encoding='utf-8').read()
js=open('script.js',encoding='utf-8').read()
data=open('data.json',encoding='utf-8').read().replace('</','<\\/')

ART_NOTE = ('Poster artwork does not load inside this shared page: the Claude artifact '
            'sandbox blocks images and requests from outside sites, so every title shows '
            'its monogram here. The downloadable copy of this file pulls the real posters '
            'from Wikipedia when you open it in a browser.')
STD_NOTE = ('Poster artwork is pulled from Wikipedia as you scroll, so the page needs a '
            'connection the first time you open it. They are cached in this browser after '
            'that. A title with no matching Wikipedia article keeps its monogram.')

def page(note):
    return body.replace('__POSTERNOTE__', note) + \
           "\n<script>\nwindow.__WATCHLOG__ = " + data + ";\n</script>\n<script>\n" + js + "\n</script>\n"

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
