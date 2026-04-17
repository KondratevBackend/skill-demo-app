from sqlalchemy import select, func

from src.core.database.dao import BaseDAO
from src.core.database.models import Feedback


class FeedbackDAO(BaseDAO):
    async def get_random_feedback(self, without_ids: list[int] | None = None) -> Feedback:
        async for session in self._db.get_session():
            query = select(Feedback).order_by(func.random()).limit(1)
            if without_ids:
                query = query.where(Feedback.id.notin_(without_ids))
            result = await session.execute(query)
        return result.scalar_one_or_none()
