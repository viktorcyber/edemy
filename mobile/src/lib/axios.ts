import axios from "axios";
import type { AxiosInstance, AxiosResponse } from "axios";

const instance: AxiosInstance = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_URL,
  timeout: 5000,
  headers: { 
    Accept: 'application/json',
    "Content-Type": "application/json" 
  },
});

instance.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => Promise.reject(error)
);

export default instance;