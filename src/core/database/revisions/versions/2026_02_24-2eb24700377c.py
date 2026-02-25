"""
init models

Revision ID: 2eb24700377c
Revises:   # noqa: UP035
Create Date: 2026-02-24 22:34:53.461828

"""

from typing import Sequence  # noqa: UP035

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2eb24700377c"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "feedback",
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("user_name", sa.String(length=64), nullable=True),
        sa.Column("advantages", sa.String(), nullable=True),
        sa.Column("flaws", sa.String(), nullable=True),
        sa.Column("comment", sa.String(), nullable=True),
        sa.Column("is_published", sa.Boolean(), nullable=False),
        sa.Column("is_verified_user", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name=op.f("ck_feedback_check_rating_range"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_feedback")),
    )
    op.create_table(
        "lead",
        sa.Column("title", sa.String(length=64), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lead")),
    )
    op.create_table(
        "server",
        sa.Column("domain", sa.String(length=64), nullable=False),
        sa.Column("connection_id", sa.Integer(), nullable=False),
        sa.Column("cookie", sa.String(length=1024), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_server")),
    )
    op.create_table(
        "tariff",
        sa.Column("text", sa.String(length=256), nullable=False),
        sa.Column("days", sa.Integer(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("limit_ip", sa.Integer(), nullable=False),
        sa.Column("order_index", sa.Integer(), server_default="0", nullable=False),
        sa.Column(
            "is_trial",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "is_popular",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tariff")),
    )
    op.create_table(
        "webhook_event",
        sa.Column(
            "provider",
            sa.Enum("yookassa", name="paymentprovidertype"),
            nullable=False,
        ),
        sa.Column("provider_event_id", sa.String(length=256), nullable=False),
        sa.Column("event_type", sa.String(), nullable=False),
        sa.Column("signature", sa.String(), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_webhook_event")),
    )
    op.create_table(
        "coupon",
        sa.Column("code", sa.String(length=128), nullable=False),
        sa.Column("tariff_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tariff_id"],
            ["tariff.id"],
            name=op.f("fk_coupon_tariff_id_tariff"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_coupon")),
        sa.UniqueConstraint("code", name=op.f("uq_coupon_code")),
    )
    op.create_table(
        "user",
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("user_name", sa.String(length=512), nullable=False),
        sa.Column("first_name", sa.String(length=512), nullable=True),
        sa.Column("last_name", sa.String(length=512), nullable=True),
        sa.Column("email", sa.String(length=256), nullable=True),
        sa.Column("phone", sa.String(length=128), nullable=True),
        sa.Column("xui_sub_id", sa.String(length=32), nullable=False),
        sa.Column("server_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["server_id"], ["server.id"], name=op.f("fk_user_server_id_server")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user")),
        sa.UniqueConstraint("telegram_id", name=op.f("uq_user_telegram_id")),
        sa.UniqueConstraint("xui_sub_id", name=op.f("uq_user_xui_sub_id")),
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
    op.create_table(
        "payment",
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(length=64), nullable=False),
        sa.Column(
            "provider",
            sa.Enum("yookassa", name="paymentprovidertype"),
            nullable=False,
        ),
        sa.Column("provider_payment_id", sa.String(length=256), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "pending",
                "succeeded",
                "refunded",
                "failed",
                name="paymentstatustype",
            ),
            nullable=False,
        ),
        sa.Column("payment_method", sa.String(length=256), nullable=True),
        sa.Column("paid_at", sa.DateTime(), nullable=True),
        sa.Column("tariff_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tariff_id"],
            ["tariff.id"],
            name=op.f("fk_payment_tariff_id_tariff"),
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name=op.f("fk_payment_user_id_user")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_payment")),
    )
    op.create_table(
        "referral",
        sa.Column(
            "status",
            sa.Enum("active", "rewarded", name="referralstatustype"),
            nullable=False,
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("referrer_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["referrer_id"],
            ["user.id"],
            name=op.f("fk_referral_referrer_id_user"),
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name=op.f("fk_referral_user_id_user")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_referral")),
        sa.UniqueConstraint("referrer_id", name=op.f("uq_referral_referrer_id")),
    )
    op.create_table(
        "subscription",
        sa.Column(
            "status",
            sa.Enum(
                "active",
                "expired",
                "canceled",
                "pending",
                name="subscriptionstatustype",
            ),
            nullable=False,
        ),
        sa.Column("starts_at", sa.DateTime(), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("tariff_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tariff_id"],
            ["tariff.id"],
            name=op.f("fk_subscription_tariff_id_tariff"),
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name=op.f("fk_subscription_user_id_user")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_subscription")),
    )


def downgrade() -> None:
    op.drop_table("subscription")
    op.drop_table("referral")
    op.drop_table("payment")
    op.drop_table("lead_user")
    op.drop_table("user")
    op.drop_table("coupon")
    op.drop_table("webhook_event")
    op.drop_table("tariff")
    op.drop_table("server")
    op.drop_table("lead")
    op.drop_table("feedback")

    sa.Enum(name="subscriptionstatustype").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="paymentprovidertype").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="referralstatustype").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="paymentstatustype").drop(op.get_bind(), checkfirst=False)
