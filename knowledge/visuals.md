# Visuals — recetas operativas

Fuente: `docs/research/visuals-pipeline.md`. Consumidor: `visuals/*` (Fase 4).

## Reglas

1. **Default del post: 1 imagen** (`cover.png` o el diagrama principal). En total (post + formulario) no pasar de 3 piezas.
2. **Carrusel (`carousel.pdf`) solo para proyectos insignia**: 3-5 páginas (portada, diagrama, prueba). Documento e imágenes **no** se mezclan en un mismo post.
3. Specs: 1080×1080 (1:1) o 1080×1350 (4:5, es el ratio máximo que LinkedIn muestra); link preview 1200×627.
4. Todo determinista y generado en `out/<slug>/<fecha>/media/`; nada se commitea.
5. Si un dato no está en `brief.json`, no se dibuja.

## Inventario

| Herramienta | Estado | Uso |
|---|---|---|
| `mmdc` 11.16.0 | ✅ | Mermaid → PNG/SVG/PDF |
| `magick` / `convert` | ✅ | Composición; unir páginas en PDF |
| `rsvg-convert` | ✅ | SVG → PNG sin navegador |
| `ffmpeg` | ✅ | GIF/MP4 |
| `silicon` | ❌ `sudo pacman -S silicon` | Snippet de código |
| `vhs` | ❌ `sudo pacman -S vhs` | GIF de terminal |
| `matplotlib` | ✅ (vía `uv add`) | Portada y charts |

## Recetas

### Diagrama (`mmdc`)

```bash
mmdc -i docs/diagrams/enforcement-flow.md -o media/diagram.png -t neutral -b transparent -s 2
mmdc -i docs/architecture.md -o /tmp/all.md -a media/diagrams/ -t neutral -s 2
```

### Portada (`matplotlib`)

- 1080×1350; título del proyecto + resultado principal + stack nombrado; sin logos de terceros.
- Los textos salen de `brief.json`: misma corrida → misma portada.

### Snippet (`silicon`)

```bash
silicon src/postforge/llm.py -o media/snippet.png --theme "One Half Dark" --pad 24
```

### GIF de terminal (`vhs`)

```tape
Output media/demo.gif
Set FontSize 18
Set Width 1200
Set Height 600
Type "uv run postforge brief focusguard"
Enter
Sleep 2s
```

### Carrusel (`magick`)

```bash
magick page-01.png page-02.png page-03.png -quality 90 media/carousel.pdf
```

Páginas de 1080×1350, RGB; 3-5 páginas; la primera es la portada.

## Naming

```text
out/<slug>/<fecha>/media/
├── cover.png          # default del post
├── diagram.png        # pieza principal alternativa
├── snippet.png
├── demo.gif
├── carousel.pdf       # proyectos insignia
└── manifest.md        # qué es cada pieza y dónde se adjunta
```
