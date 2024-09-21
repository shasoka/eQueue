#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.models.entities import SubjectAssignment, UserSubmission
from core.schemas.subject_assignments import (
    SubjectAssignmentCreate,
    SubjectAssignmentUpdate,
)
from core.schemas.subjects import WorkspaceSubjectRead
from core.schemas.user_submissions import UserSubmissionUpdate
from crud.workspaces import (
    get_workspace_subjects_casted,
    get_workspace_subject_ids_and_names,
    get_workspace_with_assignees,
)
from moodle.courses import get_subject_assignments


# noinspection PyTypeChecker
async def get_assignment_by_id(
    session: AsyncSession,
    assignment_id: int,
) -> SubjectAssignment | None:
    stmt = select(SubjectAssignment).where(SubjectAssignment.id == assignment_id)
    result = await session.scalars(stmt)
    return result.first()


# noinspection PyTypeChecker
async def get_assignment_by_constraint(
    session: AsyncSession,
    workspace_id: int,
    subject_id: int,
    name: str,
) -> SubjectAssignment | None:
    stmt = (
        select(SubjectAssignment)
        .where(SubjectAssignment.workspace_id == workspace_id)
        .where(SubjectAssignment.subject_id == subject_id)
        .where(SubjectAssignment.name == name)
    )
    result = await session.scalars(stmt)
    return result.first()


# noinspection PyTypeChecker
async def get_assignments_ids_by_constraint(
    session: AsyncSession,
    workspace_id: int,
    subject_id: int,
) -> list[int] | None:
    stmt = (
        select(SubjectAssignment.id)
        .where(SubjectAssignment.workspace_id == workspace_id)
        .where(SubjectAssignment.subject_id == subject_id)
    )
    result = await session.scalars(stmt)
    ids = result.all()
    return ids if ids else None


async def generate_subject_assignment(
    session: AsyncSession,
    user: User,
    subject_in: WorkspaceSubjectRead,
) -> list[SubjectAssignment] | None:
    if subject_in.workspace_id == user.assigned_workspace_id:
        if existing_subjects := await get_workspace_subjects_casted(
            session=session,
            workspace_id=subject_in.workspace_id,
        ):
            if (
                WorkspaceSubjectRead.model_validate(subject_in.model_dump())
                in existing_subjects
            ):
                result = []
                available_assignments = await get_subject_assignments(
                    token=user.access_token,
                    subject_in=subject_in,
                )
                for assignment in available_assignments:
                    result.append(
                        await add_assignment(
                            session=session,
                            user=user,
                            assignment_in=assignment,
                            commit=False,
                        )
                    )
                await session.commit()
                return result
            else:
                raise HTTPException(
                    status_code=403,
                    detail=f"Предмета id={subject_in.ecourses_id} нет в пространстве {subject_in.workspace_id}",
                )
        else:
            raise HTTPException(
                status_code=403,
                detail=f"В пространстве {subject_in.workspace_id} нет ни одного предмета",
            )
    else:
        raise HTTPException(
            status_code=403,
            detail=f"Вы не можете добавлять предметы в рабочее пространство {subject_in.workspace_id}",
        )


async def add_assignment(
    session: AsyncSession,
    user: User,
    assignment_in: SubjectAssignmentCreate,
    commit: bool = True,
) -> SubjectAssignment | None:
    if user.assigned_workspace_id == assignment_in.workspace_id:
        _, ids = await get_workspace_subject_ids_and_names(
            session, user.assigned_workspace_id, ecourse_id=False
        )
        if assignment_in.subject_id in ids:
            assignment = await get_assignment_by_constraint(
                session=session,
                workspace_id=assignment_in.workspace_id,
                subject_id=assignment_in.subject_id,
                name=assignment_in.name,
            )
            if assignment is None:
                assignment = SubjectAssignment(**assignment_in.model_dump())
                session.add(assignment)
                await session.flush()
                await update_submission_total_works(
                    session=session,
                    group_id=user.assigned_group_id,
                    subject_id=assignment.subject_id,
                )
                if commit:
                    await session.commit()
                    await session.refresh(assignment)
                return assignment
            else:
                raise HTTPException(
                    status_code=409,
                    detail=f"Задание {assignment_in.name} уже добавлено в рабочее пространство",
                )
        else:
            raise HTTPException(
                status_code=403,
                detail=f"Предмета id={assignment_in.subject_id} нет в пространстве {assignment_in.workspace_id}",
            )
    else:
        raise HTTPException(
            status_code=403,
            detail=f"Вы не можете добавлять задания в рабочее пространство {assignment_in.workspace_id}",
        )


async def partial_update_assignment(
    session: AsyncSession,
    assignment_in: SubjectAssignmentUpdate,
    user: User,
) -> SubjectAssignment | None:
    if user.workspace_chief:
        if assignment := await get_assignment_by_id(
            session=session,
            assignment_id=assignment_in.id,
        ):
            if assignment.workspace_id == user.assigned_workspace_id:
                assignment_in = assignment_in.model_dump(exclude_unset=True)
                for key, value in assignment_in.items():
                    setattr(assignment, key, value)
                try:
                    await session.commit()
                    await session.refresh(assignment)
                    return assignment
                except IntegrityError:
                    raise HTTPException(
                        status_code=409,
                        detail=f"Задание {assignment_in["name"]} уже есть в рабочем пространстве",
                    )
            else:
                raise HTTPException(
                    status_code=403,
                    detail="Вы не можете редактировать задание в другом рабочем пространстве",
                )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Задание с id={assignment_in.id} не найдено",
            )
    else:
        raise HTTPException(
            status_code=403,
            detail="Вы не являетесь администратором рабочего пространства",
        )


