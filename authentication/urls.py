from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='user_logout'),
]


# admin pass:1234
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Login and logout
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Registration
    path("register/", views.register_view, name="register"),

    path("profile/", views.profile_edit_view, name="profile_edit"),

    # Password reset
    # path("password_reset/", auth_views.PasswordResetView.as_view(
    #     template_name="password_reset.html"
    # ), name="password_reset"),
    # path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(
    #     template_name="password_reset_done.html"
    # ), name="password_reset_done"),
    # path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
    #     template_name="password_reset_confirm.html"
    # ), name="password_reset_confirm"),
    # path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
    #     template_name="password_reset_complete.html"
    # ), name="password_reset_complete"),
]

# urlpatterns = [
#     path('login/', views.user_login, name='login'),
#     path('logout/', views.user_logout, name='user_logout'),
# ]
