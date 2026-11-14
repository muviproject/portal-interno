#!/usr/bin/env python3
"""Genera inspiracion.html (portal interno) desde los datos.json capturados.

Fuente: ../files/med-aesthetics-materiales/inspiracion/<handle>/datos.json
        (15 competidores, top 5 reels + piezas distintas, con JPG).
Salida: inspiracion.html en este directorio (repo muviproject/portal-interno)
        + copias de los JPG en inspiracion/<handle>/ (rutas relativas, NO base64).

La página tiene DOS vistas (pestañas):
  1. Por competidor — top 5 reels + piezas distintas de cada cuenta.
  2. Por tipo de pieza — los mismos ejemplos agrupados por tipo canónico
     (tarjeta de oferta, antes/después, carrusel educativo, carrusel de
     tecnología, Black Friday, membresía, credencial, reel a cámara,
     testimonio, humor/comunidad, etc.), para decidir con Rosanna qué
     armar en una sesión de trabajo.

La inspiración es INTERNA: vive solo en el portal interno, nunca va al
portal del cliente. Los ejemplos son referencia para decidir, no para
copiar tal cual ni para publicar. La página lleva la misma cortina de
acceso que index.html (importada de build.py).
"""
import html
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import GATE_CSS, GATE_HTML  # noqa: E402

BASE = os.path.expanduser(
    "~/workspace/goals/vallure-agency-partnership-response/"
    "files/med-aesthetics-materiales/inspiracion")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_HTML = os.path.join(OUT_DIR, "inspiracion.html")
ASSETS = os.path.join(OUT_DIR, "inspiracion")

# Miami primero, luego nacional (mismo orden que la captura).
ORDER = [
    "monaco.medspa", "luxmedspabrickell", "skinneymedspa",
    "nofiltermiami", "viomedspa.aventura",
    "skinconserv", "kbeautylab808", "beautybeyondaesthetics1",
    "skinholics.miami", "kumimedspa", "beautybybel.rn",
    "skinologymedspa", "skinelixerspa_miami", "theprivatesuitela",
    "bleuspany",
]
MIAMI = set(ORDER[:5])

TYPE_ORDER = [
    "Tarjeta de oferta",
    "Antes / después",
    "Carrusel educativo",
    "Carrusel de tecnología",
    "Black Friday",
    "Membresía",
    "Credencial",
    "Reel a cámara",
    "Testimonio",
    "Humor / comunidad",
    "Portada de carrusel",
    "Imagen suelta / editorial",
    "Equipo / presentación",
    "Producto",
    "Historia",
    "Otros",
]


def canon_piece(p):
    """Tipo canónico de una pieza, desde su type + note originales."""
    s = ((p.get("type") or "") + " " + (p.get("note") or "")).lower()
    if "antes" in s and "despu" in s:
        return "Antes / después"
    # Credencial ANTES que Testimonio: "Google reviews" contiene "review"
    # y el "#1 LEADER" o el premio TOP 3 son credencial, no testimonio.
    if ("premio" in s or "top 3" in s or "award" in s or "leader" in s
            or "prensa" in s or "revista" in s or "magazine" in s
            or "forbes" in s):
        return "Credencial"
    if "testimonio" in s or "reseña" in s or "resena" in s:
        return "Testimonio"
    if "promo" in s or "oferta" in s or "gift card" in s or "referido" in s:
        return "Tarjeta de oferta"
    if "tecnolog" in s or "lanzamiento" in s:
        return "Carrusel de tecnología"
    if "educativo" in s or "infograf" in s:
        return "Carrusel educativo"
    if "humor" in s or "comunidad" in s or "convocatoria" in s or "celebridad" in s:
        return "Humor / comunidad"
    if "equipo" in s or "presentación" in s or "fundadora" in s:
        return "Equipo / presentación"
    if "producto" in s:
        return "Producto"
    if "portada" in s:
        return "Portada de carrusel"
    if ("editorial" in s or "imagen suelta" in s or "personal" in s
            or "otro servicio" in s or "inspiración" in s or "moodboard" in s):
        return "Imagen suelta / editorial"
    return "Otros"


def tags_piece(p):
    """Etiquetas extra (una pieza puede estar en más de un grupo)."""
    s = ((p.get("type") or "") + " " + (p.get("note") or "")).lower()
    tags = []
    if "black friday" in s:
        tags.append("Black Friday")
    if ("miembro" in s or "membres" in s or "club vio" in s
            or "beauty bank" in s):
        tags.append("Membresía")
    return tags


