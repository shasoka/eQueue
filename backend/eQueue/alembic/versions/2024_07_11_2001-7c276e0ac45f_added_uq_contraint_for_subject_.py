"""Added uq contraint for subject_assignments table

Revision ID: 7c276e0ac45f
Revises: cf7720571fc5
Create Date: 2024-07-11 20:01:48.113340

"""

#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7c276e0ac45f"
down_revision: Union[str, None] = "cf7720571fc5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "uq_subject_assignments_name", "subject_assignments", type_="unique"
    )
    op.create_unique_constraint(
        "uq_subj_assign_wid_sid_name",
        "subject_assignments",
        ["workspace_id", "subject_id", "name"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_subj_assign_wid_sid_name", "subject_assignments", type_="unique"
    )
    op.create_unique_constraint(
        "uq_subject_assignments_name", "subject_assignments", ["name"]
    )
