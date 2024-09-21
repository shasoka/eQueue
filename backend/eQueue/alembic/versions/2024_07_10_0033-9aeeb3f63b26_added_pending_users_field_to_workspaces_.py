"""Added pending_users field to workspaces table

Revision ID: 9aeeb3f63b26
Revises: 19b06903dc91
Create Date: 2024-07-10 00:33:09.338251

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9aeeb3f63b26"
down_revision: Union[str, None] = "19b06903dc91"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "workspaces",
        sa.Column(
            "pending_users",
            sa.ARRAY(sa.Integer()),
            server_default=sa.text("ARRAY[]::integer[]"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("workspaces", "pending_users")
