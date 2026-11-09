from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from app.core.constants import (
    PROJECT_DESCRIPTION_MIN_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_NAME_MIN_LENGTH
)


class CharityProjectBase(BaseModel):
    name: str | None = Field(
        None,
        min_length=PROJECT_NAME_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH
    )
    description: str | None = Field(
        None,
        min_length=PROJECT_DESCRIPTION_MIN_LENGTH
    )
    full_amount: int | None = Field(None, gt=0)


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=PROJECT_NAME_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH
    )
    description: str = Field(..., min_length=PROJECT_DESCRIPTION_MIN_LENGTH)
    full_amount: int = Field(..., gt=0)


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)