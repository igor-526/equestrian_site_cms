import { Select } from "antd";
import type {FilterListPropsType} from "@/types/filters/filterList";
import type {FiltersBaseType} from "@/types/filters/filterBase";

const ListFilter = <TFilters extends FiltersBaseType = FiltersBaseType>({
    filters,
    setFilters,
    filterKey,
    filterData,
    placeHolder="Выберите"
}: FilterListPropsType<TFilters>): JSX.Element => {
    return (
        <Select
            mode="multiple"
            allowClear
            style={{ marginBottom: 8, display: 'block' }}
            placeholder={placeHolder}
            value={filters[filterKey]}
            onChange={(e) => {
                setFilters((prevState) => ({
                    ...prevState,
                    [filterKey]: e
                }))}}
            options={filterData}
        />
    )
}

export default ListFilter