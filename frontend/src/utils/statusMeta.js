export const STATUS_META = {
    pendiente: {
        label: 'Pendiente',
        icon: 'pi-clock',
        color: 'var(--status-pendiente)',
        colorBg: 'var(--status-pendiente-bg)',
        solidBg: 'var(--status-pendiente-solid-bg)',
        solidText: 'var(--status-pendiente-solid-text)',
        desc: 'Por jugar más adelante'
    },
    jugando: {
        label: 'Jugando',
        icon: 'pi-play',
        color: 'var(--status-jugando)',
        colorBg: 'var(--status-jugando-bg)',
        solidBg: 'var(--status-jugando-solid-bg)',
        solidText: 'var(--status-jugando-solid-text)',
        desc: 'Lo estoy jugando ahora'
    },
    pausado: {
        label: 'Pausado',
        icon: 'pi-pause',
        color: 'var(--status-pausado)',
        colorBg: 'var(--status-pausado-bg)',
        solidBg: 'var(--status-pausado-solid-bg)',
        solidText: 'var(--status-pausado-solid-text)',
        desc: 'En pausa por ahora'
    },
    completado: {
        label: 'Completado',
        icon: 'pi-check-circle',
        color: 'var(--status-completado)',
        colorBg: 'var(--status-completado-bg)',
        solidBg: 'var(--status-completado-solid-bg)',
        solidText: 'var(--status-completado-solid-text)',
        desc: 'Terminado'
    }
};

export const STATUS_LIST = ['pendiente', 'jugando', 'pausado', 'completado'];
