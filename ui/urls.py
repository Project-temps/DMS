from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("survey/", views.survey, name="survey"),
    path("communication/", views.communication, name="communication"),
    path("contact/", views.contact, name="contact"),
]


# from django.urls import path
# from . import views

# from django.urls import path, re_path
# from django.views.generic import TemplateView
# from django.template.loader import get_template
# from django.http import Http404

# class SneatDemoView(TemplateView):
#     def get_template_names(self):
#         page = self.kwargs.get("page", "index.html")
#         if ".." in page or page.startswith("/"):
#             raise Http404
#         try:
#             get_template(page)        # وجود فایل
#         except:
#             raise Http404
#         return [page]

# urlpatterns = [
#     path("", SneatDemoView.as_view(), name="sneat_index"),
#     # ⬇️ regex سالم: - را یا اول/آخر بگذار یا با backslash فرار بده
#     re_path(
#         r"^(?P<page>[\w\.\-/]+\.html)$",
#         views.SneatTemplateView.as_view(),
#         name="sneat_page",
#     ),
# ]


# urlpatterns = [
#     path("", views.home, name="home"),
#     path("survey/", views.survey, name="survey"),
#     path("communication/", views.communication, name="communication"),
#     path("contact/", views.contact, name="contact"),

#     path("dashboard/", views.dashboard, name="dashboard"),
#     path("api/getChartData/", views.get_chart_data, name="get_chart_data"),
#     path("api/get_thi_data/", views.get_thi_data, name="get_thi_data"),
# ]


# urlpatterns = [
#     path('', views.index, name='index'),
#     path('about/', views.about, name='about'),
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('contact/', views.contact, name='contact'),
#     path('survey/', views.survey, name='survey'),
#     path('communication/', views.communication, name='communication'),
#     path('api/getChartData', views.get_chart_data, name='get_chart_data'),
#     path('api/get_thi_data/', views.get_thi_data, name='get_thi_data'),
    

# ]
