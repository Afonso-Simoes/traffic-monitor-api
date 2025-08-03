import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from traffic_data_app.models import RoadSegment, TrafficReading
from django.contrib.gis.geos import LineString, Point


class Command(BaseCommand):
    help = "Importa dados de segmentos de estrada e leituras de tráfego a partir de um ficheiro CSV."

    def add_arguments(self, parser):
        parser.add_argument(
            "--traffic_speed_path",
            type=str,
            help="Caminho para o ficheiro traffic_speed.csv.",
            default="traffic_data_app/data/traffic_speed.csv",
        )

    def handle(self, *args, **options):
        if RoadSegment.objects.exists():
            self.stdout.write(self.style.WARNING('A base de dados já contém segmentos de estrada. O seeding será ignorado.'))
            return

        self.stdout.write(self.style.NOTICE('A iniciar a importação de dados...'))

        csv_path = options['traffic_speed_path']
        if not os.path.exists(csv_path):
            raise CommandError(f'O ficheiro "{csv_path}" não foi encontrado.')

        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                road_segments_to_create = []
                traffic_readings_to_create = []

                for row in reader:
                    road_segment_id = int(row['ID'])

                    start_point = Point(float(row['Long_start']), float(row['Lat_start']))
                    end_point = Point(float(row['Long_end']), float(row['Lat_end']))
                    line_string = LineString(start_point, end_point)

                    road_segments_to_create.append(
                        RoadSegment(
                            id=road_segment_id,
                            name=f"Segmento {road_segment_id}",
                            geometry=line_string, # <--- Passar o objeto LineString
                            length=float(row['Length']),
                        )
                    )

                    traffic_readings_to_create.append(
                        TrafficReading(
                            segment_id=road_segment_id,
                            speed_measured=float(row['Speed']),
                            timestamp=timezone.now()
                        )
                    )

            RoadSegment.objects.bulk_create(road_segments_to_create)
            self.stdout.write(self.style.SUCCESS(f'Criados {len(road_segments_to_create)} segmentos de estrada.'))

            TrafficReading.objects.bulk_create(traffic_readings_to_create)
            self.stdout.write(self.style.SUCCESS(f'Criadas {len(traffic_readings_to_create)} leituras de tráfego.'))

        except Exception as e:
            raise CommandError(f'Ocorreu um erro durante a importação: {e}')

        self.stdout.write(self.style.SUCCESS('Importação de dados concluída com sucesso!'))
