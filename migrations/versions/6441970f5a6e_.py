"""empty message

Revision ID: 6441970f5a6e
Revises: 90e07de81390
Create Date: 2022-12-06 00:20:43.673838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6441970f5a6e'
down_revision = '90e07de81390'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('valid', sa.Integer(), nullable=True))
    op.add_column('post', sa.Column('valid', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'valid')
    op.drop_column('comment', 'valid')
    # ### end Alembic commands ###