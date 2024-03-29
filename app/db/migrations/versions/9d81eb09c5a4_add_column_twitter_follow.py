"""add column twitter follow

Revision ID: 9d81eb09c5a4
Revises: 80fa53e869ed
Create Date: 2022-04-22 14:11:38.378690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d81eb09c5a4'
down_revision = '80fa53e869ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('twitter_follow', sa.Column('tag', sa.String(), nullable=False))
    op.add_column('twitter_follow', sa.Column('result_type', sa.String(), server_default='mixed', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('twitter_follow', 'result_type')
    op.drop_column('twitter_follow', 'tag')
    # ### end Alembic commands ###
