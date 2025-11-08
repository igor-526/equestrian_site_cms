import type {FiltersBaseType, FiltersSetter} from "./filterBase";
import type {ReactNode} from "react";

export type TablePaginationPropsType<TFilters extends FiltersBaseType = FiltersBaseType> = {
    setFilters: FiltersSetter<TFilters>,
    total: number
}

export type GetTablePaginationElementType = <TFilters extends FiltersBaseType = FiltersBaseType>(
    props: TablePaginationPropsType<TFilters>
) => ReactNode