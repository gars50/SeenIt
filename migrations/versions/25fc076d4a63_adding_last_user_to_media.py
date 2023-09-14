"""Adding last_user to media

Revision ID: 25fc076d4a63
Revises: 9ce2619c50cb
Create Date: 2023-08-02 23:22:13.219245

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '25fc076d4a63'
down_revision = '9ce2619c50cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('apscheduler_jobs', schema=None) as batch_op:
        batch_op.alter_column('next_run_time',
               existing_type=mysql.DOUBLE(asdecimal=True),
               type_=sa.Float(precision=25),
               existing_nullable=True)

    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['last_user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('last_user_id')

    with op.batch_alter_table('apscheduler_jobs', schema=None) as batch_op:
        batch_op.alter_column('next_run_time',
               existing_type=sa.Float(precision=25),
               type_=mysql.DOUBLE(asdecimal=True),
               existing_nullable=True)

    # ### end Alembic commands ###