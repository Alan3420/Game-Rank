export const STATUS_META = {
    pendiente: {
        label: 'Pending',
        icon: 'pi-clock',
        color: 'var(--status-pendiente)',
        colorBg: 'var(--status-pendiente-bg)',
        solidBg: 'var(--status-pendiente-solid-bg)',
        solidText: 'var(--status-pendiente-solid-text)',
        desc: 'Play later'
    },
    jugando: {
        label: 'Playing',
        icon: 'pi-play',
        color: 'var(--status-jugando)',
        colorBg: 'var(--status-jugando-bg)',
        solidBg: 'var(--status-jugando-solid-bg)',
        solidText: 'var(--status-jugando-solid-text)',
        desc: 'Currently playing'
    },
    pausado: {
        label: 'Paused',
        icon: 'pi-pause',
        color: 'var(--status-pausado)',
        colorBg: 'var(--status-pausado-bg)',
        solidBg: 'var(--status-pausado-solid-bg)',
        solidText: 'var(--status-pausado-solid-text)',
        desc: 'On hold for now'
    },
    completado: {
        label: 'Completed',
        icon: 'pi-check-circle',
        color: 'var(--status-completado)',
        colorBg: 'var(--status-completado-bg)',
        solidBg: 'var(--status-completado-solid-bg)',
        solidText: 'var(--status-completado-solid-text)',
        desc: 'Finished'
    }
};

export const STATUS_LIST = ['pendiente', 'jugando', 'pausado', 'completado'];