async def delete_workspace_subject_assignment(
    session: AsyncSession,
    user: User,
    assignment_id: int,
) -> SubjectAssignment:
    if user.workspace_chief:
        if assignment := await get_assignment_by_id(
            session=session,
            assignment_id=assignment_id,
        ):
            if assignment.workspace_id == user.assigned_workspace_id:
                await update_submission_total_works(
                    session=session,
                    group_id=user.assigned_group_id,
                    subject_id=assignment.subject_id,
                    increment=-1,
                )
                await clear_submitted_works_on_assign_delete(
                    session=session,
                    subject_id=assignment.subject_id,
                    group_id=user.assigned_group_id,
                    assignment_id=assignment_id,
                )
                await session.delete(assignment)
                await session.commit()
                return assignment
            else:
                raise HTTPException(
                    status_code=403,
                    detail="Вы не можете удалять задание в другом рабочем пространстве",
                )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Задание с id={assignment_id} не найдено",
            )
    else:
        raise HTTPException(
            status_code=403,
            detail="Вы не являетесь администратором рабочего пространства",
        )


# noinspection PyTypeChecker
async def get_all_user_submissions(
    session: AsyncSession,
    user: User,
) -> list[UserSubmission]:
    stmt = (
        select(UserSubmission)
        .where(UserSubmission.user_id == user.id)
        .where(UserSubmission.workspace_id == user.assigned_workspace_id)
    )
    result = await session.scalars(stmt)
    return result.all()


# noinspection PyTypeChecker
async def get_submission(
    session: AsyncSession,
    user_id: int,
    workspace_id: int,
    subject_id: int,
) -> UserSubmission | None:
    stmt = (
        select(UserSubmission)
        .where(UserSubmission.user_id == user_id)
        .where(UserSubmission.workspace_id == workspace_id)
        .where(UserSubmission.subject_id == subject_id)
    )
    result = await session.scalars(stmt)
    return result.first()


async def add_submission(
    session: AsyncSession,
    subject_id: int,
    group_id: int,
) -> None:
    workspace = await get_workspace_with_assignees(
        session=session,
        group_id=group_id,
    )
    for assignee in workspace.users:
        new_submission = UserSubmission(
            user_id=assignee.id,
            workspace_id=assignee.assigned_workspace_id,
            subject_id=subject_id,
        )
        try:
            session.add(new_submission)
            # No commit because session will be commited in function which calls this function
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Нарушено ограничение уникальносьти. Такой submission уже добавлен",
            )


async def clear_submitted_works_on_assign_delete(
    session: AsyncSession,
    subject_id: int,
    group_id: int,
    assignment_id: int,
) -> None:
    workspace = await get_workspace_with_assignees(
        session=session,
        group_id=group_id,
    )
    for assignee in workspace.users:
        if submission := await get_submission(
            session=session,
            user_id=assignee.id,
            workspace_id=assignee.assigned_workspace_id,
            subject_id=subject_id,
        ):
            submission.submitted_works = func.array_remove(
                submission.submitted_works,
                assignment_id,
            )
            await session.flush()
            # No commit because session will be commited in function which calls this function
        else:
            raise HTTPException(
                status_code=404,
                detail="Предмета нет в рабочем пространстве",
            )


# noinspection PyTypeChecker
async def update_submission_total_works(
    session: AsyncSession,
    subject_id: int,
    group_id: int,
    increment: int = 1,
) -> None:
    workspace = await get_workspace_with_assignees(
        session=session,
        group_id=group_id,
    )
    for assignee in workspace.users:
        if submission := await get_submission(
            session=session,
            user_id=assignee.id,
            workspace_id=assignee.assigned_workspace_id,
            subject_id=subject_id,
        ):
            submission.total_required_works += increment
            await session.flush()
            # No commit because session will be commited in function which calls this function
        else:
            raise HTTPException(
                status_code=404,
                detail="Предмета нет в рабочем пространстве",
            )


# noinspection PyTypeChecker
async def update_submission_submitted_works(
    session: AsyncSession,
    user: User,
    submission_in: UserSubmissionUpdate,
) -> UserSubmission | None:
    if user.id == submission_in.user_id:
        if user.assigned_workspace_id == submission_in.workspace_id:
            _, ids = await get_workspace_subject_ids_and_names(
                session,
                user.assigned_workspace_id,
                ecourse_id=False,
            )
            if submission_in.subject_id in ids:
                if (
                    submission_in.assignment_id
                    in await get_assignments_ids_by_constraint(
                        session=session,
                        workspace_id=submission_in.workspace_id,
                        subject_id=submission_in.subject_id,
                    )
                ):
                    submission = await get_submission(
                        session=session,
                        user_id=submission_in.user_id,
                        workspace_id=submission_in.workspace_id,
                        subject_id=submission_in.subject_id,
                    )
                    if submission_in.assignment_id not in submission.submitted_works:
                        submission.submitted_works = func.array_append(
                            submission.submitted_works,
                            submission_in.assignment_id,
                        )
                    else:
                        submission.submitted_works = func.array_remove(
                            submission.submitted_works,
                            submission_in.assignment_id,
                        )
                    await session.commit()
                    await session.refresh(submission)
                    return submission
                else:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Задания id={submission_in.assignment_id} нет в"
                        f" предмете id={submission_in.subject_id}",
                    )
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Предмета id={submission_in.subject_id} нет в"
                    f" рабочем пространстве id={submission_in.workspace_id}",
                )
        else:
            raise HTTPException(
                status_code=403,
                detail=f"Пользователь id={submission_in.user_id} прикреплен к другому рабочему пространству",
            )
    else:
        raise HTTPException(
            status_code=403,
            detail="Вы не можете изменять чужие решения",
        )
