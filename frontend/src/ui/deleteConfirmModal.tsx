import { Modal } from "antd";

type DeleteConfirmModalProps = {
    open: boolean;
    text: string;
    onCancel: () => void;
    onDelete: () => void;
    confirmLoading?: boolean;
};

const DeleteConfirmModal = ({
    open,
    text,
    onCancel,
    onDelete,
    confirmLoading = false,
}: DeleteConfirmModalProps) => {
    return (
        <Modal
            title="Подтверждение удаления"
            open={open}
            onCancel={onCancel}
            onOk={onDelete}
            okText="Удалить"
            okButtonProps={{ danger: true, loading: confirmLoading }}
            cancelText="Отмена"
            destroyOnHidden
            maskClosable={false}
            zIndex={2000}
        >
            {text}
        </Modal>
    );
};

export default DeleteConfirmModal;

