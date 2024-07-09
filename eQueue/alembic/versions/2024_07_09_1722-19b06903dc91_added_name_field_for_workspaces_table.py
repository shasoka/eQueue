"""Added name field for workspaces table

Revision ID: 19b06903dc91
Revises: 17c4f3f56d9b
Create Date: 2024-07-09 17:22:26.874028

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "19b06903dc91"
down_revision: Union[str, None] = "17c4f3f56d9b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def trigger_up() -> None:
    op.execute("""
        CREATE OR REPLACE FUNCTION set_default_name()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.name IS NULL THEN
                NEW.name := 'Рабочее пространство #' || NEW.id;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """)

    op.execute("""
        CREATE TRIGGER set_default_name_trigger
        BEFORE INSERT ON workspaces
        FOR EACH ROW
        EXECUTE FUNCTION set_default_name();
        """)


def trigger_down() -> None:
    op.execute("DROP TRIGGER IF EXISTS set_default_name_trigger ON workspaces")
    op.execute("DROP FUNCTION IF EXISTS set_default_name")


def upgrade() -> None:
    op.add_column(
        "workspaces", sa.Column("name", sa.String(length=35), nullable=True)
    )
    op.create_unique_constraint(
        op.f("uq_workspaces_name"), "workspaces", ["name"]
    )
    trigger_up()


def downgrade() -> None:
    trigger_down()
    op.drop_constraint(
        op.f("uq_workspaces_name"), "workspaces", type_="unique"
    )
    op.drop_column("workspaces", "name")
