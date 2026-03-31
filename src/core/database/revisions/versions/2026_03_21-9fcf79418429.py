"""
lead fields

Revision ID: 9fcf79418429
Revises: 9a9855a7b725  # noqa: UP035
Create Date: 2026-03-21 14:07:47.710912

"""

from typing import Sequence  # noqa: UP035

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9fcf79418429"
down_revision: str | None = "9a9855a7b725"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("lead", sa.Column("description", sa.String(length=1024), nullable=True))
    op.add_column("lead", sa.Column("url_code", sa.String(length=32), nullable=False))


def downgrade() -> None:
    op.drop_column("lead", "url_code")
    op.drop_column("lead", "description")
