"""added content column to post table

Revision ID: cc2461277cbc
Revises: 1b0bd7a647ba
Create Date: 2022-03-18 15:31:05.591041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc2461277cbc'
down_revision = '1b0bd7a647ba'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
