"""Added system user possibility

Revision ID: 9ce2619c50cb
Revises: 466efa028ac9
Create Date: 2023-08-02 17:32:40.308057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ce2619c50cb'
down_revision = '466efa028ac9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('system_user', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('system_user')

    # ### end Alembic commands ###