def tags_reel(r):
    s = ((r.get("what") or "") + " " + (r.get("caption_excerpt") or "")).lower()
    tags = []
    if "black friday" in s:
        tags.append("Black Friday")
    if "club vio" in s or "beauty bank" in s or "miembro" in s:
        tags.append("Membresía")
    if ("cámara" in s or "camara" in s or "habla" in s or "talking" in s
            or "selfie" in s):
        tags.append("Reel a cámara")
    return tags


def esc(x):
    return html.escape("" if x is None else str(x), quote=True)


def fmt_num(n):
    if n is None:
        return "—"
    try:
        return f"{int(n):,}".replace(",", ".")
    except (TypeError, ValueError):
        return esc(n)


def metrics(r):
    likes = fmt_num(r.get("likes"))
    com = fmt_num(r.get("comments"))
    return f"♥ {likes} · 💬 {com}"


def safe_url(u):
    u = (u or "").strip()
    if u.startswith("https://www.instagram.com/"):
        return esc(u)
    return ""


def card(handle, img, url, title, subtitle, badge=""):
    link = safe_url(url)
    img_tag = (f'<a href="{link}" target="_blank" rel="noopener">'
               f'<img src="{esc(img)}" alt="" loading="lazy"></a>' if link
               else f'<img src="{esc(img)}" alt="" loading="lazy">')
    link_html = (f'<a href="{link}" target="_blank" rel="noopener">'
                 f'Ver en Instagram ↗</a>' if link else "")
    return (
        f'<div class="card">{img_tag}'
        f'<div class="card-body">'
        f'{"<span class=&quot;badge&quot;>" + esc(badge) + "</span> " if badge else ""}'
        f'<b>{esc(title)}</b><br>'
        f'<span class="small">{esc(subtitle)}</span><br>{link_html}'
        f'</div></div>'
    )


