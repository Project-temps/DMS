# ---------- check_sneat.py ----------
import os, json
from pathlib import Path
from django.conf import settings
import django

#  راه اندازی مختصر Django برای دسترسی به تنظیمات
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

BASE = Path(settings.BASE_DIR)

# ---- 1. مسیرهای تنظیم شده در TEMPLATES و STATICFILES_DIRS
print("TEMPLATE DIRS:", *settings.TEMPLATES[0]["DIRS"], sep="\n  • ")
print("\nSTATICFILES_DIRS:", *settings.STATICFILES_DIRS, sep="\n  • ")

# ---- 2. بررسی چند فایل مهم HTML
html_root = BASE / "ui" / "templates" / "sneat_html"
must_have = [
    "index.html",
    "auth-login-basic.html",
    "pages-account-settings-account.html",
    "layouts-without-menu.html",
]
missing = [f for f in must_have if not (html_root / f).exists()]
print("\nMissing HTML files:", json.dumps(missing, indent=2))

# ---- 3. بررسی چند فایل استاتیک مهم
assets_root = BASE / "ui" / "static" / "assets"
static_files = [
    "vendor/css/core.css",
    "vendor/js/menu.js",
    "img/avatars/1.png",
]
missing_static = [f for f in static_files if not (assets_root / f).exists()]
print("\nMissing asset files:", json.dumps(missing_static, indent=2))
