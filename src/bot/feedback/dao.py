from sqlalchemy import select, func

from src.core.database.dao import BaseDAO
from src.core.database.models import Feedback


class FeedbackDAO(BaseDAO):
    async def get_random_feedback(self) -> Feedback:
        async for session in self._db.get_session():
            query = select(Feedback).order_by(func.random()).limit(1)
            result = await session.execute(query)
        return result.scalar_one()
