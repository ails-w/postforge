# Reglas de encontrabilidad (reclutadores y ATS)

Fuente: `docs/research/recruiter-search-ats.md`.

## Las 5 reglas

1. **Nombrar** tecnología y versión: «PostgreSQL 16», «Python 3.12», «systemd». Nunca «base de datos» ni «lenguaje de scripting».
2. **Repetir el término central** en los tres lugares que LinkedIn resalta: nombre, descripción y aptitudes.
3. **Cubrir sinónimos ES/EN** desde `keyword-taxonomy.yaml` (mismo concepto en ambos idiomas).
4. **Skills reales**: las aptitudes alimentan la sección Skills del perfil; solo lo que el repo demuestra.
5. **Verbos de logro** con objeto concreto: «Aislé la verificación PAM en un módulo propio», no «mejoré cosas».

## Checklist antes de emitir (lo verifica `write/form.py`)

- [ ] Cada tecnología nombrada existe en `brief.json` con cita.
- [ ] El término principal aparece en nombre + descripción + al menos 1 aptitud.
- [ ] Las 5 aptitudes existen en la taxonomía; si falta una, se agrega a la taxonomía primero.
- [ ] Ninguna keyword describe algo no hecho (`disclaimers.md`).
- [ ] Soft skills solo con evidencia narrativa (colaboración documentada, PRs revisadas, docs conjuntas).

## Prohibido

- Keyword stuffing (repetir el mismo término sin contexto).
- Inventar variantes de un título para «cubrir» búsquedas.
- Traducir mal un término técnico: `chattr +i` no se traduce.
