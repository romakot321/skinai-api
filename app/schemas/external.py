from pydantic import BaseModel


class ExternalTaskSkinSchema(BaseModel):
    class Recommendations(BaseModel):
        morning: list[str]
        evening: list[str]

    skin_type: str
    problems: list[str]
    recommendations: Recommendations


class ExternalTaskProductSchema(BaseModel):
    class Ingredient(BaseModel):
        name: str
        risk_category: int

    product_name: str
    skin_type: str
    ingredients: list[Ingredient]
