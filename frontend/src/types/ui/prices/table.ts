import { priceListInDtoType, priceOutDtoType } from "@/types/api/prices";
import { ColumnType } from "antd/es/table";
import { TableDataItemType } from "../table";
import { pricePageMetadataType } from "./page";

export type priceTableDataItemType = priceOutDtoType & TableDataItemType

export type GetPriceTableColumnsType = (
    filters: priceListInDtoType,
    setFilters: (filtersData: priceListInDtoType) => void,
    pageMetadata: pricePageMetadataType,
) => ColumnType<priceTableDataItemType>[]