"""create_core_content_desk_tables

Revision ID: 854bf5b5a6f5
Revises: 
Create Date: 2026-08-13 23:35:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '854bf5b5a6f5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Flairs table
    op.create_table(
        'flairs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True),
        sa.Column('color', sa.String(length=20), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_flairs_name'), 'flairs', ['name'], unique=True)

    # 2. Tags table
    op.create_table(
        'tags',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True),
        sa.Column('color', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_tags_name'), 'tags', ['name'], unique=True)

    # 3. Experiences table
    op.create_table(
        'experiences',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('takeaway', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('flair_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('flairs.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 4. Ideas table
    op.create_table(
        'ideas',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('raw_thought', sa.Text(), nullable=False),
        sa.Column('development_notes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='RAW'),
        sa.Column('why_prompt', sa.Text(), nullable=True),
        sa.Column('what_happened_prompt', sa.Text(), nullable=True),
        sa.Column('actual_point_prompt', sa.Text(), nullable=True),
        sa.Column('flair_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('flairs.id', ondelete='SET NULL'), nullable=True),
        sa.Column('experience_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('experiences.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_ideas_status'), 'ideas', ['status'], unique=False)

    # 5. Content table
    op.create_table(
        'content',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('body_script', sa.Text(), nullable=True),
        sa.Column('platform', sa.String(length=50), nullable=False),
        sa.Column('content_type', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='DRAFT'),
        sa.Column('parent_idea_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('ideas.id', ondelete='SET NULL'), nullable=True),
        sa.Column('flair_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('flairs.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_content_platform'), 'content', ['platform'], unique=False)
    op.create_index(op.f('ix_content_content_type'), 'content', ['content_type'], unique=False)
    op.create_index(op.f('ix_content_status'), 'content', ['status'], unique=False)

    # 6. Checklist Items table
    op.create_table(
        'checklist_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('is_completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('position', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('content_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('content.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 7. Content Relationships table
    op.create_table(
        'content_relationships',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('source_content_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('content.id', ondelete='CASCADE'), nullable=False),
        sa.Column('target_content_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('content.id', ondelete='CASCADE'), nullable=False),
        sa.Column('relationship_type', sa.String(length=50), nullable=False, server_default='REPURPOSED_FROM'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 8. Association Tables
    op.create_table(
        'idea_tags',
        sa.Column('idea_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('ideas.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('tag_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    )
    op.create_table(
        'content_tags',
        sa.Column('content_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('content.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('tag_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    )
    op.create_table(
        'experience_tags',
        sa.Column('experience_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('experiences.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('tag_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    )


def downgrade() -> None:
    op.drop_table('experience_tags')
    op.drop_table('content_tags')
    op.drop_table('idea_tags')
    op.drop_table('content_relationships')
    op.drop_table('checklist_items')
    op.drop_table('content')
    op.drop_table('ideas')
    op.drop_table('experiences')
    op.drop_table('tags')
    op.drop_table('flairs')
