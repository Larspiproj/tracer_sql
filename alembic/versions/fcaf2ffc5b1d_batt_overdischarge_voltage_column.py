"""batt_overdischarge_voltage column

Revision ID: fcaf2ffc5b1d
Revises: 0fb2fa08e804
Create Date: 2018-03-27 21:31:56.084873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcaf2ffc5b1d'
down_revision = '0fb2fa08e804'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('parameters', sa.Column('batt_overdischarge_voltage', sa.Float))


def downgrade():
    op.drop_column('parameters', 'batt_overdischarge_voltage')
