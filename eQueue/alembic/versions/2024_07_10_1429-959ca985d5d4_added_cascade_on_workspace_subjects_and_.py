"""Added cascade on workspace_subjects and user_submissions when workspace deletion

Revision ID: 959ca985d5d4
Revises: 9aeeb3f63b26
Create Date: 2024-07-10 14:29:01.156897

"""

#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
#
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "959ca985d5d4"
down_revision: Union[str, None] = "9aeeb3f63b26"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop existing foreign key constraints
    op.drop_constraint(
        "fk_user_submissions_workspace_id_workspaces",
        "user_submissions",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_workspace_subjects_workspace_id_workspaces",
        "workspace_subjects",
        type_="foreignkey",
    )

    # Create new foreign key constraints with ON DELETE CASCADE
    op.create_foreign_key(
        "fk_user_submissions_workspace_id_workspaces",
        "user_submissions",
        "workspaces",
        ["workspace_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_workspace_subjects_workspace_id_workspaces",
        "workspace_subjects",
        "workspaces",
        ["workspace_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    # Drop the new foreign key constraints with ON DELETE CASCADE
    op.drop_constraint(
        "fk_user_submissions_workspace_id_workspaces",
        "user_submissions",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_workspace_subjects_workspace_id_workspaces",
        "workspace_subjects",
        type_="foreignkey",
    )

    # Restore the original foreign key constraints without ON DELETE CASCADE
    op.create_foreign_key(
        "fk_user_submissions_workspace_id_workspaces",
        "user_submissions",
        "workspaces",
        ["workspace_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_workspace_subjects_workspace_id_workspaces",
        "workspace_subjects",
        "workspaces",
        ["workspace_id"],
        ["id"],
    )
