"""Change skin schema

Revision ID: eb566f6756eb
Revises: a4bfbcc9e6e2
Create Date: 2025-04-18 15:44:47.308846

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'eb566f6756eb'
down_revision = 'a4bfbcc9e6e2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task_skin_items', sa.Column('score', sa.JSON(), nullable=False))
    op.drop_column('task_skin_items', 'recommendations')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task_skin_items', sa.Column('recommendations', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False))
    op.drop_column('task_skin_items', 'score')
    # ### end Alembic commands ###

