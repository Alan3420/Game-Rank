// Las claves estan en espanol porque asi se guardan en BD, pero los label
// van en ingles porque toda la UI esta en ingles. El icono de cada estado
// lo dibuja components/CardWorld/StatusIcon.vue
export const STATUS_META = {
    pendiente: {
        label: 'Pending',
        desc: 'Play later'
    },
    jugando: {
        label: 'Playing',
        desc: 'Currently playing'
    },
    pausado: {
        label: 'Paused',
        desc: 'On hold for now'
    },
    completado: {
        label: 'Completed',
        desc: 'Finished'
    }
};

export const STATUS_LIST = ['pendiente', 'jugando', 'pausado', 'completado'];
