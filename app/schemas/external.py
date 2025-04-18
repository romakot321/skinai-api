from pydantic import BaseModel


class ExternalTaskSkinSchema(BaseModel):
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

    skin_type: str
    problems: list[str]
    score: Score


class ExternalTaskProductSchema(BaseModel):
    class Ingredient(BaseModel):
        name: str
        risk_category: int

    product_name: str
    skin_type: str
    ingredients: list[Ingredient]
