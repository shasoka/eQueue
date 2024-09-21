"""Updated unique constraint for name and group_id in workspaces table

Revision ID: 3a5de8e17ab2
Revises: 1973b60ccaf6
Create Date: 2024-07-13 01:28:40.432459

"""

#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3a5de8e17ab2"
down_revision: Union[str, None] = "1973b60ccaf6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("uq_workspaces_group_id", "workspaces", type_="unique")
    op.drop_constraint("uq_workspaces_name", "workspaces", type_="unique")


def downgrade() -> None:
    op.create_unique_constraint("uq_workspaces_name", "workspaces", ["name"])
    op.create_unique_constraint("uq_workspaces_group_id", "workspaces", ["group_id"])
