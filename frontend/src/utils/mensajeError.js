// El backend responde en espanol y la interfaz va en ingles: nunca se
// enseña su texto tal cual. Se traducen los casos conocidos y, si no
// encaja ninguno, se usa el mensaje en ingles que pasa cada pantalla.
export function mensajeDeError(error, porDefecto) {
    var texto = '';
    if (error && error.response && error.response.data && error.response.data.message) {
        texto = String(error.response.data.message).toLowerCase();
    }

    if (texto.indexOf('incorrectos') !== -1) {
        return 'Incorrect email or password.';
    }
    if (texto.indexOf('contraseña actual es incorrecta') !== -1) {
        return 'Your current password is incorrect.';
    }
    if (texto.indexOf('nickname') !== -1 && texto.indexOf('en uso') !== -1) {
        return 'That nickname is already taken.';
    }
    if ((texto.indexOf('email') !== -1 || texto.indexOf('correo') !== -1) &&
        (texto.indexOf('en uso') !== -1 || texto.indexOf('registrado') !== -1)) {
        return 'That email is already registered.';
    }
    if (texto.indexOf('255') !== -1) {
        return 'Reviews can be at most 255 characters.';
    }
    if (texto.indexOf('demasiadas peticiones') !== -1) {
        return 'Too many requests. Wait a moment and try again.';
    }
    if (texto.indexOf('permisos') !== -1) {
        return "You don't have permission to do that.";
    }
    return porDefecto;
}
