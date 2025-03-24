"""completion models table additional fields
Revision ID: 45a36acc858a
Revises: b27110e2f529
Create Date: 2024-05-22 15:55:55.481712
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = "45a36acc858a"
down_revision = "b27110e2f529"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "completion_models", sa.Column("open_source", sa.Boolean(), nullable=True)
    )
    op.add_column(
        "completion_models", sa.Column("description", sa.String(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("completion_models", "description")
    op.drop_column("completion_models", "open_source")
    # ### end Alembic commands ###
