"""Init

Revision ID: e5e4ba6857f3
Revises: 80e73083be69
Create Date: 2023-11-17 01:16:46.305194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5e4ba6857f3'
down_revision: Union[str, None] = '80e73083be69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photos', sa.Column('description', sa.String(), nullable=True))
    op.create_index(op.f('ix_photos_description'), 'photos', ['description'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_photos_description'), table_name='photos')
    op.drop_column('photos', 'description')
    # ### end Alembic commands ###
