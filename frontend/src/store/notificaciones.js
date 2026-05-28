import { reactive } from 'vue';

const estado = reactive({
    items: []
});

var siguienteId = 1;


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

    // Si la duracion es 0 o menos dejamos el aviso fijo hasta que el
    // usuario lo cierre con la X
    if (duracion > 0) {
        setTimeout(function () {
            eliminarNotificacion(id);
        }, duracion);
    }

    return id;
}


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
