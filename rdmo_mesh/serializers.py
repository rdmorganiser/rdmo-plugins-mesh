from rest_framework import serializers

from .models import Descriptor, Qualifier, TreeNumber


class TreeNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = TreeNumber
        fields = (
            'tree_number',
        )


class DescriptorSerializer(serializers.ModelSerializer):

    tree_list = TreeNumberSerializer(many=True)

    class Meta:
        model = Descriptor
        fields = (
            'descriptor_ui',
            'descriptor_name',
            'tree_list',
            'parents',
            'children',
            'qualifiers'
        )


class QualifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Qualifier
        fields = (
            'qualifier_ui',
            'qualifier_name'
        )
