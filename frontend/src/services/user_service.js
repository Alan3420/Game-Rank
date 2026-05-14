import api from "./api";

export async function login(email, passwd) {
    const response = await api.post("/user/login", {
        email: email,
        password: passwd
    });
    return response.data;

}

export async function register(name, last_name, email, passwd) {
    const response = await api.post("/user/register", {
        name: name,
        last_name: last_name,
        email: email,
        password: passwd
    });

    return response.data;
}

export async function getListUsers() {
    const response = await api.get("/settings/options");
    return response.data;
}

export async function changePassword(contraseña_actual, contraseña_nueva) {
    const response = await api.put("/settings/change-password", {
        current_password: contraseña_actual,
        new_password: contraseña_nueva
    });
    return response.data;
}

export async function changeUserRole(id_user, new_role) {
    const response = await api.put("/settings/change-role", {
        id_user: id_user,
        new_role: new_role
    });
    return response.data;
}

export async function updateUser(id_user, datos) {
    const response = await api.put("/settings/options", {
        id_user: id_user,
        ...datos
    });
    return response.data;
}

export async function deleteUser(id_user) {
    const response = await api.delete("/settings/options", {
        data: { id_user: id_user }
    });
    return response.data;
}

export async function deleteOwnAccount() {
    const response = await api.delete("/settings/account");
    return response.data;
}

export async function getMe() {
    const response = await api.get("/user/me");
    return response.data;
}