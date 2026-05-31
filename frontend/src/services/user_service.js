import api from "./api";

export async function autenticarUsuario(email, contrasena) {
    const respuesta = await api.post("/user/login", {
        email: email,
        password: contrasena
    });
    return respuesta.data;
}

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

export async function obtenerListaDeUsuarios() {
    const respuesta = await api.get("/settings/options");
    return respuesta.data;
}

export async function cambiarContrasena(contrasenaActual, contrasenaNueva) {
    const respuesta = await api.put("/settings/change-password", {
        current_password: contrasenaActual,
        new_password: contrasenaNueva
    });
    return respuesta.data;
}

export async function cambiarRolDeUsuario(idUsuario, nuevoRol) {
    const respuesta = await api.put("/settings/change-role", {
        id_user: idUsuario,
        new_role: nuevoRol
    });
    return respuesta.data;
}

export async function actualizarUsuario(idUsuario, datos) {
    var cuerpo = { id_user: idUsuario };

    for (var clave in datos) {
        cuerpo[clave] = datos[clave];
    }

    const respuesta = await api.put("/settings/options", cuerpo);
    return respuesta.data;
}

export async function eliminarUsuario(idUsuario) {
    const respuesta = await api.delete("/settings/options", {
        data: { id_user: idUsuario }
    });
    return respuesta.data;
}

export async function eliminarMiCuenta() {
    const respuesta = await api.delete("/settings/account");
    return respuesta.data;
}

export async function obtenerMiUsuario() {
    const respuesta = await api.get("/user/me");
    return respuesta.data;
}

export async function obtenerEstadisticasUsuario() {
    const respuesta = await api.get("/settings/stats");
    return respuesta.data;
}
