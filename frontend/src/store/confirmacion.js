import { reactive } from 'vue';

// Dialogo de confirmacion global. Sustituye al confirm() nativo para que
// las acciones destructivas pidan confirmacion con el estilo de la app.
// Uso: if (await confirmacion.pedir({ title, message, confirmLabel })) { ... }

const estado = reactive({
    open: false,
    title: '',
    message: '',
    confirmLabel: 'Confirm',
    danger: true
});

var resolverPendiente = null;


function pedir(opciones) {
    // Si habia un dialogo abierto lo damos por cancelado
    if (resolverPendiente) {
        resolverPendiente(false);
    }

    estado.title = opciones.title || 'Are you sure?';
    estado.message = opciones.message || '';
    estado.confirmLabel = opciones.confirmLabel || 'Confirm';
    estado.danger = opciones.danger !== false;
    estado.open = true;

    return new Promise(function (resolve) {
        resolverPendiente = resolve;
    });
}


function responder(valor) {
    estado.open = false;

    if (resolverPendiente) {
        resolverPendiente(valor);
        resolverPendiente = null;
    }
}


export const confirmacion = {
    state: estado,
    pedir: pedir,
    responder: responder
};
