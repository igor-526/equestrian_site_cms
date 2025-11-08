import { priceListInDtoType, priceOutDtoType } from "@/types/api/prices";
import type { FiltersSetter } from "@/types/filters/filterBase";
import { ColumnType } from "antd/es/table";
import { TableDataItemType } from "../table";
import { pricePageMetadataType } from "./page";

export type priceTableDataItemType = priceOutDtoType & TableDataItemType

export type GetPriceTableColumnsType = (
    filters: priceListInDtoType,
    setFilters: FiltersSetter<priceListInDtoType>,
    pageMetadata: pricePageMetadataType,
) => ColumnType<priceTableDataItemType>[]