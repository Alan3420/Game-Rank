import api from "./api";

export async function login(email, passwd) {
    const response = await api.post("/user/login",{
        email:email,
        password:passwd
    });
    return response.data;
    
}

export async function register(name, last_name, email, passwd) {
    const response = await api.post("/user/register",{
        name: name,
        last_name: last_name,
        email:email,
        password:passwd
    });

    return response.data;
}