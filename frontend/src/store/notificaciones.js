import { reactive } from 'vue';

// Estado reactivo que comparte la lista de notificaciones activas con
// el componente NotificationToast. Vue se encarga de re-renderizar cuando
// se modifica la lista "items".
const estado = reactive({
    items: []
});

// Contador simple para asignar un id unico a cada notificacion.
// No usamos UUID porque la app solo necesita distinguirlas dentro de la sesion.
var siguienteId = 1;


// Quita una notificacion concreta del listado activo.
// Se llama tanto desde el temporizador interno como desde el boton de cerrar.
function eliminarNotificacion(id) {
    var indice = -1;

    for (var i = 0; i < estado.items.length; i++) {
        if (estado.items[i].id === id) {
            indice = i;
            break;
        }
    }

    if (indice !== -1) {
        estado.items.splice(indice, 1);
    }
}


// Devuelve el icono de PrimeIcons que corresponde a cada tipo de notificacion.
function iconoPorTipo(tipo) {
    if (tipo === 'success') {
        return 'pi-check-circle';
    } else if (tipo === 'error') {
        return 'pi-times-circle';
    } else if (tipo === 'warning') {
        return 'pi-exclamation-triangle';
    } else {
        return 'pi-info-circle';
    }
}


// Titulo por defecto que se muestra cuando no se pasa uno propio.
function tituloPorDefecto(tipo) {
    if (tipo === 'success') {
        return 'Done';
    } else if (tipo === 'error') {
        return 'Something went wrong';
    } else if (tipo === 'warning') {
        return 'Warning';
    } else {
        return 'Info';
    }
}


// Agrega una notificacion nueva al estado y programa su auto-cierre.
// tipo: "success", "error", "warning" o "info".
// mensaje: texto que se muestra en el cuerpo.
// opciones: objeto opcional con duracion y titulo personalizados.
function agregarNotificacion(tipo, mensaje, opciones) {
    if (!opciones) {
        opciones = {};
    }

    var duracion = 3500;
    if (opciones.duration !== undefined && opciones.duration !== null) {
        duracion = opciones.duration;
    }

    var titulo = "";
    if (opciones.title) {
        titulo = opciones.title;
    } else {
        titulo = tituloPorDefecto(tipo);
    }

    var id = siguienteId;
    siguienteId = siguienteId + 1;

    estado.items.push({
        id: id,
        type: tipo,
        message: mensaje,
        title: titulo,
        icon: iconoPorTipo(tipo)
    });

    // Cuando duracion es 0 o negativa el aviso queda fijo hasta que el
    // usuario lo cierre manualmente.
    if (duracion > 0) {
        setTimeout(function () {
            eliminarNotificacion(id);
        }, duracion);
    }

    return id;
}


// Objeto que se importa desde los componentes. Expone success(), error(),
// warning(), info(), remove() y el estado reactivo "state".
export const notificaciones = {
    state: estado,
    success: function (mensaje, opciones) {
        return agregarNotificacion('success', mensaje, opciones);
    },
    error: function (mensaje, opciones) {
        return agregarNotificacion('error', mensaje, opciones);
    },
    warning: function (mensaje, opciones) {
        return agregarNotificacion('warning', mensaje, opciones);
    },
    info: function (mensaje, opciones) {
        return agregarNotificacion('info', mensaje, opciones);
    },
    remove: eliminarNotificacion
};
