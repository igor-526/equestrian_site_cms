import { priceVariantsOutDtoType } from "@/types/api/prices";
import type { ReactNode } from "react";
import { TableDataItemType } from "../table";

export type priceVariantTableDataItemType = priceVariantsOutDtoType & TableDataItemType

export type PriceVariantsTableProps = {
    priceVariants?: priceVariantsOutDtoType[],
    onVariantClick?: (variant: priceVariantsOutDtoType) => void,
}

export type GetPriceVariantsTableElement = (props: PriceVariantsTableProps) => ReactNode