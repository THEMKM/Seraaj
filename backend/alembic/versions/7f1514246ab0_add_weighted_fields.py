"""add weighted fields

Revision ID: 7f1514246ab0
Revises: d49c28597230
Create Date: 2025-07-10 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision = '7f1514246ab0'
down_revision = 'd49c28597230'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('volunteerprofile', sa.Column('skill_proficiency', sa.JSON(), nullable=True))
    op.add_column('volunteerprofile', sa.Column('desired_skills', sa.JSON(), nullable=True))
    op.add_column('volunteerprofile', sa.Column('location_lat', sa.Float(), nullable=True))
    op.add_column('volunteerprofile', sa.Column('location_lng', sa.Float(), nullable=True))
    op.add_column('opportunity', sa.Column('skills_weighted', sa.JSON(), nullable=True))
    op.add_column('opportunity', sa.Column('categories_weighted', sa.JSON(), nullable=True))
    op.add_column('opportunity', sa.Column('availability_required', sa.JSON(), nullable=True))

def downgrade() -> None:
    op.drop_column('opportunity', 'availability_required')
    op.drop_column('opportunity', 'categories_weighted')
    op.drop_column('opportunity', 'skills_weighted')
    op.drop_column('volunteerprofile', 'location_lng')
    op.drop_column('volunteerprofile', 'location_lat')
    op.drop_column('volunteerprofile', 'desired_skills')
    op.drop_column('volunteerprofile', 'skill_proficiency')
