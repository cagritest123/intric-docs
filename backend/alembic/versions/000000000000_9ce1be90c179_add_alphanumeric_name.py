"""add alphanumeric name
Revision ID: 9ce1be90c179
Revises: 843cf217d46e
Create Date: 2024-03-08 07:54:07.084520
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = '9ce1be90c179'
down_revision = '843cf217d46e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tenants', sa.Column('alphanumeric', sa.String(), nullable=True))

    conn = op.get_bind()
    tenants = conn.execute(sa.text("SELECT * FROM tenants"))

    for tenant in tenants.fetchall():
        conn.execute(
            sa.text("UPDATE tenants SET alphanumeric = :alphanumeric WHERE id = :id"),
            parameters={
                "alphanumeric": "".join(ch for ch in tenant.name if ch.isalnum()),
                "id": tenant.id,
            },
        )

    op.alter_column('tenants', 'alphanumeric', nullable=False)
    op.create_unique_constraint(
        "tenants_alphanumeric_unique", 'tenants', ['alphanumeric']
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("tenants_alphanumeric_unique", 'tenants', type_='unique')
    op.drop_column('tenants', 'alphanumeric')
    # ### end Alembic commands ###
