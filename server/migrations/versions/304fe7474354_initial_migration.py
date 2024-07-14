"""Initial migration.

Revision ID: 304fe7474354
Revises: 
Create Date: 2024-07-14 21:02:34.895011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '304fe7474354'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('novels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile', sa.String(length=200), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('genre', sa.String(), nullable=False),
    sa.Column('author', sa.String(), nullable=False),
    sa.Column('publication_year', sa.Integer(), nullable=True),
    sa.Column('synopsis', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('profile', sa.String(length=200), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('novel_collections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('novel_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['novel_id'], ['novels.id'], name=op.f('fk_novel_collections_novel_id_novels')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_novel_collections_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('novel_collections')
    op.drop_table('users')
    op.drop_table('novels')
    # ### end Alembic commands ###