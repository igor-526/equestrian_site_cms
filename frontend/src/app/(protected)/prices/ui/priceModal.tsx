import { useEffect, useMemo, useState } from "react";
import {
    Button,
    Form,
    Input,
    InputNumber,
    Modal,
    Select,
    Space,
    message,
} from "antd";
import DeleteConfirmModal from "@/ui/deleteConfirmModal";
import { AddIcon } from "@/ui/icons";
import {
    priceCreateInDtoType,
    priceFormattersType,
    priceOutDtoType,
    priceUpdateInDtoType,
} from "@/types/api/prices";
import { pricePageMetadataType } from "@/types/ui/prices/page";
import { createPrice, deletePrice, updatePrice } from "@/api/prices";

type PriceModalProps = {
    open: boolean;
    onClose: () => void;
    selectedPrice: priceOutDtoType | null;
    pageMetadata: pricePageMetadataType;
    onDataChange: () => Promise<void> | void;
};

const GROUP_NEW = "__group_new__";
const GROUP_NONE = "__group_none__";

const priceFormatterLabels: Record<priceFormattersType, string> = {
    equal: "Равно",
    gt: "От",
    lt: "До",
    discuss: "Обсуждается",
};

const PriceModal = ({
    open,
    onClose,
    selectedPrice,
    pageMetadata,
    onDataChange,
}: PriceModalProps) => {
    const [form] = Form.useForm();
    const [submitLoading, setSubmitLoading] = useState(false);
    const [deleteModalOpen, setDeleteModalOpen] = useState(false);
    const [deleteLoading, setDeleteLoading] = useState(false);
    const [messageApi, contextHolder] = message.useMessage();

    const isEditMode = Boolean(selectedPrice);

    const groupOptions = useMemo(() => {
        const baseOptions =
            pageMetadata.priceGroups?.map((group) => ({
                label: group.label,
                value: group.value,
            })) ?? [];
        const optionsMap = new Map(baseOptions.map((option) => [option.value, option]));
        if (selectedPrice?.group && !optionsMap.has(selectedPrice.group)) {
            baseOptions.unshift({
                label: selectedPrice.group,
                value: selectedPrice.group,
            });
        }
        return [
            { label: "Без группы", value: GROUP_NONE },
            ...baseOptions,
            { label: "Новая группа", value: GROUP_NEW },
        ];
    }, [pageMetadata.priceGroups, selectedPrice]);

    useEffect(() => {
        if (!open) {
            form.resetFields();
            setDeleteModalOpen(false);
            return;
        }

        if (selectedPrice) {
            form.setFieldsValue({
                name: selectedPrice.name,
                description: selectedPrice.description ?? undefined,
                group_select: selectedPrice.group ?? GROUP_NONE,
                price_formatter: selectedPrice.price_formatter,
                price: selectedPrice.price,
            });
        } else {
            form.setFieldsValue({
                name: undefined,
                description: undefined,
                group_select: GROUP_NONE,
                price_formatter: "equal",
                price: 0,
            });
        }
    }, [open, selectedPrice, form]);

    const currentPriceFormatter = Form.useWatch("price_formatter", form);
    const currentGroupSelect = Form.useWatch("group_select", form);

    useEffect(() => {
        if (!open) {
            return;
        }
        if (currentPriceFormatter === "discuss") {
            const currentPrice = form.getFieldValue("price");
            if (currentPrice !== 0) {
                form.setFieldsValue({ price: 0 });
            }
        }
    }, [currentPriceFormatter, form, open]);

    const buildPayload = (): priceCreateInDtoType => {
        const values = form.getFieldsValue();
        let groupValue: string | null;
        if (values.group_select === GROUP_NEW) {
            const newGroupName: string | undefined = values.new_group_name;
            groupValue = newGroupName ? newGroupName.trim() : "";
        } else if (values.group_select === GROUP_NONE) {
            groupValue = null;
        } else {
            groupValue = values.group_select;
        }

        return {
            name: values.name.trim(),
            description: values.description?.trim() || null,
            group: groupValue || null,
            price:
                values.price_formatter === "discuss"
                    ? 0
                    : Number(values.price ?? 0),
            price_formatter: values.price_formatter,
        };
    };

    const handleSubmit = async () => {
        const isDiscuss = form.getFieldValue("price_formatter") === "discuss";
        try {
            await form.validateFields([
                "name",
                "description",
                "group_select",
                ...(currentGroupSelect === GROUP_NEW ? ["new_group_name"] : []),
                ...(isDiscuss ? [] : ["price"]),
                "price_formatter",
            ]);
            const payload = buildPayload();
            setSubmitLoading(true);
            if (isEditMode && selectedPrice) {
                const updatePayload: priceUpdateInDtoType = {};
                if (payload.name !== selectedPrice.name) {
                    updatePayload.name = payload.name;
                }
                if (
                    (payload.description ?? null) !==
                    (selectedPrice.description ?? null)
                ) {
                    updatePayload.description = payload.description ?? null;
                }
                if ((payload.group ?? null) !== (selectedPrice.group ?? null)) {
                    updatePayload.group = payload.group ?? null;
                }
                if (payload.price !== selectedPrice.price) {
                    updatePayload.price = payload.price;
                }
                if (
                    payload.price_formatter !== selectedPrice.price_formatter
                ) {
                    updatePayload.price_formatter = payload.price_formatter;
                }

                if (Object.keys(updatePayload).length === 0) {
                    messageApi.info("Изменений не найдено");
                    onClose();
                    return;
                }

                await updatePrice(selectedPrice.id, updatePayload);
                messageApi.success("Цена обновлена");
            } else {
                await createPrice(payload);
                messageApi.success("Цена создана");
            }
            await onDataChange();
            onClose();
        } catch (error) {
            if ((error as { errorFields?: unknown }).errorFields) {
                return;
            }
            messageApi.error("Не удалось сохранить цену");
        } finally {
            setSubmitLoading(false);
        }
    };

    const handleDelete = async () => {
        if (!selectedPrice) {
            return;
        }
        try {
            setDeleteLoading(true);
            await deletePrice(selectedPrice.id);
            messageApi.success("Цена удалена");
            await onDataChange();
            setDeleteLoading(false);
            setDeleteModalOpen(false);
            onClose();
        } catch {
            setDeleteLoading(false);
            messageApi.error("Не удалось удалить цену");
        }
    };

    const modalTitle = isEditMode
        ? selectedPrice?.name ?? "Редактирование цены"
        : "Новая цена";

    const modalFooter = isEditMode ? (
        <Space>
            <Button onClick={onClose}>Отмена</Button>
            <Button
                danger
                onClick={() => setDeleteModalOpen(true)}
            >
                Удалить
            </Button>
            <Button
                type="primary"
                onClick={handleSubmit}
                loading={submitLoading}
            >
                Сохранить
            </Button>
        </Space>
    ) : (
        <Space>
            <Button onClick={onClose}>Отмена</Button>
            <Button
                type="primary"
                icon={<AddIcon size={18} />}
                onClick={handleSubmit}
                loading={submitLoading}
            >
                Добавить
            </Button>
        </Space>
    );

    return (
        <>
            {contextHolder}
            <Modal
                title={modalTitle}
                open={open}
                onCancel={onClose}
                footer={modalFooter}
                destroyOnHidden
                maskClosable={false}
            >
                <Form
                    layout="vertical"
                    form={form}
                    initialValues={{
                        price_formatter: "equal",
                        group_select: GROUP_NONE,
                        price: 0,
                    }}
                >
                    <Form.Item
                        label="Группа"
                        name="group_select"
                        rules={[{ required: true, message: "Выберите группу" }]}
                    >
                        <Select
                            placeholder="Выберите группу"
                            options={groupOptions}
                        />
                    </Form.Item>

                    {currentGroupSelect === GROUP_NEW && (
                        <Form.Item
                            label="Новая группа"
                            name="new_group_name"
                            rules={[
                                { required: true, message: "Введите название группы" },
                                { whitespace: true, message: "Название группы не может состоять только из пробелов" },
                                {
                                    transform: (value: string) => value?.trim(),
                                    max: 31,
                                    message: "Максимум 31 символ",
                                },
                            ]}
                        >
                            <Input placeholder="Введите название новой группы" />
                        </Form.Item>
                    )}

                    <Form.Item
                        label="Наименование"
                        name="name"
                        rules={[
                            { required: true, message: "Наименование обязательно" },
                            {
                                whitespace: true,
                                message: "Наименование обязательно",
                            },
                            {
                                transform: (value: string) => value?.trim(),
                                max: 63,
                                message: "Максимум 63 символа",
                            },
                        ]}
                    >
                        <Input placeholder="Введите наименование услуги" />
                    </Form.Item>

                    <Form.Item
                        label="Описание"
                        name="description"
                        rules={[
                            {
                                max: 255,
                                message: "Максимум 255 символов",
                            },
                        ]}
                    >
                        <Input.TextArea
                            placeholder="Введите описание услуги"
                            autoSize={{ minRows: 2, maxRows: 4 }}
                        />
                    </Form.Item>

                    <Form.Item label="Цена" required>
                        <Space.Compact block>
                            <Form.Item
                                name="price_formatter"
                                noStyle
                                rules={[{ required: true }]}
                            >
                                <Select
                                    style={{ width: 180 }}
                                    options={(
                                        Object.keys(priceFormatterLabels) as priceFormattersType[]
                                    ).map((formatter) => ({
                                        label: priceFormatterLabels[formatter],
                                        value: formatter,
                                    }))}
                                />
                            </Form.Item>
                            {currentPriceFormatter !== "discuss" && (
                                <Form.Item
                                    name="price"
                                    noStyle
                                    rules={[
                                        { required: true, message: "Укажите стоимость" },
                                    ]}
                                >
                                    <InputNumber
                                        min={0}
                                        precision={0}
                                        style={{ width: "100%" }}
                                        placeholder="Введите стоимость"
                                    />
                                </Form.Item>
                            )}
                        </Space.Compact>
                        {currentPriceFormatter === "discuss" && (
                            <div className="text-xs text-gray-500 mt-2">
                                Стоимость будет обсуждаться. В систему будет сохранено значение 0.
                            </div>
                        )}
                    </Form.Item>
                </Form>
            </Modal>

            <DeleteConfirmModal
                open={deleteModalOpen}
                text="Вы действительно хотите удалить цену? Это действие нельзя отменить."
                onCancel={() => setDeleteModalOpen(false)}
                onDelete={handleDelete}
                confirmLoading={deleteLoading}
            />
        </>
    );
};

export default PriceModal;
