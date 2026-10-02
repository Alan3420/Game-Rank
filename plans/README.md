# Planes de animación

Generados con la skill `improve-animations` (criterio de Emil Kowalski) sobre el commit `0229bee`.

| # | Plan | Severidad | Estado |
|---|---|---|---|
| 001 | [Tokens de easing y movimiento reducido](001-tokens-y-movimiento-reducido.md) | MEDIUM | DONE |
| 002 | [Entrada escalonada de GameCard](002-entrada-escalonada-gamecard.md) | HIGH | DONE |
| 003 | [Desplegable de estado](003-dropdown-de-estado.md) | MEDIUM | DONE |
| 004 | [Salida de modales](004-salida-de-modales.md) | MEDIUM | DONE |
| 005 | [Feedback al pulsar y hover](005-feedback-al-pulsar-y-hover.md) | MEDIUM | DONE |
| 006 | [Lista de reseñas](006-lista-de-resenas.md) | LOW | DONE |

## Orden recomendado

1. **001** primero: define `--ease-out`, que usan todos los demás.
2. **002** antes que 005: libera el `transform` de `.game-card` que 005 limita a ratón.
3. 003, 004 y 006 son independientes entre sí.

## Dependencias

- 002, 003, 004, 005 y 006 dependen de 001.
- 005 depende de 002.
