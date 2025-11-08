export type priceFormattersType = "equal" | "gt" | "lt" | "discuss";

export type priceAvailableSortType = "name" | "description" | "group" | "price" | "-name" | "-description" | "-group" | "-price";

export type priceListInDtoType = {
    limit?: number,
    offset?: number,
    name?: string | null,
    description?: string | null,
    group?: string[] | null,
    price_gt?: number | null,
    price_lt?: number | null,
    sort?: priceAvailableSortType[] | null,
}

export type priceCreateInDtoType = {
    name: string,
    description?: string | null,
    group?: string | null,
    price: number,
    price_formatter: priceFormattersType,
}

export type priceUpdateInDtoType = Partial<priceCreateInDtoType>

export type priceVariantCreateInDtoType = {
    name: string,
    description?: string | null,
    price: number,
    price_formatter: priceFormattersType,
}

export type priceVariantUpdateInDtoType = Partial<priceVariantCreateInDtoType>

export type priceVariantsOutDtoType = {
    id: string,
    name: string,
    description: string | null,
    price: number,
    price_formatter: priceFormattersType,
}

export type priceVariantOutDtoType = priceVariantsOutDtoType

export type priceOutDtoType = {
    id: string,
    name: string,
    description: string | null,
    group: string | null,
    price: number,
    price_formatter: priceFormattersType,
    variants: priceVariantsOutDtoType[],
}

export type priceGroupsOutDtoType = string[]
