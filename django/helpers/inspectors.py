# from collections import OrderedDict
from typing import Union  # Any,

from drf_yasg.inspectors import (
    CoreAPICompatInspector,
    FieldInspector,
    NotHandled,
)  # PaginatorInspector,
from drf_yasg.openapi import (
    FORMAT_SLUG,
    IN_QUERY,
    Items,
    Parameter,
    Schema,
    TYPE_ARRAY,  # TYPE_BOOLEAN,; TYPE_OBJECT,
    TYPE_STRING,
)
from rest_framework.serializers import ReadOnlyField


TAGS_DESCRIPTION = (
    "Filtre as entidades por múltiplas tags (use os slugs).\n\n"
    "As tags são agrupadas no modelo 'pai e filho' ('Ministério do Meio Ambiente' como "
    "'pai' e 'Ibama' como 'filho', por exemplo).\n\nA API foi projetada para obter entidades "
    "marcadas com as respectivas tags e, TAMBÉM, suas 'filhas'. "
    "Ou seja, uma consulta buscando ações marcadas com a tag 'Ministério do Meio Ambiente' "
    "também retornará ações marcadas com a tag 'Ibama'. A recíproca não é verdadeira."
)


class TagsFieldInspector(FieldInspector):
    """Inspector para o campo 'tags' das entidades"""

    def field_to_swagger_object(
        self,
        field: ReadOnlyField,
        swagger_object_type: Schema,
        use_references: bool,
        **kwargs,
    ) -> Union[object, Schema]:
        """NotHandled = object()"""
        SwaggerType, _ = self._get_partial_types(  # pylint: disable=invalid-name
            field, swagger_object_type, use_references, **kwargs
        )

        if isinstance(field, ReadOnlyField) and field.source == "tags_names":
            return SwaggerType(
                type=TYPE_ARRAY,
                items=Items(type=TYPE_STRING),
            )

        return NotHandled


class TagsFilterInspector(CoreAPICompatInspector):
    """Inspector para o filtro 'tags' das entidades"""

    def coreapi_field_to_parameter(self, field):
        if field.name == "tags":
            return Parameter(
                name=field.name,
                in_=IN_QUERY,
                required=field.required,
                description=TAGS_DESCRIPTION,
                type=TYPE_ARRAY,
                items=Items(type=TYPE_STRING, format=FORMAT_SLUG),
            )
        return super().coreapi_field_to_parameter(field=field)


# pylint: disable=pointless-string-statement
"""
class CustomPaginatorInspector(PaginatorInspector):
    '''
    No momento não vamos usar este inspector pois a biblioteca drf-yasg não suporta o OpenAPI 3.0.

    Sendo assim, não conseguimos documentar mais de uma resposta para o mesmo código. Como o código
    200 pode ter duas respostas - uma da entidade, na ausência do parâmetro 'page', e a retornada
    por 'get_paginated_response' -, optamos por documentar apenas a da entidade.

    Avaliar a biblioteca drf-spectacular
    '''

    def get_paginated_response(self, paginator: Any, response_schema: Schema) -> Schema:
        return Schema(
            type=TYPE_OBJECT,
            properties=OrderedDict(
                (
                    ("hasMore", Schema(type=TYPE_BOOLEAN)),
                    ("results", response_schema),
                )
            ),
            required=["results"],
        )
"""
