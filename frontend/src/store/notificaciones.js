import { reactive } from 'vue';

const state = reactive({
    items: []
});

let nextId = 1;

const remove = (id) => {
    const index = state.items.findIndex(n => n.id === id);
    if (index !== -1) {
        state.items.splice(index, 1);
    }
};

const push = (type, message, options = {}) => {
    const id = nextId++;
    const duration = options.duration ?? 3500;

    state.items.push({
        id,
        type,
        message,
        title: options.title || (type === 'success' ? 'Listo' : 'Algo salió mal')
    });

    if (duration > 0) {
        setTimeout(() => remove(id), duration);
    }

    return id;
};

export const notificaciones = {
    state,
    success(message, options) {
        return push('success', message, options);
    },
    error(message, options) {
        return push('error', message, options);
    },
    remove
};
