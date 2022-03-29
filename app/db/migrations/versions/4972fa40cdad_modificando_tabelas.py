"""modificando tabelas

Revision ID: 4972fa40cdad
Revises: cef2e1c0ca81
Create Date: 2022-03-25 09:41:39.642127

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4972fa40cdad'
down_revision = 'cef2e1c0ca81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('kraken',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('post_status', sa.String(), nullable=False),
    sa.Column('kraken_hand', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('twitch')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('twitch',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('clip_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('post_status', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('kraken_hand', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='twitch_pkey')
    )
    op.drop_table('kraken')
    # ### end Alembic commands ###