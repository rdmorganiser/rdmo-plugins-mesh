from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Descriptor, Qualifier
from .serializers import DescriptorSerializer, QualifierSerializer


class DescriptorViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Descriptor.objects.prefetch_related('tree_list', 'parents', 'children')
    serializer_class = DescriptorSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = (
        'descriptor_name',
    )
    filterset_fields = (
        'tree_list__tree_number',
        'parents__tree_list__tree_number',
        'children__tree_list__tree_number'
    )


class QualifierViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Qualifier.objects.all()
    serializer_class = QualifierSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = (
        'qualifier_name',
    )
    filterset_fields = (
        'descriptors__descriptor_ui',
        'descriptors__tree_list__tree_number'
    )
