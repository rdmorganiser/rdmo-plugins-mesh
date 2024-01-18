from django.urls import include, path

from rest_framework import routers

from .viewsets import ConceptViewSet, DescriptorViewSet, QualifierViewSet, TermViewSet

app_name = 'v1-mesh'

router = routers.DefaultRouter()
router.register(r'descriptors', DescriptorViewSet, basename='descriptor')
router.register(r'qualifiers', QualifierViewSet, basename='qualifier')
router.register(r'concepts', ConceptViewSet, basename='concept')
router.register(r'terms', TermViewSet, basename='term')

urlpatterns = [
    path('', include(router.urls)),
]
