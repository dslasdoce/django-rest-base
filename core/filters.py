import django_filters as filters


class BaseFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('id', 'id'),
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        )
    )

    class Meta:
        fields = ('user', )



