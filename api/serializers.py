"""serializers"""
from rest_framework import serializers

from handbook.models import Handbook, HandbookElement


class HandbookSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор для модели Справочник."""
    class Meta:
        model = Handbook
        fields = ['identifier', 'title', 'short_title', 'description',
                  'version', 'begin_date']


class HandbookElementSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор для модели Элемент справочника."""
    class Meta:
        model = HandbookElement
        fields = ['id', 'handbook', 'parent_identifier', 'code', 'value']
