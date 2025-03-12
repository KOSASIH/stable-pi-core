# scripts/run_migrations.py

import os
from alembic.config import Config
from alembic import command

# Set up the Alembic configuration
def run_migrations():
    alembic_cfg = Config("alembic.ini")  # Ensure you have an alembic.ini file in your project
    command.upgrade(alembic_cfg, "head")  # Upgrade to the latest migration
    print("Database migrations completed.")

if __name__ == "__main__":
    run_migrations()
