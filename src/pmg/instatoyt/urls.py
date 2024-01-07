# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReelViewSet

# router = DefaultRouter()
# router.register(r'reel', ReelViewSet, basename='reel')

urlpatterns = [
    path('reel/', ReelViewSet.as_view({'get': 'list', 'post': 'create'}), name='reel-list'),
]
