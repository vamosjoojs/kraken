"""modificando tabela tasks

Revision ID: 6e9f6707d408
Revises: 4eb01181679c
Create Date: 2022-04-20 13:26:18.937874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e9f6707d408'
down_revision = '4eb01181679c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('twitter_tasks', 'result_type')
    op.drop_column('twitter_tasks', 'message')
    op.drop_column('twitter_tasks', 'tag')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('twitter_tasks', sa.Column('tag', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('twitter_tasks', sa.Column('message', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('twitter_tasks', sa.Column('result_type', sa.VARCHAR(), server_default=sa.text("'mixed'::character varying"), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
