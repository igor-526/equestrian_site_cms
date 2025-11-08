import {Pagination} from "antd";
import type {TablePaginationPropsType} from "@/types/filters/pagination";
import type {FiltersBaseType} from "@/types/filters/filterBase";


const TablePagination = <TFilters extends FiltersBaseType = FiltersBaseType>({
    setFilters,
    total
}: TablePaginationPropsType<TFilters>): JSX.Element => {
    return (
        <Pagination
            defaultCurrent={1}
            total={total}
            hideOnSinglePage={true}
            onChange = {(current, size) => {
                setFilters((prevState) => ({
                    ...prevState,
                    limit: size,
                    offset: (current - 1) * size
                }))
            }}
        />
    )
}

export default TablePagination