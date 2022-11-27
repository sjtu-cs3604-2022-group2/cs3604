"""empty message

Revision ID: 3332f7bdffa0
Revises: bab425f18e03
Create Date: 2022-11-27 21:24:25.284201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3332f7bdffa0'
down_revision = 'bab425f18e03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notifation', sa.Column('action_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'notifation', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'notifation', 'post', ['post_id'], ['id'])
    op.create_foreign_key(None, 'photo', 'post', ['post_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'photo', type_='foreignkey')
    op.drop_constraint(None, 'notifation', type_='foreignkey')
    op.drop_constraint(None, 'notifation', type_='foreignkey')
    op.drop_column('notifation', 'action_id')
    # ### end Alembic commands ###
