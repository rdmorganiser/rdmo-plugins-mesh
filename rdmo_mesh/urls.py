from django.urls import include, path
from rest_framework import routers

from .viewsets import DescriptorViewSet, QualifierViewSet

app_name = 'v1-mesh'

router = routers.DefaultRouter()
router.register(r'descriptors', DescriptorViewSet, basename='descriptor')
router.register(r'qualifiers', QualifierViewSet, basename='qualifier')

urlpatterns = [
    path('', include(router.urls)),
]
