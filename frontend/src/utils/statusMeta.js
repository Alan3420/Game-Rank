// Catalogo de los estados que un usuario puede asignar a un juego de su
// coleccion. Las claves estan en espanol porque asi se guardan en el backend,
// pero los labels viajan en ingles porque toda la UI esta en ingles.
//
// Cada entrada incluye el label, el icono de PrimeIcons y los colores que usa
// el componente GameStatusDropdown para pintar el badge correspondiente.

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

// Lista ordenada de las claves para iterarlas en el mismo orden en toda la app.
// Se usa para pintar la lista de opciones en el dropdown de estado.
export const STATUS_LIST = ['pendiente', 'jugando', 'pausado', 'completado'];
