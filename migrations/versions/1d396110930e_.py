"""empty message

Revision ID: 1d396110930e
Revises: dec3c51d8ba1
Create Date: 2019-09-20 04:40:01.369932

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1d396110930e'
down_revision = 'dec3c51d8ba1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('price',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('market_name', sa.Enum('publix', 'walmart', 'president', 'whole_foods', name='market'), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('id_ingrediente', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_ingrediente'], ['ingrediente.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receta_ingrediente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_receta', sa.Integer(), nullable=True),
    sa.Column('id_ingrediente', sa.Integer(), nullable=True),
    sa.Column('autor', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('messurment', sa.Enum('mililiter', 'miligram', 'ounce', name='messurments'), nullable=False),
    sa.ForeignKeyConstraint(['autor'], ['profile.id'], ),
    sa.ForeignKeyConstraint(['id_ingrediente'], ['ingrediente.id'], ),
    sa.ForeignKeyConstraint(['id_receta'], ['receta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stock',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_profile', sa.Integer(), nullable=True),
    sa.Column('id_ingrediente', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['id_ingrediente'], ['ingrediente.id'], ),
    sa.ForeignKeyConstraint(['id_profile'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('association')
    op.add_column('ingrediente', sa.Column('calory', sa.Integer(), nullable=False))
    op.add_column('ingrediente', sa.Column('category', sa.Enum('meet', 'grane', 'vedgetable', 'dary', 'fruit', 'nut', name='category'), nullable=False))
    op.drop_column('ingrediente', 'tipo')
    op.drop_column('ingrediente', 'caloria')
    op.drop_column('profile', 'stock')
    op.add_column('receta', sa.Column('calory', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'receta', ['name'])
    op.drop_column('receta', 'caloria')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('receta', sa.Column('caloria', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'receta', type_='unique')
    op.drop_column('receta', 'calory')
    op.add_column('profile', sa.Column('stock', mysql.VARCHAR(length=200), nullable=False))
    op.add_column('ingrediente', sa.Column('caloria', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('ingrediente', sa.Column('tipo', mysql.VARCHAR(length=80), nullable=False))
    op.drop_column('ingrediente', 'category')
    op.drop_column('ingrediente', 'calory')
    op.create_table('association',
    sa.Column('receta_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('ingrediente_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('ing_qty', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['ingrediente_id'], ['ingrediente.id'], name='association_ibfk_1'),
    sa.ForeignKeyConstraint(['receta_id'], ['receta.id'], name='association_ibfk_2'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.drop_table('stock')
    op.drop_table('receta_ingrediente')
    op.drop_table('price')
    # ### end Alembic commands ###
