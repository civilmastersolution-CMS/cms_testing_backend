#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🔧 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📦 Collecting static files..."
python manage.py collectstatic --no-input

echo "📁 Creating media directories..."
mkdir -p media/articles/pdfs
chmod -R 755 media

echo "🗄️ Running migrations..."
python manage.py migrate

echo "👤 Creating superuser (if environment variables are set)..."
python manage.py create_superuser

echo "✅ Build completed successfully!"
