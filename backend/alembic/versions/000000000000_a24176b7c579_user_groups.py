"""user groups
Revision ID: a24176b7c579
Revises: 7fe4a2273f93
Create Date: 2024-03-26 16:53:11.646949
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = "a24176b7c579"
down_revision = "7fe4a2273f93"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_groups",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "tenant_id", name="user_groups_name_tenant_unique"),
    )
    op.create_index(op.f("ix_user_groups_id"), "user_groups", ["id"], unique=False)
    op.create_index(op.f("ix_user_groups_uuid"), "user_groups", ["uuid"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_groups_uuid"), table_name="user_groups")
    op.drop_index(op.f("ix_user_groups_id"), table_name="user_groups")
    op.drop_table("user_groups")
    # ### end Alembic commands ###
