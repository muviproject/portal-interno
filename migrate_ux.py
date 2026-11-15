"""One-time, lossless import of the already published reference cards.

Source data was outside this repository. This script captures only information
present in the original HTML, without inferring missing metrics or video content.
The resulting source/ files are versioned and used by portal_ux.py thereafter.
"""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parent


def text(markup):
    markup = html.unescape(html.unescape(markup))
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', markup)).strip()


def migrate():
    out = ROOT / 'source'
    if (out / 'inspiration.json').exists():
        raise SystemExit('Source already imported; no overwrite performed.')
    raw = (ROOT / 'inspiracion.html').read_text(encoding='utf-8')
    type_view = raw.split('<div id="vista-tipo"', 1)[1]
    types_by_image = {}
    for sec in re.findall(r'<section\b[^>]*>(.*?)</section>', type_view, re.S):
        title = text(re.search(r'<h2>(.*?)<span', sec, re.S)[1])
        for image in re.findall(r'<img src="([^"]+)"', sec):
            types_by_image.setdefault(image, []).append(title)
    accounts = []
    for handle, sec in re.findall(r'<section id="c-([^"]+)">(.*?)</section>', raw, re.S):
        intro = sec.split('<h3>', 1)[0]
        paragraphs = re.findall(r'<p>(.*?)</p>', intro, re.S)
        items = []
        for card in re.findall(r'<div class="card">(.*?)</div></div>', sec, re.S):
            image = re.search(r'<img src="([^"]+)"', card)[1]
            url = html.unescape(re.search(r'<a href="([^"]+)"', card)[1])
            title = text(re.search(r'<b>(.*?)</b>', card, re.S)[1])
            subtitle = text(re.search(r'<span class="small">(.*?)</span>', card, re.S)[1])
            items.append({'image': image, 'url': url, 'title': title,
                          'description': subtitle, 'types': types_by_image.get(image, []),
                          'format': 'Reel' if 'Reel' in title else 'Pieza gráfica'})
        accounts.append({'handle': handle, 'group': 'national' if 'Nacional · benchmark' in intro else 'miami',
                         'sample': text(paragraphs[0]),
                         'analysis': text(paragraphs[1]) if len(paragraphs) > 1 else '',
                         'missing': [text(p) for p in re.findall(r'<p class="small">(.*?)</p>', sec, re.S)],
                         'items': items})
    assert len(accounts) == 15 and sum(len(a['items']) for a in accounts) == 149
    out.mkdir(exist_ok=True)
    (out / 'inspiration.json').write_text(json.dumps({'captured': '2026-11-14', 'provenance': 'Imported from the existing published HTML; not a new social-media measurement.', 'accounts': accounts}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    knowledge = (ROOT / 'index.html').read_text(encoding='utf-8').split('<main>', 1)[1].split('</main>', 1)[0]
    (out / 'knowledge.html').write_text(knowledge, encoding='utf-8')
    print('Imported 15 accounts, 149 references and the full knowledge source.')


if __name__ == '__main__':
    migrate()
