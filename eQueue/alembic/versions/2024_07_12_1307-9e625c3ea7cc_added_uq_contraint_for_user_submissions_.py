"""Added uq contraint for user_submissions table

Revision ID: 9e625c3ea7cc
Revises: 7c276e0ac45f
Create Date: 2024-07-12 13:07:19.822216

"""

#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9e625c3ea7cc"
down_revision: Union[str, None] = "7c276e0ac45f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_user_submissons_uid_wid_sid",
        "user_submissions",
        ["user_id", "workspace_id", "subject_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_user_submissons_uid_wid_sid", "user_submissions", type_="unique"
    )
