"""Added relation between workspaces.chief and users table

Revision ID: 4ac190792905
Revises: 4e8574ec6144
Create Date: 2024-07-09 14:48:25.909875

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4ac190792905"
down_revision: Union[str, None] = "4e8574ec6144"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        op.f("fk_workspaces_chief_id_users"),
        "workspaces",
        "users",
        ["chief_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_workspaces_chief_id_users"), "workspaces", type_="foreignkey"
    )
