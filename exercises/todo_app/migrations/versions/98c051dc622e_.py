"""empty message

Revision ID: 98c051dc622e
Revises: 3966764ac5bd
Create Date: 2020-08-22 00:43:38.627362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98c051dc622e'
down_revision = '3966764ac5bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todolist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('todo', sa.Column('todolist_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'todo', 'todolist', ['todolist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todo', type_='foreignkey')
    op.drop_column('todo', 'todolist_id')
    op.drop_table('todolist')
    # ### end Alembic commands ###
