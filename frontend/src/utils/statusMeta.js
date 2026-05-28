// Las claves estan en espanol porque asi se guardan en BD, pero los label
// van en ingles porque toda la UI esta en ingles
export const STATUS_META = {
    pendiente: {
        label: 'Pending',
        icon: 'pi-clock',
        color: 'var(--color-primary)',
        colorBg: 'var(--color-primary-light)',
        solidBg: 'var(--color-primary-light)',
        solidText: 'var(--color-primary)',
        desc: 'Play later'
    },
    jugando: {
        label: 'Playing',
        icon: 'pi-play',
        color: 'var(--color-primary)',
        colorBg: 'var(--color-primary-light)',
        solidBg: 'var(--color-primary-light)',
        solidText: 'var(--color-primary)',
        desc: 'Currently playing'
    },
    pausado: {
        label: 'Paused',
        icon: 'pi-pause',
        color: 'var(--color-primary)',
        colorBg: 'var(--color-primary-light)',
        solidBg: 'var(--color-primary-light)',
        solidText: 'var(--color-primary)',
        desc: 'On hold for now'
    },
    completado: {
        label: 'Completed',
        icon: 'pi-check-circle',
        color: 'var(--color-primary)',
        colorBg: 'var(--color-primary-light)',
        solidBg: 'var(--color-primary-light)',
        solidText: 'var(--color-primary)',
        desc: 'Finished'
    }
};

export const STATUS_LIST = ['pendiente', 'jugando', 'pausado', 'completado'];
