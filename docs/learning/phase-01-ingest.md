# Fase 1 — Ingesta + índice

> Qué se aprende en esta fase y por qué importa.
> Conecta con las fases vecinas: convierte un repo real en datos consultables (la Fase 2 los lee).
> Log de la fase → `docs/progress-log/phase-01-ingest.md`

## Glosario de la fase

| Término | Qué significa (en una línea) |
|---|---|
| **Ingesta** | Convertir archivos de un repo en unidades indexables |
| **Scanner** | Enumera *qué* archivos entran (respeta `.gitignore`) |
| **Chunk** | Fragmento de documento que se indexa como una unidad |
| **Chunker** | Parte documentos en chunks por su estructura |
| **FTS5** | Motor de búsqueda de texto completo de SQLite |
| **BM25** | Ranking léxico que usa FTS5 (rareza + frecuencia) |
| **Token** | Unidad mínima de búsqueda (aprox. una palabra) |
| **Tokenización** | Regla que decide qué cuenta como un token |
| **Normalización** | Unificar formas (minúsculas, acentos) antes de indexar |
| **Golden file** | Salida esperada escrita a mano; el oráculo del test |
| **Seam** | Punto de inyección para reemplazar una dependencia en tests |

## Mapa de conceptos

```text
scanner (qué archivos) ──► chunker (cómo partirlos) ──► store (SQLite FTS5)
                                                            │
tokenización + normalización ──► MATCH sanitizado ──► búsqueda léxica (BM25)
                                                            │
                                          oráculo (golden files): ¿recupera lo correcto?
```

## Puntos de inyección de la fase

| Componente | Seam | Doble | Test real |
|---|---|---|---|
| Git | `list_tracked_files(root)` | lista fija en el test | `git ls-files` |
| Filesystem | `Path` por parámetro | `tmp_path` de pytest | fixtures del corpus |

---

## Chunking por estructura

### En una frase

Partir un documento por sus unidades de significado (headings, funciones, clases), no por cantidad de caracteres.

### Fundamentos previos

Un **documento** es cualquier archivo de texto del repo (markdown, código, configuración). Un **chunk** es el fragmento que se indexa como unidad. La **metadata** es información que acompaña al chunk (de qué archivo salió, qué heading lo abarca).

### Qué es

Chunking es la decisión de dónde cortar un documento antes de indexarlo. Cortar por estructura significa respetar las fronteras que ya existen en el texto: un `##` de markdown abre una sección, una `def` en Python abre una función.

### Qué problema resuelve

Si cortás cada N caracteres, partís una función al medio: la mitad de arriba pierde su nombre y la de abajo pierde su firma. Al recuperar, traés fragmentos incompletos y el LLM (Fase 2) no puede citar `archivo:línea`.

### Cómo funciona paso a paso

1. Se lee el archivo como texto.
2. Se detectan marcas estructurales según el tipo: headings para markdown, símbolos para código.
3. Cada unidad se convierte en un chunk con metadata: `path`, `heading`/símbolo y orden.
4. Si una unidad es enorme, se subdivide; si es diminuta, se fusiona con la vecina.

### Qué se rompería sin esto en postforge

El `brief.json` de la Fase 2 citaría fragmentos sin sentido y los golden files no podrían exigir `modules/01-pam-gate` como recuperable.

### Para qué sirve en este proyecto

Es el núcleo de `ingest/chunker.py` y la razón de que `search` devuelva `archivo:línea` con contexto útil.

### Cómo se usa (código real)

> Pendiente: se completa al implementar `ingest/chunker.py` (Feature 1.2/1.3, TDD).

### Error común

Medir la calidad del chunking por cantidad de chunks. Lo correcto es medirlo por los golden files: ¿recupera lo que el oráculo dice que debe recuperar?

### Punto de inyección (si aplica)

El chunker es lógica pura sobre texto: no necesita seam. El `Path` entra por parámetro y se testea con `tmp_path`.

### Para profundizar

- `docs/development-plan.md` §Oráculo de ingesta.

---

## Búsqueda léxica: BM25 y FTS5

### En una frase

FTS5 es el buscador de texto de SQLite; BM25 es el criterio con el que decide qué resultado va primero.

### Fundamentos previos

**Índice invertido**: mapa de palabra → documentos que la contienen (al revés de documento → palabras). **SQLite** es una base de datos embebida en un solo archivo, sin servidor. **FTS5** es su módulo de texto completo.

