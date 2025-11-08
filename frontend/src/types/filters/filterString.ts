import type {FiltersBaseType, FiltersSetter} from "./filterBase";
import type {ReactNode} from "react";

export type FilterStringPropsType<TFilters extends FiltersBaseType = FiltersBaseType> = {
    filters: TFilters
    setFilters: FiltersSetter<TFilters>,
    filterKey: keyof TFilters & string,
    placeHolder?: string,
}

export type GetFilterStringElementType = <TFilters extends FiltersBaseType = FiltersBaseType>(
    props: FilterStringPropsType<TFilters>
) => ReactNode