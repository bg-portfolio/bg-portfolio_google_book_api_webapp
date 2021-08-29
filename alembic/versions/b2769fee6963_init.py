"""init

Revision ID: b2769fee6963
Revises: 
Create Date: 2021-08-29 17:23:25.029187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2769fee6963'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'books',
        sa.Column('isbn_13', sa.Integer, primary_key=True),
        sa.Column('title', sa.String),
        sa.Column('publish_date', sa.String),
        sa.Column('author', sa.String),
        sa.Column('page_count', sa.Integer),
        sa.Column('thumbnail_url', sa.String),
        sa.Column('language', sa.String)
    )


def downgrade():
    op.drop_table('books')
