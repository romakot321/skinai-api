from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from app.schemas import BaseSearchSchema


class TaskProductSchema(BaseModel):
    class TaskProductItem(BaseModel):
        class Ingredient(BaseModel):
            name: str
            risk_category: int

        id: int
        product_name: str
        skin_type: str
        ingredients: list[Ingredient]

        model_config = ConfigDict(from_attributes=True)

    id: UUID
    items: list[TaskProductItem] = Field(validation_alias="product_items")

    model_config = ConfigDict(from_attributes=True)


class TaskProductShortSchema(BaseModel):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class TaskProductUpdateSchema(BaseModel):
    pass


class TaskProductSearchSchema(BaseSearchSchema):
    pass


class TaskProductCreateSchema(BaseModel):
    app_bundle: str
    user_id: str
