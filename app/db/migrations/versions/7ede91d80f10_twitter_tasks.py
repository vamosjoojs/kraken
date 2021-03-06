"""twitter-tasks

Revision ID: 7ede91d80f10
Revises: 91f0ef7be2cf
Create Date: 2022-04-02 17:12:07.372313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ede91d80f10'
down_revision = '91f0ef7be2cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('twitter_tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('oauth_token', sa.String(), nullable=False),
    sa.Column('oauth_secret', sa.String(), nullable=False),
    sa.Column('consumer_key', sa.String(), nullable=False),
    sa.Column('consumer_secret', sa.String(), nullable=False),
    sa.Column('tag', sa.String(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('twitter_handle', sa.String(), nullable=False),
    sa.Column('activated', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('twitter_tasks')
    # ### end Alembic commands ###
