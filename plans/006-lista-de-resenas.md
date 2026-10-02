# 006 — Transición al publicar y borrar reseñas

- **Status**: DONE
- **Commit**: 0229bee
- **Severity**: LOW
- **Category**: Missed opportunities
- **Estimated scope**: 2 archivos, ~25 líneas
- **Depends on**: 001 (token `--ease-out`)

## Problem

Al publicar o borrar una reseña, el elemento aparece o desaparece de golpe y el resto de la lista salta:

```html
<!-- frontend/src/components/GameDetail/GameDetail.vue:290 — current -->
<div v-else class="comments-list">
    <div v-for="comment in comments" :key="comment.id_comment" class="comment-item">
        ...
    </div>
</div>
```

```css
/* frontend/src/components/GameDetail/styles_GameDetail.css:914 — current */
.comments-list {
    display: flex;
    flex-direction: column;
}
```

Frecuencia: poco frecuente (pocas reseñas por usuario y juego).

## Target

```html
<TransitionGroup v-else tag="div" name="comment" class="comments-list">
    <div v-for="comment in comments" :key="comment.id_comment" class="comment-item">
        ...
    </div>
</TransitionGroup>
```

```css
.comments-list {
    display: flex;
    flex-direction: column;
    position: relative;
}
.comment-enter-active {
    transition: opacity 200ms var(--ease-out), transform 200ms var(--ease-out);
}
.comment-leave-active {
    transition: opacity 150ms var(--ease-out);
    position: absolute;
    left: 0;
    right: 0;
}
.comment-enter-from {
    opacity: 0;
    transform: translateY(-8px);
}
.comment-leave-to {
    opacity: 0;
}
.comment-move {
    transition: transform 200ms var(--ease-out);
}
```

`TransitionGroup` no anima el primer render, así que abrir un juego no dispara nada; sí anima "Load more" (los nuevos elementos entran con fundido), lo cual es aceptable.

## Nota de ejecución

`.comment-item` declara su propio `transition: background 0.15s ease` más abajo en `styles_GameDetail.css` con la misma especificidad, lo que anularía `.comment-enter-active`. Por eso las reglas se escribieron con prefijo `.comments-list > .comment-*` (mayor especificidad).

## Steps

1. `GameDetail.vue:290`: cambiar `<div v-else class="comments-list">` por `<TransitionGroup v-else tag="div" name="comment" class="comments-list">` y su `</div>` de cierre (el que cierra `.comments-list`, justo antes de `<!-- CARGAR MÁS -->`) por `</TransitionGroup>`.
2. `styles_GameDetail.css`: añadir `position: relative;` a `.comments-list` y las reglas `.comment-*` del Target después.

## Boundaries

- No tocar el contenido de `.comment-item` ni la lógica de publicar/borrar.

## Verification

- **Mechanical**: `npx vite build` termina con `✓ built`.
- **Feel check**:
  - Publicar una reseña: entra con fundido y desliza 8px; el resto se recoloca suave.
  - Borrar la reseña (confirmando): se desvanece y la lista se cierra sin salto.
  - Movimiento reducido: solo fundidos.
- **Done when**: la lista usa `<TransitionGroup name="comment">`.
