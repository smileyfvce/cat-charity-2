from datetime import datetime
from app.models.charity_project import CharityProject
from app.models.donation import Donation


def _distribute(target, sources) -> None:
    remaining = target.full_amount - target.invested_amount
    for source in sources:
        if remaining <= 0:
            break
        source_remaining = source.full_amount - source.invested_amount
        to_invest = min(remaining, source_remaining)
        source.invested_amount += to_invest
        target.invested_amount += to_invest
        remaining -= to_invest
        if source.invested_amount == source.full_amount:
            source.fully_invested = True
            source.close_date = datetime.now()
    if target.invested_amount == target.full_amount:
        target.fully_invested = True
        target.close_date = datetime.now()


def invest_new_donation(
    target: Donation, sources: list[CharityProject],
) -> list[CharityProject]:
    _distribute(target, sources)
    return sources


def invest_new_project(
    target: CharityProject, sources: list[Donation],
) -> list[Donation]:
    _distribute(target, sources)
    return sources