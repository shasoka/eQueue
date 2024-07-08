"""Changed field moodle_token to access_token for oauth2 spec

Revision ID: 98c36c0d131e
Revises: dc90b8d1dbe7
Create Date: 2024-07-09 01:05:23.652153

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "98c36c0d131e"
down_revision: Union[str, None] = "dc90b8d1dbe7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("access_token", sa.String(length=64), nullable=False),
    )
    op.drop_constraint("uq_users_moodle_token", "users", type_="unique")
    op.create_unique_constraint(
        op.f("uq_users_access_token"), "users", ["access_token"]
    )
    op.drop_column("users", "moodle_token")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "moodle_token",
            sa.VARCHAR(length=64),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(op.f("uq_users_access_token"), "users", type_="unique")
    op.create_unique_constraint(
        "uq_users_moodle_token", "users", ["moodle_token"]
    )
    op.drop_column("users", "access_token")
