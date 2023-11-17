from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
import cloudinary
from cloudinary.uploader import upload
from src.database.db import get_db
from src.database.models import User
from src.services.auth import auth_service
import src.repository.photo as repository_photo
from src.conf.config import settings

from src.schemas import PhotoModels, ImageTagResponse, PhotoBase

cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

router = APIRouter(prefix='/photos', tags=["photos"])

@router.post("/", response_model=PhotoModels)
async def post_photo(
    body: PhotoBase,
    tags: List[ImageTagResponse] = [],
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
    file: UploadFile = File(...),
):
    # Загружаем фото в Cloudinary
    try:
        response = upload(file.file, folder="photoss")
        photo_url = response['secure_url']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки фотографии в Cloudinary: {str(e)}")

    # Сохраняем детали фотографии в базу данных
    return await repository_photo.add_photo(body, tags, current_user, db, file, photo_url)


@router.delete("/{photo_id}", response_model=PhotoModels)
async def delete_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_photo.remove_photo(photo_id, current_user, db)

@router.put("/{photo_id}", response_model=PhotoModels)
async def put_description(
    body: PhotoBase,
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_photo.update_description(photo_id, body, current_user, db)

@router.get("/{photo_id}", response_model=PhotoModels)
async def get_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_photo.see_photo(photo_id, current_user, db)