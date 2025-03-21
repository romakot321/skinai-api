from contextlib import suppress
from fastapi import Response
from loguru import logger
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_service import BaseService as BaseRepository
from uuid import UUID

from app.db.tables import Task, TaskItem, engine


class TaskRepository[Table: Task, int](BaseRepository):
    base_table = Task
    engine = engine
    session: AsyncSession
    response: Response

    async def create(self, **fields) -> Task:
        return await self._create(**fields)

    async def store(self, model: Task) -> Task | None:
        self.session.add(model)
        try:
            await self._commit()
        except exc.IntegrityError as e:
            if "conflict" in str(e).lower():
                self.response.status_code = 200
                return
            logger.exception(e)
        self.response.status_code = 201
        return await self.get(model.id)

    async def create_items(self, *models: TaskItem):
        [self.session.add(model) for model in models]
        await self._commit()

    async def list(self, page=None, count=None) -> list[Task]:
        return list(await self._get_list(page=page, count=count))

    async def get(self, model_id: UUID) -> Task:
        return await self._get_one(
            id=model_id,
            select_in_load=[Task.items]
        )

    async def update(self, model_id: UUID, **fields) -> Task:
        return await self._update(model_id, **fields)

    async def delete(self, model_id: UUID):
        await self._delete(model_id)

    async def count(self):
        return await self._count()

