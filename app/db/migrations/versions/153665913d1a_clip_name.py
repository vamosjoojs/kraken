"""clip name

Revision ID: 153665913d1a
Revises: 3a6470d307fc
Create Date: 2022-03-25 13:28:22.997463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '153665913d1a'
down_revision = '3a6470d307fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('twitch_clips', sa.Column('clip_name', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('twitch_clips', 'clip_name')
    # ### end Alembic commands ###
