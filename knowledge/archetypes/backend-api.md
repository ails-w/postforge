# Arquetipo — Backend y APIs

> Base común: `hooks-psychology.md`, `recruiter-ats.md`, `linkedin-form.md`.

## Señales (detección)

- Controladores/routers, endpoints, DTOs, capas service/repository.
- OpenAPI/Swagger, migraciones, esquemas de BD, tests de integración.
- Docker/Compose para levantar el servicio.

## Hook recomendado

Fórmulas: **pregunta específica** o **métrica**.

Forma: «¿Por qué este endpoint devolvía 500 solo los lunes? La causa era X.» / «Bajé la latencia de A a B con Y.»

## Prueba que importa

| Prueba | De dónde sale |
|---|---|
| Contrato de la API | Endpoints, OpenAPI |
| Cobertura de casos límite | Tests de integración |
| Latencia o throughput | Solo si está medido en el repo |
| Decisiones de diseño | ADRs, README |

## Media

| Pieza | Formato | Por qué |
|---|---|---|
| Principal | Diagrama de secuencia request → handler → DB (`mmdc`) | Explica el flujo real |
| Secundaria | Snippet del handler clave (`silicon`) | Muestra el código que importa |

## Aptitudes típicas (taxonomía)

Lenguaje y framework del servicio · `datos-y-sql` (SQL, esquemas) · `devops` (Docker, CI).

## Descripción del formulario

Problema de negocio (1 línea) → qué expone/automatiza (2-3) → stack nombrado (1) → prueba (1).

## Evitar

- JSON crudo como imagen.
- Enumerar endpoints sin contar el problema que resuelven.

## Ejemplos del autor

`TODO_API` (C#/.NET) · `JAVA_CODE` (Spring Boot: library-management-api, solid-payments).
