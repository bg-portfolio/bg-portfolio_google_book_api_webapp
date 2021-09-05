"""init

Revision ID: 53611afb4c60
Revises:
Create Date: 2021-09-05 23:44:03.784183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53611afb4c60'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'books',
        sa.Column("isbn_13", sa.BigInteger, primary_key=True),
        sa.Column("title", sa.String),
        sa.Column("publish_date", sa.String),
        sa.Column("author", sa.ARRAY(sa.String)),
        sa.Column("page_count", sa.Integer),
        sa.Column("thumbnail_url", sa.String),
        sa.Column("language", sa.String)
    )


def downgrade():
    op.drop_table('books')
