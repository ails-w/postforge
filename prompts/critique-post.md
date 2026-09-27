# Prompt — critique-post

> Tier: `model_write` · Una vez por variante · Salida: JSON según `knowledge/rubric.md`.

## Entrada

- `{{post}}`: una variante generada.
- `{{brief}}`: brief.json (la única evidencia válida).
- `{{rubric}}`: criterios y pesos.

## Salida

```json
{
  "scores": {
    "hook": 0,
    "evidence": 0,
    "discoverability": 0,
    "structure": 0,
    "clarity": 0,
    "hygiene": 0
  },
  "total": 0,
  "hard_failures": [],
  "fixes": ["máximo 3, accionables"],
  "verdict": "publish|rewrite|discard"
}
```

Pesos: hook 25 · evidence 25 · discoverability 20 · structure 15 · clarity 10 · hygiene 5.

## Reglas

1. `hard_failures`: hechos sin respaldo en el brief, límites violados (255/2.000/5), keywords de cosas no hechas.
2. Con un `hard_failure`, `verdict` no puede ser `publish` (el total se ignora).
3. Cada `fix` cita el criterio que viola y es accionable («acortar el hook a ≤ 140», no «mejorar el hook»).
4. Umbrales: ≥ 80 publish · 60-79 rewrite · < 60 discard.
5. **No reescribas el post acá**: solo puntuá y señalá.
