from django.contrib import admin
from django.urls import path, include
from pathlib import Path
from django.conf import settings
from django.conf.urls.static import static

assets_dir = Path(settings.BASE_DIR) / "ui" / "static" / "sneat" / "assets"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("ui.urls")),
    path("accounts/", include("authentication.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns += static("/assets/", document_root=assets_dir)
