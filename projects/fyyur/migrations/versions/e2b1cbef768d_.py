"""empty message

Revision ID: e2b1cbef768d
Revises: af443cfa1733
Create Date: 2020-08-25 21:54:39.457803

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e2b1cbef768d'
down_revision = 'af443cfa1733'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('show', 'date', new_column_name='start_time')
    # op.drop_column('show', 'date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('show', 'start_time')
    # ### end Alembic commands ###