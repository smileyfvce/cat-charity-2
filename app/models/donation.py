from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Donation(BaseModel):
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)