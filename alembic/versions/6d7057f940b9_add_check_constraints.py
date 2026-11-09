"""Add check constraints

Revision ID: 6d7057f940b9
Revises: 6224551b5e7d
Create Date: 2026-11-09 23:36:57.268272

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '6d7057f940b9'
down_revision = '6224551b5e7d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('charityproject') as batch_op:
        batch_op.create_check_constraint(
            'positive_full_amount', 'full_amount > 0',
        )
        batch_op.create_check_constraint(
            'invested_le_full', 'invested_amount <= full_amount',
        )
    with op.batch_alter_table('donation') as batch_op:
        batch_op.create_check_constraint(
            'positive_full_amount', 'full_amount > 0',
        )
        batch_op.create_check_constraint(
            'invested_le_full', 'invested_amount <= full_amount',
        )


def downgrade():
    with op.batch_alter_table('charityproject') as batch_op:
        batch_op.drop_constraint('positive_full_amount', type_='check')
        batch_op.drop_constraint('invested_le_full', type_='check')

    with op.batch_alter_table('donation') as batch_op:
        batch_op.drop_constraint('positive_full_amount', type_='check')
        batch_op.drop_constraint('invested_le_full', type_='check')
