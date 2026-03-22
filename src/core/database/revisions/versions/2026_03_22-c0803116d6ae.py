"""
edit url field lead model

Revision ID: c0803116d6ae
Revises: 9fcf79418429  # noqa: UP035
Create Date: 2026-03-22 09:47:09.325586

"""

from typing import Sequence  # noqa: UP035

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "c0803116d6ae"
down_revision: str | None = "9fcf79418429"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "lead", sa.Column("url", sa.String(length=32), nullable=False)
    )
    op.create_unique_constraint(op.f("uq_lead_url"), "lead", ["url"])
    op.drop_column("lead", "url_code")


def downgrade() -> None:
    op.add_column(
        "lead",
        sa.Column(
            "url_code",
            sa.VARCHAR(length=32),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(op.f("uq_lead_url"), "lead", type_="unique")
    op.drop_column("lead", "url")
