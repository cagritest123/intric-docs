"""add feedback to sessions
Revision ID: 1ac150bc6360
Revises: 912fecff999a
Create Date: 2024-03-26 08:36:15.933214
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = '1ac150bc6360'
down_revision = '912fecff999a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sessions', sa.Column('feedback_value', sa.Integer(), nullable=True))
    op.add_column('sessions', sa.Column('feedback_text', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sessions', 'feedback_text')
    op.drop_column('sessions', 'feedback_value')
    # ### end Alembic commands ###
