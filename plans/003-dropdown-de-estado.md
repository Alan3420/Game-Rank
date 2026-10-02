# 003 — Animar el desplegable de estado desde su botón

- **Status**: DONE
- **Commit**: 0229bee
- **Severity**: MEDIUM
- **Category**: Missed opportunities · Physicality & origin
- **Estimated scope**: 4 archivos, ~30 líneas
- **Depends on**: 001 (token `--ease-out`)

## Problem

El desplegable de estado (Playing, Completed…) aparece y desaparece al instante, sin relación espacial con su botón, mientras que el menú de usuario (`frontend/src/base/style_app.css:373`, `<Transition name="dropdown">`) sí anima. Dos ubicaciones:

```html
<!-- frontend/src/components/Cards/GameCard.vue:67 — current -->
<div v-if="mostrarDropdown && canChangeStatus" class="card-status-dropdown-wrap">
  <GameStatusDropdown ... />
</div>
```

```html
<!-- frontend/src/components/GameDetail/GameDetail.vue:167 — current -->
<div v-if="showStatusModal && game" class="hero-status-dropdown-wrap">
  <GameStatusDropdown ... />
</div>
```

El de la tarjeta se abre hacia abajo desde un botón arriba a la izquierda (`top: 52px; left: 8px`, `GameCard.css:148`). El del detalle se abre hacia arriba, alineado a la derecha (`bottom: calc(100% + 8px); right: 0`, `styles_GameDetail.css:361`).

## Target

Envolver cada `div` con `<Transition name="gsd">` y añadir en el CSS de cada componente:

```css
.gsd-enter-active {
  transition: opacity 160ms var(--ease-out), transform 160ms var(--ease-out);
}
.gsd-leave-active {
  transition: opacity 100ms var(--ease-out);
}
.gsd-enter-from {
  opacity: 0;
  transform: scale(0.96);
}
.gsd-leave-to {
  opacity: 0;
}
```

Origen: `.card-status-dropdown-wrap { transform-origin: top left; }` y `.hero-status-dropdown-wrap { transform-origin: bottom right; }`.

## Repo conventions to follow

- Ejemplar: `frontend/src/base/App.vue:54` (`<Transition name="dropdown">` alrededor de `.user-dropdown`) y sus clases en `style_app.css:373`.
- Los estilos de cada componente son `scoped` (`<style scoped src=...>`); las clases de transición van en el CSS del componente que contiene el `<Transition>`.

## Steps

1. `GameCard.vue:67`: envolver el `div.card-status-dropdown-wrap` completo (hasta su `</div>`) en `<Transition name="gsd">…</Transition>`.
2. `GameCard.css`: añadir `transform-origin: top left;` a `.card-status-dropdown-wrap` y las 4 reglas `.gsd-*` del Target después de ella.
3. `GameDetail.vue:167`: envolver el `div.hero-status-dropdown-wrap` completo en `<Transition name="gsd">…</Transition>`.
4. `styles_GameDetail.css`: añadir `transform-origin: bottom right;` a `.hero-status-dropdown-wrap` y las 4 reglas `.gsd-*` después.

## Boundaries

- No tocar `GameStatusDropdown.vue`.
- No cambiar la lógica de apertura (`mostrarDropdown`, `showStatusModal`).

## Verification

- **Mechanical**: `npx vite build` termina con `✓ built`.
- **Feel check**:
  - En el catálogo, el desplegable crece desde la esquina del botón de marcador, no desde el centro.
  - En el detalle, crece hacia arriba desde el botón "Status".
  - Abrir y cerrar rápido varias veces: nunca reinicia desde cero de golpe (son transiciones).
  - Con movimiento reducido emulado: solo fundido, sin escala.
- **Done when**: ambos desplegables usan `<Transition name="gsd">`.
