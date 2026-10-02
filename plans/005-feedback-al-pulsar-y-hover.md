# 005 — Feedback al pulsar los favoritos y hover solo con ratón

- **Status**: DONE
- **Commit**: 0229bee
- **Severity**: MEDIUM
- **Category**: Physicality & origin · Accessibility
- **Estimated scope**: 2 archivos, ~30 líneas
- **Depends on**: 001 (token `--ease-out`), 002 (libera el `transform` de `.game-card`)

## Problem

Los botones de favorito no responden al pulsar y su escalado de hover se dispara también en táctil (un toque deja el `:hover` pegado):

```css
/* frontend/src/components/Cards/GameCard.css:73 — current */
.card-action-btn {
  ...
  transition: transform 0.15s ease, background 0.15s ease;
}
.card-action-btn:hover {
  transform: scale(1.12);
  background: white;
}
```

```css
/* frontend/src/components/GameDetail/styles_GameDetail.css:281 — current */
.hero-fav-btn {
    ...
    transition: transform 0.2s ease, background 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}
.hero-fav-btn:hover {
    background: rgba(255, 255, 255, 0.18);
    border-color: rgba(255, 255, 255, 0.75);
    transform: scale(1.06);
}
```

La elevación de la tarjeta (`.game-card:hover { transform: translateY(-8px) }`) tampoco está limitada a dispositivos con ratón.

## Target

```css
/* GameCard.css */
.card-action-btn {
  transition: transform 160ms var(--ease-out), background-color 150ms ease;
}
@media (hover: hover) and (pointer: fine) {
  .card-action-btn:hover {
    transform: scale(1.12);
    background: white;
  }
  .game-card:hover {
    /* reglas actuales de .game-card:hover, sin cambios */
  }
}
.card-action-btn:active,
.card-action-btn:hover:active {
  transform: scale(0.95);
}
```

```css
/* styles_GameDetail.css */
.hero-fav-btn {
    transition: transform 160ms var(--ease-out), background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}
@media (hover: hover) and (pointer: fine) {
    .hero-fav-btn:hover {
        background: rgba(255, 255, 255, 0.18);
        border-color: rgba(255, 255, 255, 0.75);
        transform: scale(1.06);
    }
}
.hero-fav-btn:active,
.hero-fav-btn:hover:active {
    transform: scale(0.95);
}
```

Con movimiento reducido, el plan 001 ya deja el `transform` sin transición (cambio instantáneo, sin desplazamiento animado).

## Repo conventions to follow

- Hay que conservar las reglas de tema oscuro existentes (`[data-theme="dark"] .card-action-btn:hover`); envolverlas también en el mismo `@media (hover: hover) and (pointer: fine)`.

## Steps

1. `GameCard.css`: sustituir el `transition` de `.card-action-btn` por el del Target.
2. `GameCard.css`: mover `.card-action-btn:hover`, `.game-card:hover` (y sus variantes `[data-theme="dark"] … :hover` y `.game-card:hover .game-image`/`.image-overlay`) dentro de `@media (hover: hover) and (pointer: fine) { … }` sin cambiar sus declaraciones.
3. `GameCard.css`: añadir la regla `:active` del Target después del bloque `@media`.
4. `styles_GameDetail.css`: lo mismo para `.hero-fav-btn` (transition, `:hover` dentro del `@media`, `:active`).

## Boundaries

- No tocar `GameCard.vue` ni `GameDetail.vue`.
- No cambiar colores ni tamaños.

## Verification

- **Mechanical**: `npx vite build` termina con `✓ built`.
- **Feel check**:
  - Pulsar y mantener el corazón de una tarjeta: se encoge ligeramente (0.95) y vuelve al soltar.
  - DevTools en modo dispositivo táctil: tocar una tarjeta no deja el corazón escalado ni la tarjeta elevada.
- **Done when**: los dos botones tienen `:active` y sus `:hover` con `transform` están dentro de `@media (hover: hover) and (pointer: fine)`.
