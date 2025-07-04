from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ui.urls')),  # Route for the main UI
    path('auth/', include('authentication.urls')),
    # path('dashboard/', include('ui.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('api/', include('api.urls')),
]
