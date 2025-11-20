#!/bin/bash
set -e

echo "🚀 Starting Kenyan Smart Grid Backend..."

# Navigate to backend folder (needed if root is repo root)
cd "$(dirname "$0")"

# Setup virtual environment if missing
if [ ! -d "venv" ]; then
  echo "📦 Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip and install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Launch FastAPI app
echo "▶️ Launching FastAPI app..."
exec uvicorn app:app --host 0.0.0.0 --port 8000 --reload
