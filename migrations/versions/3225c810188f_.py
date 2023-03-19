"""empty message

Revision ID: 3225c810188f
Revises: 924b425819ac
Create Date: 2023-03-19 14:55:55.773205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3225c810188f'
down_revision = '924b425819ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('registration', schema=None) as batch_op:
        batch_op.alter_column('course_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('registration', schema=None) as batch_op:
        batch_op.alter_column('course_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False)

    # ### end Alembic commands ###