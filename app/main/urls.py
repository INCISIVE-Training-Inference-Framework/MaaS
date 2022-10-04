from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.api import views


router = DefaultRouter()
router.register(r'ai_engines', views.AIEngineViewSet, basename='ai_engines')
router.register(r'models', views.ModelViewSet, basename='models')
router.register(r'metrics', views.MetricViewSet, basename='metrics')
router.register(r'inference_results', views.InferenceResultsViewSet, basename='inference_results')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
