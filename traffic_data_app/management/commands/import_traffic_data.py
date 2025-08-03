import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from traffic_data_app.models import RoadSegment, TrafficReading
from django.contrib.gis.geos import LineString, Point


class Command(BaseCommand):
    help = "Imports road segment and traffic reading data from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--traffic_speed_path",
            type=str,
            help="Path to the traffic_speed.csv file.",
            default="traffic_data_app/data/traffic_speed.csv",
        )

    def handle(self, *args, **options):
        if RoadSegment.objects.exists():
            self.stdout.write(self.style.WARNING('Database already contains road segments. Seeding will be skipped.'))
            return

        self.stdout.write(self.style.NOTICE('Starting data import...'))

        csv_path = options['traffic_speed_path']
        if not os.path.exists(csv_path):
            raise CommandError(f'File "{csv_path}" not found.')

        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Use a dictionary to store unique segments, keyed by their CSV ID.
                segments_to_create = {}
                rows_with_readings = []
                
                # Step 1: Read the CSV to identify unique segments and all readings.
                for row in reader:
                    csv_id = int(row['ID'])
                    segment_key = (
                        float(row['Long_start']), float(row['Lat_start']), 
                        float(row['Long_end']), float(row['Lat_end'])
                    )
                    
                    if csv_id not in segments_to_create:
                        start_point = Point(segment_key[0], segment_key[1])
                        end_point = Point(segment_key[2], segment_key[3])
                        line_string = LineString(start_point, end_point)

                        segments_to_create[csv_id] = RoadSegment(
                            name=f"Segment {csv_id}",
                            geometry=line_string,
                            length=float(row['Length']),
                        )
                    
                    rows_with_readings.append(row)
                
                # Step 2: Bulk create the unique RoadSegment objects.
                # Django's bulk_create will return the objects with their new database IDs.
                created_segments = RoadSegment.objects.bulk_create(
                    list(segments_to_create.values())
                )
                self.stdout.write(self.style.SUCCESS(f'Created {len(created_segments)} unique road segments.'))
                
                # Step 3: Create a map from the original CSV ID to the new database ID.
                # This uses the 'name' field as a bridge.
                csv_id_to_db_id = {
                    int(seg.name.split(' ')[1]): seg.id for seg in created_segments
                }
                
                # Step 4: Prepare all readings for bulk creation using the new mapping.
                traffic_readings_to_create = [
                    TrafficReading(
                        segment_id=csv_id_to_db_id[int(row['ID'])],
                        speed_measured=float(row['Speed']),
                        timestamp=timezone.now()
                    ) for row in rows_with_readings
                ]

                TrafficReading.objects.bulk_create(traffic_readings_to_create)
                self.stdout.write(self.style.SUCCESS(f'Created {len(traffic_readings_to_create)} traffic readings.'))
                
                self.stdout.write(self.style.SUCCESS('Data import completed successfully!'))

        except Exception as e:
            raise CommandError(f'An error occurred during import: {e}')