### Qué es

FTS5 guarda el texto tokenizado en un índice invertido y responde consultas con `MATCH`. BM25 puntúa cada resultado combinando cuántas veces aparece el término (frecuencia) con cuán raro es en el corpus (rareza).

### Qué problema resuelve

Buscar sin FTS5 obligaría a recorrer cada chunk con substrings: lento y sin ranking. BM25 ordena por relevancia y hace que el término raro pese más que el común.

### Cómo funciona paso a paso

1. Al indexar, el texto se tokeniza y se guarda en la tabla FTS5.
2. La consulta se transforma en una expresión `MATCH`.
3. FTS5 calcula BM25 por fila y ordena.
4. Se devuelven los top-k con su `path` y número de línea.

### Qué se rompería sin esto en postforge

`search "pam"` tendría que leer todos los archivos cada vez y no podría priorizar; el brief no tendría de dónde sacar evidencia citada.

### Para qué sirve en este proyecto

Es el motor de `index/store.py` (Feature 1.4) y la mitad léxica de la búsqueda híbrida de la Fase 2.

### Cómo se usa (código real)

> Pendiente: se completa al implementar `index/store.py` (Feature 1.4, TDD).

### Error común

Creer que FTS5 "entiende" significado. Es léxico: busca palabras. La paráfrasis la cubren los embeddings (Fase 2), por eso la fusión es obligatoria.

### Punto de inyección (si aplica)

La base se abre sobre un `Path` temporal en los tests (`tmp_path`), nunca sobre la caché real.

### Para profundizar

- Documentación oficial de SQLite FTS5.
- `docs/adr/ADR-004-embeddings-model.md` — por qué el léxico no alcanza solo.

---

## Tokenización y normalización (query sanitizada)

### En una frase

Antes de indexar o buscar hay que decidir qué es "una palabra" y unificar sus variantes; y antes de armar un `MATCH` hay que neutralizar los caracteres que FTS5 interpreta como operadores.

### Fundamentos previos

**Token**: la unidad que el índice guarda. **Normalización**: llevar texto a una forma canónica (p. ej. minúsculas) para que variantes coincidan. **Sanitizar**: quitar o escapar lo que tiene significado especial en un lenguaje.

### Qué es

FTS5 interpreta su sintaxis de consulta: comillas, `*`, `NEAR`, `OR`, `:`. Un término de usuario con esos caracteres no se busca: se *ejecuta* como operador y puede romper la query.

### Qué problema resuelve

Sin sanitizar, `search "chattr +i"` o un path con `:` (como `C:\...`) lanzan error de sintaxis en `MATCH`; sin normalizar, "PAM" y "pam" serían mundos distintos.

### Cómo funciona paso a paso

1. Se elige un tokenizer al crear la tabla FTS5 (p. ej. `unicode61`).
2. Al buscar, se parte la query en términos.
3. Cada término se escapa o se envuelve en comillas dobles para tratarlo como literal.
4. Recién ahí se arma la expresión `MATCH`.

### Qué se rompería sin esto en postforge

El gotcha conocido del proyecto: términos con caracteres especiales rompen la búsqueda. Un `search` del usuario fallaría de forma críptica.

### Para qué sirve en este proyecto

Es la regla defensiva de `index/store.py`: toda query pasa por un sanitizador antes de tocar `MATCH`.

### Cómo se usa (código real)

> Pendiente: se completa al implementar `index/store.py` (Feature 1.4, TDD).

### Error común

Concatenar la query del usuario directo en el `MATCH`. Se ve funcionar con "pam" y explota con `"chattr +i"`.

### Punto de inyección (si aplica)

Lógica pura: se testea con casos borde (operadores, comillas, acentos) sin dependencias externas.

### Para profundizar

- Documentación oficial de SQLite FTS5 (tokenizers y sintaxis de query).

---

## Relación entre estos conceptos

El **scanner** decide qué archivos entran; el **chunker** los parte por estructura; el **store** los guarda en FTS5 y los busca con BM25. La **tokenización/normalización** atraviesa el indexado y la búsqueda: define las palabras del índice y evita que la sintaxis de la query la rompa. El **oráculo (golden files)** no es un concepto técnico sino la garantía de que todo esto recupera lo *correcto*, no solo lo *consistente*.
