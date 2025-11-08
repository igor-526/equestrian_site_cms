import axios, {
    type AxiosInstance,
    type AxiosRequestConfig,
    type AxiosResponse,
    type InternalAxiosRequestConfig
} from 'axios';
import type { AuthResponsePayload } from '@/types/api/auth';

interface CustomAxiosRequestConfig<D = unknown> extends AxiosRequestConfig<D> {
    _retry?: boolean;
    _skipAuthRefresh?: boolean;
}

interface CustomInternalAxiosRequestConfig<D = unknown> extends InternalAxiosRequestConfig<D> {
    _retry?: boolean;
    _skipAuthRefresh?: boolean;
}

interface CustomAxiosInstance extends AxiosInstance {
    post<T = unknown, R = AxiosResponse<T>, D = unknown>(
        url: string,
        data?: D,
        config?: CustomAxiosRequestConfig<D>
    ): Promise<R>;
}

const backendUrl: string =
    process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8001/api";

const api: CustomAxiosInstance = axios.create({
    baseURL: backendUrl,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true
}) as CustomAxiosInstance;

api.interceptors.request.use(
    (config: CustomInternalAxiosRequestConfig) => {
        config.withCredentials = true;
        return config;
    },
    (error) => Promise.reject(error)
);

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config as CustomInternalAxiosRequestConfig | undefined;

        const redirectToLogin = () => {
            if (typeof window !== "undefined" && window.location.pathname !== "/login") {
                window.location.href = "/login";
            }
        };

        if (error.response?.status === 401 && originalRequest) {
            if (originalRequest._skipAuthRefresh) {
                redirectToLogin();
                return Promise.reject(error);
            }

            const requestUrl = originalRequest.url ?? "";
            const isAuthEndpoint =
                requestUrl.includes("auth/login") || requestUrl.includes("auth/refresh");

            if (!originalRequest._retry && !isAuthEndpoint) {
                originalRequest._retry = true;

                try {
                    const refreshResponse = await api.post<AuthResponsePayload>(
                        "/auth/refresh",
                        undefined,
                        {_skipAuthRefresh: true} as CustomAxiosRequestConfig
                    );

                    if (refreshResponse.data?.status === "ok") {
                        return api.request(originalRequest);
                    }

                    redirectToLogin();
                    return Promise.reject(error);
                } catch (refreshError) {
                    if (axios.isAxiosError(refreshError) && refreshError.response?.status === 401) {
                        redirectToLogin();
                    }

                    return Promise.reject(refreshError);
                }
            }

            redirectToLogin();
        }
        return Promise.reject(error);
    }
);

export default api;