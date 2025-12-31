"""crear usuario inicial

Revision ID: 8c26cc45ab4d
Revises: f4a85daa9f6a
Create Date: 2025-12-30 19:06:43.797114

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8c26cc45ab4d'
down_revision: str = 'f4a85daa9f6a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Hash bcrypt para "admin123"
    hashed_password = "$2b$12$rQUxHudgzjsO3Vz2HjczVOeSWYcrg31j03A.8ic0oFbO4IUSnwQ2e"
    
    # Insertar usuario inicial
    op.execute(
        sa.text(
            "INSERT INTO users (email, hashed_password, is_active, created_at) "
            "VALUES (:email, :hashed_password, :is_active, NOW())"
        ).bindparams(
            email="admin@example.com",
            hashed_password=hashed_password,
            is_active=True
        )
    )


def downgrade() -> None:
    # Eliminar usuario inicial
    op.execute(
        sa.text("DELETE FROM users WHERE email = 'admin@example.com'")
    )