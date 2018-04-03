"""batt_full_voltage column

Revision ID: 0fb2fa08e804
Revises: 
Create Date: 2018-03-27 20:17:56.943044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fb2fa08e804'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('parameters', sa.Column('batt_full_voltage', sa.Float))

def downgrade():
    op.drop_column('parameters', 'batt_full_voltage')
