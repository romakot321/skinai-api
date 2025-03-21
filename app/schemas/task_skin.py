from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from app.schemas import BaseSearchSchema


class TaskSkinSchema(BaseModel):
    class TaskSkinItem(BaseModel):
        class Recommendations(BaseModel):
            morning: list[str]
            evening: list[str]

        id: int
        skin_type: str
        problems: list[str]
        recommendations: Recommendations

        model_config = ConfigDict(from_attributes=True)

    id: UUID
    items: list[TaskSkinItem] = Field(validation_alias="skin_items")

    model_config = ConfigDict(from_attributes=True)


class TaskSkinShortSchema(BaseModel):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class TaskSkinUpdateSchema(BaseModel):
    pass


class TaskSkinSearchSchema(BaseSearchSchema):
    pass


class TaskSkinCreateSchema(BaseModel):
    app_bundle: str
    user_id: str
