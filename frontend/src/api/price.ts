import { ApiListPaginatedResponseType, ApiResult } from "@/types/api/api";
import apiFetch, { addQueryParamsToUrl } from "./client";
import { UUID } from "crypto";
import { PriceCreateInDto, PriceListQueryParams, PriceOutDto, PriceUpdateInDto } from "@/types/api/prices";

export const priceList = (
    params: PriceListQueryParams = {},
    options?: RequestInit,
): Promise<ApiResult<ApiListPaginatedResponseType<PriceOutDto>>> => {
    const paramtrizedUrl = addQueryParamsToUrl("/prices", params);
    return apiFetch<ApiListPaginatedResponseType<PriceOutDto>>(paramtrizedUrl, options);
};

export const priceDetail = (
    priceId: UUID,
    params?: { tables?: boolean; page_data?: boolean },
): Promise<ApiResult<PriceOutDto>> => {
    const paramtrizedUrl = addQueryParamsToUrl(`/prices/${priceId}`, params || {});
    return apiFetch<PriceOutDto>(paramtrizedUrl, {
        method: "GET",
    });
};

export const priceCreate = (
    payload: PriceCreateInDto,
): Promise<ApiResult<PriceOutDto>> => {
    return apiFetch<PriceOutDto>("/prices", {
        method: "POST",
        body: JSON.stringify(payload),
    });
};

export const priceUpdate = (
    priceId: UUID,
    payload: PriceUpdateInDto,
): Promise<ApiResult<PriceOutDto>> => {
    return apiFetch<PriceOutDto>(`/prices/${priceId}`, {
        method: "PATCH",
        body: JSON.stringify(payload),
    });
};

export const priceDelete = (
    priceId: UUID,
): Promise<ApiResult<null>> => {
    return apiFetch<null>(`/prices/${priceId}`, {
        method: "DELETE",
    });
};