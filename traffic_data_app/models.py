import uuid
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import LineString, Point


class RoadSegment(gis_models.Model):
    name = models.CharField(max_length=200)
    uuid = models.UUIDField(
        default=uuid.uuid4, unique=True, db_index=True, editable=False
    )

    geometry = gis_models.LineStringField(srid=4326)

    length = models.FloatField()

    def __str__(self):
        return f"RoadSegment {self.id} - {self.name}"


class TrafficReading(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, unique=True, db_index=True, editable=False
    )

    segment = models.ForeignKey(
        RoadSegment, on_delete=models.CASCADE, related_name="traffic_readings"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    speed_measured = models.FloatField()

    def __str__(self):
        return f"Speed for {self.segment.name} at {self.timestamp}: {self.speed_measured} km/h"
