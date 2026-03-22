"""
edit url field lead model

Revision ID: a2642146b0f4
Revises: c0803116d6ae  # noqa: UP035
Create Date: 2026-03-22 09:49:34.063218

"""

from typing import Sequence  # noqa: UP035

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "a2642146b0f4"
down_revision: str | None = "c0803116d6ae"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "lead",
        "url",
        existing_type=sa.VARCHAR(length=32),
        type_=sa.String(length=128),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "lead",
        "url",
        existing_type=sa.String(length=128),
        type_=sa.VARCHAR(length=32),
        existing_nullable=False,
    )
