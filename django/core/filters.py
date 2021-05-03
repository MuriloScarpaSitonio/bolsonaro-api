import django_filters

from django.db.models import Q

from .exceptions import BolsonaroAPIException


class EntityFilterSet(django_filters.FilterSet):
    """Classe responsável pela geração dos filtros das entidades"""

    description = django_filters.CharFilter(lookup_expr="icontains")
    start_date = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")
    tags = django_filters.CharFilter(method="tags_custom_filter")

    def tags_custom_filter(self, queryset, _, value):
        if value:
            tags = [tag.strip() for tag in value.split(",")]
            tags_qs = queryset.model.tags.through.tag_model().objects.filter(
                slug__in=tags
            )
            if tags_qs.count() != len(tags):
                tags_in_db = tags_qs.values_list("slug", flat=True)
                not_valid_tags = [tag for tag in set(tags) if tag not in tags_in_db]
                raise BolsonaroAPIException(
                    detail={
                        "errorMessage": (
                            "A(s) seguinte(s) tag(s) não existe(m): "
                            f"{', '.join(not_valid_tags)}."
                        )
                    }
                )

        return queryset.filter(Q(tags__slug__in=tags) | Q(tags__parent__slug__in=tags))
