from rest_framework import viewsets
from .models import RoadSegment, TrafficReading
from .serializers import RoadSegmentSerializer, TrafficReadingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsAdminUserOrReadOnly
from .filters import RoadSegmentFilter

import logging

logger = logging.getLogger(__name__)


class RoadSegmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows RoadSegments to be viewed or edited.
    """

    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_class = RoadSegmentFilter

    @action(detail=True, methods=['get'])
    def readings_count(self, request, pk=None):
        segment = self.get_object()
        count = segment.traffic_readings.count()
        return Response({'readings_count': count})

    def create(self, request, *args, **kwargs):
        print("Corpo da requisição:", request.body)
        print("Dados da requisição:", request.data)

        # Este log vai mostrar a informação
        logger.info(f"Recebi uma requisição POST com os dados: {request.data}")

        # O super() vai chamar o método original da viewset
        return super().create(request, *args, **kwargs)


class TrafficReadingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TrafficReadings to be viewed or edited.
    """

    queryset = TrafficReading.objects.all()
    serializer_class = TrafficReadingSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["segment"]