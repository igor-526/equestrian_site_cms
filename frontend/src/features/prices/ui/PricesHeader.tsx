import { PriceGroupListQueryParams } from "@/types/api/priceGroups";
import { PriceListQueryParams } from "@/types/api/prices";
import { FiltersBaseType, FiltersSetter } from "@/types/filters/filterBase";
import { TablePaginator } from "@/ui";
import { FilterOutlined, PlusOutlined } from "@ant-design/icons";
import { Button } from "antd";
import React from "react";
import { PricesTabs } from "./PricesTabs";

export type PricesHeaderProps = {
    activeTab: string;
    setActiveTab: (tab: string) => void;
    onCreatePriceGroup: () => void;
    onCreatePrice: () => void;
    resetPriceGroupsFilters: () => void;
    resetPricesFilters: () => void;
    priceGroupsTotal: number;
    priceGroupsFilters: PriceGroupListQueryParams;
    setPriceGroupsFilters: (filters: PriceGroupListQueryParams) => void;
    priceTotal: number;
    priceFilters: PriceListQueryParams;
    setPriceFilters: (filters: PriceListQueryParams) => void;

};

export const PricesHeader: React.FC<PricesHeaderProps> = ({
    activeTab,
    setActiveTab,
    onCreatePriceGroup,
    onCreatePrice,
    resetPriceGroupsFilters,
    resetPricesFilters,
    priceGroupsTotal,
    priceGroupsFilters,
    setPriceGroupsFilters,
    priceTotal,
    priceFilters,
    setPriceFilters,
}) => {
    const handleCreateButtonClick = () => {
        if (activeTab === 'groups') {
            onCreatePriceGroup();
        } else {
            onCreatePrice();
        }
    }

    const handleResetFilters = () => {
        if (activeTab === 'groups') {
            resetPriceGroupsFilters();
        } else {
            resetPricesFilters();
        }
    }

    const currentFilters = activeTab === 'groups' ? priceGroupsFilters : priceFilters;
    const setCurrentFilters = activeTab === 'groups' ? setPriceGroupsFilters : setPriceFilters;
    const currentTotal = activeTab === 'groups' ? priceGroupsTotal : priceTotal;

    return (
        <>
            <PricesTabs activeTab={activeTab} setActiveTab={setActiveTab} />
            <div className="flex items-center gap-2">
                <TablePaginator
                    filters={currentFilters as FiltersBaseType}
                    setFilters={setCurrentFilters as FiltersSetter<FiltersBaseType>}
                    total={currentTotal}
                />
                <Button color="danger" variant="outlined" onClick={handleResetFilters}>
                    <FilterOutlined /> Сбросить
                </Button>
                <Button color="primary" variant="outlined" onClick={handleCreateButtonClick}>
                    <PlusOutlined />Добавить
                </Button>
            </div>
        </>
    );
};



