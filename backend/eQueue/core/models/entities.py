#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from datetime import datetime, timezone
from sqlalchemy import (
    String,
    TIMESTAMP,
    func,
    ForeignKey,
    ARRAY,
    Integer,
    text,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    access_token: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    ecourses_user_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    assigned_group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id"), nullable=True
    )
    assigned_workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"), nullable=True
    )
    workspace_chief: Mapped[bool] = mapped_column(default=False, server_default="false")
    first_name: Mapped[str] = mapped_column(String(50))
    second_name: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(
        String(100),
        default="Привет! Я использую eQueue! 🎫",
        server_default=text("Привет! Я использую eQueue! 🎫"),
    )
    talon: Mapped[str] = mapped_column(String(50), nullable=True, unique=True)
    user_picture_url: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
    )

    achievements: Mapped[list["UserAchievement"]] = relationship(
        "UserAchievement", back_populates="user"
    )
    assigned_group: Mapped["Group"] = relationship("Group", back_populates="users")
    assigned_workspace: Mapped["Workspace"] = relationship(
        "Workspace", back_populates="users"
    )
    submissions: Mapped[list["UserSubmission"]] = relationship(
        "UserSubmission", back_populates="user"
    )


class Achievement(Base):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    user_achievements: Mapped[list["UserAchievement"]] = relationship(
        "UserAchievement", back_populates="achievement"
    )


class UserAchievement(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True
    )
    achievement_id: Mapped[int] = mapped_column(
        ForeignKey("achievements.id"), nullable=False, unique=True
    )

    user: Mapped["User"] = relationship("User", back_populates="achievements")
    achievement: Mapped["Achievement"] = relationship(
        "Achievement", back_populates="user_achievements"
    )


class Group(Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    users: Mapped[list["User"]] = relationship("User", back_populates="assigned_group")
    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="group")


class Workspace(Base):
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id"),
        nullable=False,
    )
    semester: Mapped[int] = mapped_column(
        default=1,
        server_default=text("1"),
    )
    about: Mapped[str] = mapped_column(nullable=True)

    # There is a trigger function for name field in migrations
    name: Mapped[str] = mapped_column(
        String(35),
        nullable=True,
    )

    pending_users: Mapped[list[int]] = mapped_column(
        default=[],
        server_default=text("ARRAY[]::integer[]"),
    )

    group: Mapped["Group"] = relationship(
        "Group",
        back_populates="workspace",
    )
    subjects: Mapped[list["WorkspaceSubject"]] = relationship(
        "WorkspaceSubject",
        back_populates="workspace",
        cascade="all, delete-orphan",
    )
    submissions: Mapped[list["UserSubmission"]] = relationship(
        "UserSubmission",
        back_populates="workspace",
        cascade="all, delete-orphan",
    )
    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="assigned_workspace",
    )
    assignments: Mapped[list["SubjectAssignment"]] = relationship(
        "SubjectAssignment",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "group_id",
            "name",
            name="uq_workspace_gid_name",
        ),
    )


class WorkspaceSubject(Base):
    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=False,
    )
    ecourses_id: Mapped[int] = mapped_column(
        nullable=True,
        unique=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
    )
    ecourses_link: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    professor: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )
    professor_contact: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )
    requirements: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )
    additional_fields: Mapped[dict] = mapped_column(
        JSONB,
        default={},
        server_default=func.text("{}"),
    )
    queue: Mapped[list[int]] = mapped_column(
        ARRAY(Integer),
        default=[],
        server_default=text("ARRAY[]::integer[]"),
    )

    workspace: Mapped["Workspace"] = relationship(
        "Workspace",
        back_populates="subjects",
    )
    submissions: Mapped[list["UserSubmission"]] = relationship(
        "UserSubmission",
        back_populates="subject",
        cascade="all, delete-orphan",
    )
    assignments: Mapped[list["SubjectAssignment"]] = relationship(
        "SubjectAssignment",
        cascade="all, delete-orphan",
    )
    

class SubjectAssignment(Base):
    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=False,
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("workspace_subjects.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    url: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "workspace_id",
            "subject_id",
            "name",
            name="uq_subj_assign_wid_sid_name",
        ),
    )


class UserSubmission(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"), nullable=False
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("workspace_subjects.id"),
        nullable=False,
    )
    submitted_works: Mapped[list[int]] = mapped_column(
        ARRAY(Integer),
        default=[],
        server_default=text("ARRAY[]::integer[]"),
    )
    total_required_works: Mapped[int] = mapped_column(
        default=0, server_default=text("0")
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="submissions",
    )
    workspace: Mapped["Workspace"] = relationship(
        "Workspace", back_populates="submissions"
    )
    subject: Mapped["WorkspaceSubject"] = relationship(
        "WorkspaceSubject",
        back_populates="submissions",
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "workspace_id",
            "subject_id",
            name="uq_user_submissons_uid_wid_sid",
        ),
    )
