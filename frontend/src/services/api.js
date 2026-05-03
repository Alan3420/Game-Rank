import axios from 'axios';

const api = axios.create({
    // Para pruebas en mobil 192.168.1.XXX, pruebas generales localhost, para identificar la ip local CMD ipconfig
    baseURL: 'http://localhost:5000'
});

export default api;