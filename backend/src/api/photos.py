from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile

from core.entities.base import PaginatedEntities
from core.schemas.photos import PhotoCreateDto, PhotoOutDto, PhotoUpdateDto
from core.services.photos import PhotoService
from depends.services import get_photo_service
from settings import settings

router = APIRouter()


@router.get(
    "/photos",
    response_model=PaginatedEntities[PhotoOutDto],
    tags=["Photos"],
    description="Получить список фотографий с фильтрацией и сортировкой",
)
async def get_photos(
    photo_service: Annotated[PhotoService, Depends(get_photo_service)],
    name: str | None = Query(None, description="Фильтр по названию (вхождение)"),
    description: str | None = Query(None, description="Фильтр по описанию (вхождение)"),
    sort: list[Literal["name", "description", "-name", "-description"]] | None = Query(
        None, description="Сортировка"
    ),
    limit: int | None = Query(None, description="Лимит"),
    offset: int | None = Query(None, description="Смещение"),
) -> PaginatedEntities[PhotoOutDto]:
    entities, total = await photo_service.get_filtered(
        name=name,
        description=description,
        sort=sort,
        limit=limit,
        offset=offset,
    )
    # Преобразуем entities в DTO (url вычисляется автоматически через computed_field)
    items = [PhotoOutDto.model_validate(entity) for entity in entities]
    return PaginatedEntities(items=items, total=total)


@router.get(
    "/photos/{id}",
    response_model=PhotoOutDto,
    tags=["Photos"],
    description="Получить фотографию по UUID",
)
async def get_photo(
    id: UUID,
    photo_service: Annotated[PhotoService, Depends(get_photo_service)],
) -> PhotoOutDto:
    photo = await photo_service.get_by_id(id)
    if photo is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Фотография не найдена")

    return PhotoOutDto.model_validate(photo)


@router.post(
    "/photos",
    response_model=PhotoOutDto,
    tags=["Photos"],
    description="Создать новую фотографию",
)
async def create_photo(
    photo_service: Annotated[PhotoService, Depends(get_photo_service)],
    file: UploadFile = File(..., description="Файл фотографии или видео"),
    name: str | None = Form(None, description="Название (опционально, генерируется из имени файла)"),
    description: str | None = Form(None, description="Описание (опционально, по умолчанию пустая строка)"),
) -> PhotoOutDto:
    if not file.filename:
        from core.exceptions.base import ClientError
        raise ClientError("Имя файла не указано")
    
    file_content = await file.read()
    
    # Обрабатываем пустые значения: если передана пустая строка, преобразуем в None
    # чтобы сервис мог обработать это правильно
    name_value = name if name and name.strip() else None
    description_value = description if description is not None else None
    
    data = PhotoCreateDto(name=name_value, description=description_value)
    photo = await photo_service.create(data, file_content, file.filename)
    
    return PhotoOutDto.model_validate(photo)


@router.patch(
    "/photos/{id}",
    response_model=PhotoOutDto,
    tags=["Photos"],
    description="Обновить фотографию",
)
async def update_photo(
    photo_service: Annotated[PhotoService, Depends(get_photo_service)],
    id: UUID,
    file: UploadFile | None = File(None, description="Новый файл фотографии или видео (опционально)"),
    name: str | None = Form(None, description="Название (опционально)"),
    description: str | None = Form(None, description="Описание (опционально, пустая строка если не указано)"),
) -> PhotoOutDto:
    file_content = None
    original_filename = None
    if file:
        if not file.filename:
            from core.exceptions.base import ClientError
            raise ClientError("Имя файла не указано")
        file_content = await file.read()
        original_filename = file.filename
    
    # Обрабатываем пустые значения
    # name: если пустая строка или None, передаем "" чтобы сервис сгенерировал из файла
    # Если не передан вообще (None из Form), не обновляем
    name_value: str | None = None
    if name is not None:
        # Поле передано (даже как пустая строка)
        name_value = name if name.strip() else ""  # Пустая строка = генерировать из файла
    
    # description: если передан (даже как ""), сохраняем как ""
    # Если None (не передан), не обновляем
    description_value: str | None = None
    if description is not None:
        # Поле передано - сохраняем как "" (даже если было "")
        description_value = ""
    
    data = PhotoUpdateDto(name=name_value, description=description_value)
    photo = await photo_service.update(id, data, file_content, original_filename)
    
    return PhotoOutDto.model_validate(photo)


@router.delete(
    "/photos/{id}",
    status_code=204,
    tags=["Photos"],
    description="Удалить фотографию",
)
async def delete_photo(
    id: UUID,
    photo_service: Annotated[PhotoService, Depends(get_photo_service)],
) -> None:
    await photo_service.delete(id)

