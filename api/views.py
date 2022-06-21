"""views"""
import uuid

from rest_framework import viewsets

# Create your views here.
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError, ValidationError, NotFound
from rest_framework.response import Response
from datetime import date
import datetime

from handbook.models import Handbook
from handbook.models import HandbookElement
from api.serializers import HandbookSerializer
from api.serializers import HandbookElementSerializer


class HandbookViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Справочник.

    По дефолту позволяет получить список всех справочников (всех версий).
    example:
    > http://localhost:8000/handbooks/
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "begin_date": "2022-06-15",
                "description": "Справочних о собаках",
                "identifier": "5c25bdda-ef0d-11ec-8ea0-0242ac120002",
                "short_title": "Собаки",
                "title": "Собачьи собаки",
                "version": "1"
            },
            {
                "begin_date": "2022-06-08",
                "description": "Справочник о кошках",
                "identifier": "00000000-0000-0000-0000-000000000001",
                "short_title": "Кошки",
                "title": "Кошки и коты",
                "version": "1"
            },
            ...
        ]
    }

    """
    queryset = Handbook.objects.all()
    serializer_class = HandbookSerializer

    @action(detail=False)
    def up_to_date(self, request):
        """
        Метод, возвращающий список справочников, актуальных на
        текущую дату.

        Справочники, дата начала действия которых ещё не наступила, не
        являются актуальными на текущую дату.

        example:
        > http://localhost:8000/handbooks/up_to_date/?date=2022-06-18
        [
            {
                "identifier": "00000000-0000-0000-0000-000000000001",
                "title": "Кошки и коты",
                "short_title": "Кошки",
                "description": "Справочник о кошках",
                "version": "1",
                "begin_date": "2022-06-08"
            },
            {
                "identifier": "5c25bdda-ef0d-11ec-8ea0-0242ac120002",
                "title": "asd",
                "short_title": "asd",
                "description": "asd",
                "version": "2",
                "begin_date": "2022-06-16"
            },
            ...
        ]
        """
        if not request.query_params.get('date'):
            raise ParseError('date param is required')
        try:
            date_param = datetime.datetime.strptime(
                request.query_params.get('date'), "%Y-%m-%d"
            ).date()
        except ValueError:
            raise ValidationError(
                'date has an invalid date format. It must be in YYYY-MM-DD '
                'format.'
            )
        query = Handbook.objects.filter(
            begin_date__lte=date_param
        ).distinct(
            'identifier'
        ).order_by(
            'identifier',
            '-begin_date'
        )

        serializer = self.get_serializer(query, many=True)
        return Response(serializer.data)


class HandbookElementViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Элемент справочника.
    """
    queryset = HandbookElement.objects.all()
    serializer_class = HandbookElementSerializer

    @action(detail=False)
    def get_by_handbook(self, request, *args, **kwargs):
        """
        Метод, возвращающий список элементов актуальной версии
        справочника по глобальному идентификатору справочника.

        example:
        > http://localhost:8000/elements/get_by_handbook/?handbook_identifier=00000000-0000-0000-0000-000000000001
        [

            {
                "id": 4,
                "handbook": "http://localhost:8000/handbooks/1/",
                "parent_identifier": "00000000-0000-0000-0000-000000000001",
                "code": "5997",
                "value": "Манул"
            },
            {
                "id": 1,
                "handbook": "http://localhost:8000/handbooks/1/",
                "parent_identifier": "00000000-0000-0000-0000-000000000001",
                "code": "8XZAFFV",
                "value": "Тигр"
            },
            ...
        ]
        """
        self.validate_handbook_identifier(request)
        identifier_param = uuid.UUID(
            request.query_params.get('handbook_identifier')
        )

        handbook = Handbook.objects.filter(
            identifier=identifier_param,
            begin_date__lte=date.today()
        ).order_by('-begin_date').first()
        query = handbook.elements

        serializer = self.get_serializer(query, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def get_by_handbook_version(self, request, *args, **kwargs):
        """
        Метод, возвращающий список элементов указанной версии
        справочника по глобальному идентификатору справочника.

        Если версия не передана, поведение идентично методу
        get_by_handbook.

        example:
        > http://localhost:8000/elements/get_by_handbook_version/?handbook_identifier=00000000-0000-0000-0000-000000000001&handbook_version=2
        [
            {
                "id": 2,
                "handbook": "http://localhost:8000/handbooks/5/",
                "parent_identifier": "00000000-0000-0000-0000-000000000001",
                "code": "194213",
                "value": "Лев"
            }
        ]
        """
        self.validate_handbook_identifier(request)
        identifier_param = uuid.UUID(
            request.query_params.get('handbook_identifier')
        )

        if request.query_params.get('handbook_version'):
            version_param = request.query_params.get('handbook_version')
            if not Handbook.objects.filter(
                    identifier=identifier_param, version=version_param
            ).exists():
                raise NotFound(
                    f'handbook with {identifier_param} identifier has no '
                    f'{version_param} version'
                )
            query = self.get_queryset().filter(
                handbook__identifier=identifier_param,
                handbook__version=request.query_params.get('handbook_version')
            )
        else:
            handbook = Handbook.objects.filter(
                identifier=identifier_param,
                begin_date__lte=date.today()
            ).order_by('-begin_date').first()
            query = handbook.elements

        serializer = self.get_serializer(query, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def validate_by_handbook(self, request, *args, **kwargs):
        """
        Метод, проверяющий, являются ли переданные параметры элементами
        текущей версии справочника с переданным идентификатором.

        Возвращает словарь, в котором для каждого параметра указано
        True или False.

        example:
        > http://localhost:8000/elements/validate_by_handbook/?handbook_identifier=00000000-0000-0000-0000-000000000001&q1=word&q2=Лев&q3=Тигр&q4=Саблезуб
        {
            "word": false,
            "Лев": false,
            "Тигр": true,
            "Саблезуб": false
        }
        """
        self.validate_handbook_identifier(request)

        handbook = Handbook.objects.filter(
            identifier=request.query_params.get('handbook_identifier'),
            begin_date__lte=date.today()
        ).order_by('-begin_date').first()
        response = {}
        for key in request.query_params:
            if key.startswith('q'):
                value = request.query_params.get(key)
                response[value] = HandbookElement.objects.filter(
                    handbook=handbook,
                    value__iexact=value
                ).exists()

        return Response(response)

    @action(detail=False)
    def validate_by_handbook_version(self, request, *args, **kwargs):
        """
        Метод, проверяющий, являются ли переданные параметры элементами
        текущей версии справочника с переданным идентификатором.

        Возвращает словарь, в котором для каждого параметра указано
        True или False.

        Если версия не передана, поведение идентично методу
        validate_by_handbook

        example:
        > http://localhost:8000/elements/validate_by_handbook_version/?handbook_identifier=00000000-0000-0000-0000-000000000001&q1=word&q2=Лев&q3=Тигр&q4=Саблезуб&version=0
        {
            "word": false,
            "Лев": false,
            "Тигр": false,
            "Саблезуб": true
        }
        """
        self.validate_handbook_identifier(request)

        identifier_param = request.query_params.get('handbook_identifier')
        version_param = request.query_params.get('handbook_version')
        response = {}
        if version_param:
            for key in request.query_params:
                if key.startswith('q'):
                    value = request.query_params.get(key)
                    response[value] = HandbookElement.objects.filter(
                        handbook__identifier=identifier_param,
                        handbook__version=version_param,
                        value__iexact=value
                    ).exists()
        else:
            return self.validate_by_handbook(request, args, kwargs)

        return Response(response)

    @staticmethod
    def validate_handbook_identifier(request):
        """Валидация переданного идентификатора справочника."""
        if not request.query_params.get('handbook_identifier'):
            raise ParseError('handbook_identifier param is required')
        try:
            identifier_param = uuid.UUID(
                request.query_params.get('handbook_identifier')
            )
        except ValueError:
            raise ValidationError(
                'handbook_identifier has an invalid uuid format.'
            )
        if not Handbook.objects.filter(identifier=identifier_param).exists():
            raise NotFound(
                f'handbook with {identifier_param} identifier was not found'
            )
