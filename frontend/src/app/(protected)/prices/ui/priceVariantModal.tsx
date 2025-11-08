import { useEffect, useState } from "react";
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
    priceFormattersType,
    priceVariantCreateInDtoType,
    priceVariantOutDtoType,
    priceVariantUpdateInDtoType,
} from "@/types/api/prices";
import {
    createPriceVariant,
    deletePriceVariant,
    updatePriceVariant,
} from "@/api/prices";

type PriceVariantModalProps = {
    open: boolean;
    onClose: () => void;
    priceId: string | null;
    variant: priceVariantOutDtoType | null;
    onDataChange: () => Promise<void> | void;
};

const priceVariantFormatterLabels: Record<priceFormattersType, string> = {
    equal: "Равно",
    gt: "От",
    lt: "До",
    discuss: "Обсуждается",
};

const PriceVariantModal = ({
    open,
    onClose,
    priceId,
    variant,
    onDataChange,
}: PriceVariantModalProps) => {
    const [form] = Form.useForm();
    const [messageApi, contextHolder] = message.useMessage();
    const [submitLoading, setSubmitLoading] = useState(false);
    const [deleteModalOpen, setDeleteModalOpen] = useState(false);
    const [deleteLoading, setDeleteLoading] = useState(false);

    const isEditMode = Boolean(variant);

    useEffect(() => {
        if (!open) {
            form.resetFields();
            setDeleteModalOpen(false);
            return;
        }

        if (variant) {
            form.setFieldsValue({
                name: variant.name,
                description: variant.description ?? undefined,
                price_formatter: variant.price_formatter,
                price: variant.price,
            });
        } else {
            form.setFieldsValue({
                name: undefined,
                description: undefined,
                price_formatter: "equal",
                price: 0,
            });
        }
    }, [variant, open, form]);

    const currentPriceFormatter = Form.useWatch("price_formatter", form);

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

    const buildPayload = (): priceVariantCreateInDtoType => {
        const values = form.getFieldsValue();
        return {
            name: values.name.trim(),
            description: values.description?.trim() || null,
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
                ...(isDiscuss ? [] : ["price"]),
                "price_formatter",
            ]);
            const payload = buildPayload();
            if (!priceId) {
                messageApi.error("Не удалось определить цену");
                onClose();
                return;
            }
            setSubmitLoading(true);
            if (isEditMode && variant) {
                const updatePayload: priceVariantUpdateInDtoType = {};
                if (payload.name !== variant.name) {
                    updatePayload.name = payload.name;
                }
                if (
                    (payload.description ?? null) !==
                    (variant.description ?? null)
                ) {
                    updatePayload.description = payload.description ?? null;
                }
                if (payload.price !== variant.price) {
                    updatePayload.price = payload.price;
                }
                if (payload.price_formatter !== variant.price_formatter) {
                    updatePayload.price_formatter = payload.price_formatter;
                }

                if (Object.keys(updatePayload).length === 0) {
                    messageApi.info("Изменений не найдено");
                    onClose();
                    return;
                }

                await updatePriceVariant(priceId, variant.id, updatePayload);
                messageApi.success("Вариант цены обновлён");
            } else {
                await createPriceVariant(priceId, payload);
                messageApi.success("Вариант цены создан");
            }
            await onDataChange();
            onClose();
        } catch (error) {
            if ((error as { errorFields?: unknown }).errorFields) {
                return;
            }
            messageApi.error("Не удалось сохранить вариант цены");
        } finally {
            setSubmitLoading(false);
        }
    };

    const handleDelete = async () => {
        if (!variant) {
            return;
        }
        try {
            if (!priceId) {
                messageApi.error("Не удалось определить цену");
                return;
            }
            setDeleteLoading(true);
            await deletePriceVariant(priceId, variant.id);
            messageApi.success("Вариант цены удалён");
            setDeleteModalOpen(false);
            await onDataChange();
            onClose();
        } catch {
            messageApi.error("Не удалось удалить вариант цены");
        } finally {
            setDeleteLoading(false);
        }
    };

    const modalTitle = isEditMode
        ? variant?.name ?? "Редактирование варианта цены"
        : "Новый вариант цены";

    const modalFooter = isEditMode ? (
        <Space>
            <Button onClick={onClose}>Отмена</Button>
            <Button danger onClick={() => setDeleteModalOpen(true)}>
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
                    form={form}
                    layout="vertical"
                    initialValues={{
                        price_formatter: "equal",
                        price: 0,
                    }}
                >
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
                        <Input placeholder="Введите наименование варианта" />
                    </Form.Item>

                    <Form.Item
                        label="Описание"
                        name="description"
                        rules={[
                            {
                                transform: (value: string) => value?.trim(),
                                max: 255,
                                message: "Максимум 255 символов",
                            },
                        ]}
                    >
                        <Input.TextArea
                            placeholder="Введите описание варианта"
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
                                        Object.keys(priceVariantFormatterLabels) as priceFormattersType[]
                                    ).map((formatter) => ({
                                        label: priceVariantFormatterLabels[formatter],
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
                text="Вы действительно хотите удалить вариант цены? Это действие нельзя отменить."
                onCancel={() => setDeleteModalOpen(false)}
                onDelete={handleDelete}
                confirmLoading={deleteLoading}
            />
        </>
    );
};

export default PriceVariantModal;

