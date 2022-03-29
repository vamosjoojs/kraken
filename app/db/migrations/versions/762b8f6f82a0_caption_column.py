"""caption column

Revision ID: 762b8f6f82a0
Revises: 153665913d1a
Create Date: 2022-03-25 13:30:51.701964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '762b8f6f82a0'
down_revision = '153665913d1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('kraken', sa.Column('caption', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('kraken', 'caption')
    # ### end Alembic commands ###