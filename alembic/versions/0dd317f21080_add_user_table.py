"""add user table

Revision ID: 0dd317f21080
Revises: cc2461277cbc
Create Date: 2022-03-18 15:36:12.250076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0dd317f21080'
down_revision = 'cc2461277cbc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')                    
                    )
    pass

def downgrade():
    op.drop_table('users')
    pass
