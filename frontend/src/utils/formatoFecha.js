// Formato de fecha unico para toda la app. Usamos el idioma del documento
// (la interfaz esta en ingles) en vez de arrays de meses escritos a mano.

const formateador = new Intl.DateTimeFormat(document.documentElement.lang || 'en', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
});

export function formatearFechaCorta(valor) {
    if (!valor) {
        return '—';
    }

    var fecha = new Date(valor);
    if (isNaN(fecha.getTime())) {
        return '—';
    }

    return formateador.format(fecha);
}
