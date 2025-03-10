"""empty message

Revision ID: 2a9efdd8906d
Revises: 
Create Date: 2025-02-15 15:15:07.778701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a9efdd8906d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('device_name', sa.String(length=256), nullable=True),
    sa.Column('device_type', sa.String(length=256), nullable=True),
    sa.Column('description', sa.String(length=4096), nullable=True),
    sa.Column('is_available', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('device')
    # ### end Alembic commands ###
