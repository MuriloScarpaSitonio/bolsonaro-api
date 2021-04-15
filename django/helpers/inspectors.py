# from collections import OrderedDict
from typing import Union  # Any,

from drf_yasg.inspectors import FieldInspector, NotHandled  # PaginatorInspector,
from drf_yasg.openapi import (
    TYPE_ARRAY,  # TYPE_BOOLEAN,; TYPE_OBJECT,
    TYPE_STRING,
    Items,
    Schema,
)
from rest_framework.serializers import ReadOnlyField


class TagFieldInspector(FieldInspector):
    """Inspector para o campo tag da entidades"""

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
