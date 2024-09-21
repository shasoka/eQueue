"""Added unique constraint for name and group_id in workspaces table

Revision ID: 1973b60ccaf6
Revises: 49ac040b713e
Create Date: 2024-07-13 01:10:14.863998

"""

#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "1973b60ccaf6"
down_revision: Union[str, None] = "49ac040b713e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "user_submissions",
        "submitted_works",
        existing_type=postgresql.ARRAY(sa.INTEGER()),
        nullable=False,
        existing_server_default=sa.text("'{}'::integer[]"),
    )
    op.create_unique_constraint(
        "uq_workspace_gid_name", "workspaces", ["group_id", "name"]
    )


def downgrade() -> None:
    op.drop_constraint("uq_workspace_gid_name", "workspaces", type_="unique")
    op.alter_column(
        "user_submissions",
        "submitted_works",
        existing_type=postgresql.ARRAY(sa.INTEGER()),
        nullable=True,
        existing_server_default=sa.text("'{}'::integer[]"),
    )
