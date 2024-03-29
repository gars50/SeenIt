"""Removing pick method

Revision ID: b6cfbc29dcb2
Revises: d6bd5d900e35
Create Date: 2023-11-16 16:12:37.184127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6cfbc29dcb2'
down_revision = 'd6bd5d900e35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pick', schema=None) as batch_op:
        batch_op.drop_column('pick_method')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pick', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pick_method', sa.VARCHAR(length=100), nullable=True))

    # ### end Alembic commands ###
