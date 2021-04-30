from django.db.models import F, Q

from rdmo.options.providers import Provider

from .models import Descriptor


class MeSHProvider(Provider):

    search = True

    def get_options(self, project, search):
        if search:
            queryset = Descriptor.objects.filter(Q(descriptor_name__icontains=search) |
                                                 Q(tree_list__tree_number__icontains=search))
            return queryset.annotate(id=F('descriptor_ui'), text=F('label')) \
                           .values('id', 'text').distinct()[:10]
        else:
            return []
