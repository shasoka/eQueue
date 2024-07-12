"""Changed submitted_works filed of user_submissions type from int to list[int]

Revision ID: 49ac040b713e
Revises: 9e625c3ea7cc
Create Date: 2024-07-12 14:39:43.697816

"""

#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "49ac040b713e"
down_revision: Union[str, None] = "9e625c3ea7cc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# noinspection SqlResolve
def upgrade() -> None:
    # Шаг 1: Добавить временный столбец
    op.add_column(
        "user_submissions",
        sa.Column("submitted_works_temp", sa.ARRAY(sa.Integer), server_default="{}"),
    )

    # Шаг 2: Скопировать данные из старого столбца в новый
    op.execute(
        "UPDATE user_submissions SET submitted_works_temp = ARRAY[submitted_works]"
    )

    # Шаг 3: Удалить старый столбец
    op.drop_column("user_submissions", "submitted_works")

    # Шаг 4: Переименовать новый столбец в старое имя
    op.alter_column(
        "user_submissions", "submitted_works_temp", new_column_name="submitted_works"
    )


# noinspection SqlResolve
def downgrade() -> None:
    # Шаг 1: Добавить временный столбец
    op.add_column(
        "user_submissions",
        sa.Column("submitted_works_temp", sa.Integer, server_default="0"),
    )

    # Шаг 2: Скопировать данные из нового столбца в старый
    op.execute(
        "UPDATE user_submissions SET submitted_works_temp = COALESCE(submitted_works[1], 0)"
    )

    # Шаг 3: Удалить новый столбец
    op.drop_column("user_submissions", "submitted_works")

    # Шаг 4: Переименовать временный столбец в старое имя
    op.alter_column(
        "user_submissions", "submitted_works_temp", new_column_name="submitted_works"
    )
