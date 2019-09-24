"""empty message

Revision ID: 8fab36ae3f8c
Revises: 5bf021b25530
Create Date: 2019-09-21 16:22:50.654147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fab36ae3f8c'
down_revision = '5bf021b25530'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'ingrediente', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ingrediente', type_='unique')
    # ### end Alembic commands ###
