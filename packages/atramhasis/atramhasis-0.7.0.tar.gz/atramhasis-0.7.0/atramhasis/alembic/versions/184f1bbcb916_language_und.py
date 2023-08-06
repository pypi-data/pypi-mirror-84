"""language_und

Revision ID: 184f1bbcb916
Revises: 6dfc3e2324aa
Create Date: 2017-07-25 16:38:39.439673

"""

# revision identifiers, used by Alembic.
revision = '184f1bbcb916'
down_revision = '6dfc3e2324aa'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy.orm import Session

language_table = table('language',
                       column('id', sa.String),
                       column('name', sa.String)
                       )


def upgrade():

    op.bulk_insert(language_table,
                   [
                       {'id': 'und', 'name': 'Undetermined'}
                   ]
    )


def downgrade():
    connection = op.get_bind()
    session = Session(bind=connection)
    connection.execute(
        language_table.delete().where(language_table.c.id == 'und')
    )
    session.flush()
