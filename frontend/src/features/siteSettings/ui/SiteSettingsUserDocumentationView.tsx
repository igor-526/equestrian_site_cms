import React from "react";
import { SiteSettingsTabs } from "./SiteSettingsTabs";

export type SiteSettingsUserDocumentationViewProps = {
    activeTab: string;
    setActiveTab: (tab: string) => void;
};

export const SiteSettingsUserDocumentationView: React.FC<SiteSettingsUserDocumentationViewProps> = ({
    activeTab,
    setActiveTab,
}) => {
    return (
        <>
            <SiteSettingsTabs activeTab={activeTab} setActiveTab={setActiveTab} />
        </>
    );
};



