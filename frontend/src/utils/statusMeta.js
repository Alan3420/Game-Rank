// Las claves estan en espanol porque asi se guardan en BD, pero los label
// van en ingles porque toda la UI esta en ingles
export const STATUS_META = {
    pendiente: {
        label: 'Pending',
        icon: 'pi-clock',
        desc: 'Play later'
    },
    jugando: {
        label: 'Playing',
        icon: 'pi-play',
        desc: 'Currently playing'
    },
    pausado: {
        label: 'Paused',
        icon: 'pi-pause',
        desc: 'On hold for now'
    },
    completado: {
        label: 'Completed',
        icon: 'pi-check-circle',
        desc: 'Finished'
    }
};

export const STATUS_LIST = ['pendiente', 'jugando', 'pausado', 'completado'];
