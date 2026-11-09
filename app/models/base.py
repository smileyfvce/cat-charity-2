from datetime import datetime

from sqlalchemy import Boolean, Integer, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin


class BaseModel(CommonMixin, Base):
    __abstract__ = True

    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )
    close_date: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    __table_args__ = (
        CheckConstraint('full_amount > 0', name='positive_full_amount'),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='invested_le_full'
        ),
    )
