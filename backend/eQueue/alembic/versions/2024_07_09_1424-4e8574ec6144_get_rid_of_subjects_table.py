"""Get rid of subjects table

Revision ID: 4e8574ec6144
Revises: 98c36c0d131e
Create Date: 2024-07-09 14:24:58.183418

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4e8574ec6144"
down_revision: Union[str, None] = "98c36c0d131e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "fk_user_submissions_subject_id_subjects",
        "user_submissions",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("fk_user_submissions_subject_id_workspace_subjects"),
        "user_submissions",
        "workspace_subjects",
        ["subject_id"],
        ["id"],
    )
    op.drop_constraint(
        "fk_workspace_subjects_subject_id_subjects",
        "workspace_subjects",
        type_="foreignkey",
    )
    op.drop_column("workspace_subjects", "subject_id")
    op.drop_table(
        "subjects",
    )


def downgrade() -> None:
    op.create_table(
        "subjects",
        sa.Column("name", sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_subjects"),
        sa.UniqueConstraint("name", name="uq_subjects_name"),
    )
    op.add_column(
        "workspace_subjects",
        sa.Column("subject_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.create_foreign_key(
        "fk_workspace_subjects_subject_id_subjects",
        "workspace_subjects",
        "subjects",
        ["subject_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_user_submissions_subject_id_subjects",
        "user_submissions",
        "subjects",
        ["subject_id"],
        ["id"],
    )
    op.drop_constraint(
        op.f("fk_user_submissions_subject_id_workspace_subjects"),
        "user_submissions",
        type_="foreignkey",
    )
