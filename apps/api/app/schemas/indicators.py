from pydantic import BaseModel


class Indicator(BaseModel):
    id: str
    name: str
    category: str
    description: str
    unit: str
    frequency: str
    source_id: str
    higher_is_good: bool
    display_precision: int = 1
    human_translation: str
