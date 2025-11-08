import type { ColumnsType, TableProps } from "antd/es/table";
import type { ReactNode } from "react";

export type TableDataItemType = {
    key: string;
    [field: string]: unknown;
};

export interface TableWithFiltersProps<RecordType extends TableDataItemType = TableDataItemType> {
    tableColumns?: ColumnsType<RecordType>;
    tableData?: RecordType[];
    tableLoading?: boolean;
    filtersElements?: ReactNode;
    onRowListener?: TableProps<RecordType>["onRow"];
    expandable?: TableProps<RecordType>["expandable"];
}