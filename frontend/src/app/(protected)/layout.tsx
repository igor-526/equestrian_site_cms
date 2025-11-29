"use client"

import { useState, useEffect } from 'react';
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

    // Перехватываем события popstate для обработки навигации
    useEffect(() => {
        const handlePopState = (event: PopStateEvent) => {
            // При навигации назад/вперед обновляем роутер
            router.replace(window.location.pathname);
        };

        window.addEventListener('popstate', handlePopState);
        return () => window.removeEventListener('popstate', handlePopState);
    }, [router]);

    const handleMenuClick = (path: string, e?: React.MouseEvent) => {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        // При статическом экспорте Next.js может делать полную перезагрузку
        // Используем комбинацию History API и router для клиентской навигации
        if (typeof window !== 'undefined' && pathname !== path) {
            // Сначала обновляем состояние Next.js роутера
            router.replace(path, { scroll: false });
            // Затем обновляем URL без перезагрузки страницы
            // Используем setTimeout чтобы дать роутеру время на обновление
            setTimeout(() => {
                if (window.location.pathname !== path) {
                    window.history.replaceState({ path }, '', path);
                }
            }, 0);
        }
    };

    const items = [
        {
            key: 'main',
            label: 'Дэшборд',
            icon: <DashboardIcon size={18} />,
            onClick: (e: any) => { handleMenuClick('/dashboard/', e) }
        },
        {
            key: 'horses',
            label: 'Лошади',
            icon: <HorsesIcon size={18} />,
            onClick: (e: any) => { handleMenuClick('/horses/', e) }
        },
        {
            key: 'info',
            label: 'Информация',
            icon: <InfoIcon size={18} />,
            onClick: (e: any) => { handleMenuClick('/info/', e) }
        },
        {
            key: 'gallery',
            label: 'Галерея',
            icon: <GalleryIcon size={18} />,
            onClick: (e: any) => { handleMenuClick('/gallery/', e) }
        },
        {
            key: 'prices',
            label: 'Услуги и цены',
            icon: <ServicesIcon size={18} />,
            onClick: (e: any) => { handleMenuClick('/prices/', e) }
        },
        {
            key: 'logout',
            label: 'Выйти',
            icon: <LogoutIcon size={18} />,
            onClick: (e: any) => { handleMenuClick('/login/', e) }
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