"""Added base models

Revision ID: c06abe37ee50
Revises: 
Create Date: 2024-07-07 01:46:22.982976

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c06abe37ee50"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "achievments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_achievments")),
        sa.UniqueConstraint("name", name=op.f("uq_achievments_name")),
    )
    op.create_table(
        "groups",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_groups")),
        sa.UniqueConstraint("name", name=op.f("uq_groups_name")),
    )
    op.create_table(
        "subjects",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_subjects")),
        sa.UniqueConstraint("name", name=op.f("uq_subjects_name")),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("moodle_token", sa.String(length=32), nullable=False),
        sa.Column("ecourses_user_id", sa.Integer(), nullable=False),
        sa.Column("assigned_group_id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("second_name", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("talon", sa.String(length=50), nullable=True),
        sa.Column("user_picture_url", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint(
            "ecourses_user_id", name=op.f("uq_users_ecourses_user_id")
        ),
        sa.UniqueConstraint(
            "moodle_token", name=op.f("uq_users_moodle_token")
        ),
        sa.UniqueConstraint("talon", name=op.f("uq_users_talon")),
    )
    op.create_table(
        "user_achievements",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("achievment_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_achievements_user_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_achievements")),
        sa.UniqueConstraint(
            "achievment_id", name=op.f("uq_user_achievements_achievment_id")
        ),
        sa.UniqueConstraint(
            "user_id", name=op.f("uq_user_achievements_user_id")
        ),
    )
    op.create_table(
        "workspaces",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("chief_id", sa.Integer(), nullable=False),
        sa.Column("semester", sa.Integer(), nullable=False),
        sa.Column("about", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["groups.id"],
            name=op.f("fk_workspaces_group_id_groups"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_workspaces")),
        sa.UniqueConstraint("group_id", name=op.f("uq_workspaces_group_id")),
    )
    op.create_table(
        "user_submissions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("submitted_works", sa.Integer(), nullable=False),
        sa.Column("total_required_works", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["subject_id"],
            ["subjects.id"],
            name=op.f("fk_user_submissions_subject_id_subjects"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_submissions_user_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspaces.id"],
            name=op.f("fk_user_submissions_workspace_id_workspaces"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_submissions")),
    )
    op.create_table(
        "workspace_subjects",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("scoped_name", sa.String(length=50), nullable=False),
        sa.Column("professor", sa.String(length=255), nullable=False),
        sa.Column("professor_contact", sa.String(), nullable=False),
        sa.Column("requirements", sa.String(length=255), nullable=False),
        sa.Column(
            "additional_fields",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("queue", sa.ARRAY(sa.Integer()), nullable=False),
        sa.ForeignKeyConstraint(
            ["subject_id"],
            ["subjects.id"],
            name=op.f("fk_workspace_subjects_subject_id_subjects"),
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspaces.id"],
            name=op.f("fk_workspace_subjects_workspace_id_workspaces"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_workspace_subjects")),
    )


def downgrade() -> None:
    op.drop_table("workspace_subjects")
    op.drop_table("user_submissions")
    op.drop_table("workspaces")
    op.drop_table("user_achievements")
    op.drop_table("users")
    op.drop_table("subjects")
    op.drop_table("groups")
    op.drop_table("achievments")
