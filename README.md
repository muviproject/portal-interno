# Portal interno de MuViProject

Conocimiento de la empresa, por cliente. Se consulta online en https://muviproject.github.io/portal-interno/ (acceso con clave, cortina visual).

Fuente: `../files/portal-interno-muviproject.html`. Para actualizar: editar ese archivo y correr `python3 build.py`, luego commit + push.

Página de inspiración (`inspiracion.html`, dos vistas: por competidor y por tipo de pieza): la genera `build_inspiracion.py` desde `../files/med-aesthetics-materiales/inspiracion/<handle>/datos.json` (15 competidores, top 5 reels + piezas distintas, captura 14-nov-2026) y copia los JPG a `inspiracion/<handle>/`. `build.py` la regenera sola al final. Es referencia INTERNA para decidir con Rosanna, nunca va al portal del cliente.
