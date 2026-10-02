# 001 — Añadir tokens de easing y suavizar el modo de movimiento reducido

- **Status**: DONE
- **Commit**: 0229bee
- **Severity**: MEDIUM
- **Category**: Cohesion & tokens · Accessibility
- **Estimated scope**: 1 archivo (`frontend/src/style.css`), ~20 líneas

## Problem

1. No existen tokens de curvas. Cada componente escribe su propia curva (`ease`, `ease-out`, `cubic-bezier(0.16, 1, 0.3, 1)` en `frontend/src/components/User/style_perfil.css:696`, `cubic-bezier(0.16, 1, 0.3, 1)` en `frontend/src/style.css` para `.ext-modal`). Los planes 002–006 necesitan una curva compartida.

2. El bloque de movimiento reducido anula TODA la animación, incluido el feedback de opacidad:

```css
/* frontend/src/style.css:274 — current */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Movimiento reducido significa menos movimiento y más suave, no cero: hay que quitar desplazamientos y escalados, pero conservar fundidos y cambios de color.

## Target

```css
/* frontend/src/style.css — dentro de :root (tema claro), al final del bloque */
  /* === MOTION === */
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
```

```css
/* frontend/src/style.css — sustituye al bloque actual */
@media (prefers-reduced-motion: reduce) {
  html {
    scroll-behavior: auto;
  }

  /* fuera desplazamientos y escalados: las transiciones solo pueden
     animar opacidad y color; transform cambia al instante */
  *,
  *::before,
  *::after {
    transition-property: opacity, color, background-color, border-color, box-shadow !important;
  }
}
```

Las animaciones `@keyframes` se tratan en su propio componente (planes 002 y 004, y `.dots` de login/registro en este plan).

## Repo conventions to follow

- Los tokens de color viven en `:root` de `frontend/src/style.css` agrupados con comentarios `/* === NOMBRE === */`. Añadir `/* === MOTION === */` igual.
- El tema oscuro (`[data-theme="dark"]`) no necesita redefinir estos tokens.

## Steps

1. En `frontend/src/style.css`, dentro del primer bloque `:root { ... }`, justo antes de su `}` de cierre, añadir el bloque `/* === MOTION === */` del Target.
2. Sustituir el bloque `@media (prefers-reduced-motion: reduce)` actual por el del Target.
3. En `frontend/src/components/LoginRegister/style_login.css` y `style_register.css`, añadir al final:
   ```css
   @media (prefers-reduced-motion: reduce) {
     .dot { animation: none; opacity: 0.6; }
   }
   ```
   Antes, comprobar el selector exacto que usa `animation: dots` (buscar `animation: dots`) y usar ese selector.

## Boundaries

- No tocar otros componentes; los planes 002–006 los adoptan.
- No cambiar `Skeleton.vue`: ya tiene su propio `prefers-reduced-motion`.
- Si el bloque actual no coincide con el extracto, PARAR e informar.

## Verification

- **Mechanical**: `npx vite build` en `frontend/` termina con `✓ built`.
- **Feel check**: DevTools > Rendering > Emulate `prefers-reduced-motion: reduce`:
  - El menú de usuario aparece con fundido, sin desplazarse.
  - Los botones con hover siguen cambiando de color, sin escalar con transición.
- **Done when**: los tres tokens existen en `:root` y el bloque reducido ya no contiene `transition-duration: 0.01ms`.
