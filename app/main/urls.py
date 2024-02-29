from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from main.api import views

router = DefaultRouter()
router.register(r'ai_engines', views.AIEngineViewSet, basename='ai_engines')
router.register(r'ai_engines_versions', views.AIEngineVersionViewSet, basename='ai_engines_versions')
router.register(r'ai_models', views.AIModelViewSet, basename='ai_models')
router.register(r'evaluation_metrics', views.MetricViewSet, basename='evaluation_metrics')
router.register(r'generic_files', views.GenericFilesViewSet, basename='generic_files')

"""
For nested representations check:
1 - (https://www.django-rest-framework.org/api-guide/relations/#custom-hyperlinked-fields) If you require more complex hyperlinked representation you'll need to customize the field, as described in the custom hyperlinked fields section, below.
2 - drf-nested-resources package
"""

urlpatterns = [
    path(r'', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    # SPECTACULAR URLS
    path('api/schemas/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schemas/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schemas'), name='swagger-ui'),
    path('api/schemas/redoc/', SpectacularRedocView.as_view(url_name='schemas'), name='redoc')
]
