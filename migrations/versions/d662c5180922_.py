"""empty message

Revision ID: d662c5180922
Revises: 1fc4cf756b2b
Create Date: 2020-04-28 11:07:58.813820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd662c5180922'
down_revision = '1fc4cf756b2b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'booking', ['studio_id', 'start_time'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'booking', type_='unique')
    # ### end Alembic commands ###
