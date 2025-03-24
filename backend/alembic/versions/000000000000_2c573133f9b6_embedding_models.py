"""embedding models
Revision ID: 2c573133f9b6
Revises: 34688ff6661a
Create Date: 2024-05-16 11:50:43.779337
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = "2c573133f9b6"
down_revision = "34688ff6661a"
branch_labels = None
depends_on = None


INSERT_STATEMENT = """
    INSERT INTO embedding_models
    (name, family, open_source, dimensions, max_input, selectable, stability, hosting, hf_link)
    VALUES
    (
        :name,
        :family,
        :open_source,
        :dimensions,
        :max_input,
        :selectable,
        :stability,
        :hosting,
        :hf_link
    )
"""


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "embedding_models",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("open_source", sa.Boolean(), nullable=False),
        sa.Column("dimensions", sa.Integer(), nullable=True),
        sa.Column("max_input", sa.Integer(), nullable=True),
        sa.Column("selectable", sa.Boolean(), nullable=False),
        sa.Column("hf_link", sa.String(), nullable=True),
        sa.Column("family", sa.String(), nullable=False),
        sa.Column("stability", sa.String(), nullable=False),
        sa.Column("hosting", sa.String(), nullable=False),
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    # insert default embedding models
    conn = op.get_bind()

    conn.execute(
        sa.text(INSERT_STATEMENT),
        parameters={
            "name": "text-embedding-3-small",
            "family": "openai",
            "open_source": False,
            "dimensions": 512,
            "max_input": 8191,
            "selectable": True,
            "stability": "stable",
            "hosting": "usa",
            "hf_link": None,
        },
    )

    conn.execute(
        sa.text(INSERT_STATEMENT),
        parameters={
            "name": "text-embedding-ada-002",
            "family": "openai",
            "open_source": False,
            "dimensions": None,
            "max_input": 8191,
            "selectable": True,
            "stability": "stable",
            "hosting": "usa",
            "hf_link": None,
        },
    )

    conn.execute(
        sa.text(INSERT_STATEMENT),
        parameters={
            "name": "multilingual-e5-large",
            "family": "e5",
            "open_source": True,
            "dimensions": None,
            "max_input": 8191,
            "selectable": True,
            "stability": "experimental",
            "hosting": "eu",
            "hf_link": "https://huggingface.co/intfloat/multilingual-e5-large",
        },
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("embedding_models")
    # ### end Alembic commands ###
