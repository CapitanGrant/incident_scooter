"""empty message

Revision ID: 5b7ff4935a5a
Revises:
Create Date: 2025-11-08 09:56:58.016591
"""
from typing import Sequence, Union
from sqlalchemy import text
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = '5b7ff4935a5a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    conn.execute(text("""
    DO $$ BEGIN
        CREATE TYPE incidentstatus AS ENUM ('NEW', 'IN_PROGRESS', 'RESOLVED', 'CLOSED', 'REJECTED');
    EXCEPTION WHEN duplicate_object THEN null; END $$;
    """))

    conn.execute(text("""
    DO $$ BEGIN
        CREATE TYPE incidentsource AS ENUM ('OPERATOR', 'MONITORING', 'PARTNER', 'SYSTEM');
    EXCEPTION WHEN duplicate_object THEN null; END $$;
    """))

    op.create_table(
        'incidents',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=False),
        sa.Column(
            'status',
            sa.Enum(
                'NEW', 'IN_PROGRESS', 'RESOLVED', 'CLOSED', 'REJECTED',
                name='incidentstatus',
                create_type=False
            ),
            nullable=False
        ),
        sa.Column(
            'source',
            sa.Enum(
                'OPERATOR', 'MONITORING', 'PARTNER', 'SYSTEM',
                name='incidentsource',
                create_type=False
            ),
            nullable=False
        ),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('incidents')
    op.execute(text("DROP TYPE IF EXISTS incidentstatus CASCADE;"))
    op.execute(text("DROP TYPE IF EXISTS incidentsource CASCADE;"))
