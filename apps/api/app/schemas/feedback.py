from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


FeedbackType = Literal["bug", "data_issue", "confusing", "feature_request", "design_feedback", "general"]
FeedbackStatus = Literal["new", "reviewed", "planned", "fixed", "closed"]


class FeedbackCreate(BaseModel):
    page_path: str | None = Field(default=None, max_length=500)
    feedback_type: FeedbackType
    rating: int | None = Field(default=None, ge=1, le=5)
    message: str = Field(min_length=10, max_length=4000)
    email: str | None = Field(default=None, max_length=320)
    metadata: dict[str, Any] | None = None

    @field_validator("message")
    @classmethod
    def strip_message(cls, value: str) -> str:
        return value.strip()

    @field_validator("email")
    @classmethod
    def simple_email_check(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        cleaned = value.strip()
        if "@" not in cleaned or "." not in cleaned.split("@")[-1]:
            raise ValueError("Enter a valid email address.")
        return cleaned


class FeedbackUpdate(BaseModel):
    status: FeedbackStatus


class FeedbackResponse(BaseModel):
    id: str
    user_id: str | None = None
    page_path: str | None = None
    feedback_type: str
    rating: int | None = None
    message: str
    email: str | None = None
    metadata: dict[str, Any] | None = None
    status: str
    created_at: str
    updated_at: str


class FeedbackListResponse(BaseModel):
    items: list[FeedbackResponse]
