"""create job application table and update email templates table

Revision ID: 7231aadcf4e4
Revises: 854472eb449d
Create Date: 2024-08-05 23:36:45.552152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '7231aadcf4e4'
down_revision: Union[str, None] = '854472eb449d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_applications',
    sa.Column('job_id', sa.String(), nullable=False),
    sa.Column('applicant_name', sa.String(), nullable=False),
    sa.Column('applicant_email', sa.String(), nullable=False),
    sa.Column('cover_letter', sa.Text(), nullable=True),
    sa.Column('resume_link', sa.String(), nullable=False),
    sa.Column('portfolio_link', sa.String(), nullable=True),
    sa.Column('application_status', sa.Enum('pending', 'accepted', 'rejected', name='application_status'), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_applications_id'), 'job_applications', ['id'], unique=False)

    # Create the ENUM type
    template_status_enum = postgresql.ENUM('online', 'offline', name='template_status')
    template_status_enum.create(op.get_bind())
    op.add_column('email_templates', sa.Column('type', sa.String(), nullable=False))
    op.add_column('email_templates', sa.Column('template_status', sa.Enum('online', 'offline', name='template_status'), server_default='online', nullable=True))
    op.drop_column('email_templates', 'status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('email_templates', sa.Column('status', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=True))
    op.drop_column('email_templates', 'template_status')
    op.drop_column('email_templates', 'type')
    op.drop_index(op.f('ix_job_applications_id'), table_name='job_applications')
    op.drop_table('job_applications')

    # Drop the ENUM type
    template_status_enum = postgresql.ENUM('online', 'offline', name='template_status')
    template_status_enum.drop(op.get_bind())
    # ### end Alembic commands ###
