from rest_framework import serializers

from .models import Concept, Descriptor, Qualifier, Term, TreeNumber


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
            'qualifiers',
            'concepts'
        )


class QualifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Qualifier
        fields = (
            'qualifier_ui',
            'qualifier_name'
        )


class ConceptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concept
        fields = (
            'concept_ui',
            'concept_name',
            'terms'
        )


class TermSerializer(serializers.ModelSerializer):

    class Meta:
        model = Term
        fields = (
            'term_ui',
            'string'
        )


class QualifierProviderSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='qualifier_ui')
    text = serializers.CharField(source='qualifier_name')

    class Meta:
        model = Descriptor
        fields = (
            'id',
            'text'
        )


class DescriptorProviderSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='descriptor_ui')
    text = serializers.CharField(source='label')

    class Meta:
        model = Descriptor
        fields = (
            'id',
            'text',
            'qualifiers'
        )
