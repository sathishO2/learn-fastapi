"""add reviews table

Revision ID: 1dcfa3fc4a1b
Revises: c44ad3988c8d
Create Date: 2024-12-25 19:52:02.715496

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1dcfa3fc4a1b'
down_revision: Union[str, None] = 'c44ad3988c8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
