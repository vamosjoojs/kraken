"""back populates

Revision ID: 3a6470d307fc
Revises: a9e7e8f4007b
Create Date: 2022-03-25 11:35:56.839926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a6470d307fc'
down_revision = 'a9e7e8f4007b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('twitch_clips', 'clip_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('twitch_clips', 'clip_url',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('twitch_clips', 'clip_url',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('twitch_clips', 'clip_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###