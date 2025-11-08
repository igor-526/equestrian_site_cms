import { SearchOutlined } from "@ant-design/icons";
import StringFilter from "@/ui/filters/stringFilter";
import ListFilter from "@/ui/filters/listFilter";
import { GetPriceTableColumnsType, priceTableDataItemType } from "@/types/ui/prices/table";
import { priceVariantTableDataItemType } from "@/types/ui/prices/priceVariantsTable";
import trimText from "@/utils/trimText";
import formatPrice from "@/utils/prices/priceFormatter";
import { Table } from "antd";

export const priceVariantTableColumns = [
    {
        title: 'Наименование',
        render: (record: priceVariantTableDataItemType) => {
            return (
                <>
                    <span>{record.name}</span>
                </>
            )
        },
        key: 'name'
    },
    {
        title: 'Описание',
        render: (record: priceVariantTableDataItemType) => {
            return (
                <>
                    <span>{record.description ? record.description : 'Без описания'}</span>
                </>
            )
        },
        key: 'description'
    },
    {
        title: 'Цена',
        render: (record: priceVariantTableDataItemType) => {
            return (
                <>
                    <span>{record.price}</span>
                </>
            )
        },
        key: 'price'
    },
]

export const getPriceTableColumns: GetPriceTableColumnsType = (
    filters, setFilters, pageMetadata) => {
    return [
        {
            title: 'Группа',
            render: (record: priceTableDataItemType) => {
                return (
                    <>
                        <span>{record.group ? record.group : 'Без группы'}</span>
                    </>
                )
            },
            key: 'group',
            filterIcon: <SearchOutlined style={{ color: filters.group?.length ? '#1677ff' : undefined }} />,
            filterDropdown: <>
                <div style={{ padding: 8, minWidth: 250 }}>
                   <ListFilter
                    filters={filters}
                    setFilters={setFilters}
                    filterKey="group"
                    filterData={pageMetadata.priceGroups}
                    placeHolder="Выберите группы цен"
                   />
                </div>
            </>,
        },
        {
            title: 'Наименование',
            render: (record: priceTableDataItemType) => {
                return (
                    <>
                        <span>{record.name}</span>
                    </>
                )
            },
            key: 'name',
            filterIcon: <SearchOutlined style={{ color: filters.description ? '#1677ff' : undefined }} />,
            filterDropdown: <>
                <div style={{ padding: 8 }}>
                    <StringFilter
                        filters={filters}
                        setFilters={setFilters}
                        filterKey="name"
                        placeHolder="Поиск по наименованию" />
                </div>
            </>,
        },
        {
            title: 'Описание',
            render: (record: priceTableDataItemType) => {
                return (
                    <>
                        <span>{record.description ? trimText(record.description, 30) : 'Без описания'}</span>
                    </>
                )
            },
            key: 'description',
            filterIcon: <SearchOutlined style={{ color: filters.description ? '#1677ff' : undefined }} />,
            filterDropdown: <>
                <div style={{ padding: 8 }}>
                    <StringFilter
                        filters={filters}
                        setFilters={setFilters}
                        filterKey="description"
                        placeHolder="Поиск по описанию" />
                </div>
            </>,
        },
        Table.EXPAND_COLUMN,
        {
            title: 'Цена',
            render: (record: priceTableDataItemType) => {
                return (
                    <>
                        <span>{formatPrice(record.price, record.price_formatter)}</span>
                    </>
                )
            },
            key: 'price'
        },
    ]
}

// const oldColumns = [
//     {
//         title: 'ФИО',
//         render: (record: UserTableDataItemType) => {
//             let fullName = `${record.last_name} ${record.first_name}`
//             if (record.patronymic) {
//                 fullName += ` ${record.patronymic}`
//             }
//             return (
//                 <>
//                     <span>{fullName}</span>
//                 </>
//             )
//         },
//         key: 'name',
//         filterIcon: <SearchOutlined style={{ color: filters.name ? '#1677ff' : undefined }} />,
//         filterDropdown: <>
//             <div style={{ padding: 8 }}>
//                 <StringFilter
//                     filters={filters}
//                     setFilters={setFilters}
//                     filterKey="name"
//                     placeHolder="Поиск по ФИО" />
//             </div>
//         </>,
//     },
//     {
//         title: 'Username',
//         render: (record: UserTableDataItemType) => {
//             return (
//                 <>
//                     <span>{record.username}</span>
//                 </>
//             )
//         },
//         key: 'username',
//         filterIcon: <SearchOutlined style={{ color: filters.username ? '#1677ff' : undefined }} />,
//         filterDropdown: <>
//             <div style={{ padding: 8 }}>
//                 <StringFilter
//                     filters={filters}
//                     setFilters={setFilters}
//                     filterKey="username"
//                     placeHolder="Поиск по username" />
//             </div>
//         </>,
//     },
//     {
//         title: 'Email',
//         render: (record: UserTableDataItemType) => {
//             return (
//                 <>
//                     <span>{record.email}</span>
//                 </>
//             )
//         },
//         key: 'email',
//         filterIcon: <SearchOutlined style={{ color: filters.email ? '#1677ff' : undefined }} />,
//         filterDropdown: <>
//             <div style={{ padding: 8 }}>
//                 <StringFilter
//                     filters={filters}
//                     setFilters={setFilters}
//                     filterKey="email"
//                     placeHolder="Поиск по email" />
//             </div>
//         </>,
//     },
//     {
//         title: 'Группы',
//         render: (record: UserTableDataItemType) => {
//             return (
//                 <>
//                     <span>{record.groups}</span>
//                 </>
//             )
//         },
//         key: 'groups',
//         filterIcon: <SearchOutlined style={{ color: filters.groups?.length ? '#1677ff' : undefined }} />,
//         filterDropdown:
//             <div style={{ padding: 8, minWidth: 250 }}>
//                 <ListFilter
//                     filters={filters}
//                     setFilters={setFilters}
//                     filterKey="groups"
//                     filterData={pageMetadata.user_groups}
//                     placeHolder="Выберите группы"
//                 />
//             </div>

//     }
// ]