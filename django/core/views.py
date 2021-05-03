import logging
from random import randint

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework.viewsets import GenericViewSet

from django.db.models import Max, QuerySet
from helpers.inspectors import (
    TagsFieldInspector,
    TagsFilterInspector,
)  # CustomPaginatorInspector
from helpers.schemas import CustomAutoSchema
from helpers.sendgrid_helper import send_suggestion_received_email

from .filters import EntityFilterSet
from .serializers import EntityCountSerializer, TagSerializer


logger = logging.getLogger("db")


class CustomPaginetdViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    @property
    def paginator(self):
        """Property responsável pela definição da paginação da view.

        Retornamos uma view com paginação se, e apenas se, o endpoint contiver o parâmetro "page".
        """
        return super().paginator if self.request.query_params.get("page") else None

    def get_paginated_response(self, data: ReturnList) -> Response:
        return Response({"hasMore": self._paginator.page.has_next(), "results": data})


class EntityViewSet(CustomPaginetdViewSet):
    """ViewSet responsável pelos endpoints das entidades."""

    filterset_class = EntityFilterSet
    swagger_schema = CustomAutoSchema

    def get_queryset(self) -> QuerySet:
        return self.model.objects.all().order_by("-date")

    @swagger_auto_schema(
        # paginator_inspectors=[CustomPaginatorInspector],
        field_inspectors=[TagsFieldInspector],
        filter_inspectors=[TagsFilterInspector],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Lista de todas as entidades.
        Suporta os parâmetros de filtro e paginação abaixo.
        """  # swagger
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: EntityCountSerializer})
    @action(methods=["GET"], detail=False)
    def count(self, request: Request) -> Response:
        """Obtenha o número de entidades cadastradas."""  # swagger
        return Response(
            EntityCountSerializer({"total": self.model.objects.count()}).data
        )

    @action(methods=["GET"], detail=False)
    def random(self, request: Request) -> Response:
        """Obtenha uma entidade randomicamente."""  # swagger
        max_id = self.model.objects.all().aggregate(max_id=Max("id"))["max_id"]
        while True:
            pk = randint(1, max_id)  # nosec
            entity_qs = self.model.objects.filter(pk=pk)
            if entity_qs.exists():
                serializer = self.serializer_class(  # pylint: disable=not-callable
                    entity_qs.first()
                )
                return Response(serializer.data)

    @swagger_auto_schema(auto_schema=None)
    def create(self, request: Request) -> Response:
        """
        Sugestão de novas entidades.

        Em caso de uma requisição inválida, a resposta conterá erros.
        """
        logger.info("Sugestão recebida! E-mail: %s", request.data.get("user_email"))

        serializer = self.suggestion_serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            suggestion = serializer.save()
            send_suggestion_received_email(request=request, obj=suggestion)
            return Response(
                {
                    "message": "Obrigado por contribuir! Aguarde mais informações por e-mail :)"
                },
                status=HTTP_200_OK,
            )

        logger.warning("Dados inválidos! request.data: %s", request.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(auto_schema=None)
    def update(self, request: Request, **kwargs) -> Response:
        """
        Sugestão de alteração em entidades.

        Em caso de uma requisição inválida, a resposta conterá erros.
        """
        logger.info("Sugestão recebida! E-mail: %s", request.data.get("user_email"))

        request.data["original_" + self.model.__name__.lower()] = kwargs["pk"]
        serializer = self.suggestion_change_serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            suggestion = serializer.save()
            send_suggestion_received_email(request=request, obj=suggestion)
            return Response(
                {
                    "message": "Obrigado por contribuir! Aguarde mais informações por e-mail :)"
                },
                status=HTTP_200_OK,
            )

        logger.warning("Dados inválidos! request.data: %s", request.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class EntityTagsView(CustomPaginetdViewSet):
    serializer_class = TagSerializer
    swagger_schema = CustomAutoSchema
    lookup_field = "slug"

    def get_queryset(self) -> QuerySet:
        return self.model.objects.all().order_by("id")

    def list(  # pylint: disable=useless-super-delegation
        self, request: Request, *args, **kwargs
    ) -> Response:
        """Obtenha as tags da entidade."""  # swagger
        return super().list(request, *args, **kwargs)

    def main(self, request: Request) -> Response:
        queryset = self.model.objects.filter(parent=None)
        return Response(self.tags_serializer_class(queryset, many=True).data)
