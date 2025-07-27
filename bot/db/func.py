from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserDB


async def _get_user_db_model(session: AsyncSession,sessionmaker,user_id: int) -> UserDB | None:
    r = await session.scalar(select(UserDB).where(UserDB.user_id == user_id))
    if not r:
        async with sessionmaker() as _session:
            user = UserDB(user_id=user_id)
            _session.add(user)
            await _session.commit()
            return user
    return r
