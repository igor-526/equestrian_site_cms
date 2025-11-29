import { Tabs } from "antd";
import React from "react";

export type PricesTabsProps = {
    activeTab: string;
    setActiveTab: (tab: string) => void;

};

export const PricesTabs: React.FC<PricesTabsProps> = ({
    activeTab,
    setActiveTab,
}) => {
    const items = [
        {
            key: 'prices',
            label: 'Цены и услуги',
        },
        {
            key: 'groups',
            label: 'Группы услуг',
        },
        {
            key: 'docs',
            label: 'Документация',
        }
    ];
    return (
        <div className="flex items-center">
            <Tabs activeKey={activeTab} items={items} onChange={setActiveTab} />
        </div>
    );
};



