"""roles tenant_id
Revision ID: c18093554e08
Revises: 8043137f2894
Create Date: 2024-04-22 12:08:59.241059
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = "c18093554e08"
down_revision = "8043137f2894"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("roles", sa.Column("tenant_id", sa.Integer(), nullable=False))
    op.drop_constraint("roles_name_key", "roles", type_="unique")
    op.create_unique_constraint(
        "roles_name_tenant_unique", "roles", ["name", "tenant_id"]
    )
    op.create_foreign_key(
        "roles_tenant_fk", "roles", "tenants", ["tenant_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("roles_tenant_fk", "roles", type_="foreignkey")
    op.drop_constraint("roles_name_tenant_unique", "roles", type_="unique")
    op.create_unique_constraint("roles_name_key", "roles", ["name"])
    op.drop_column("roles", "tenant_id")
    # ### end Alembic commands ###
