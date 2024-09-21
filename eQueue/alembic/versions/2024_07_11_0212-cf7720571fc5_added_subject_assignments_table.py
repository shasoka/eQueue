"""Added subject_assignments table

Revision ID: cf7720571fc5
Revises: 363c50ad760d
Create Date: 2024-07-11 02:12:59.244897

"""

#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cf7720571fc5"
down_revision: Union[str, None] = "363c50ad760d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "subject_assignments",
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["subject_id"],
            ["workspace_subjects.id"],
            name=op.f("fk_subject_assignments_subject_id_workspace_subjects"),
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspaces.id"],
            name=op.f("fk_subject_assignments_workspace_id_workspaces"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_subject_assignments")),
        sa.UniqueConstraint("name", name=op.f("uq_subject_assignments_name")),
    )
    op.alter_column(
        "workspace_subjects",
        "name",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=255),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "workspace_subjects",
        "name",
        existing_type=sa.String(length=255),
        type_=sa.VARCHAR(length=50),
        existing_nullable=False,
    )
    op.drop_table("subject_assignments")
