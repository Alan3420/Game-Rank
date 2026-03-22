import api from "./api";

export async function login(email, passwd) {
    const response = await api.post("/user/login",{
        email:email,
        password:passwd
    });
    return response.data;
    
}