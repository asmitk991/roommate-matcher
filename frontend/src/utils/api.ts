import axios from 'axios';

const instance = axios.create({
  baseURL: 'https://roommate-matcher-1.onrender.com', // your Django backend base URL
  withCredentials: true, // allows cookies / session headers
});

export default instance;