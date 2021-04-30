import shutil
import urllib.request as request
import xml.etree.ElementTree as et
from contextlib import closing
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import tqdm

from ...models import Descriptor, Qualifier, TreeNumber


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            path = Path(settings.MESH_PATH)

            qualifier_url = settings.MESH_QUALIFIER_URL
            qualifier_path = path / qualifier_url.split('/')[-1]

            descriptor_url = settings.MESH_DESCRIPTOR_URL
            descriptor_path = path / descriptor_url.split('/')[-1]

        except AttributeError:
            raise CommandError('MESH_PATH, MESH_QUALIFIER_URL, MESH_DESCRIPTOR_URL are not set.')

        # check if the files are already there
        if not qualifier_path.exists():
            print('Downloading {}'.format(qualifier_url))
            self.download_xml(qualifier_url, qualifier_path)
        if not descriptor_path.exists():
            print('Downloading {}'.format(descriptor_url))
            self.download_xml(descriptor_url, descriptor_path)

        self.import_qualifiers(qualifier_path)
        self.import_descriptors(descriptor_path)

    def download_xml(self, url, path):
        # create mesh path
        path.parent.mkdir(parents=True, exist_ok=True)

        # download the file
        with closing(request.urlopen(url)) as response:
            with open(path, 'wb') as fp:
                shutil.copyfileobj(response, fp)

    def import_qualifiers(self, path):
        # remove all old qualifiers
        Qualifier.objects.all().delete()

        # parse qualifier xmlfile
        tree = et.parse(path)
        root = tree.getroot()

        # loop over qualifiers and create model instances
        print('Importing qualifiers ...')
        self.qualifiers = {}
        for node in tqdm.tqdm(root.findall('QualifierRecord')):
            qualifier = Qualifier.objects.create(
                qualifier_ui=node.find('QualifierUI').text,
                qualifier_name=node.find('QualifierName').find('String').text
            )

            self.qualifiers[qualifier.qualifier_ui] = qualifier

    def import_descriptors(self, path):
        # remove all old descriptors
        Descriptor.objects.all().delete()

        # parse descriptor xmlfile
        tree = et.parse(path)
        root = tree.getroot()

        # loop over descriptors and create model instances
        print('Importing descriptors ...')
        for node in tqdm.tqdm(root.findall('DescriptorRecord')):
            descriptor = Descriptor.objects.create(
                descriptor_ui=node.find('DescriptorUI').text,
                descriptor_name=node.find('DescriptorName').find('String').text,
                label=node.find('DescriptorName').find('String').text
            )

            # add tree numbers
            tree_number_list_node = node.find('TreeNumberList')
            if tree_number_list_node:
                tree_list = []
                for tree_number_node in tree_number_list_node.findall('TreeNumber'):
                    tree_number = TreeNumber(descriptor=descriptor, tree_number=tree_number_node.text)
                    tree_list.append(tree_number)
                if tree_list:
                    TreeNumber.objects.bulk_create(tree_list)

                # update label
                descriptor.label += ' [%s]' % ', '.join([tree_number.tree_number for tree_number in tree_list])
                descriptor.save()

            # add qualifiers
            allowable_qualifiers_list_node = node.find('AllowableQualifiersList')
            if allowable_qualifiers_list_node:
                qualifiers = []
                for allowable_qualifiers_node in allowable_qualifiers_list_node.findall('AllowableQualifier'):
                    qualifier_ui = allowable_qualifiers_node.find('QualifierReferredTo').find('QualifierUI').text
                    qualifiers.append(self.qualifiers[qualifier_ui])
                if qualifiers:
                    descriptor.qualifiers.set(qualifiers)

        # loop over descriptors in the database and add parents
        print('Finding parents ...')
        for descriptor in tqdm.tqdm(Descriptor.objects.prefetch_related('tree_list')):
            parents = []
            for tree_number in descriptor.tree_list.all():
                parent_tree_number = '.'.join(tree_number.tree_number.split('.')[:-1])
                if parent_tree_number:
                    parent = Descriptor.objects.get(tree_list__tree_number=parent_tree_number)
                    parents.append(parent)
            if parents:
                descriptor.parents.set(parents)
