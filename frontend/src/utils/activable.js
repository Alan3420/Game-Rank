// Directiva v-activable: hace accesible por teclado un elemento que no es
// <a> ni <button> pero tiene @click (cards que contienen botones dentro y
// por eso no pueden ser enlaces). Le da foco, un rol y dispara el click
// con Enter (y con Espacio si el rol es "button").
//
// Uso: <div v-activable @click="..."> o <div v-activable="'button'" @click="...">

export const activable = {
    mounted(el, binding) {
        var rol = binding.value || 'link';

        el.setAttribute('role', rol);
        if (!el.hasAttribute('tabindex')) {
            el.setAttribute('tabindex', '0');
        }

        el._manejarTecla = function (evento) {
            // Ignoramos teclas que vienen de botones internos de la card
            if (evento.target !== el) {
                return;
            }
            if (evento.key === 'Enter' || (rol === 'button' && evento.key === ' ')) {
                evento.preventDefault();
                el.click();
            }
        };

        el.addEventListener('keydown', el._manejarTecla);
    },

    unmounted(el) {
        el.removeEventListener('keydown', el._manejarTecla);
    }
};
