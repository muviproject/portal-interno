# Portal interno de MuViProject

## Generación actual (UX, 15-nov-2026)

Ejecutar `python -B build.py` con Python 3, sin dependencias externas.
`build_inspiracion.py` permite regenerar solo la biblioteca. Los dos puntos
de entrada usan `portal_ux.py` y las fuentes versionadas en este repositorio:

- `source/knowledge.html`: contenido completo de conocimiento, por tema.
- `source/inspiration.json`: captura del 14-nov-2026; 15 cuentas, 75 reels y 74 piezas gráficas.
- `portal.css` y `portal.js`: diseño, filtros y navegación accesible.
- `inspiracion/<cuenta>/`: imágenes originales existentes.

Las fuentes se recuperaron del HTML publicado; no representan una nueva
medición. `migrate_ux.py` documenta esa importación única y no sobrescribe
una fuente ya importada. Ya no se necesita el directorio del agente anterior.
Editar estas fuentes y regenerar, no editar solo los HTML de salida.

Las referencias nacionales son el filtro inicial y aparecen primero. Miami
sigue disponible como contexto. Los filtros se combinan por grupo, formato,
tipo y texto. Sin JavaScript todas las referencias siguen legibles. Las
imágenes se muestran completas y enlazan al archivo y a Instagram.

Conservar fecha y procedencia al actualizar. No transformar datos ausentes
en ceros ni presentar estas muestras diferentes como un ranking homogéneo.
Las capturas y descripciones no sustituyen ver los reels completos.

Se mantiene el acceso visual original. La inspiración sigue siendo interna;
al cliente van solo análisis y propuestas seleccionadas. GitHub Pages publica
la raíz de `main`. Validar enlaces, filtros e imágenes antes de publicar.

## Documentación anterior (archivo)

Conocimiento de la empresa, por cliente. Se consulta online en https://muviproject.github.io/portal-interno/ (acceso con clave, cortina visual).

Fuente: `../files/portal-interno-muviproject.html`. Para actualizar: editar ese archivo y correr `python3 build.py`, luego commit + push.

Página de inspiración (`inspiracion.html`, dos vistas: por competidor y por tipo de pieza): la genera `build_inspiracion.py` desde `../files/med-aesthetics-materiales/inspiracion/<handle>/datos.json` (15 competidores, top 5 reels + piezas distintas, captura 14-nov-2026) y copia los JPG a `inspiracion/<handle>/`. `build.py` la regenera sola al final. Es referencia INTERNA para decidir con Rosanna, nunca va al portal del cliente.
