"""Change phone_number type to number users table

Revision ID: 5a5d2b5548d1
Revises: 048505748a31
Create Date: 2024-01-20 19:32:33.601949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a5d2b5548d1'
down_revision: Union[str, None] = '048505748a31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'phone_number', type_=sa.NUMERIC(10), nullable=True)


def downgrade() -> None:
    op.alter_column('users', 'phone_number', type_=sa.VARCHAR(40), nullable=True)
