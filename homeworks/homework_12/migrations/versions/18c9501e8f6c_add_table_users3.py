"""add table users3

Revision ID: 18c9501e8f6c
Revises: 8d16da6f4b07
Create Date: 2024-05-23 11:06:42.767738

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18c9501e8f6c'
down_revision: Union[str, None] = '8d16da6f4b07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'Login',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.alter_column('users', 'Password',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.alter_column('users', 'Email',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=255),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'Email',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
    op.alter_column('users', 'Password',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
    op.alter_column('users', 'Login',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
    # ### end Alembic commands ###
