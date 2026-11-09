from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB,
)
from app.services.investing import invest_new_donation


router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    summary="Вывести список пожертвований"
)
async def get_all_donations(session: SessionDep):
    """Показать список всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.post('/', response_model=DonationDB, summary="Сделать пожертвование")
async def create_donation(
    donation_in: DonationCreate,
    session: SessionDep,
):
    """Создать пожертвование."""
    new_donation = Donation(**donation_in.model_dump())
    session.add(new_donation)

    sources = await session.execute(
        select(CharityProject)
        .where(CharityProject.fully_invested.is_(False))
        .order_by(CharityProject.create_date)
    )
    invest_new_donation(new_donation, sources.scalars().all())

    await session.commit()
    await session.refresh(new_donation)
    return new_donation