"""Added some fields to workspace_subjects table

Revision ID: 363c50ad760d
Revises: 959ca985d5d4
Create Date: 2024-07-10 20:11:36.000737

"""

#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "363c50ad760d"
down_revision: Union[str, None] = "959ca985d5d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "fk_user_submissions_workspace_id_workspaces",
        "user_submissions",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("fk_user_submissions_workspace_id_workspaces"),
        "user_submissions",
        "workspaces",
        ["workspace_id"],
        ["id"],
    )
    op.add_column(
        "workspace_subjects",
        sa.Column("ecourses_id", sa.Integer(), nullable=True),
    )
    op.add_column(
        "workspace_subjects",
        sa.Column("name", sa.String(length=255), nullable=False),
    )
    op.add_column(
        "workspace_subjects",
        sa.Column("ecourses_link", sa.Text(), nullable=True),
    )
    op.drop_constraint(
        "uq_workspace_subjects_scoped_name",
        "workspace_subjects",
        type_="unique",
    )
    op.create_unique_constraint(
        op.f("uq_workspace_subjects_ecourses_id"),
        "workspace_subjects",
        ["ecourses_id"],
    )
    op.create_unique_constraint(
        op.f("uq_workspace_subjects_name"), "workspace_subjects", ["name"]
    )
    op.drop_constraint(
        "fk_workspace_subjects_workspace_id_workspaces",
        "workspace_subjects",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("fk_workspace_subjects_workspace_id_workspaces"),
        "workspace_subjects",
        "workspaces",
        ["workspace_id"],
        ["id"],
    )
    op.drop_column("workspace_subjects", "scoped_name")


def downgrade() -> None:
    op.add_column(
        "workspace_subjects",
        sa.Column(
            "scoped_name",
            sa.VARCHAR(length=50),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(
        op.f("fk_workspace_subjects_workspace_id_workspaces"),
        "workspace_subjects",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_workspace_subjects_workspace_id_workspaces",
        "workspace_subjects",
        "workspaces",
        ["workspace_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(
        op.f("uq_workspace_subjects_name"),
        "workspace_subjects",
        type_="unique",
    )
    op.drop_constraint(
        op.f("uq_workspace_subjects_ecourses_id"),
        "workspace_subjects",
        type_="unique",
    )
    op.create_unique_constraint(
        "uq_workspace_subjects_scoped_name",
        "workspace_subjects",
        ["scoped_name"],
    )
    op.drop_column("workspace_subjects", "ecourses_link")
    op.drop_column("workspace_subjects", "name")
    op.drop_column("workspace_subjects", "ecourses_id")
    op.drop_constraint(
        op.f("fk_user_submissions_workspace_id_workspaces"),
        "user_submissions",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_user_submissions_workspace_id_workspaces",
        "user_submissions",
        "workspaces",
        ["workspace_id"],
        ["id"],
        ondelete="CASCADE",
    )
