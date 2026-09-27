# Pipeline de visuales para backend, APIs y scripts

- **Fecha:** 2026-09-27
- **Estado:** snapshot
- **Pregunta:** ¿con qué imagen se postea un proyecto sin UI?

## Inventario verificado (2026-09-27)

| Herramienta | Estado | Uso |
|---|---|---|
| `mmdc` 11.16.0 | ✅ instalado | Mermaid → SVG/PNG/PDF; con `-i file.md` extrae **todos** los bloques mermaid del markdown |
| ImageMagick (`magick`, `convert`) | ✅ | Composición, resize, optimización |
| `rsvg-convert` | ✅ | SVG → PNG sin navegador |
| `ffmpeg` | ✅ | Conversión de video/GIF |
| Go 1.27 / Cargo 1.98 | ✅ | Vía alternativa de instalación si falta el paquete |
| `silicon`, `vhs`, `asciinema` | ❌ (están en repo `extra`) | Snippet de código, GIF de terminal, grabación |

**Prueba real de mmdc:** `mmdc -i t.mmd -o t.png -q` → exit 0, PNG 394×70 generado **sin Chromium en PATH** (usa el navegador propio de puppeteer). La ruta Mermaid → PNG funciona hoy.

## Qué se postea cuando no hay UI

| Arquetipo | Pieza principal | Pieza secundaria | Evitar |
|---|---|---|---|
| `backend-api` | Diagrama de secuencia (request → handler → DB) | Snippet del handler + métrica | JSON crudo en terminal |
| `cli-systems` | GIF de terminal (`vhs`) | Diagrama de componentes | Muro de código |
| `iac-security` | Diagrama de capas (`mmdc`) | Config antes/después | Logs |
| `docs-data` | Portada + flujo del pipeline | Tabla comparativa | — |
| `lib` | Ejemplo de uso | Diagrama de API pública | — |

Regla de atención: **1 pieza fuerte > 3 mediocres**. El post solo lleva la que se sostiene sola.

## Recetas

### 1. Mermaid → PNG (`mmdc`)

```bash
# Un diagrama
mmdc -i diagram.mmd -o diagram.png -t neutral -b transparent -s 2

# TODOS los diagramas de un doc (los repos ya tienen docs/diagrams/*.md)
mmdc -i docs/architecture.md -o out/diagrams.md -a out/diagrams/ -t neutral -s 2
```

- `-s 2` = retina; `-t neutral` o `themeVariables` vía `-c config.json` para un tema consistente.
- `--iconPacks` (logos de tecnologías) descarga de unpkg: dejar para después.

### 2. Terminal → GIF (`vhs`) — a instalar en Fase 4

```bash
sudo pacman -S vhs
vhs demo.tape   # guion versionado: width/height/fontSize/theme + comandos
```

Guion determinista en `visuals/demos/*.tape`; misma corrida → mismo GIF.

### 3. Snippet de código (`silicon`) — a instalar en Fase 4

```bash
sudo pacman -S silicon
silicon src/postforge/llm.py -o snippet.png --theme Dracula --pad 24
```

### 4. Charts y portada (matplotlib, se instala con uv)

- Portada: 1200×627 o 1080×1350 con título + stack + resultado; los datos salen de `brief.json` (única fuente).
- Charts: barras simples (tests, LOC, latencia) **solo si hay dato real** del repo.
- Alternativa sin Python: SVG a mano + `rsvg-convert`.

### 5. Fallback sin navegador

- SVG + `rsvg-convert -w 1080` → PNG; composición fina con `magick`.

## Specs de LinkedIn (2026)

| Formato | Medida | Uso |
|---|---|---|
| Imagen cuadrada | 1080×1080 (1:1) | Feed |
| Vertical | 1080×1350 (4:5) | Más área en móvil |
| Link preview | 1200×627 (1.91:1) | Cuando el post lleva link |
| Documento/carrusel | PDF, **RGB (no CMYK)**, 1080×1080 o 1080×1350 | Multi-página |

Límites de subida del formulario → `linkedin-form-contract.md` (100 MB, 300 páginas).

## Integración en postforge (Fase 4)

| Pieza | Módulo | Salida |
|---|---|---|
| Diagramas | `visuals/mermaid.py` | `out/<slug>/<fecha>/media/diagrams/*.png` |
| GIF de terminal | `visuals/terminal.py` | `.../media/demo.gif` |
| Snippet | `visuals/snippet.py` | `.../media/snippet.png` |
| Portada y charts | `visuals/cover.py` | `.../media/cover.png` |

- `form.md` lista la media con ruta, medidas y formato (se sube a mano).
- Todo determinista: mismo repo → misma media.
- Fase 4 instala `silicon`/`vhs`; `mmdc` ya está.

## Fuentes y verificación

| Fuente | Uso | Consultado |
|---|---|---|
| `mmdc --help` (v11.16.0, local) | Flags reales | 2026-09-27 |
| Prueba local `mmdc` | Rasteriza sin Chromium en PATH | 2026-09-27 |
| `pacman -Si` | `silicon`/`vhs`/`asciinema` en `extra` | 2026-09-27 |
| Guías 2026 (Hootsuite, Sendible, LinkedIn Pulse) | Tamaños y ratios | 2026-09-27 |
