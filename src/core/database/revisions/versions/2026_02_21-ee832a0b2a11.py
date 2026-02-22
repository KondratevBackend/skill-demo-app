"""
add lead

Revision ID: ee832a0b2a11
Revises: 6be801b961be  # noqa: UP035
Create Date: 2026-02-21 18:37:10.246277

"""

from typing import Sequence  # noqa: UP035

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ee832a0b2a11"
down_revision: str | None = "6be801b961be"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "lead",
        sa.Column("title", sa.String(length=64), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lead")),
    )
    op.create_table(
        "lead_user",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["lead_id"], ["lead.id"], name=op.f("fk_lead_user_lead_id_lead")),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name=op.f("fk_lead_user_user_id_user")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lead_user")),
        sa.UniqueConstraint("user_id", name=op.f("uq_lead_user_user_id")),
    )


def downgrade() -> None:
    op.drop_table("lead_user")
    op.drop_table("lead")
