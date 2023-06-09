"""choices table

Revision ID: 0942ca5fc7af
Revises: 6fb10dcd9990
Create Date: 2023-03-17 23:14:30.407187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0942ca5fc7af'
down_revision = '6fb10dcd9990'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('choice', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test', sa.String(length=128), nullable=True))
        batch_op.create_index(batch_op.f('ix_choice_test'), ['test'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('choice', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_choice_test'))
        batch_op.drop_column('test')

    # ### end Alembic commands ###
