import api from "./api";

// Manda credenciales al backend y devuelve los datos del usuario + token.
// Usamos el nombre "autenticarUsuario" para no chocar con el metodo
// "iniciarSesion" que vive dentro del store de autenticacion.
export async function autenticarUsuario(email, contrasena) {
    const respuesta = await api.post("/user/login", {
        email: email,
        password: contrasena
    });
    return respuesta.data;
}

// Crea una cuenta nueva con los datos del formulario de registro.
export async function registrarUsuario(nombre, apellido, nickname, email, contrasena) {
    const respuesta = await api.post("/user/register", {
        name: nombre,
        last_name: apellido,
        nickname: nickname,
        email: email,
        password: contrasena
    });
    return respuesta.data;
}

// Devuelve la lista de usuarios para el panel de admin.
export async function obtenerListaDeUsuarios() {
    const respuesta = await api.get("/settings/options");
    return respuesta.data;
}

// Cambia la contrasena del usuario actual. Manda la actual + la nueva,
// el backend valida que la actual sea correcta.
export async function cambiarContrasena(contrasenaActual, contrasenaNueva) {
    const respuesta = await api.put("/settings/change-password", {
        current_password: contrasenaActual,
        new_password: contrasenaNueva
    });
    return respuesta.data;
}

// Cambia el rol (user / admin) de un usuario concreto. Solo admin puede usarlo.
export async function cambiarRolDeUsuario(idUsuario, nuevoRol) {
    const respuesta = await api.put("/settings/change-role", {
        id_user: idUsuario,
        new_role: nuevoRol
    });
    return respuesta.data;
}

// Actualiza los datos editables de un usuario (nombre, nickname, etc.).
// "datos" es un objeto plano con los campos a modificar.
export async function actualizarUsuario(idUsuario, datos) {
    var cuerpo = { id_user: idUsuario };

    // Copiamos campo por campo en vez de hacer spread, para que se vea
    // claramente que el id va aparte y los demas campos se mandan tal cual.
    for (var clave in datos) {
        if (Object.prototype.hasOwnProperty.call(datos, clave)) {
            cuerpo[clave] = datos[clave];
        }
    }

    const respuesta = await api.put("/settings/options", cuerpo);
    return respuesta.data;
}

// Borra la cuenta de un usuario por id. Lo usa el admin.
export async function eliminarUsuario(idUsuario) {
    const respuesta = await api.delete("/settings/options", {
        data: { id_user: idUsuario }
    });
    return respuesta.data;
}

// El usuario actual pide borrar su propia cuenta.
export async function eliminarMiCuenta() {
    const respuesta = await api.delete("/settings/account");
    return respuesta.data;
}

// Devuelve los datos del usuario actual usando el token guardado.
// Se llama al iniciar la app para restaurar la sesion.
export async function obtenerMiUsuario() {
    const respuesta = await api.get("/user/me");
    return respuesta.data;
}

// Devuelve las estadisticas del usuario (juegos calificados, favoritos, etc.)
// para mostrarlas en el perfil.
export async function obtenerEstadisticasUsuario() {
    const respuesta = await api.get("/settings/stats");
    return respuesta.data;
}
