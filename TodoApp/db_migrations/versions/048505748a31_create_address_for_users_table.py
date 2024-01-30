"""Create address for users table

Revision ID: 048505748a31
Revises: 720699f84474
Create Date: 2024-01-20 19:03:39.211083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '048505748a31'
down_revision: Union[str, None] = '720699f84474'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address', sa.VARCHAR(length=80), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'address')
