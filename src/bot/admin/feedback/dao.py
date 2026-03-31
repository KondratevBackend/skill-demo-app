from src.core.database.dao import BaseDAO
from src.core.database.models import Feedback


class FeedbackAdminDAO(BaseDAO):
    async def create_feedback(
        self,
        # TODO: use DTO
        rating: int,
        user_name: str,
        is_verified_user: bool,
        advantages: str,
        flaws: str,
        comment: str,
        is_published: bool = True,
    ) -> Feedback:
        async for session in self._db.get_session():
            instance = Feedback(
                rating=rating,
                user_name=user_name,
                is_verified_user=is_verified_user,
                advantages=advantages,
                flaws=flaws,
                comment=comment,
                is_published=is_published,
            )
            session.add(instance)
            await session.commit()
        return instance
