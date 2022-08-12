"""kraken schedule

Revision ID: af788221f67d
Revises: 514b47e5132c
Create Date: 2022-06-23 13:26:43.503915

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'af788221f67d'
down_revision = '514b47e5132c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('kraken', sa.Column('schedule', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('kraken', 'schedule')
    # ### end Alembic commands ###
