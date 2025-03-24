"""remove created with
Revision ID: c5ab99259246
Revises: 9f886203509c
Create Date: 2025-01-31 12:32:22.196711
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = 'c5ab99259246'
down_revision = '9f886203509c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'created_with')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'users',
        sa.Column('created_with', sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###
