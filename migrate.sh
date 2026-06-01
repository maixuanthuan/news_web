#!/bin/bash
# Chạy 1 lần từ thư mục gốc news_web/ để migrate structure cũ → mới
# Usage: bash migrate.sh

set -e

echo "📁 Tạo thư mục mới..."
mkdir -p frontend/css frontend/js backend/api

echo "🚚 Di chuyển frontend..."
mv backend/app/static/index.html   frontend/index.html
mv backend/app/static/css/style.css frontend/css/style.css
mv backend/app/static/js/config.js  frontend/js/config.js
mv backend/app/static/js/data.js    frontend/js/data.js
mv backend/app/static/js/renderer.js frontend/js/renderer.js
mv backend/app/static/js/app.js     frontend/js/app.js

echo "🚚 Di chuyển backend..."
mv backend/app/api/routes.py         backend/api/routes.py
mv backend/app/api/rss_fetcher.py    backend/api/rss_fetcher.py
mv backend/app/api/scraper_vnexpress.py backend/api/scraper_vnexpress.py
mv backend/app/main.py               backend/main.py
touch backend/api/__init__.py

echo "🧹 Xóa thư mục app/ cũ..."
rm -rf backend/app

echo "✅ Done! Chạy server: ./run.sh"
