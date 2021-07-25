from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Concept, Descriptor, Qualifier, Term
from .serializers import (ConceptSerializer, DescriptorSerializer,
                          QualifierSerializer, TermSerializer)


class Pagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'


class DescriptorViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )
    pagination_class = Pagination
    queryset = Descriptor.objects.order_by('descriptor_ui').prefetch_related(
        'tree_list', 'parents', 'children', 'qualifiers', 'concepts'
    )
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
    pagination_class = Pagination
    queryset = Qualifier.objects.order_by('qualifier_ui')
    serializer_class = QualifierSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = (
        'qualifier_name',
    )
    filterset_fields = (
        'descriptors__descriptor_ui',
        'descriptors__tree_list__tree_number'
    )


class ConceptViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )
    pagination_class = Pagination
    queryset = Concept.objects.order_by('concept_ui').prefetch_related('terms')
    serializer_class = ConceptSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = (
        'concept_name',
    )
    filterset_fields = (
        'descriptors__descriptor_ui',
        'descriptors__tree_list__tree_number'
    )


class TermViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )
    pagination_class = Pagination
    queryset = Term.objects.all()
    serializer_class = TermSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = (
        'string',
    )
    filterset_fields = (
        'concepts__concept_ui',
        'concepts__concept_name',
        'concepts__descriptors__descriptor_ui',
        'concepts__descriptors__tree_list__tree_number'
    )
