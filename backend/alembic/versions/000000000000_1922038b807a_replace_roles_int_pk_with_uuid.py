"""replace roles int pk with uuid
Revision ID: 1922038b807a
Revises: 778d94899fe5
Create Date: 2024-07-08 14:44:18.090062
"""

from typing import Optional

import sqlalchemy as sa
from pydantic import BaseModel

from alembic import op

# revision identifiers, used by Alembic
revision = '1922038b807a'
down_revision = '778d94899fe5'
branch_labels = None
depends_on = None


TABLE = "roles"
COLUMN_NAME = "role"


class Relationship(BaseModel):
    table_name: str
    col_name: Optional[str] = None
    fk_name: Optional[str] = None
    other_pk_col: Optional[str] = None
    ondelete: str
    create_temporary_uuid_col: bool = True


RELATIONSHIPS = [
    Relationship(
        table_name="users_roles",
        other_pk_col="user_id",
        ondelete="CASCADE",
    ),
]


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    for relationship in RELATIONSHIPS:
        if relationship.create_temporary_uuid_col:
            # Create temporary column
            op.add_column(
                relationship.table_name,
                sa.Column(f"{COLUMN_NAME}_uuid", sa.UUID(as_uuid=True)),
            )

            # Set column name
            if relationship.col_name:
                col_name = relationship.col_name
            else:
                col_name = f"{COLUMN_NAME}_id"

            # Fill temporary column with uuid:s matching the id
            op.execute(
                f"""
            UPDATE {relationship.table_name}
            SET {COLUMN_NAME}_uuid = (
                SELECT uuid FROM {TABLE}
                WHERE id = {relationship.table_name}.{col_name}
            )
            """
            )

        # Drop old foreign key constraint and remove old foreign key
        if relationship.fk_name:
            fk = relationship.fk_name
        else:
            fk = f"{relationship.table_name}_{COLUMN_NAME}_id_fkey"

        op.drop_constraint(fk, relationship.table_name, type_="foreignkey")

        if relationship.create_temporary_uuid_col:
            op.drop_column(relationship.table_name, col_name)

            # Rename uuid column to id
            op.alter_column(
                relationship.table_name,
                f"{COLUMN_NAME}_uuid",
                new_column_name=f"{COLUMN_NAME}_id",
            )

    # Drop old contraints
    op.drop_constraint(f"{TABLE}_pkey", TABLE, type_="primary")
    op.drop_index(f"ix_{TABLE}_uuid", TABLE, if_exists=True)

    # Drop old primary key, rename new primary key to "id"
    op.drop_column(TABLE, "id")
    op.alter_column(TABLE, "uuid", new_column_name="id")

    # Create new constraint
    op.create_primary_key(f"{TABLE}_pkey", TABLE, ["id"])

    for relationship in RELATIONSHIPS:

        # Create a new foreign key constraint,
        # pointing to the "same" column that has now been updated
        op.create_foreign_key(
            f"{relationship.table_name}_{TABLE}_fkey",
            relationship.table_name,
            TABLE,
            [f"{COLUMN_NAME}_id"],
            ["id"],
            ondelete=relationship.ondelete,
        )

        # If the foreign key is a part of a composite primary key, create that here
        if (
            relationship.other_pk_col is not None
            and relationship.create_temporary_uuid_col
        ):
            op.create_primary_key(
                f"{relationship.table_name}_pkey",
                relationship.table_name,
                [f"{COLUMN_NAME}_id", relationship.other_pk_col],
            )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Made by GPT-4, will probably not work
    # Downgrade will be made using database backups...

    # Reverse all changes related to foreign key and primary key constraints
    for relationship in reversed(RELATIONSHIPS):
        # If the foreign key is a part of a composite primary key, drop that first
        if relationship.other_pk_col is not None:
            op.drop_constraint(
                f"{relationship.table_name}_pkey",
                relationship.table_name,
                type_="primary",
            )

        # Drop the new foreign key constraints
        op.drop_constraint(
            f"{relationship.table_name}_{TABLE}_fkey",
            relationship.table_name,
            type_="foreignkey",
        )

        # Rename the 'id' column back to uuid
        op.alter_column(
            relationship.table_name,
            f"{COLUMN_NAME}_id",
            new_column_name=f"{COLUMN_NAME}_uuid",
        )

        # Recreate the original columns
        if relationship.col_name:
            col_name = relationship.col_name
        else:
            col_name = f"{COLUMN_NAME}_id"

        op.add_column(
            relationship.table_name, sa.Column(col_name, sa.INTEGER, autoincrement=True)
        )

        # Repopulate the original column with ids matching the uuid
        op.execute(
            f"""
            UPDATE {relationship.table_name}
            SET {col_name} = (
                SELECT id FROM {TABLE}
                WHERE uuid = {relationship.table_name}.{COLUMN_NAME}_uuid
            )
            """
        )

        # Drop the temporary uuid column
        op.drop_column(relationship.table_name, f"{COLUMN_NAME}_uuid")

        # Recreate the old foreign key constraint
        if relationship.fk_name:
            fk = relationship.fk_name
        else:
            fk = f"{relationship.table_name}_{COLUMN_NAME}_id"

        op.create_foreign_key(
            fk,
            relationship.table_name,
            TABLE,
            [col_name],
            ["id"],
            ondelete=relationship.ondelete,
        )

    # Restore the original primary key and index
    op.add_column(
        TABLE, sa.Column("id", sa.INTEGER, autoincrement=True, primary_key=True)
    )
    op.alter_column(TABLE, "id", new_column_name="uuid")
    op.create_index(f"ix_{TABLE}_uuid", TABLE, ["uuid"])

    # Restore the primary key constraint
    op.create_primary_key(f"{TABLE}_pkey", TABLE, ["id"])

    # ### end Alembic commands ###
