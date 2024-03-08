"""some_changes

Revision ID: 038ca19eec15
Revises: 5bac8a4513b3
Create Date: 2024-03-07 16:47:21.237927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '038ca19eec15'
down_revision = '5bac8a4513b3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_purchase_client_id_client', 'purchase', type_='foreignkey')
    op.create_foreign_key(op.f('fk_purchase_client_id_client'), 'purchase', 'client', ['client_id'], ['user_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_purchase_client_id_client'), 'purchase', type_='foreignkey')
    op.create_foreign_key('fk_purchase_client_id_client', 'purchase', 'client', ['client_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###