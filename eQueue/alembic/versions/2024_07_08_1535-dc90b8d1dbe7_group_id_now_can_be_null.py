"""Group id now can be null

Revision ID: dc90b8d1dbe7
Revises: a9b0c49d1d61
Create Date: 2024-07-08 15:35:00.270348

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dc90b8d1dbe7"
down_revision: Union[str, None] = "a9b0c49d1d61"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users", "assigned_group_id", existing_type=sa.INTEGER(), nullable=True
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "assigned_group_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
