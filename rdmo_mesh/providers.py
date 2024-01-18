from django.contrib.postgres.search import SearchQuery, SearchRank

from rdmo.options.providers import Provider

from .models import Descriptor, Qualifier
from .serializers import DescriptorProviderSerializer, QualifierProviderSerializer


class DescriptorProvider(Provider):

    search = True

    def get_options(self, project, search):
        if search:
            search_query = SearchQuery(search)
            search_rank = SearchRank('search_vector', search_query)

            queryset = Descriptor.objects.filter(
                search_vector=search_query
            ).annotate(
                search_rank=search_rank
            ).order_by('-search_rank').prefetch_related('qualifiers').distinct()[:10]

            serializer = DescriptorProviderSerializer(queryset, many=True)
            return serializer.data
        else:
            return []


class QualifierProvider(Provider):

    def get_options(self, project, search):
        queryset = Qualifier.objects.all()
        serializer = QualifierProviderSerializer(queryset, many=True)
        return serializer.data
