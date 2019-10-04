"""empty message

Revision ID: 016ce336e883
Revises: 
Create Date: 2019-09-25 00:53:34.327398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '016ce336e883'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ingrediente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('category', sa.Enum('meet', 'grane', 'vedgetable', 'dary', 'fruit', 'nut', name='category'), nullable=False),
    sa.Column('calory', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('calory', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('price',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('market_name', sa.Enum('publix', 'walmart', 'president', 'whole_foods', name='market'), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('id_ingrediente', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_ingrediente'], ['ingrediente.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('peso', sa.Integer(), nullable=False),
    sa.Column('talla', sa.Integer(), nullable=False),
    sa.Column('alergia', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('receta_id', sa.Integer(), nullable=False),
    sa.Column('ingrediente_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ingrediente_id'], ['ingrediente.id'], ),
    sa.ForeignKeyConstraint(['receta_id'], ['receta.id'], ),
    sa.PrimaryKeyConstraint('receta_id', 'ingrediente_id')
    )
    op.create_table('stock',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_profile', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['id_profile'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stock')
    op.drop_table('tags')
    op.drop_table('profile')
    op.drop_table('price')
    op.drop_table('user')
    op.drop_table('receta')
    op.drop_table('ingrediente')
    # ### end Alembic commands ###