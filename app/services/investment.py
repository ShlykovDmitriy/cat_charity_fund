from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def create_investment(
        session: AsyncSession,
        obj,
):
    projects = await session.execute(select(CharityProject).where(
        CharityProject.fully_invested == 0
    ).order_by('create_date'))
    project = projects.scalars().first()

    donations = await session.execute(select(Donation).where(
        Donation.fully_invested == 0
    ).order_by('create_date'))
    donation = donations.scalars().first()

    if not project or not donation:
        await session.commit()
        await session.refresh(obj)
        return obj

    amount_project = project.full_amount - project.invested_amount
    amount_donation = donation.full_amount - donation.invested_amount

    if amount_project > amount_donation:
        project.invested_amount += amount_donation
        donation.invested_amount += amount_donation
        donation.fully_invested = True
        donation.close_date = datetime.now()

    else:
        project.invested_amount += amount_project
        donation.invested_amount += amount_project
        project.fully_invested = True
        project.close_date = datetime.now()
        if amount_project == amount_donation:
            donation.fully_invested = True
            donation.close_date = datetime.now()

    session.add(project)
    session.add(donation)
    await session.commit()
    await session.refresh(project)
    await session.refresh(donation)
    await create_investment(session, obj)
    return obj