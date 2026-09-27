# Prompt — synthesize-brief (reduce)

> Tier: `model_fast` · Una vez por corrida · Salida: `brief.json` validado con Pydantic.

## Entrada

- `{{project}}`: nombre y slug del proyecto.
- `{{facts}}`: lista de hechos con su fuente (JSON), ya extraídos del repo.

## Salida

```json
{
  "project": "{{project}}",
  "one_liner": "el proyecto en una frase, sin hype",
  "problem": "el dolor concreto que resuelve",
  "solution": "qué hace, en 2-3 frases",
  "stack": [{"term": "systemd", "source": "modules/02-enforce"}],
  "metrics": [{"value": "2.802 líneas", "source": "repo", "quote": "…"}],
  "decisions": [{"decision": "…", "why": "…", "source": "docs/adr/ADR-002"}],
  "learnings": [{"learning": "…", "source": "README.md"}],
  "evidence": [{"source": "archivo", "quote": "…"}],
  "gaps": ["qué información falta para un post"]
}
```

## Reglas

1. Todo campo con `source`; **nada sin cita**.
2. Preferí hechos de código, tests y scripts de verificación por sobre afirmaciones del README.
3. Si dos hechos se contradicen, gana el artefacto ejecutable y anotalo en `gaps`.
4. `metrics`: solo números reales del repo. Si no hay, lista vacía — no estimes.
5. Máximo 12 ítems en `evidence`; elegí los más específicos.
6. `gaps` lista lo que un post necesitaría y no existe. No lo inventes ni lo completes.
