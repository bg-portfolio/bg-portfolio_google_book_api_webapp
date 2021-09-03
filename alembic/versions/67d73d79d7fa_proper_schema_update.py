"""proper schema update

Revision ID: 67d73d79d7fa
Revises: b2769fee6963
Create Date: 2021-08-31 20:19:20.742856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67d73d79d7fa'
down_revision = 'b2769fee6963'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('books')
    op.create_table(
        'books',
        sa.Column('isbn_13', sa.Integer, primary_key=True),
        sa.Column('title', sa.String),
        sa.Column('publish_date', sa.String),
        sa.Column('author', sa.ARRAY(sa.String)),
        sa.Column('page_count', sa.Integer),
        sa.Column('thumbnail_url', sa.String),
        sa.Column('language', sa.String)
    )


def downgrade():
    op.drop_table('books')
