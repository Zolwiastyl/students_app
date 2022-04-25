"""empty message

Revision ID: 79386f03e582
Revises: 34dc54ce7ae2
Create Date: 2022-04-25 14:12:01.522547

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '79386f03e582'
down_revision = '34dc54ce7ae2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student_subject_aggregate', sa.Column('student_id', postgresql.UUID(as_uuid=True), nullable=False))
    op.create_foreign_key(None, 'student_subject_aggregate', 'student', ['student_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'student_subject_aggregate', type_='foreignkey')
    op.drop_column('student_subject_aggregate', 'student_id')
    # ### end Alembic commands ###
