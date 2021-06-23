from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.openapi import FORMAT_DATE, IN_QUERY, Parameter, TYPE_INTEGER


class CustomAutoSchema(SwaggerAutoSchema):
    """Custom Schema para geração de documentação via Swagger"""

    def get_filter_parameters(self):
        if self.view.action != "list":
            return []

        result = super().get_filter_parameters()
        for param in result:
            if param.name == "description":
                param.description = "Filtre as entidades por um texto."
            if param.name == "start_date":
                param.description = (
                    "Filtre as entidades a partir de uma data específica "
                    "(formato dd/mm/yyyy)."
                )
                param.format = FORMAT_DATE
            if param.name == "end_date":
                param.description = (
                    "Filtre as entidades até uma data específica (formato dd/mm/yyyy)."
                )
                param.format = FORMAT_DATE

        return result

    def should_page(self):
        if self.view.action == "list" or "tags" in self.view.action:
            return True
        return super().should_page()

    def get_pagination_parameters(self):
        if self.should_page():
            return [
                Parameter(
                    name="page",
                    in_=IN_QUERY,
                    description="Use este parâmetro para obter o resultado com paginação.",
                    type=TYPE_INTEGER,
                )
            ]
        return super().get_pagination_parameters()
