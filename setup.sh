#!/bin/bash

echo "Installing dependencies..."

alembic upgrade head
python database/seed.py

echo "Setup completed"