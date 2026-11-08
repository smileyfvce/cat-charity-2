from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DonationCreate(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: str | None = None


class DonationDB(BaseModel):
    id: int
    full_amount: int
    comment: str | None = None
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DonationFullInfoDB(DonationDB):
    invested_amount: int
    fully_invested: bool
    close_date: datetime | None = None