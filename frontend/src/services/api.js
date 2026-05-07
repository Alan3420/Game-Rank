import axios from 'axios';

const api = axios.create({
    // Para pruebas en mobil 192.168.1.XXX, pruebas generales localhost, para identificar la ip local CMD ipconfig
    baseURL: 'http://localhost:5000'
});

api.interceptors.request.use(config => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

export default api;