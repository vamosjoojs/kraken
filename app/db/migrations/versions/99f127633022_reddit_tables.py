"""reddit tables

Revision ID: 99f127633022
Revises: af788221f67d
Create Date: 2022-08-17 17:29:22.577854

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '99f127633022'
down_revision = 'af788221f67d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reddit_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('reddit_handle', sa.String(), nullable=False),
    sa.Column('tag', sa.String(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reddit_send_message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('sended', sa.Boolean(), nullable=False),
    sa.Column('reddit_handle', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reddit_tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('client_id', sa.String(), nullable=False),
    sa.Column('client_secret', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('reddit_handle', sa.String(), nullable=False),
    sa.Column('activated', sa.Boolean(), nullable=False),
    sa.Column('reddit_messages_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['reddit_messages_id'], ['reddit_messages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reddit_tasks')
    op.drop_table('reddit_send_message')
    op.drop_table('reddit_messages')
    # ### end Alembic commands ###
