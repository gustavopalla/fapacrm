from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadViewSet, InteractionViewSet, TaskViewSet, ProjectViewSet, AnalyticsViewSet

router = DefaultRouter()
router.register(r'leads', LeadViewSet)
router.register(r'interactions', InteractionViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'analytics', AnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
]
