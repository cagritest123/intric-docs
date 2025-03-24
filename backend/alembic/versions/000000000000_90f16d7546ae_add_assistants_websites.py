"""add assistants_websites
Revision ID: 90f16d7546ae
Revises: f6871a69b246
Create Date: 2024-06-14 08:42:25.735077
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = '90f16d7546ae'
down_revision = 'f6871a69b246'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'assistants_websites',
        sa.Column('assistant_id', sa.UUID(), nullable=False),
        sa.Column('website_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ['assistant_id'], ['assistants.id'], ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(['website_id'], ['websites.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('assistant_id', 'website_id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assistants_websites')
    # ### end Alembic commands ###
