from django.db.models import Q

from rdmo.options.providers import Provider

from .models import Descriptor, Qualifier
from .serializers import (DescriptorProviderSerializer,
                          QualifierProviderSerializer)


class DescriptorProvider(Provider):

    search = True

    def get_options(self, project, search):
        if search:
            print(search)
            queryset = Descriptor.objects.filter(Q(label__icontains=search) |
                                                 Q(tree_list__tree_number__icontains=search)) \
                                         .prefetch_related('qualifiers').distinct()[:10]

            serializer = DescriptorProviderSerializer(queryset, many=True)
            return serializer.data
        else:
            return []


class QualifierProvider(Provider):

    def get_options(self, project, search):
        queryset = Qualifier.objects.all()
        serializer = QualifierProviderSerializer(queryset, many=True)
        return serializer.data
