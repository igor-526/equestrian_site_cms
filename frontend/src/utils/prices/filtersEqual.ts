import { priceListInDtoType } from "@/types/api/prices";

const normalizeArray = <T,>(value?: T[] | null): T[] => value ?? ([] as T[]);

const areArraysEqual = <T,>(first: T[], second: T[]) =>
    first.length === second.length && first.every((item, index) => item === second[index]);

export const isPriceFiltersEqualToInitial = (initial: priceListInDtoType, current: priceListInDtoType): boolean => (
    current.limit === initial.limit &&
    current.offset === initial.offset &&
    (current.name ?? null) === (initial.name ?? null) &&
    (current.description ?? null) === (initial.description ?? null) &&
    areArraysEqual(
        normalizeArray(current.group),
        normalizeArray(initial.group)
    ) &&
    (current.price_gt ?? null) === (initial.price_gt ?? null) &&
    (current.price_lt ?? null) === (initial.price_lt ?? null) &&
    areArraysEqual(
        normalizeArray(current.sort),
        normalizeArray(initial.sort)
    )
);