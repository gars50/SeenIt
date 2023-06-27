"""Added expirty date to media

Revision ID: 38d6142eee64
Revises: 739141de548b
Create Date: 2023-06-27 12:15:45.635248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38d6142eee64'
down_revision = '739141de548b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.add_column(sa.Column('expiryDate', sa.DateTime(), nullable=True))

    with op.batch_alter_table('tv_show', schema=None) as batch_op:
        batch_op.add_column(sa.Column('expiryDate', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tv_show', schema=None) as batch_op:
        batch_op.drop_column('expiryDate')

    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.drop_column('expiryDate')

    # ### end Alembic commands ###
