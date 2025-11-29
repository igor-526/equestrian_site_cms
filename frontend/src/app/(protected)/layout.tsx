"use client"

import { useState } from 'react';
import { MenuFoldOutlined, MenuUnfoldOutlined } from '@ant-design/icons';
import { Button, Layout, Menu } from 'antd';
import { useRouter, usePathname } from "next/navigation";
import {
    DashboardIcon,
    ServicesIcon,
    LogoutIcon,
    HorsesIcon,
    InfoIcon,
    GalleryIcon,
} from '@/ui/icons';

const { Header, Sider, Content } = Layout;

const BaseLayout = ({ children }: { children: React.ReactNode }) => {
    const [collapsed, setCollapsed] = useState(true)
    const router = useRouter();
    const pathname = usePathname();


    const handleMenuClick = (path: string) => {
        // Обычный клиентский роутинг Next.js
        if (pathname !== path) {
            router.push(path);
        }
    };

    const items = [
        {
            key: 'main',
            label: 'Дэшборд',
            icon: <DashboardIcon size={18} />,
            onClick: () => { handleMenuClick('/dashboard') }
        },
        {
            key: 'horses',
            label: 'Лошади',
            icon: <HorsesIcon size={18} />,
            onClick: () => { handleMenuClick('/horses') }
        },
        {
            key: 'info',
            label: 'Информация',
            icon: <InfoIcon size={18} />,
            onClick: () => { handleMenuClick('/info') }
        },
        {
            key: 'gallery',
            label: 'Галерея',
            icon: <GalleryIcon size={18} />,
            onClick: () => { handleMenuClick('/gallery') }
        },
        {
            key: 'prices',
            label: 'Услуги и цены',
            icon: <ServicesIcon size={18} />,
            onClick: () => { handleMenuClick('/prices') }
        },
        {
            key: 'logout',
            label: 'Выйти',
            icon: <LogoutIcon size={18} />,
            onClick: () => { handleMenuClick('/login') }
        },
    ]

    // Определяем активный ключ на основе текущего пути
    const getActiveKey = () => {
        if (pathname?.startsWith('/dashboard')) return 'main';
        if (pathname?.startsWith('/horses')) return 'horses';
        if (pathname?.startsWith('/info')) return 'info';
        if (pathname?.startsWith('/gallery')) return 'gallery';
        if (pathname?.startsWith('/prices')) return 'prices';
        return 'main';
    };

    return (
        <Layout className="h-screen">
            <Sider
                collapsedWidth="50"
                trigger={null}
                collapsible
                collapsed={collapsed}
            >
                <Menu
                    theme="dark"
                    mode="vertical"
                    selectedKeys={[getActiveKey()]}
                    items={items}
                />
            </Sider>
            <Layout className="flex flex-col h-screen overflow-y-hidden">
                <Header style={{ padding: 0, background: "#FFFFFF" }}>
                    <Button
                        type="text"
                        icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
                        onClick={() => setCollapsed(!collapsed)}
                        style={{
                            fontSize: '16px',
                            width: 64,
                            height: 64,
                        }}
                    />
                    <span style={{color: "grey", fontSize: 18, fontWeight: 600}}>Страница</span>
                </Header>
                <Content
                    style={{
                        margin: '24px 16px',
                        padding: 24,
                        minHeight: 280,
                        background: "#FFFFFF",
                        borderRadius: 8,
                    }}
                >
                    <div className="h-full overflow-y-auto overflow-x-auto">
                        {children}
                    </div>
                </Content>
            </Layout>
        </Layout>
    );
};

export default BaseLayout;