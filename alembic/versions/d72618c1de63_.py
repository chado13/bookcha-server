"""empty message

Revision ID: d72618c1de63
Revises: 
Create Date: 2025-04-12 16:59:36.055012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd72618c1de63'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('last_login', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('nickname', sa.String(length=12), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('photo', sa.String(length=200), nullable=False),
    sa.Column('intro', sa.Text(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('nickname')
    )
    op.create_table('record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('author', sa.String(length=50), nullable=False),
    sa.Column('evaluation', sa.Integer(), nullable=True),
    sa.Column('review', sa.String(length=100), nullable=True),
    sa.Column('commentary', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_recode_user_author_title', 'record', ['user_id', 'author', 'title'], unique=True)
    op.create_index('ix_record_id', 'record', ['id'], unique=False)
    op.create_index('ix_record_updated_at', 'record', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_record_updated_at', table_name='record')
    op.drop_index('ix_record_id', table_name='record')
    op.drop_index('ix_recode_user_author_title', table_name='record')
    op.drop_table('record')
    op.drop_table('user')
    # ### end Alembic commands ###
