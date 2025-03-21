from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, status
from uuid import UUID

from app.schemas.task_product import TaskProductCreateSchema, TaskProductSchema
from app.services.task_product import TaskProductService
from . import validate_api_token

router = APIRouter(prefix="/api/task/product", tags=["Task Product"])

max_file_size = 25 * 1024 * 1024


async def _validate_file_size(file: UploadFile = File()) -> UploadFile:
    body = await file.read()
    if len(body) > max_file_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size is too big. Limit is 25mb"
        )
    await file.seek(0)
    return file


@router.post("", response_model=TaskProductSchema, dependencies=[Depends(validate_api_token)])
async def create_task(
    background_tasks: BackgroundTasks,
    schema: TaskProductCreateSchema = Depends(),
    file: UploadFile = Depends(_validate_file_size),
    service: TaskProductService = Depends(),
):
    task = await service.create(schema)
    background_tasks.add_task(service.send, task.id, await file.read())
    return task


@router.get("/{task_id}", response_model=TaskProductSchema, dependencies=[Depends(validate_api_token)])
async def get_task(task_id: UUID, service: TaskProductService = Depends()):
    return await service.get(task_id)

