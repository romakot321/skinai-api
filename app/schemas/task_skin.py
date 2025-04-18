from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from app.schemas import BaseSearchSchema


class TaskSkinSchema(BaseModel):
    class TaskSkinItem(BaseModel):
        class Score(BaseModel):
            class ScoreValue(BaseModel):
                value: int
                recommendations: list[str]

            overall: ScoreValue
            hydration: ScoreValue
            texture: ScoreValue
            redness: ScoreValue
            acne: ScoreValue
            wrinkles: ScoreValue

        id: int
        skin_type: str
        problems: list[str]
        score: Score

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
    language: str = "english"
