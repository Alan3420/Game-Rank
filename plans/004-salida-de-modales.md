# 004 — Dar salida a los modales y unificar su movimiento

- **Status**: DONE
- **Commit**: 0229bee
- **Severity**: MEDIUM
- **Category**: Interruptibility · Cohesion & tokens · Missed opportunities
- **Estimated scope**: 5 archivos, ~60 líneas
- **Depends on**: 001 (token `--ease-out`)

## Problem

Los modales entran con `@keyframes` y salen al instante (se desmontan con `v-if`), y cada familia usa una curva distinta:

```css
/* frontend/src/style.css — .ext-modal-overlay / .ext-modal (current) */
animation: extOverlayIn 0.2s ease;
animation: extModalUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
```

```css
/* frontend/src/components/User/style_perfil.css:680 y :696 — current */
animation: overlayFadeIn 0.25s ease;
animation: modalSlideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
```

Modales afectados:
- `frontend/src/components/Confirm/ConfirmDialog.vue:3` (`.ext-modal-overlay`)
- `frontend/src/components/GameDetail/GameDetail.vue` modal de enlace externo (`<div v-if="externalLink.open" class="ext-modal-overlay"`)
- `frontend/src/components/User/perfil_user.vue:364` (Editar perfil) y `:486` (Cambiar contraseña), `.edit-modal-overlay`

`frontend/src/base/App.vue:188` (`<Transition name="modal-fade">`) ya tiene salida; queda fuera de alcance salvo para alinear su curva.

## Target

Clases globales en `frontend/src/style.css` (sustituyen a los keyframes):

```css
/* entrada 220ms, salida 150ms: el sistema responde rápido al cerrar */
.modal-enter-active {
  transition: opacity 220ms var(--ease-out);
}
.modal-leave-active {
  transition: opacity 150ms var(--ease-out);
}
.modal-enter-active .ext-modal,
.modal-enter-active .edit-modal {
  transition: opacity 220ms var(--ease-out), transform 220ms var(--ease-out);
}
.modal-leave-active .ext-modal,
.modal-leave-active .edit-modal {
  transition: opacity 150ms var(--ease-out), transform 150ms var(--ease-out);
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .ext-modal,
.modal-enter-from .edit-modal {
  opacity: 0;
  transform: translateY(8px) scale(0.97);
}
.modal-leave-to .ext-modal,
.modal-leave-to .edit-modal {
  opacity: 0;
  transform: scale(0.97);
}
```

Los modales siguen centrados (`transform-origin: center` por defecto, correcto en modales).

## Repo conventions to follow

- Ejemplar de `<Transition>` alrededor de un overlay: `frontend/src/base/App.vue:188`.
- `.ext-modal*` son estilos globales en `frontend/src/style.css`; por eso las clases `.modal-*` van ahí y valen también para el `scoped` de perfil (las clases de transición se aplican al elemento raíz, que no depende del scope).

## Steps

1. `style.css`: quitar `animation: extOverlayIn 0.2s ease;` de `.ext-modal-overlay` y `animation: extModalUp …;` de `.ext-modal`; borrar `@keyframes extOverlayIn` y `@keyframes extModalUp`; añadir las reglas `.modal-*` del Target.
2. `style_perfil.css`: quitar `animation: overlayFadeIn 0.25s ease;` y `animation: modalSlideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);`; borrar `@keyframes overlayFadeIn` y `@keyframes modalSlideUp`.
3. `ConfirmDialog.vue`: envolver el `div.ext-modal-overlay` (dentro del `<Teleport>`) en `<Transition name="modal">…</Transition>`.
4. `GameDetail.vue`: envolver el `div.ext-modal-overlay` del enlace externo en `<Transition name="modal">…</Transition>`.
5. `perfil_user.vue`: envolver cada `div.edit-modal-overlay` (líneas 364 y 486, cada uno hasta su `</div>` de cierre) en `<Transition name="modal">…</Transition>`.
6. `style_app.css`: en `.modal-fade-enter-active .confirm-modal, .modal-fade-leave-active .confirm-modal` cambiar `transition: transform 0.2s ease;` por `transition: transform 0.2s var(--ease-out);`, y en `.modal-fade-enter-active, .modal-fade-leave-active` cambiar `transition: opacity 0.2s ease;` por `transition: opacity 0.2s var(--ease-out);`.

## Boundaries

- No cambiar la lógica de apertura/cierre ni el foco de `ConfirmDialog`.
- No tocar el contenido de los modales.

## Verification

- **Mechanical**: `npx vite build` termina con `✓ built`; `grep -rn "extModalUp\|modalSlideUp\|overlayFadeIn\|extOverlayIn" frontend/src` no devuelve nada.
- **Feel check**:
  - Perfil > Editar perfil > Cancelar: el modal se desvanece y encoge un poco en ~150ms, no desaparece de golpe.
  - Quitar un favorito > Cancel: igual.
  - DevTools > Animations al 10 %: la salida es más corta que la entrada.
  - Movimiento reducido: solo fundido.
- **Done when**: los cuatro modales usan `<Transition name="modal">` y no quedan keyframes de modal.
