"""initial version

Revision ID: d612fa9439ea
Revises:
Create Date: 2025-10-29 22:01:21.609735

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "d612fa9439ea"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
