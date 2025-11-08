export type BooleanFilterType = 'true' | 'false' | null | undefined;

export type ApiListPaginatedResponseType<T> = {
    total: number,
    items: T[]
}