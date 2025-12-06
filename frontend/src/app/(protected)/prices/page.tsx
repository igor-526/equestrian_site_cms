"use client";

import React, { useEffect, useState } from "react";
import { PricesHeader } from "@/features/prices/ui/PricesHeader";
import { usePrices } from "@/features/prices/hooks/usePrices";
import { PricesGroupsTable } from "@/features/prices/ui/PriceGroup/PricesGroupsTable";
import { PriceGroupModal } from "@/features/prices/ui/PriceGroup/PriceGroupModal";
import { PriceGroupCreateInDto, PriceGroupOutDto, PriceGroupUpdateInDto } from "@/types/api/priceGroups";
import { PriceCreateInDto, PriceOutDto, PriceUpdateInDto } from "@/types/api/prices";
import { UUID } from "crypto";
import { PricesTable } from "@/features/prices/ui/Price/PricesTable";
import { PriceModal } from "@/features/prices/ui/Price/PriceModal";
import { PriceTableModal } from "@/features/prices/ui/Price/PriceTableModal";
import { TableType } from "@/types/api/table";
import { PricesDeveloperDocumentationView } from "@/features/prices/ui/PricesDeveloperDocumentationView";
import { PricesUserDocumentationView } from "@/features/prices/ui/PricesUserDocumentationView";
import { PricesTabsEnum } from "@/features/prices/ui/PricesTabs";
import { usePricePageActionScopes } from "@/features/prices/hooks/usePriceScopes";


