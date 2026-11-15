#!/usr/bin/env python3
"""Genera index.html del portal interno a partir del archivo maestro.

Fuente: ../files/portal-interno-muviproject.html (se edita ese archivo).
Salida: index.html en este directorio (repo muviproject/portal-interno).

Inyecta la misma cortina de acceso del portal del cliente (email +
contraseña, solo visual: el sitio es estático y la clave se ve en el
código). Clave interna: MuViProject2026. Email: musadaniel@gmail.com
o cualquier @muviproject.com.
"""
import pathlib

SRC = pathlib.Path(__file__).parent.parent / "files" / "portal-interno-muviproject.html"
OUT = pathlib.Path(__file__).parent / "index.html"

GATE_CSS = """
<style>
#gate{position:fixed;inset:0;z-index:100;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#1f1f1f 0%,#4b3618 60%,#e3b533 130%);padding:20px}
#gate.hidden{display:none}
.gate-card{background:#fff;border-radius:14px;max-width:420px;width:100%;padding:34px 30px;box-shadow:0 20px 60px rgba(0,0,0,.35);text-align:center}
.gate-card h1{font-family:Georgia,serif;color:#4b3618;font-size:26px;font-weight:400;letter-spacing:1px;margin:6px 0}
.gate-card .sub{color:#606163;font-size:14px;margin:6px 0 22px}
.gate-card label{display:block;text-align:left;font-size:13px;color:#606163;margin:12px 0 4px}
.gate-card input{width:100%;padding:11px 12px;border:1px solid #d8d2c4;border-radius:8px;font-size:15px}
.gate-card input:focus{outline:2px solid #e3b533}
.gate-card button{width:100%;margin-top:16px;padding:12px;background:#4b3618;color:#fff;border:0;border-radius:8px;font-size:15px;cursor:pointer}
.gate-card button:hover{background:#606163}
#gate-err{color:#b3261e;font-size:13px;min-height:18px;margin-top:10px}
.gate-note{font-size:12px;color:#999;margin-top:16px}
</style>
"""

GATE_HTML = """
<!-- ============================================================
     ACCESO (cortina visual, no seguridad real: sitio estático,
     cualquiera que lea el código puede ver la clave).
     Clave: MuViProject2026. Email: musadaniel@gmail.com o @muviproject.com
     ============================================================ -->
<script>
var PORTAL_PASSWORD = "MuViProject2026";
</script>
<div id="gate">
  <div class="gate-card">
    <div style="color:#e3b533;font-size:15px;letter-spacing:2px">MuViProject</div>
    <h1>Portal interno</h1>
    <div class="sub">Conocimiento de la empresa, por cliente. Solo MuViProject.</div>
    <form id="gate-form">
      <label for="gate-email">Email</label>
      <input id="gate-email" type="email" placeholder="musadaniel@gmail.com" autocomplete="username" required>
      <label for="gate-pass">Contraseña</label>
      <input id="gate-pass" type="password" placeholder="Contraseña" autocomplete="current-password" required>
      <div id="gate-err"></div>
      <button type="submit">Entrar al portal</button>
    </form>
    <div class="gate-note">Si no entrás, escribime por WhatsApp al (845) 699-6606.</div>
  </div>
</div>
<script>
(function(){
  var gate = document.getElementById('gate');
  try { if (sessionStorage.getItem('muviproject_interno_auth') === '1') { gate.classList.add('hidden'); } } catch(e){}
  document.getElementById('gate-form').addEventListener('submit', function(ev){
    ev.preventDefault();
    var email = document.getElementById('gate-email').value.trim().toLowerCase();
    var pass = document.getElementById('gate-pass').value;
    var err = document.getElementById('gate-err');
    var okEmail = (email === 'musadaniel@gmail.com') || email.endsWith('@muviproject.com');
    if (!okEmail) {
      err.textContent = 'Usá tu email de MuViProject (musadaniel@gmail.com o @muviproject.com).';
      return;
    }
    if (pass !== PORTAL_PASSWORD) {
      err.textContent = 'Contraseña incorrecta. Revisala e intentá de nuevo.';
      return;
    }
    try { sessionStorage.setItem('muviproject_interno_auth', '1'); } catch(e){}
    gate.classList.add('hidden');
    window.scrollTo(0, 0);
  });
})();
</script>
"""

def _legacy_main():
    html = SRC.read_text(encoding="utf-8")
    if "id=\"gate\"" in html:
        raise SystemExit("el archivo maestro ya trae la cortina; no regenerar desde index.html")
    html = html.replace("</head>", GATE_CSS + "</head>", 1)
    html = html.replace("<body>", "<body>" + GATE_HTML, 1)
    OUT.write_text(html, encoding="utf-8")
    print(f"generado {OUT} ({OUT.stat().st_size} bytes)")
    # Página de inspiración (no frena el index si falla).
    try:
        import build_inspiracion
        build_inspiracion.main()
    except Exception as e:
        print(f"AVISO: inspiración no se regeneró: {e}")

def main():
    from portal_ux import build
    build()

if __name__ == "__main__":
    main()
