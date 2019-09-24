"""empty message

Revision ID: c1f9f4c34aef
Revises: b87f9c5096d3
Create Date: 2019-09-21 17:48:56.770509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1f9f4c34aef'
down_revision = 'b87f9c5096d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('price', sa.Column('id_ingrediente', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'price', 'ingrediente', ['id_ingrediente'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'price', type_='foreignkey')
    op.drop_column('price', 'id_ingrediente')
    # ### end Alembic commands ###
