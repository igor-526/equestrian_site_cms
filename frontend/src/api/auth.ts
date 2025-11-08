import axios from "axios";
import api from "@/api/base";
import {loginCredentialsType} from "@/types/api/login";
import { AuthResponsePayload, AuthStatus } from "@/types/api/auth";

const authApiLogin = async (
    credentials: loginCredentialsType
): Promise<AuthStatus> => {
    try {
        const response = await api.post<AuthResponsePayload>(
            "/auth/login",
            {
                username: credentials.username,
                password: credentials.password
            }
        );
        const status = response.data?.status;

        if (status === "ok" || status === "denied") {
            return status;
        }

        return "error";
    } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 401) {
            return "denied";
        }

        return "error";
    }
};

export default authApiLogin;