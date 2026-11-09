from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import PROJECT_NAME_MAX_LENGTH
from app.models.base import BaseModel


class CharityProject(BaseModel):
    name: Mapped[str] = mapped_column(
        String(PROJECT_NAME_MAX_LENGTH),
        unique=True,
        nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self) -> str:
        return (
            f'<CharityProject(id={self.id}, name={self.name!r}, '
            f'invested={self.invested_amount}/{self.full_amount})>'
        )