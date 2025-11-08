"use client"

import { useCallback, useEffect, useState } from 'react';
import TablePagination from "@/ui/pagination";
import TableWithFilters from "@/ui/tableWithFilters";
import { Button } from 'antd';
import { AddIcon, ResetFiltersIcon } from '@/ui/icons';
import { priceGroupsOutDtoType, priceListInDtoType, priceOutDtoType, priceVariantsOutDtoType } from '@/types/api/prices';
import { getPriceGroups, getPriceList } from '@/api/prices';
import { getPriceTableColumns } from './priceTableColumns';
import PriceVariantsTable from './ui/priceVariantsTable';
import { priceTableDataItemType } from '@/types/ui/prices/table';
import { pricePageMetadataType } from '@/types/ui/prices/page';
import { isPriceFiltersEqualToInitial } from '@/utils/prices/filtersEqual';
import PriceModal from './ui/priceModal';
import PriceVariantModal from './ui/priceVariantModal';

const FILTER_INITIAL_STATE: priceListInDtoType = {
    limit: 25,
    offset: 0,
    name: undefined,
    description: undefined,
    group: [],
    price_gt: undefined,
    price_lt: undefined,
    sort: []
}

const PricesPage: React.FC = () => {

    const [filters, setFilters] = useState<priceListInDtoType>(FILTER_INITIAL_STATE);
    const [filtersReset, setFiltersReset] = useState<boolean>(true);
    const [loading, setLoading] = useState<boolean>(false);
    const [priceData, setPriceData] = useState<priceTableDataItemType[]>([]);
    const [priceDataCount, setPriceDataTotal] = useState<number>(0);
    const [pricePageMetadata, setPricePageMetadata] = useState<pricePageMetadataType>({
        priceGroups: [],
    });
    const [isPriceModalOpen, setIsPriceModalOpen] = useState<boolean>(false);
    const [selectedPrice, setSelectedPrice] = useState<priceOutDtoType | null>(null);

    const priceTableColumns = getPriceTableColumns(filters, setFilters, pricePageMetadata);

    const fetchPriceGroups = useCallback(async () => {
        const data: priceGroupsOutDtoType = await getPriceGroups();
        setPricePageMetadata(prev => ({
            ...prev,
            priceGroups: data.map(group => ({
                label: group,
                value: group,
                key: group,
            })),
        }));
    }, []);

    const fetchPrices = useCallback(async () => {
        setLoading(true);
        try {
            const data = await getPriceList(filters);
            setPriceData(
                data.items.map(
                    (item: priceOutDtoType) => ({
                        ...item,
                        key: item.id.toString(),
                    })
                )
            );
            setPriceDataTotal(data.total);
        } finally {
            setLoading(false);
        }
    }, [filters]);

    const handleDataChange = useCallback(async () => {
        await fetchPrices();
        await fetchPriceGroups();
    }, [fetchPrices, fetchPriceGroups]);

    const openCreatePriceModal = () => {
        setSelectedPrice(null);
        setIsPriceModalOpen(true);
    };

    const openEditPriceModal = (price: priceOutDtoType) => {
        setSelectedPrice(price);
        setIsPriceModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsPriceModalOpen(false);
        setSelectedPrice(null);
    };

    const headerElements = <>
        <div className="flex items-end">
            <TablePagination
                setFilters={setFilters}
                total={priceDataCount}
            />
            <Button
                className="mx-1"
                icon={<AddIcon size={18} />}
                onClick={openCreatePriceModal}>
                Новая цена
            </Button>
            <Button
                className="mx-1"
                color="danger"
                variant="outlined"
                disabled={filtersReset}
                icon={<ResetFiltersIcon size={18} />}
                onClick={() => { setFilters({ ...FILTER_INITIAL_STATE }); }}>
                Сбросить фильтры
            </Button>
        </div>
    </>

    useEffect(() => {
        fetchPrices();
    }, [fetchPrices]);
    useEffect(() => {
        setFiltersReset(isPriceFiltersEqualToInitial(FILTER_INITIAL_STATE, filters));
    }, [filters]);

    useEffect(() => {
        fetchPriceGroups();
    }, [fetchPriceGroups]);

    const [variantModalState, setVariantModalState] = useState<{
        open: boolean;
        priceId: string | null;
        variant: priceVariantsOutDtoType | null;
    }>({ open: false, priceId: null, variant: null });

    const openVariantModal = (priceId: string, variant: priceVariantsOutDtoType | null) => {
        setVariantModalState({ open: true, priceId, variant });
    };

    const closeVariantModal = () => {
        setVariantModalState({ open: false, priceId: null, variant: null });
    };

    const onExpandedPrice = (record: priceTableDataItemType) => {
        const priceVariants = priceData.find(item => item.id === record.id)?.variants;
        if (!priceVariants) {
            return (
                <div>
                    <h1>Произошла ошибка. Попробуйте обновить страницу.</h1>
                </div>
            )
        }
        return (
            <div className="m-2 p-4 bg-white border-1 border-gray-400 rounded-md">
                <PriceVariantsTable
                    priceVariants={priceVariants}
                    onVariantClick={(variant) => openVariantModal(record.id, variant)}
                />
                <div className="mt-3">
                    <Button
                        icon={<AddIcon size={18} />}
                        onClick={() => openVariantModal(record.id, null)}>
                        Новый вариант цены
                    </Button>
                </div>
            </div>

        )
    }

    return (
        <>
            <TableWithFilters
                tableColumns={priceTableColumns}
                tableData={priceData}
                tableLoading={loading}
                filtersElements={headerElements}
                expandable={{
                    expandedRowRender: (record: priceTableDataItemType) => onExpandedPrice(record),
                }}
                onRowListener={(record: priceTableDataItemType) => ({
                    onClick: () => openEditPriceModal(record),
                })}
            />
            <PriceModal
                open={isPriceModalOpen}
                onClose={handleCloseModal}
                selectedPrice={selectedPrice}
                pageMetadata={pricePageMetadata}
                onDataChange={handleDataChange}
            />
            {variantModalState.open && (
                <PriceVariantModal
                    open={variantModalState.open}
                    onClose={closeVariantModal}
                    priceId={variantModalState.priceId}
                    variant={variantModalState.variant}
                    onDataChange={handleDataChange}
                />
            )}
        </>
    )
}

export default PricesPage;
