"""add is_featured and highlight to projects

Revision ID: 550677042fe6
Revises: 693fc81383de
Create Date: 2026-07-29 20:42:05.888717

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '550677042fe6'
down_revision: str | Sequence[str] | None = '693fc81383de'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "projects",
        sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    with op.batch_alter_table("projects") as batch_op:
        batch_op.alter_column("is_featured", server_default=None)
    op.add_column(
        "projects",
        sa.Column("highlight", sa.String(length=200), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("projects", "highlight")
    op.drop_column("projects", "is_featured")
