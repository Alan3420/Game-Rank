# 002 — Acortar la entrada escalonada de GameCard y liberar el hover

- **Status**: DONE
- **Commit**: 0229bee
- **Severity**: HIGH
- **Category**: Cohesion & tokens · Purpose & frequency
- **Estimated scope**: 1 archivo (`frontend/src/components/Cards/GameCard.css`), ~25 líneas
- **Depends on**: 001 (token `--ease-out`)

## Problem

```css
/* frontend/src/components/Cards/GameCard.css:235 — current */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.game-card {
  animation: fadeIn 0.4s ease-out both;
  animation-delay: calc(var(--card-index, 0) * 90ms);
}
```

1. 90ms por tarjeta sin límite: en el catálogo (20 tarjetas por página) la última aparece a los 1,8 s + 0,4 s. Se repite en cada cambio de página (decenas de veces al día). El escalonado es decorativo y nunca debe bloquear: 30–80ms y con tope.
2. `animation-fill-mode: both` mantiene `transform: translateY(0)` al terminar, y una animación pisa a la declaración normal, así que `.game-card:hover { transform: translateY(-8px) }` nunca se aplica.
3. 20px de recorrido y `ease-out` estándar son demasiado para una entrada tan frecuente.

## Target

```css
@keyframes cardEnter {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
}

.game-card {
  /* backwards: aplica el estado inicial durante el retraso y libera
     transform al terminar, para que el hover funcione */
  animation: cardEnter 300ms var(--ease-out) backwards;
  /* 40ms entre tarjetas, con tope en la 8.ª (máx. 320ms) */
  animation-delay: calc(min(var(--card-index, 0), 8) * 40ms);
}

@media (prefers-reduced-motion: reduce) {
  .game-card {
    animation-name: cardFade;
    animation-delay: 0ms;
  }
}

@keyframes cardFade {
  from { opacity: 0; }
}
```

## Repo conventions to follow

- El índice llega por `:style="{ '--card-index': index }"` en `frontend/src/components/Cards/GameCard.vue:2`; no cambiarlo.
- Curva: `var(--ease-out)` definida en `frontend/src/style.css` (plan 001).

## Steps

1. Sustituir `@keyframes fadeIn {...}` por `@keyframes cardEnter` del Target.
2. Sustituir la regla `.game-card { animation…; animation-delay… }` por la del Target.
3. Añadir el bloque `prefers-reduced-motion` y `@keyframes cardFade` del Target justo después.
4. Comprobar que no queda ninguna referencia a `fadeIn` en el archivo.

## Boundaries

- No tocar el `transition` ni el `:hover` de `.game-card` (los gestiona el plan 005).
- No tocar `GameCard.vue`.

## Verification

- **Mechanical**: `npx vite build` termina con `✓ built`.
- **Feel check**: abrir `/content/overview`:
  - Todas las tarjetas visibles han aparecido en menos de ~0,6 s.
  - Al pasar el ratón por una tarjeta, se eleva (`translateY(-8px)`), cosa que antes no hacía.
  - DevTools > Animations al 10 %: el escalonado se detiene en la 9.ª tarjeta; de ahí en adelante entran a la vez.
- **Done when**: no hay `90ms` ni `both` en la regla `.game-card`, y el hover eleva la tarjeta.
