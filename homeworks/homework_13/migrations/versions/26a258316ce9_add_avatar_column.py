"""add avatar column

Revision ID: 26a258316ce9
Revises: 23466e4eeac6
Create Date: 2024-05-31 18:28:15.151604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26a258316ce9'
down_revision: Union[str, None] = '23466e4eeac6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('Avatar', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'Avatar')
    # ### end Alembic commands ###
