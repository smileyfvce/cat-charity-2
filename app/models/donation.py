from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Donation(BaseModel):
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return (
            f'<Donation(id={self.id}, amount={self.full_amount}, '
            f'invested={self.invested_amount})>'
        )