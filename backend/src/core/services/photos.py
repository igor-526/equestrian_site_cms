import os
import uuid
from pathlib import Path
from typing import Literal
from uuid import UUID

from core.entities.photos import Photo
from core.exceptions.base import ClientError
from core.protocols.repositories.photo_repository import PhotoRepositoryProtocol
from core.schemas.photos import PhotoCreateDto, PhotoUpdateDto
from settings import settings


class PhotoService:
    def __init__(self, photo_repository: PhotoRepositoryProtocol):
        self.photo_repository = photo_repository
        # Путь к папке media в src (как указано в требованиях: src/media)
        # __file__ = backend/src/core/services/photos.py
        # parent.parent.parent = backend/src
        self.media_dir = Path(__file__).parent.parent.parent / "media"
        self.media_dir.mkdir(parents=True, exist_ok=True)

    async def _generate_unique_name(self, base_name: str, exclude_id: UUID | None = None) -> str:
        """Генерирует уникальное имя, добавляя суффиксы -1, -2 и т.д."""
        counter = 1
        current_name = base_name

        while True:
            existing = await self.photo_repository.find_by_name(current_name)
            if existing is None or (exclude_id is not None and existing.id == exclude_id):
                return current_name
            current_name = f"{base_name}-{counter}"
            counter += 1

    def _get_file_extension(self, filename: str) -> str:
        """Получить расширение файла."""
        return Path(filename).suffix

    def _generate_filename(self, original_filename: str) -> str:
        """Генерирует уникальное имя файла."""
        extension = self._get_file_extension(original_filename)
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{extension}"

    def _get_file_path(self, filename: str) -> Path:
        """Получить полный путь к файлу."""
        return self.media_dir / filename

    def _get_url(self, filename: str) -> str:
        """Получить URL для доступа к файлу."""
        protocol = "https" if not settings.debug else "http"
        return f"{protocol}://{settings.cms_backend_domain}/media/{filename}"

    async def _save_file(self, file_content: bytes, filename: str) -> str:
        """Сохранить файл и вернуть имя файла."""
        import asyncio
        file_path = self._get_file_path(filename)
        # Используем run_in_executor для неблокирующей записи
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: file_path.write_bytes(file_content))
        return filename

    async def _delete_file(self, filename: str) -> None:
        """Удалить файл."""
        import asyncio
        file_path = self._get_file_path(filename)
        if file_path.exists():
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, file_path.unlink)

    def _get_name_from_filename(self, filename: str) -> str:
        """Получить имя без расширения из имени файла."""
        return Path(filename).stem

    def _validate_file_type(self, filename: str, content: bytes) -> None:
        """Валидирует тип файла - только изображения и видео."""
        extension = self._get_file_extension(filename).lower()
        
        # Разрешенные расширения для изображений
        image_extensions = {
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg",
            ".ico", ".tiff", ".tif", ".heic", ".heif"
        }
        
        # Разрешенные расширения для видео
        video_extensions = {
            ".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mkv",
            ".m4v", ".3gp", ".ogv", ".mpeg", ".mpg"
        }
        
        allowed_extensions = image_extensions | video_extensions
        
        if extension not in allowed_extensions:
            raise ClientError(
                f"Недопустимый тип файла: {extension}. "
                f"Разрешены только изображения и видео файлы"
            )

    async def create(
        self, data: PhotoCreateDto, file_content: bytes, original_filename: str
    ) -> Photo:
        """Создать новую фотографию."""
        # Валидируем тип файла
        self._validate_file_type(original_filename, file_content)
        
        # Генерируем уникальное имя файла
        filename = self._generate_filename(original_filename)
        
        # Сохраняем файл
        await self._save_file(file_content, filename)
        
        # Обрабатываем name: если пустой (None или ""), генерируем из имени файла
        name = data.name
        if not name or name.strip() == "":
            name = self._get_name_from_filename(original_filename)
        
        # Обеспечиваем уникальность name
        name = await self._generate_unique_name(name)
        
        # Обрабатываем description: если пустой, сохраняем как ""
        description = data.description if data.description is not None else ""
        
        # Создаём сущность (храним только имя файла в path)
        photo = Photo(
            name=name,
            description=description,
            path=filename,
        )
        
        return await self.photo_repository.create(photo)

    async def update(
        self, id: UUID, data: PhotoUpdateDto, file_content: bytes | None = None, original_filename: str | None = None
    ) -> Photo:
        """Обновить фотографию."""
        photo = await self.photo_repository.get_by_id(id)
        if photo is None:
            raise ClientError("Фотография не найдена")

        # Если загружен новый файл
        if file_content is not None and original_filename is not None:
            # Валидируем тип файла
            self._validate_file_type(original_filename, file_content)
            
            # Удаляем старый файл
            old_filename = photo.path
            await self._delete_file(old_filename)
            
            # Сохраняем новый файл
            filename = self._generate_filename(original_filename)
            await self._save_file(file_content, filename)
            photo.path = filename

        update_data = {}
        
        # Обрабатываем name: если передан (даже как ""), обновляем
        if data.name is not None:
            name_value = data.name
            # Если пустая строка, генерируем из имени файла
            if not name_value or name_value.strip() == "":
                if original_filename:
                    name_value = self._get_name_from_filename(original_filename)
                else:
                    # Если файл не загружен, используем текущее имя файла
                    name_value = self._get_name_from_filename(photo.path)
            
            # Проверяем уникальность name
            name_value = await self._generate_unique_name(name_value, exclude_id=photo.id)
            update_data["name"] = name_value
        
        # Обрабатываем description: если передан (даже как ""), сохраняем как ""
        if data.description is not None:
            update_data["description"] = ""

        for key, value in update_data.items():
            setattr(photo, key, value)

        return await self.photo_repository.update(photo)

    async def get_by_id(self, id: UUID) -> Photo | None:
        """Получить фотографию по UUID."""
        return await self.photo_repository.get_by_id(id)

    async def delete(self, id: UUID) -> None:
        """Удалить фотографию."""
        photo = await self.photo_repository.get_by_id(id)
        if photo is None:
            raise ClientError("Фотография не найдена")
        
        # Удаляем файл
        filename = photo.path
        await self._delete_file(filename)
        
        await self.photo_repository.delete(id)

    async def get_filtered(
        self,
        *,
        name: str | None = None,
        description: str | None = None,
        sort: list[Literal["name", "description", "-name", "-description"]] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> tuple[list[Photo], int]:
        """Получить отфильтрованный список фотографий."""
        return await self.photo_repository.get_filtered(
            name=name,
            description=description,
            sort=sort,
            limit=limit,
            offset=offset,
        )

