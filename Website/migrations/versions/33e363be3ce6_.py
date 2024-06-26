"""empty message

Revision ID: 33e363be3ce6
Revises: 6e79b430868b
Create Date: 2024-05-17 14:04:18.921476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33e363be3ce6'
down_revision = '6e79b430868b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_offer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('acceptedStatus', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_offer', schema=None) as batch_op:
        batch_op.drop_column('acceptedStatus')

    # ### end Alembic commands ###
