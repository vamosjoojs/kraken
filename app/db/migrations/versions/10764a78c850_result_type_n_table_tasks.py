"""result type n table tasks

Revision ID: 10764a78c850
Revises: f43deb4c9a79
Create Date: 2022-04-17 15:58:18.924752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10764a78c850'
down_revision = 'f43deb4c9a79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('twitter_tasks', sa.Column('result_type', sa.String(), server_default='mixed', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('twitter_tasks', 'result_type')
    # ### end Alembic commands ###
