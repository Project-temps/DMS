<<<<<<< HEAD
=======
# authentication/apps.py
>>>>>>> origin/New_ui
from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
<<<<<<< HEAD
=======

    def ready(self):
        # لازم است سیگنال‌ها بارگذاری شوند
        import authentication.models  # این خط برای فراخوانی سیگنال‌ها کافی‌ست
>>>>>>> origin/New_ui
