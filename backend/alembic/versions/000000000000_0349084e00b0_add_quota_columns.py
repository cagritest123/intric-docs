"""add quota columns
Revision ID: 0349084e00b0
Revises: f77f46ec8b80
Create Date: 2023-11-10 16:08:07.392700
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = '0349084e00b0'
down_revision = 'f77f46ec8b80'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('quota_size', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('quota_used', sa.Integer(), nullable=True))

    op.execute("UPDATE users SET quota_used = 0")
    op.alter_column('users', 'quota_used', nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'quota_used')
    op.drop_column('users', 'quota_size')
    # ### end Alembic commands ###
