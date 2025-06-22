from django.urls import path
from .views import PredictionAPIView, CalculateTHIAPIView

urlpatterns = [
    path('predict/', PredictionAPIView.as_view(), name='predict-api'),
from .views import CalculateTHIAPIView
# from .views import PredictionAPIView

urlpatterns = [
    # path('predict/', PredictionAPIView.as_view(), name='predict-api'),
    path('calculate_thi/', CalculateTHIAPIView.as_view(), name='calculate-thi-api'),
]
