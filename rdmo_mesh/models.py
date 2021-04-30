from django.db import models


class Descriptor(models.Model):

    descriptor_ui = models.CharField(max_length=16, primary_key=True)
    descriptor_name = models.CharField(max_length=128)
    parents = models.ManyToManyField('self', symmetrical=False, related_name='children')
    qualifiers = models.ManyToManyField('Qualifier', related_name='descriptors')
    label = models.TextField(max_length=128)


class Qualifier(models.Model):

    qualifier_ui = models.CharField(max_length=16, primary_key=True)
    qualifier_name = models.CharField(max_length=128)


class TreeNumber(models.Model):

    tree_number = models.CharField(max_length=64, primary_key=True)
    descriptor = models.ForeignKey(Descriptor, on_delete=models.CASCADE, related_name='tree_list')
