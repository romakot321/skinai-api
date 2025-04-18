from uuid import UUID
from fastapi import Depends
from loguru import logger
from pydantic import ValidationError

from app.db.tables import Task, TaskSkinItem
from app.repositories.external import ExternalRepository
from app.repositories.task import TaskRepository
from app.schemas.external import ExternalTaskSkinSchema
from app.schemas.task_skin import TaskSkinCreateSchema, TaskSkinSchema


class TaskSkinService:
    def __init__(
            self,
            task_repository: TaskRepository = Depends(TaskRepository.depend),
            external_repository: ExternalRepository = Depends()
    ):
        self.task_repository = task_repository
        self.external_repository = external_repository

    async def create(self, schema: TaskSkinCreateSchema) -> TaskSkinSchema:
        model = Task(**schema.model_dump())
        model = await self.task_repository.store(model)
        return TaskSkinSchema.model_validate(model)

    async def send(self, task_id: UUID, image_body: bytes, language: str):
        response = await self.external_repository.recognize_skin(image_body, language)

        try:
            schema = ExternalTaskSkinSchema.model_validate(response)
        except ValidationError as e:
            logger.debug(e)
            return await self.task_repository.update(task_id, error="Generation error")

        await self.task_repository.create_items(TaskSkinItem(**schema.model_dump(), task_id=task_id))

    async def get(self, task_id: UUID) -> TaskSkinSchema:
        model = await self.task_repository.get(task_id)
        return TaskSkinSchema.model_validate(model)
