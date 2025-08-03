import django_filters
from django.db.models import OuterRef, Subquery
from .models import RoadSegment, TrafficReading

class RoadSegmentFilter(django_filters.FilterSet):
    """
    A filter set for RoadSegment to filter by the characterization of the last reading.
    """
    last_reading_characterization = django_filters.CharFilter(
        method='filter_by_last_reading_characterization'
    )

    class Meta:
        model = RoadSegment
        fields = ['last_reading_characterization']

    def filter_by_last_reading_characterization(self, queryset, name, value):
        speed_ranges = {
            'high_speed': (50, 999),
            'medium_speed': (20, 49.99),
            'low_speed': (0, 19.99),
        }
        
        speed_range = speed_ranges.get(value)
        if not speed_range:
            return queryset.none()

        last_reading_subquery = TrafficReading.objects.filter(
            segment=OuterRef('pk'),
            speed_measured__gte=speed_range[0],
            speed_measured__lte=speed_range[1]
        ).order_by('-timestamp').values('pk')[:1]

        queryset = queryset.annotate(
            last_reading_id=Subquery(last_reading_subquery)
        )
        return queryset.filter(last_reading_id__isnull=False)