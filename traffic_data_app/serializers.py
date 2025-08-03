from rest_framework import serializers
from .models import RoadSegment, TrafficReading
from django.contrib.gis.geos import LineString


class TrafficReadingSerializer(serializers.ModelSerializer):
    """Serializer for the TrafficReading model."""
    segment = serializers.PrimaryKeyRelatedField(queryset=RoadSegment.objects.all())

    class Meta:
        model = TrafficReading
        fields = (
            "id",
            "uuid",
            "timestamp",
            "speed_measured",
            "segment"
        )
        read_only_fields = ("id", "uuid", "timestamp")

    def validate_speed_measured(self, value):
        if value < 0:
            raise serializers.ValidationError("Speed cannot be negative.")
        return value


class RoadSegmentSerializer(serializers.ModelSerializer):
    """Serializer for the RoadSegment model."""
    long_start = serializers.SerializerMethodField(read_only=True)
    lat_start = serializers.SerializerMethodField(read_only=True)
    long_end = serializers.SerializerMethodField(read_only=True)
    lat_end = serializers.SerializerMethodField(read_only=True)

    long_start_write = serializers.FloatField(write_only=True)
    lat_start_write = serializers.FloatField(write_only=True)
    long_end_write = serializers.FloatField(write_only=True)
    lat_end_write = serializers.FloatField(write_only=True)

    readings_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = RoadSegment
        fields = (
            "id",
            "uuid",
            "name",
            "length",
            "long_start",
            "lat_start",
            "long_end",
            "lat_end",
            "long_start_write",
            "lat_start_write",
            "long_end_write",
            "lat_end_write",
            'readings_count'
        )
        read_only_fields = (
            "id",
            "uuid",
            'readings_count'
        )

    def get_long_start(self, obj):
        return obj.geometry.coords[0][0]

    def get_lat_start(self, obj):
        return obj.geometry.coords[0][1]

    def get_long_end(self, obj):
        return obj.geometry.coords[1][0]

    def get_lat_end(self, obj):
        return obj.geometry.coords[1][1]

    def get_readings_count(self, obj):
        return obj.traffic_readings.count()

    def create(self, validated_data):
        # Extract the write-only fields to create the LineString
        long_start = validated_data.pop("long_start_write")
        lat_start = validated_data.pop("lat_start_write")
        long_end = validated_data.pop("long_end_write")
        lat_end = validated_data.pop("lat_end_write")

        validated_data["geometry"] = LineString(
            (long_start, lat_start), (long_end, lat_end)
        )

        return super().create(validated_data)

    def validate_length(self, value):
        if value <= 0:
            raise serializers.ValidationError("Length must be a positive number.")
        return value
