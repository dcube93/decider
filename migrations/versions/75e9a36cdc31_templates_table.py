"""templates table

Revision ID: 75e9a36cdc31
Revises: 776b241dc03d
Create Date: 2023-03-18 15:47:44.855242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75e9a36cdc31'
down_revision = '776b241dc03d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('choice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=128), nullable=True),
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['template_id'], ['template.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('choice', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_choice_value'), ['value'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('choice', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_choice_value'))

    op.drop_table('choice')
    # ### end Alembic commands ###
