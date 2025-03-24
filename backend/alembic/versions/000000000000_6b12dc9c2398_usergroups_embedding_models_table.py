"""usergroups_embedding_models table
Revision ID: 6b12dc9c2398
Revises: f7bddc455b6c
Create Date: 2024-05-22 16:54:40.721116
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = "6b12dc9c2398"
down_revision = "f7bddc455b6c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "usergroups_embedding_models",
        sa.Column("embedding_model_id", sa.UUID(), nullable=False),
        sa.Column("user_group_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["embedding_model_id"], ["embedding_models.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_group_id"], ["user_groups.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("embedding_model_id", "user_group_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("usergroups_embedding_models")
    # ### end Alembic commands ###
