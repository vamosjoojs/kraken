"""modificando auto tasks

Revision ID: 2c876dd0a4f9
Revises: 1950285f49da
Create Date: 2022-03-25 16:38:05.122624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c876dd0a4f9'
down_revision = '1950285f49da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auto_tasks', sa.Column('post_type', sa.String(), nullable=False))
    op.add_column('auto_tasks', sa.Column('activated_at', sa.DateTime(), nullable=True))
    op.add_column('auto_tasks', sa.Column('deactivated_at', sa.DateTime(), nullable=True))
    op.add_column('auto_tasks', sa.Column('twitch_creator_name', sa.String(), nullable=False))
    op.drop_column('auto_tasks', 'post_instagram')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auto_tasks', sa.Column('post_instagram', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('auto_tasks', 'twitch_creator_name')
    op.drop_column('auto_tasks', 'deactivated_at')
    op.drop_column('auto_tasks', 'activated_at')
    op.drop_column('auto_tasks', 'post_type')
    # ### end Alembic commands ###
