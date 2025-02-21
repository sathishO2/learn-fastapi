"""published_date format changed str to date

Revision ID: 5b8470385b43
Revises: 281b278a178a
Create Date: 2024-12-25 15:48:44.607417

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b8470385b43'
down_revision: Union[str, None] = '281b278a178a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'books',
        'published_date',
        existing_type=sa.String(),
        type_=sa.Date(),
        postgresql_using="published_date::date"
    )
    op.create_unique_constraint(None, 'users', ['uid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.alter_column('books', 'published_date',
               existing_type=sa.Date(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    # ### end Alembic commands ###
