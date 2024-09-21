"""Changed token column length from 32 to 64

Revision ID: a9b0c49d1d61
Revises: 514bd7502c50
Create Date: 2024-07-07 23:50:30.068986

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a9b0c49d1d61"
down_revision: Union[str, None] = "514bd7502c50"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "moodle_token",
        existing_type=sa.VARCHAR(length=32),
        type_=sa.String(length=64),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "moodle_token",
        existing_type=sa.String(length=64),
        type_=sa.VARCHAR(length=32),
        existing_nullable=False,
    )
