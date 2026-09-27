# Arquetipo — Datos, RAG y pipelines

> Base común: `hooks-psychology.md`, `recruiter-ats.md`, `linkedin-form.md`.

## Señales (detección)

- Ingesta → índice → consulta; embeddings; FTS; evaluación de resultados.
- Schema de datos, migraciones, notebooks o scripts de análisis.
- Configuración de modelos (ONNX, APIs) y prompts en archivos.

## Hook recomendado

Fórmulas: **métrica** o **resultado inesperado**.

Forma: «Bajé el contexto que recibe el LLM de N a M tokens sin perder precisión» / «El índice léxico le ganaba al vectorial en este caso».

## Prueba que importa

| Prueba | De dónde sale |
|---|---|
| Comparación de enfoques (léxico vs vectorial, A/B) | Benchmarks del repo |
| Calidad de recuperación (precision, casos) | Golden files, tests |
| Coste/velocidad por corrida | Si está medido |
| Decisiones y sus trade-offs | ADRs |

## Media

| Pieza | Formato | Por qué |
|---|---|---|
| Principal | Diagrama del pipeline (`mmdc`) | Es el producto en una imagen |
| Secundaria | Chart de resultados (`matplotlib`) | Muestra la mejora con datos reales |

## Aptitudes típicas (taxonomía)

`ia-y-rag` (RAG, embeddings, FTS5, prompt engineering) · `python-cli` (Python, pytest) · `datos-y-sql`.

## Descripción del formulario

Problema del flujo de datos (1 línea) → pipeline en pasos (2-3) → stack (1) → resultado medido (1).

## Evitar

- «Usé IA» sin decir para qué.
- Mostrar embeddings como vectores ilegibles.

## Ejemplos del autor

`postforge` (RAG local para posts) · bases para pipelines de datos futuros.
