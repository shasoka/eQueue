"""Added base models and seeder for groups table

Revision ID: 8c675877d4ba
Revises:
Create Date: 2024-07-07 03:10:31.326831

"""

from typing import Sequence, Union

import requests
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from core.config import settings

# revision identifiers, used by Alembic.
revision: str = "514bd7502c50"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _fetch_raw_groups() -> list[dict]:
    response = requests.get(settings.moodle.timetable_url)
    response.raise_for_status()
    raw_data = response.json()

    unique_groups = []
    for group in raw_data:
        base_name = group["name"].split(" (")[0] + " (Глобальная группа)"
        if base_name not in unique_groups:
            unique_groups.append(base_name)
        if group["name"] not in unique_groups:
            unique_groups.append(group["name"])
    return [{"name": group} for group in unique_groups]


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "achievements",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_achievements")),
        sa.UniqueConstraint("name", name=op.f("uq_achievements_name")),
    )
    groups_t = op.create_table(
        "groups",
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_groups")),
        sa.UniqueConstraint("name", name=op.f("uq_groups_name")),
    )
    op.bulk_insert(groups_t, _fetch_raw_groups())
    op.create_table(
        "subjects",
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_subjects")),
        sa.UniqueConstraint("name", name=op.f("uq_subjects_name")),
    )
    op.create_table(
        "users",
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
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["assigned_group_id"],
            ["groups.id"],
            name=op.f("fk_users_assigned_group_id_groups"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("ecourses_user_id", name=op.f("uq_users_ecourses_user_id")),
        sa.UniqueConstraint("moodle_token", name=op.f("uq_users_moodle_token")),
        sa.UniqueConstraint("talon", name=op.f("uq_users_talon")),
    )
    op.create_table(
        "workspaces",
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("chief_id", sa.Integer(), nullable=False),
        sa.Column("semester", sa.Integer(), nullable=False),
        sa.Column("about", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["groups.id"],
            name=op.f("fk_workspaces_group_id_groups"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_workspaces")),
        sa.UniqueConstraint("group_id", name=op.f("uq_workspaces_group_id")),
    )
    op.create_table(
        "user_achievements",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("achievement_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["achievement_id"],
            ["achievements.id"],
            name=op.f("fk_user_achievements_achievement_id_achievements"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_achievements_user_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_achievements")),
        sa.UniqueConstraint(
            "achievement_id", name=op.f("uq_user_achievements_achievement_id")
        ),
        sa.UniqueConstraint("user_id", name=op.f("uq_user_achievements_user_id")),
    )
    op.create_table(
        "user_submissions",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("submitted_works", sa.Integer(), nullable=False),
        sa.Column("total_required_works", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
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
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
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
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("workspace_subjects")
    op.drop_table("user_submissions")
    op.drop_table("user_achievements")
    op.drop_table("workspaces")
    op.drop_table("users")
    op.drop_table("subjects")
    op.drop_table("groups")
    op.drop_table("achievements")
    # ### end Alembic commands ###
