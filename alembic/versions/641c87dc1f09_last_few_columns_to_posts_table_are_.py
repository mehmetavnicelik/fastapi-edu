"""last few columns to posts table are added.

Revision ID: 641c87dc1f09
Revises: 8cbd9b09f5e8
Create Date: 2022-03-18 16:02:07.476106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '641c87dc1f09'
down_revision = '8cbd9b09f5e8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
