"""added_status_on_product

Revision ID: e213b32d41c1
Revises: 5a8d9bdada1e
Create Date: 2024-02-29 17:29:15.979590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e213b32d41c1'
down_revision = '5a8d9bdada1e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('status', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'status')
    # ### end Alembic commands ###