"""Assistants and Services as single table inheritance
Revision ID: e69bc6245edd
Revises: f77f46ec8b80
Create Date: 2023-11-09 11:51:10.404709
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = 'e69bc6245edd'
down_revision = 'f77f46ec8b80'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assistants', sa.Column('type', sa.Text(), nullable=True))
    op.add_column(
        'assistants', sa.Column('output_validation', sa.Text(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('assistants', 'output_validation')
    op.drop_column('assistants', 'type')
    # ### end Alembic commands ###
