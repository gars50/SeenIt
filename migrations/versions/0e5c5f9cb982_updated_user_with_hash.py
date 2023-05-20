"""updated user with hash

Revision ID: 0e5c5f9cb982
Revises: 4ba86f70aa80
Create Date: 2023-05-20 15:46:19.801401

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0e5c5f9cb982'
down_revision = '4ba86f70aa80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('password_hash',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=128),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.String(length=120),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###
