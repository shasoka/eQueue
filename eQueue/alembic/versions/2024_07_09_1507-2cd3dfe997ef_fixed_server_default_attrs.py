"""Fixed server_default attrs

Revision ID: 2cd3dfe997ef
Revises: 4ac190792905
Create Date: 2024-07-09 15:07:58.572010

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2cd3dfe997ef"
down_revision: Union[str, None] = "4ac190792905"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "workspace_subjects",
        "professor",
        existing_type=sa.VARCHAR(length=255),
        nullable=True,
    )
    op.alter_column(
        "workspace_subjects",
        "professor_contact",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "workspace_subjects",
        "requirements",
        existing_type=sa.VARCHAR(length=255),
        nullable=True,
    )
    op.create_unique_constraint(
        op.f("uq_workspace_subjects_scoped_name"),
        "workspace_subjects",
        ["scoped_name"],
    )
    op.execute(
        "ALTER TABLE workspace_subjects ALTER COlUMN additional_fields set DEFAULT '{}'::jsonb;"
    )
    op.execute(
        "ALTER TABLE workspace_subjects ALTER COlUMN queue set DEFAULT ARRAY[]::integer[];"
    )
    op.execute(
        "ALTER TABLE users ALTER COlUMN status set DEFAULT 'Привет! Я использую eQueue! 🎫';"
    )
    op.execute("ALTER TABLE workspaces ALTER COlUMN semester set DEFAULT 1;")
    op.execute(
        "ALTER TABLE user_submissions ALTER COlUMN submitted_works set DEFAULT 0;"
    )
    op.execute(
        "ALTER TABLE user_submissions ALTER COlUMN total_required_works set DEFAULT 0;"
    )
    op.alter_column("workspaces", "about", existing_type=sa.VARCHAR(), nullable=True)


def downgrade() -> None:
    op.alter_column("workspaces", "about", existing_type=sa.VARCHAR(), nullable=False)
    op.drop_constraint(
        op.f("uq_workspace_subjects_scoped_name"),
        "workspace_subjects",
        type_="unique",
    )
    op.alter_column(
        "workspace_subjects",
        "requirements",
        existing_type=sa.VARCHAR(length=255),
        nullable=False,
    )
    op.alter_column(
        "workspace_subjects",
        "professor_contact",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.execute(
        "ALTER TABLE workspace_subjects ALTER COlUMN additional_fields DROP DEFAULT;"
    )
    op.execute("ALTER TABLE users ALTER COlUMN status DROP DEFAULT;")
    op.execute("ALTER TABLE workspaces ALTER COlUMN semester DROP DEFAULT;")
    op.execute("ALTER TABLE workspace_subjects ALTER COlUMN queue DROP DEFAULT ;")
    op.execute(
        "ALTER TABLE user_submissions ALTER COlUMN submitted_works DROP DEFAULT ;"
    )
    op.execute(
        "ALTER TABLE user_submissions ALTER COlUMN total_required_works DROP DEFAULT;"
    )
    op.alter_column(
        "workspace_subjects",
        "professor",
        existing_type=sa.VARCHAR(length=255),
        nullable=False,
    )
