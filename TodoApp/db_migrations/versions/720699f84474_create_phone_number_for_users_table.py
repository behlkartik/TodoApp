"""Create phone number for users table

Revision ID: 720699f84474
Revises: 
Create Date: 2024-01-20 18:54:30.127872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '720699f84474'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.VARCHAR(length=10), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
