import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000', // your Django backend base URL
  withCredentials: true, // allows cookies / session headers
});

export default instance;