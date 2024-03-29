"""youtube-clips

Revision ID: 5c5ea4396771
Revises: 3647b012ac78
Create Date: 2022-05-17 11:33:19.344563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c5ea4396771'
down_revision = '3647b012ac78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('youtube_clips',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('clip_name', sa.String(), nullable=False),
    sa.Column('clip_id', sa.String(), nullable=False),
    sa.Column('clip_url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('kraken', sa.Column('youtube_clips_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'kraken', 'youtube_clips', ['youtube_clips_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'kraken', type_='foreignkey')
    op.drop_column('kraken', 'youtube_clips_id')
    op.drop_table('youtube_clips')
    # ### end Alembic commands ###
