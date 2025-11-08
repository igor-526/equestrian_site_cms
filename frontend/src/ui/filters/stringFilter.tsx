import {Button, Input, Space} from "antd";
import ClearIcon from '@mui/icons-material/Clear';
import type {FilterStringPropsType} from "@/types/filters/filterString";
import type {FiltersBaseType} from "@/types/filters/filterBase";

const StringFilter = <TFilters extends FiltersBaseType = FiltersBaseType>({
    filters,
    setFilters,
    filterKey,
    placeHolder="Поиск"
}: FilterStringPropsType<TFilters>) => {
    return (
        <>
            <Input
                placeholder={placeHolder}
                value={filters[filterKey] as string | undefined}
                onChange={(e) => setFilters((prevState) => ({
                    ...prevState,
                    [filterKey]: e.target.value.trim() ? e.target.value.trim() : null
                }))}
                style={{ marginBottom: 8, display: 'block' }}
            />
            <Space>
                <Button
                    size="small"
                    color="danger"
                    variant="outlined"
                    onClick={() => {
                        setFilters((prevState) => ({
                            ...prevState,
                            [filterKey]: null
                        }))
                    }}
                >
                    <ClearIcon /> Очистить
                </Button>
            </Space>
        </>
    )
}

export default StringFilter