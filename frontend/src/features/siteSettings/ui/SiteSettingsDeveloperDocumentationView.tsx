import React from "react";
import { SiteSettingsTabs } from "./SiteSettingsTabs";

export type SiteSettingsDeveloperDocumentationViewProps = {
    activeTab: string;
    setActiveTab: (tab: string) => void;
};

export const SiteSettingsDeveloperDocumentationView: React.FC<SiteSettingsDeveloperDocumentationViewProps> = ({
    activeTab,
    setActiveTab,
}) => {
    return (
        <>
            <SiteSettingsTabs activeTab={activeTab} setActiveTab={setActiveTab} />
        </>
    );
};



