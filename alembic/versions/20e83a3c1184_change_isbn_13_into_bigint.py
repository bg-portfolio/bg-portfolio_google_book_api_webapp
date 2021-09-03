"""change isbn_13 into bigint

Revision ID: 20e83a3c1184
Revises: 67d73d79d7fa
Create Date: 2021-09-03 14:22:53.734881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20e83a3c1184'
down_revision = '67d73d79d7fa'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('books')
    op.create_table(
        'books',
        sa.Column('isbn_13', sa.BigInteger, primary_key=True),
        sa.Column('title', sa.String),
        sa.Column('publish_date', sa.String),
        sa.Column('author', sa.ARRAY(sa.String)),
        sa.Column('page_count', sa.Integer),
        sa.Column('thumbnail_url', sa.String),
        sa.Column('language', sa.String)
    )


def downgrade():
    op.drop_table('books')