export default function PricesPage() {
    const [activeTab, setActiveTab] = useState<PricesTabsEnum>(PricesTabsEnum.PRICES);
    const [priceGroupModalOpen, setPriceGroupModalOpen] = useState<boolean>(false);
    const [selectedPriceGroup, setSelectedPriceGroup] = useState<PriceGroupOutDto | null>(null);
    const [priceModalOpen, setPriceModalOpen] = useState<boolean>(false);
    const [selectedPrice, setSelectedPrice] = useState<PriceOutDto | null>(null);
    const [priceTableModalOpen, setPriceTableModalOpen] = useState<boolean>(false);
    const [pricePhotosModalOpen, setPricePhotosModalOpen] = useState<boolean>(false);
    const [pricePageModalOpen, setPricePageModalOpen] = useState<boolean>(false);

    const {
        priceGroups,
        priceGroupsTotal,
        priceGroupsLoading,
        priceGroupsFilters,
        setPriceGroupsFilters,
        priceGroupsValidationErrors,
        resetPriceGroupsValidation,
        resetPriceGroupsFilters,
        createPriceGroup,
        updatePriceGroup,
        deletePriceGroup,
        prices,
        pricesTotal,
        pricesLoading,
        pricesFilters,
        setPricesFilters,
        pricesValidationErrors,
        resetPricesValidation,
        resetPricesFilters,
        priceGroupsOptions,
        createPrice,
        updatePrice,
        deletePrice,
        priceDetail,
        priceDetailLoading,
        loadPriceDetail,
    } = usePrices();

    const {
        hasPermission,
    } = usePricePageActionScopes();

    const filtersElements = (
        <PricesHeader
            activeTab={activeTab}
            setActiveTab={setActiveTab}
            onCreatePriceGroup={() => handleOpenPriceGroupModal(null)}
            onCreatePrice={() => handleOpenPriceModal(null)}
            resetPriceGroupsFilters={resetPriceGroupsFilters}
            resetPricesFilters={resetPricesFilters}
            priceGroupsTotal={priceGroupsTotal}
            priceGroupsFilters={priceGroupsFilters}
            setPriceGroupsFilters={setPriceGroupsFilters}
            priceTotal={pricesTotal}
            priceFilters={pricesFilters}
            setPriceFilters={setPricesFilters}
            hasPermission={hasPermission}
        />
    );

    const handleOpenPriceGroupModal = (priceGroupId: UUID | null) => {
        if (priceGroupId) {
            setSelectedPriceGroup(priceGroups.find((priceGroup) => priceGroup.id === priceGroupId) || null);
        } else {
            setSelectedPriceGroup(null);
        }
        setPriceGroupModalOpen(true);
    };

    const handleOpenPriceModal = (priceId: UUID | null) => {
        if (priceId) {
            setSelectedPrice(prices.find((price) => price.id === priceId) || null);
        } else {
            setSelectedPrice(null);
        }
        setPriceModalOpen(true);
    };

    const handleCreatePriceGroup = async (createData: PriceGroupCreateInDto) => {
        const result = await createPriceGroup(createData);
        if (result) {
            setPriceGroupModalOpen(false);
        }
    };

    const handleUpdatePriceGroup = async (priceGroupId: UUID, updateData: PriceGroupUpdateInDto) => {
        const result = await updatePriceGroup(priceGroupId, updateData);
        if (result) {
            setPriceGroupModalOpen(false);
        }
    };

    const handleDeletePriceGroup = async (priceGroupId: UUID) => {
        const result = await deletePriceGroup(priceGroupId);
        if (result) {
            setPriceGroupModalOpen(false);
        }
    };

    const handleCreatePrice = async (createData: PriceCreateInDto) => {
        const result = await createPrice(createData);
        if (result) {
            setPriceModalOpen(false);
        }
    };

    const handleUpdatePrice = async (priceId: UUID, updateData: PriceUpdateInDto) => {
        const result = await updatePrice(priceId, updateData);
        if (result) {
            setPriceModalOpen(false);
        }
    };

    const handleDeletePrice = async (priceId: UUID) => {
        const result = await deletePrice(priceId);
        if (result) {
            setPriceModalOpen(false);
        }
    };

    const handleOpenPriceTablesModal = (priceId: UUID) => {
        loadPriceDetail(priceId);
        setPriceTableModalOpen(true);
    };

    const handleOpenPricePhotosModal = (priceId: UUID) => {
        setPricePhotosModalOpen(true);
    };

    const handleOpenPricePageModal = (priceId: UUID) => {
        setPricePageModalOpen(true);
    };

    const handleUpdatePriceTables = async (tableData: TableType[]) => {
        if (!priceDetail?.id) {
            return;
        }
        const result = await updatePrice(priceDetail.id, { price_tables: tableData });
        if (result) {
            // Перезагружаем данные цены с таблицами
            await loadPriceDetail(priceDetail.id);
            setPriceTableModalOpen(false);
        }
    };

    return <>
        {activeTab === PricesTabsEnum.PRICES && (
            <>
                <PricesTable
                    prices={prices}
                    loading={pricesLoading}
                    filters={pricesFilters}
                    setFilters={setPricesFilters}
                    filtersElements={filtersElements}
                    onOpenPriceModal={handleOpenPriceModal}
                    priceGroupsOptions={priceGroupsOptions}
                    onOpenPriceTablesModal={handleOpenPriceTablesModal}
                    onOpenPricePhotosModal={handleOpenPricePhotosModal}
                    onOpenPricePageModal={handleOpenPricePageModal}
                />
                <PriceModal
                    open={priceModalOpen}
                    onClose={() => setPriceModalOpen(false)}
                    selectedPrice={selectedPrice}
                    onCreate={handleCreatePrice}
                    onUpdate={handleUpdatePrice}
                    onDelete={handleDeletePrice}
                    validationErrors={pricesValidationErrors}
                    onResetValidation={resetPricesValidation}
                    priceGroupsOptions={priceGroupsOptions}
                />
                <PriceTableModal
                    open={priceTableModalOpen}
                    onClose={() => setPriceTableModalOpen(false)}
                    tableData={priceDetail?.price_tables || []}
                    onSave={handleUpdatePriceTables}
                    loading={priceDetailLoading}
                />
            </>
        )}
        {activeTab === PricesTabsEnum.GROUPS && (
            <>
                <PricesGroupsTable
                    priceGroups={priceGroups}
                    loading={priceGroupsLoading}
                    filters={priceGroupsFilters}
                    setFilters={setPriceGroupsFilters}
                    filtersElements={filtersElements}
                    onOpenPriceGroupModal={handleOpenPriceGroupModal}
                />
                <PriceGroupModal
                    open={priceGroupModalOpen}
                    onClose={() => setPriceGroupModalOpen(false)}
                    selectedPriceGroup={selectedPriceGroup}
                    onCreate={handleCreatePriceGroup}
                    onUpdate={handleUpdatePriceGroup}
                    onDelete={handleDeletePriceGroup}
                    validationErrors={priceGroupsValidationErrors}
                    onResetValidation={resetPriceGroupsValidation}
                />
            </>
        )}
        {activeTab === PricesTabsEnum.DEVELOPER_DOCS && (
            <>
                <PricesDeveloperDocumentationView
                    activeTab={activeTab}
                    setActiveTab={setActiveTab}
                />
            </>
        )}
        {activeTab === PricesTabsEnum.USER_DOCS && (
            <>
                <PricesUserDocumentationView
                    activeTab={activeTab}
                    setActiveTab={setActiveTab}
                />
            </>
        )}
    </>;
}
