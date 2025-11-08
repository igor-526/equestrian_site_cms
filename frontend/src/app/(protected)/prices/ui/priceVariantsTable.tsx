import { GetPriceVariantsTableElement } from '@/types/ui/prices/priceVariantsTable';
import { priceVariantTableColumns } from '../priceTableColumns';
import { Table } from 'antd';


const PriceVariantsTable: GetPriceVariantsTableElement = ({ priceVariants = [], onVariantClick }) => {
    const priceVariantsData = priceVariants.map(variant => ({
        ...variant,
        key: variant.id.toString(),
    }));

    return (
        <Table
            columns={priceVariantTableColumns}
            dataSource={priceVariantsData}
            loading={false}
            pagination={false}
            size="small"
            onRow={(record) => ({
                onClick: () => onVariantClick?.(record),
            })}
        />
    )
}

export default PriceVariantsTable;
