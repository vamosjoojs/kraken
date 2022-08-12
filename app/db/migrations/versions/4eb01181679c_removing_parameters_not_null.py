"""removing parameters not null

Revision ID: 4eb01181679c
Revises: 10764a78c850
Create Date: 2022-04-19 16:01:39.463882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4eb01181679c'
down_revision = '10764a78c850'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parameters', 'value',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('parameters', 'bool_value',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('parameters', 'int_value',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parameters', 'int_value',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('parameters', 'bool_value',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('parameters', 'value',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
