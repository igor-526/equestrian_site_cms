import {
    priceCreateInDtoType,
    priceGroupsOutDtoType,
    priceListInDtoType,
    priceOutDtoType,
    priceUpdateInDtoType,
    priceVariantCreateInDtoType,
    priceVariantOutDtoType,
    priceVariantUpdateInDtoType
} from "@/types/api/prices";
import { AxiosResponse } from "axios";
import api from "./base";
import { ApiListPaginatedResponseType } from "@/types/api/api";

export const getPriceList = async (
    filters: priceListInDtoType
): Promise<ApiListPaginatedResponseType<priceOutDtoType>> => {
    const response: AxiosResponse<ApiListPaginatedResponseType<priceOutDtoType>> = await api.get<ApiListPaginatedResponseType<priceOutDtoType>>(
        "prices", { params: filters }
    );
    return response.data;
};

export const getPriceGroups = async (
): Promise<priceGroupsOutDtoType> => {
    const response: AxiosResponse<priceGroupsOutDtoType> = await api.get<priceGroupsOutDtoType>(
        "prices/groups"
    );
    return response.data;
};

export const createPrice = async (
    data: priceCreateInDtoType,
): Promise<priceOutDtoType> => {
    const response: AxiosResponse<priceOutDtoType> = await api.post<priceOutDtoType>(
        "prices",
        data,
    );
    return response.data;
};

export const updatePrice = async (
    priceId: string,
    data: priceUpdateInDtoType,
): Promise<priceOutDtoType> => {
    const response: AxiosResponse<priceOutDtoType> = await api.put<priceOutDtoType>(
        `prices/${priceId}`,
        data,
    );
    return response.data;
};

export const deletePrice = async (
    priceId: string,
): Promise<void> => {
    await api.delete<void>(`prices/${priceId}`);
};

export const createPriceVariant = async (
    priceId: string,
    data: priceVariantCreateInDtoType,
): Promise<priceVariantOutDtoType> => {
    const response: AxiosResponse<priceVariantOutDtoType> = await api.post<priceVariantOutDtoType>(
        `prices/${priceId}/variants`,
        data,
    );
    return response.data;
};

export const updatePriceVariant = async (
    priceId: string,
    variantId: string,
    data: priceVariantUpdateInDtoType,
): Promise<priceVariantOutDtoType> => {
    const response: AxiosResponse<priceVariantOutDtoType> = await api.put<priceVariantOutDtoType>(
        `prices/${priceId}/variants/${variantId}`,
        data,
    );
    return response.data;
};

export const deletePriceVariant = async (
    priceId: string,
    variantId: string,
): Promise<void> => {
    await api.delete<void>(`prices/${priceId}/variants/${variantId}`);
};