"""completion models relationships
Revision ID: 34688ff6661a
Revises: d48c7ec8a356
Create Date: 2024-05-16 11:38:37.121695
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = "34688ff6661a"
down_revision = "d48c7ec8a356"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "assistants", sa.Column("completion_model_id", sa.UUID(), nullable=True)
    )
    op.create_foreign_key(
        "assistants_completion_model_id_fkey",
        "assistants",
        "completion_models",
        ["completion_model_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.add_column(
        "questions", sa.Column("completion_model_id", sa.UUID(), nullable=True)
    )
    op.create_foreign_key(
        "questions_completion_model_id_fkey",
        "questions",
        "completion_models",
        ["completion_model_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # Get completion models
    conn = op.get_bind()
    res = conn.execute(sa.text("SELECT id, name, nickname FROM completion_models"))
    models = res.fetchall()

    for model in models:
        completion_model_id = model[0]
        completion_model_name = model[1]
        completion_model_nickname = model[2]

        # update assistants
        conn.execute(
            sa.text(
                """
                UPDATE assistants
                SET completion_model_id = :completion_model_id
                WHERE completion_model = :completion_model_nickname
                """
            ),
            parameters={
                "completion_model_id": completion_model_id,
                "completion_model_nickname": completion_model_nickname,
            },
        )
        # update questions
        conn.execute(
            sa.text(
                """
                UPDATE questions
                SET completion_model_id = :completion_model_id
                WHERE model = :completion_model_name
                """
            ),
            parameters={
                "completion_model_id": completion_model_id,
                "completion_model_name": completion_model_name,
            },
        )

    op.drop_column("questions", "model")
    op.drop_column("assistants", "completion_model")

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "questions",
        sa.Column(
            "model",
            sa.Text,
            nullable=True,
        ),
    )

    op.add_column(
        "assistants",
        sa.Column(
            "completion_model",
            sa.Text,
            nullable=True,
        ),
    )
    # Get completion models
    conn = op.get_bind()
    res = conn.execute(sa.text("SELECT id, name, nickname FROM completion_models"))
    models = res.fetchall()

    for model in models:
        completion_model_id = model[0]
        completion_model_name = model[1]
        completion_model_nickname = model[2]

        # update assistants
        conn.execute(
            sa.text(
                """
                UPDATE assistants
                SET completion_model = :completion_model_nickname
                WHERE completion_model_id = :completion_model_id
                """
            ),
            parameters={
                "completion_model_id": completion_model_id,
                "completion_model_nickname": completion_model_nickname,
            },
        )
        # update questions
        conn.execute(
            sa.text(
                """
                UPDATE questions
                SET model = :completion_model_name
                WHERE completion_model_id = :completion_model_id
                """
            ),
            parameters={
                "completion_model_id": completion_model_id,
                "completion_model_name": completion_model_name,
            },
        )

    op.alter_column("assistants", "completion_model", nullable=False)

    op.drop_constraint(
        "questions_completion_model_id_fkey", "questions", type_="foreignkey"
    )
    op.drop_column("questions", "completion_model_id")
    op.drop_constraint(
        "assistants_completion_model_id_fkey", "assistants", type_="foreignkey"
    )
    op.drop_column("assistants", "completion_model_id")
    # ### end Alembic commands ###
