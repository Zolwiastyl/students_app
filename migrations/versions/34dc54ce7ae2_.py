"""empty message

Revision ID: 34dc54ce7ae2
Revises: c883f3f16485
Create Date: 2022-04-25 14:07:13.401043

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '34dc54ce7ae2'
down_revision = 'c883f3f16485'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student_subject_aggregate', sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False))
    op.create_index(op.f('ix_student_subject_aggregate_id'), 'student_subject_aggregate', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_student_subject_aggregate_id'), table_name='student_subject_aggregate')
    op.drop_column('student_subject_aggregate', 'id')
    # ### end Alembic commands ###