def main():
    data = {}
    for h in ORDER:
        path = os.path.join(BASE, h, "datos.json")
        if not os.path.exists(path):
            print(f"AVISO: sin datos.json para {h}, se saltea")
            continue
        with open(path, encoding="utf-8") as f:
            data[h] = json.load(f)

    # Copiar JPGs al repo (solo los referenciados).
    n_img = 0
    for h, d in data.items():
        dest = os.path.join(ASSETS, h)
        os.makedirs(dest, exist_ok=True)
        for item in list(d.get("top_reels", [])) + list(d.get("pieces", [])):
            img = item.get("image")
            if not img:
                continue
            src = os.path.join(BASE, h, img)
            if os.path.exists(src):
                shutil.copyfile(src, os.path.join(dest, img))
                n_img += 1
            else:
                print(f"AVISO: falta imagen {src}")

    n_reels = sum(len(d.get("top_reels", [])) for d in data.values())
    n_pieces = sum(len(d.get("pieces", [])) for d in data.values())

    # --- Vista por competidor ---
    comp_sections = []
    for h in ORDER:
        d = data.get(h)
        if not d:
            continue
        grp = "Miami · directo" if h in MIAMI else "Nacional · benchmark"
        profile = f"https://www.instagram.com/{h}/"
        sec = [f'<section id="c-{esc(h)}">',
               f'<h2>@{esc(h)} <span class="tag">{esc(grp)}</span></h2>',
               f'<p><b>{fmt_num(d.get("followers"))} seguidores</b> · '
               f'<a href="{esc(profile)}" target="_blank" rel="noopener">'
               f'instagram.com/{esc(h)}</a><br>'
               f'<span class="small">Ranking: {esc(d.get("ranking_metric"))} · '
               f'muestra: {esc(d.get("sample_note"))}</span></p>',
               f'<p>{esc(d.get("nota_visual", ""))}</p>']
        sec.append('<h3>Top 5 reels</h3><div class="grid">')
        for r in d.get("top_reels", []):
            img = f"inspiracion/{h}/{r.get('image', '')}"
            sub = (f"{metrics(r)} · {esc(r.get('date'))}<br>"
                   f"{esc(r.get('what', ''))}")
            sec.append(card(h, img, r.get("url"), f"#{r.get('rank')} · Reel",
                            sub, badge="REEL"))
        sec.append('</div>')
        sec.append('<h3>Piezas distintas</h3><div class="grid">')
        for p in d.get("pieces", []):
            img = f"inspiracion/{h}/{p.get('image', '')}"
            sub = (f"{esc(p.get('type', ''))} · {metrics(p)} · "
                   f"{esc(p.get('date'))}<br>{esc(p.get('note', ''))}")
            sec.append(card(h, img, p.get("url"), canon_piece(p), sub))
        sec.append('</div>')
        if d.get("faltante"):
            sec.append('<p class="small">Faltante: '
                       + esc("; ".join(d["faltante"])) + '</p>')
        sec.append('</section>')
        comp_sections.append("\n".join(sec))

    # --- Vista por tipo ---
    by_type = {t: [] for t in TYPE_ORDER}
    for h in ORDER:
        d = data.get(h)
        if not d:
            continue
        for p in d.get("pieces", []):
            img = f"inspiracion/{h}/{p.get('image', '')}"
            sub = (f"@{esc(h)} · {esc(p.get('type', ''))} · {metrics(p)} · "
                   f"{esc(p.get('date'))}<br>{esc(p.get('note', ''))}")
            entry = card(h, img, p.get("url"), canon_piece(p), sub)
            by_type[canon_piece(p)].append(entry)
            for t in tags_piece(p):
                if t in by_type:
                    by_type[t].append(entry)
        for r in d.get("top_reels", []):
            for t in tags_reel(r):
                if t not in by_type:
                    continue
                img = f"inspiracion/{h}/{r.get('image', '')}"
                sub = (f"@{esc(h)} · {metrics(r)} · {esc(r.get('date'))}<br>"
                       f"{esc(r.get('what', ''))}")
                by_type[t].append(card(h, img, r.get("url"),
                                      f"#{r.get('rank')} · Reel", sub,
                                      badge="REEL"))

    type_sections = []
    for t in TYPE_ORDER:
        entries = by_type[t]
        sec = [f'<section id="t-{esc(t.lower().replace(" ", "-").replace("/", "-"))}">',
               f'<h2>{esc(t)} <span class="tag">{len(entries)} ejemplo(s)</span></h2>']
        if t == "Historia":
            sec.append('<p class="small">Las historias no se capturan con '
                       'este método (instagram-cli solo trae el feed). '
                       'Sin ejemplos en esta tanda.</p>')
        if t == "Membresía" and not entries:
            sec.append('<p class="small">Sin ejemplos claros de membresía '
                       'en esta tanda.</p>')
        if entries:
            sec.append('<div class="grid">' + "\n".join(entries) + '</div>')
        elif t not in ("Historia", "Membresía"):
            sec.append('<p class="small">Sin ejemplos en esta tanda.</p>')
        sec.append('</section>')
        type_sections.append("\n".join(sec))

    type_nav = " · ".join(
        f'<a href="#t-{esc(t.lower().replace(" ", "-").replace("/", "-"))}">'
        f'{esc(t)}</a>' for t in TYPE_ORDER)

    html_doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MuViProject · Inspiración — Portal Interno</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; background: #f4f2ee; color: #2b2b2b; line-height: 1.55; }}
  header {{ background: #1f1f1f; color: #fff; padding: 28px 24px 22px; }}
  header h1 {{ margin: 0 0 4px; font-size: 26px; }}
  header p {{ margin: 0; color: #cfc9bd; font-size: 15px; }}
  .gold {{ color: #e3b533; }}
  .banner {{ background: #8a1f1f; color: #fff; padding: 10px 24px; font-size: 14px; font-weight: 600; }}
  .banner span {{ font-weight: 400; opacity: .9; }}
  nav {{ background: #fff; border-bottom: 1px solid #ddd; padding: 10px 24px; position: sticky; top: 0; z-index: 10; }}
  nav a {{ margin-right: 18px; color: #6b5a1e; text-decoration: none; font-weight: 600; font-size: 14px; }}
  nav a:hover {{ text-decoration: underline; }}
  main {{ max-width: 980px; margin: 0 auto; padding: 24px; }}
  section {{ background: #fff; border: 1px solid #e2ddd3; border-radius: 10px; padding: 22px 26px; margin-bottom: 22px; }}
  h2 {{ margin: 0 0 10px; font-size: 21px; border-bottom: 2px solid #e3b533; padding-bottom: 6px; }}
  h3 {{ margin: 20px 0 6px; font-size: 17px; }}
  p, li {{ font-size: 15px; }}
  .tag {{ display: inline-block; background: #606163; color: #fff; font-size: 12px; padding: 2px 8px; border-radius: 20px; margin-right: 6px; }}
  .tag.gold {{ background: #e3b533; color: #3a2c05; }}
  .small {{ font-size: 13px; color: #666; }}
  .badge {{ display: inline-block; background: #e3b533; color: #3a2c05; font-size: 11px; font-weight: 700; padding: 1px 7px; border-radius: 20px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 14px; margin: 10px 0; }}
  .card {{ border: 1px solid #e2ddd3; border-radius: 8px; overflow: hidden; background: #faf7f1; }}
  .card img {{ width: 100%; aspect-ratio: 4/5; object-fit: cover; display: block; background: #ddd; }}
  .card-body {{ padding: 10px 12px; font-size: 13px; }}
  .card-body a {{ color: #6b5a1e; font-weight: 600; }}
  .tabs {{ margin: 0 0 18px; }}
  .tabs button {{ padding: 10px 18px; margin-right: 8px; border: 1px solid #d8d2c4; border-radius: 8px; background: #fff; font-size: 15px; font-weight: 600; color: #6b5a1e; cursor: pointer; }}
  .tabs button.active {{ background: #4b3618; color: #fff; border-color: #4b3618; }}
  .typenav {{ font-size: 14px; line-height: 2; }}
  .typenav a {{ color: #6b5a1e; }}
  footer {{ max-width: 980px; margin: 0 auto; padding: 0 24px 30px; color: #777; font-size: 13px; }}
</style>
{GATE_CSS}
</head>
<body>
{GATE_HTML}
<header>
  <h1>MuViProject <span class="gold">·</span> Inspiración</h1>
  <p>Referencia interna para decidir con Rosanna qué armar. <a href="index.html" style="color:#e3b533">← Volver al portal interno</a></p>
</header>
<div class="banner">INTERNO — Solo MuViProject. <span>Los ejemplos son referencia para decidir en una sesión de trabajo, no para copiar tal cual ni para publicar. Nunca van al portal del cliente.</span></div>
<nav>
  <a href="index.html">Portal interno</a>
  <a href="#vista-competidor" onclick="showView('competidor');return false;">Por competidor</a>
  <a href="#vista-tipo" onclick="showView('tipo');return false;">Por tipo de pieza</a>
</nav>
<main>
<section>
  <h2>Inspiración — 15 competidores</h2>
  <p><b>{len(data)} cuentas</b> · <b>{n_reels} reels top</b> · <b>{n_pieces} piezas distintas</b> · capturado el 14-nov-2026. Top 5 reels de los posteos más recientes de cada cuenta, rankeados por likes salvo que se indique otra métrica. Las métricas son las que devolvieron las herramientas; donde vinieron en null, quedó anotado en cada cuenta. Las vistas de reels no las entrega la herramienta. De los carruseles solo se capturó la portada.</p>
  <p class="small">Cómo se usa: cuando Rosanna quiera armar una pieza concreta, se abre su tipo en la vista «Por tipo de pieza» y se deciden juntos los elementos. Los links «Ver en Instagram» abren el post original.</p>
  <div class="tabs">
    <button id="tab-competidor" class="active" onclick="showView('competidor')">Por competidor</button>
    <button id="tab-tipo" onclick="showView('tipo')">Por tipo de pieza</button>
  </div>
  <p class="typenav" id="typenav" style="display:none">{type_nav}</p>
</section>
<div id="vista-competidor">
{chr(10).join(comp_sections)}
</div>
<div id="vista-tipo" style="display:none">
{chr(10).join(type_sections)}
</div>
</main>
<footer>
  MuViProject · Portal interno · Inspiración · Captura: 14-nov-2026 · Método: instagram-cli (posts + profile) y hatch-zeitgeist (miniaturas). Muestras: posteos más recientes por cuenta, no el feed completo ni el histórico. «Reel a cámara» agrupa los reels cuya descripción indica que la persona habla o se graba a cámara (incluye selfies); «Black Friday» y «Membresía» son etiquetas extra: esas piezas aparecen también en su grupo principal.
</footer>
<script>
function showView(v) {{
  document.getElementById('vista-competidor').style.display = v === 'competidor' ? '' : 'none';
  document.getElementById('vista-tipo').style.display = v === 'tipo' ? '' : 'none';
  document.getElementById('typenav').style.display = v === 'tipo' ? '' : 'none';
  document.getElementById('tab-competidor').classList.toggle('active', v === 'competidor');
  document.getElementById('tab-tipo').classList.toggle('active', v === 'tipo');
  window.scrollTo(0, 0);
}}
</script>
</body>
</html>
"""
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_doc)
    print(f"generado {OUT_HTML} ({os.path.getsize(OUT_HTML)} bytes)")
    print(f"competidores={len(data)} reels={n_reels} piezas={n_pieces} "
          f"imágenes copiadas={n_img}")
    for t in TYPE_ORDER:
        print(f"  tipo {t}: {len(by_type[t])}")


if __name__ == "__main__":
    main()
