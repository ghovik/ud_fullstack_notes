"""empty message

Revision ID: 0d7ed65de5bb
Revises: efa4446b5caa
Create Date: 2020-08-24 23:06:54.321082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d7ed65de5bb'
down_revision = 'efa4446b5caa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('artist_id', sa.Integer(), nullable=False))
    op.add_column('show', sa.Column('venue_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'show', 'artist', ['artist_id'], ['id'])
    op.create_foreign_key(None, 'show', 'venue', ['venue_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'show', type_='foreignkey')
    op.drop_constraint(None, 'show', type_='foreignkey')
    op.drop_column('show', 'venue_id')
    op.drop_column('show', 'artist_id')
    # ### end Alembic commands ###