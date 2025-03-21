from uuid import UUID
from fastapi import Depends
from loguru import logger
from pydantic import ValidationError

from app.db.tables import Task, TaskProductItem
from app.repositories.external import ExternalRepository
from app.repositories.task import TaskRepository
from app.schemas.external import ExternalTaskProductSchema
from app.schemas.task_product import TaskProductCreateSchema, TaskProductSchema


class TaskProductService:
    def __init__(
            self,
            task_repository: TaskRepository = Depends(TaskRepository.depend),
            external_repository: ExternalRepository = Depends()
    ):
        self.task_repository = task_repository
        self.external_repository = external_repository

    async def create(self, schema: TaskProductCreateSchema) -> TaskProductSchema:
        model = Task(**schema.model_dump())
        model = await self.task_repository.store(model)
        return TaskProductSchema.model_validate(model)

    async def send(self, task_id: UUID, image_body: bytes):
        response = await self.external_repository.recognize_product(image_body, "russian")

        try:
            schema = ExternalTaskProductSchema.model_validate(response)
        except ValidationError as e:
            logger.debug(e)
            return await self.task_repository.update(task_id, error="Generation error")

        await self.task_repository.create_items(TaskProductItem(**schema.model_dump(), task_id=task_id))

    async def get(self, task_id: UUID) -> TaskProductSchema:
        model = await self.task_repository.get(task_id)
        return TaskProductSchema.model_validate(model)
