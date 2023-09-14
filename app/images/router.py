import shutil

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import process_image

router = APIRouter(prefix="/images", tags=["Upload images"])


@router.post("/hotels")
async def upload_hotel_image(name: int, image: UploadFile):
    image_path = f"app/static/images/{str(name)}.webp"
    with open(image_path, "wb+") as image_file:
        shutil.copyfileobj(image.file, image_file)
    process_image.delay(image_path)
