from openai import AsyncOpenAI
from loguru import logger
import base64
import json


class ExternalRepository:
    def __init__(self):
        self.client = AsyncOpenAI()

    async def recognize_product(self, image_raw: bytes, language: str) -> dict | None:
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": 'Identify a skincare or cosmetic product from a photo, determine its composition, relate ingredients to health risk categories, and specify the skin type that the product is suitable for.\n\n# Steps\n\n1. **Photo Analysis:** Use the photo to identify the name or brand of the product.\n2. **Composition Determination:** Obtain a list of the product\'s ingredients using public data or cosmetic databases.\n3. **Risk Analysis:** Classify each ingredient according to health risk categories (low - 0, medium - 1, high - 2).\n4. **Skin Type Specification:** Determine which skin types (e.g., dry, oily, combination, sensitive) the product suits based on its composition. List them separated by commas.\n\n# Output Format\n\nThe response should be in JSON format with the following structure:\n```json\n{\n  \"product_name\": \"product name + brand in {language}\",\n  \"ingredients\": [\n    {\n      \"name\": \"ingredient name in {language}\",\n      \"risk_category\": risk category (low - 0/medium - 1/high - 2)\n    },\n    ...\n  ],\n  \"skin_type\": \"skin type\"\n}\n```\n\n# Notes\n\n- Ensure the data is sourced from reliable sources for accuracy.\n- Consider possible individual allergic reactions that do not fall into general risk categories.\n- Use current databases and publications for ingredient information.'
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "data:image/jpeg;base64,"
                                + base64.b64encode(image_raw).decode()
                            },
                        }
                    ],
                },
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_completion_tokens=1624,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        logger.debug(f"Get image response: {response}")
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return None

    async def recognize_skin(self, image_raw: bytes, language: str) -> dict | None:
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": 'Determine the skin type in the photograph and identify skin problems. Based on the analysis, provide skincare recommendations for this entity. Do not include reasoning in the response. It is important to give precise recommendations, find all skin issues, and accurately determine the skin type. The skin problem is a general term for a condition without specific words.\n\n# Steps\n\n1. Analyze the image and determine the skin type.\n2. Find potential problem areas on the skin from the photograph. List them as problems.\n3. Identify skin problems based on the photograph and previous step data. High accuracy is required, ensure all problems are found.\n4. If there are signs of allergies or other features, add them to the list of problems.\n5. Develop personalized skincare recommendations considering the identified skin type and problems.\n6. Divide recommendations into morning and evening routines.\n\n# Output Format\n\nProvide the result using the following JSON format, values must be translated to {language} language:\n{\n    \"skin_type\": \"skin type in {language}\",\n    \"problems\": [\"problem 1\", \"problem 2\", ...],\n    \"recommendations\": {\n        \"morning\": [\"Morning recommendation 1\", \"Morning recommendation 2\", ...],\n        \"evening\": [\"Evening recommendation 1\", \"Evening recommendation 2\", ...]\n    }\n}\n\n# Notes\n\n- Recommendations may include daily care as well as additional procedures.\n- If there are difficulties in determining the skin type or problems, you may give general care recommendations.\n- Ensure the analysis is as accurate as possible.'
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "data:image/jpeg;base64,"
                                + base64.b64encode(image_raw).decode()
                            },
                        }
                    ],
                },
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_completion_tokens=1624,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        logger.debug(f"Get image response: {response}")
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return None
