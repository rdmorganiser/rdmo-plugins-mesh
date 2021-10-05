from django.db import models

from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex


class Descriptor(models.Model):

    descriptor_ui = models.CharField(max_length=16, primary_key=True)
    descriptor_name = models.CharField(max_length=256)
    parents = models.ManyToManyField('self', symmetrical=False, related_name='children')
    qualifiers = models.ManyToManyField('Qualifier', related_name='descriptors')
    concepts = models.ManyToManyField('Concept', related_name='descriptors')
    label = models.TextField(max_length=128)
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = (GinIndex(fields=['search_vector']),)


class Qualifier(models.Model):

    qualifier_ui = models.CharField(max_length=16, primary_key=True)
    qualifier_name = models.CharField(max_length=128)


class Concept(models.Model):

    concept_ui = models.CharField(max_length=16, primary_key=True)
    concept_name = models.CharField(max_length=256)
    terms = models.ManyToManyField('Term', related_name='concepts')


class Term(models.Model):

    term_ui = models.CharField(max_length=16, primary_key=True)
    string = models.CharField(max_length=256)


class TreeNumber(models.Model):

    tree_number = models.CharField(max_length=64, primary_key=True)
    descriptor = models.ForeignKey(Descriptor, on_delete=models.CASCADE, related_name='tree_list')
