from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.charity_project import CharityProject
from app.models.donation import Donation


def _distribute(source, targets) -> None:
    remaining = source.full_amount - source.invested_amount
    for target in targets:
        if remaining <= 0:
            break
        target_remaining = target.full_amount - target.invested_amount
        to_invest = min(remaining, target_remaining)
        target.invested_amount += to_invest
        source.invested_amount += to_invest
        remaining -= to_invest
        if target.invested_amount == target.full_amount:
            target.fully_invested = True
            target.close_date = datetime.now()
    if source.invested_amount == source.full_amount:
        source.fully_invested = True
        source.close_date = datetime.now()


async def invest_new_donation(
    donation: Donation, session: AsyncSession,
) -> Donation:
    session.add(donation)
    projects = await session.execute(
        select(CharityProject)
        .where(CharityProject.fully_invested.is_(False))
        .order_by(CharityProject.create_date)
    )
    _distribute(donation, projects.scalars().all())
    await session.commit()
    await session.refresh(donation)
    return donation


async def invest_new_project(
    project: CharityProject, session: AsyncSession,
) -> CharityProject:
    session.add(project)
    donations = await session.execute(
        select(Donation)
        .where(Donation.fully_invested.is_(False))
        .order_by(Donation.create_date)
    )
    _distribute(project, donations.scalars().all())
    await session.commit()
    await session.refresh(project)
    return project