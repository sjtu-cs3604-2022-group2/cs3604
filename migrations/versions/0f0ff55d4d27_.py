"""empty message

Revision ID: 0f0ff55d4d27
Revises: 258c15c0ac60
Create Date: 2022-11-26 22:52:06.601984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f0ff55d4d27'
down_revision = '258c15c0ac60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notification',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_timestamp'), 'notification', ['timestamp'], unique=False)
    op.add_column('photo', sa.Column('photo_path', sa.String(length=1000), nullable=True))
    op.add_column('photo', sa.Column('post_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'photo', 'post', ['post_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'photo', type_='foreignkey')
    op.drop_column('photo', 'post_id')
    op.drop_column('photo', 'photo_path')
    op.drop_index(op.f('ix_notification_timestamp'), table_name='notification')
    op.drop_table('notification')
    # ### end Alembic commands ###
