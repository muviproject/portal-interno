"""Build the internal portal from versioned sources; no external workspace needed."""
from pathlib import Path
import html
import json
import re
from build import GATE_CSS, GATE_HTML

ROOT = Path(__file__).resolve().parent
E = html.escape


def shell(title, active, body):
    body = '\n'.join(line.rstrip() for line in body.splitlines())
    nav = ''.join(f'<a href="{href}"' + (' aria-current="page"' if active == href else '') + f'>{label}</a>' for href, label in [('index.html', 'Conocimiento'), ('inspiracion.html', 'Inspiración')])
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} · MuViProject</title>{GATE_CSS}<link rel="stylesheet" href="portal.css"></head>
      <body><a class="skip" href="#contenido">Saltar al contenido</a>{GATE_HTML}
      <header class="masthead"><div class="wrap"><a class="wordmark" href="index.html">MuVi<span>Project</span></a><span class="internal-label">Portal interno · Med Aesthetics Miami</span></div></header>
      <nav class="nav" aria-label="Navegación principal"><div class="wrap">{nav}</div></nav>
      <main id="contenido" class="wrap">{body}</main>
      <footer class="wrap">Referencia interna de MuViProject · Las capturas y los análisis conservan su fecha original.</footer><script src="portal.js" defer></script></body></html>'''


def build_knowledge():
    source = (ROOT / 'source/knowledge.html').read_text(encoding='utf-8')
    sections = re.findall(r'<section id="([^"]+)">(.*?)</section>', source, re.S)
    lookup = dict(sections)
    body = '''<div class="heading"><p class="eyebrow">Investigación → ideas → decisiones</p><h1>Conocimiento para crear mejor.</h1><p>La investigación de Med Aesthetics Miami, organizada para consultar y convertir referencias en propuestas.</p></div>
      <div class="hero"><div><span class="eyebrow">Prioridad de investigación</span><h2>Inspiración nacional, con contexto.</h2><p>Explora las cuentas de referencia y sus piezas. Compara el formato y el concepto antes de adaptar una idea a la marca.</p><a class="button primary" href="inspiracion.html">Explorar referencias</a></div><aside><strong>15 cuentas</strong><span>75 reels · 74 piezas gráficas</span><small>Captura archivada: 14 nov 2026</small></aside></div>
      <p class="notice">Uso interno. Al portal del cliente van los análisis y las propuestas seleccionadas, no este archivo de referencias.</p>
      <h2 class="section-title">Consultar por tema</h2>'''
    labels = {'top10': 'Referencias nacionales', 'miami': 'Contexto de Miami', 'resumen': 'Hallazgos de la investigación', 'novedades': 'Novedades — 14–15 nov 2026', 'sistema': 'Sistema de elementos', 'marca': 'Marca Med Aesthetics Miami', 'rosanna': 'Archivo de Vallure', 'clientes': 'Ficha del cliente', 'fuentes': 'Fuentes y límites de la muestra'}
    ordered = ['top10', 'resumen', 'novedades', 'sistema', 'marca', 'miami', 'rosanna', 'clientes', 'fuentes']
    ordered += [k for k in lookup if k not in ordered]
    for ident in ordered:
        if ident not in lookup:
            continue
        content = re.sub(r'<h2>.*?</h2>', '', lookup[ident], count=1, flags=re.S)
        body += f'<details class="knowledge" id="{ident}"><summary>{E(labels.get(ident, ident))}</summary><div class="knowledge-body">{content}</div></details>'
    (ROOT / 'index.html').write_text(shell('Conocimiento', 'index.html', body), encoding='utf-8')


def build_inspiration():
    data = json.loads((ROOT / 'source/inspiration.json').read_text(encoding='utf-8'))
    accounts = sorted(data['accounts'], key=lambda a: a['group'] != 'national')
    types = sorted({t for a in accounts for r in a['items'] for t in r['types']})
    body = '''<div class="heading"><p class="eyebrow">Biblioteca de referencias</p><h1>Ideas que vale la pena estudiar.</h1><p>Reels, formatos y conceptos para adaptar a Med Aesthetics Miami. Las referencias nacionales aparecen primero.</p></div>
      <details class="method"><summary>Qué incluye esta captura · 14 nov 2026</summary><p>15 cuentas, 75 reels seleccionados y 74 piezas distintas. Los reels se ordenaron principalmente por likes dentro de la muestra de cada cuenta, no por reproducciones ni por todo el histórico. Algunas cuentas se ordenaron por comentarios. Las muestras tienen fechas y tamaños diferentes.</p><p>Las descripciones e imágenes son las archivadas: no equivalen a una revisión completa del video. De los carruseles solo se capturó la portada. «—» significa dato no disponible, nunca cero.</p></details>
      <form class="filters" role="search" onsubmit="return false">
      <label class="search">Buscar referencia<input id="query" type="search" placeholder="Morpheus8, humor, testimonio…"></label>
      <label>Grupo<select id="group"><option value="national">Referencias nacionales</option><option value="miami">Contexto de Miami</option><option value="all">Todas las cuentas</option></select></label>
      <label>Formato<select id="format"><option value="all">Todos los formatos</option><option>Reel</option><option>Pieza gráfica</option></select></label>
      <label>Tipo de pieza<select id="type"><option value="all">Todos los tipos</option>'''
    body += ''.join(f'<option>{E(t)}</option>' for t in types) + '</select></label><button class="button" id="reset" type="reset">Restablecer</button></form>'
    body += '<p id="result-count" class="meta" role="status" aria-live="polite">15 cuentas · 149 referencias archivadas</p><p id="no-results" class="notice" hidden>No hay coincidencias. Prueba otro término o restablece los filtros.</p>'
    for account in accounts:
        h = account['handle']
        body += f'<section class="account" id="c-{E(h)}" data-group="{account["group"]}"><div class="account-heading"><h2>@{E(h)}</h2><span class="tag">{"Nacional · referencia" if account["group"] == "national" else "Miami · contexto"}</span></div>'
        body += f'<details class="method"><summary>Contexto, muestra y análisis de la cuenta</summary><p>{E(account["sample"])}</p><p>{E(account["analysis"])}</p>'
        body += ''.join(f'<p class="meta">{E(p)}</p>' for p in account['missing']) + '</details><div class="reference-grid">'
        for i, item in enumerate(account['items']):
            tags = '|'.join(item['types'])
            body += f'''<article class="reference" data-format="{E(item['format'])}" data-types="{E(tags, quote=True)}">
              <a class="reference-image" href="{E(item['image'], quote=True)}" target="_blank" rel="noopener" aria-label="Ver imagen completa de @{E(h)}: {E(item['title'], quote=True)}"><img loading="lazy" src="{E(item['image'], quote=True)}" alt="Captura de referencia de @{E(h)}: {E(item['title'], quote=True)}"></a>
              <div class="reference-body"><span class="tag">{E(item['format'])}</span><h3>{E(item['title'])}</h3><p>{E(item['description'])}</p>
              <div class="reference-actions"><a href="{E(item['url'], quote=True)}" target="_blank" rel="noopener">Abrir publicación ↗</a><a href="{E(item['image'], quote=True)}" target="_blank" rel="noopener">Imagen completa ↗</a></div></div></article>'''
        body += '</div></section>'
    (ROOT / 'inspiracion.html').write_text(shell('Inspiración', 'inspiracion.html', body), encoding='utf-8')


def build():
    build_knowledge()
    build_inspiration()
    print('Built both pages from versioned sources: 15 accounts, 149 references.')


if __name__ == '__main__':
    build()
