"""add size and tenant_id to info_blobs and info_blob_chunks
Revision ID: cff8c549ca0c
Revises: ec23b59d7df1
Create Date: 2024-08-16 07:29:27.157333
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = 'cff8c549ca0c'
down_revision = 'ec23b59d7df1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('info_blob_chunks', sa.Column('size', sa.Integer(), nullable=True))
    op.add_column('info_blob_chunks', sa.Column('tenant_id', sa.UUID(), nullable=True))
    op.create_foreign_key(
        'info_blob_chunks_tenants_fkey',
        'info_blob_chunks',
        'tenants',
        ['tenant_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.add_column('info_blobs', sa.Column('tenant_id', sa.UUID(), nullable=True))
    op.create_foreign_key(
        'info_blobs_tenants_fkey',
        'info_blobs',
        'tenants',
        ['tenant_id'],
        ['id'],
        ondelete='CASCADE',
    )

    # Set columns for info-blob-chunks
    op.execute(
        sa.text(
            "UPDATE info_blob_chunks ibc "
            "SET size = octet_length(ibc.text) + vector_dims(ibc.embedding) * 4, "
            "tenant_id = u.tenant_id "
            "FROM info_blobs ib "
            "JOIN users u ON ib.user_id = u.id "
            "WHERE ibc.info_blob_id = ib.id;"
        )
    )

    # Set columns for info-blobs
    op.execute(
        sa.text(
            "UPDATE info_blobs ib "
            "SET tenant_id = u.tenant_id "
            "FROM public.users u "
            "WHERE ib.user_id = u.id;"
        )
    )

    op.alter_column('info_blob_chunks', column_name='tenant_id', nullable=False)
    op.alter_column('info_blob_chunks', column_name='size', nullable=False)
    op.alter_column('info_blobs', column_name='tenant_id', nullable=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('info_blobs_tenants_fkey', 'info_blobs', type_='foreignkey')
    op.drop_column('info_blobs', 'tenant_id')
    op.drop_constraint(
        'info_blob_chunks_tenants_fkey', 'info_blob_chunks', type_='foreignkey'
    )
    op.drop_column('info_blob_chunks', 'tenant_id')
    op.drop_column('info_blob_chunks', 'size')
    # ### end Alembic commands ###
