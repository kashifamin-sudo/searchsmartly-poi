import csv
import json
import xml.etree.ElementTree as ET
import os
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from poi.models import PointOfInterest


class Command(BaseCommand):
    help = 'Import Point of Interest data from CSV, JSON, or XML files'

    def add_arguments(self, parser):
        parser.add_argument(
            'files',
            nargs='+',
            type=str,
            help='Path to file(s) to import'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before import'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing PoI data...')
            PointOfInterest.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        total_imported = 0

        for file_path in options['files']:
            try:
                imported_count = self.import_file(file_path)
                total_imported += imported_count
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully imported {imported_count} records from {file_path}'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error importing {file_path}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Total records imported: {total_imported}')
        )

    def import_file(self, file_path):
        if not os.path.exists(file_path):
            raise CommandError(f'File does not exist: {file_path}')

        file_ext = Path(file_path).suffix.lower()
        filename = os.path.basename(file_path)

        if file_ext == '.csv':
            return self.import_csv(file_path, filename)
        elif file_ext == '.json':
            return self.import_json(file_path, filename)
        elif file_ext == '.xml':
            return self.import_xml(file_path, filename)
        else:
            raise CommandError(f'Unsupported file type: {file_ext}')

    @transaction.atomic
    def import_csv(self, file_path, filename):
        imported_count = 0

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    poi_data = {
                        'external_id': str(row.get('poi_id', '')).strip(),
                        'name': str(row.get('poi_name', '')).strip(),
                        'latitude': float(row.get('poi_latitude', 0)),
                        'longitude': float(row.get('poi_longitude', 0)),
                        'category': str(row.get('poi_category', '')).strip(),
                        'ratings_data': str(row.get('poi_ratings', '')).strip(),
                        'source_file': filename
                    }

                    if not poi_data['external_id'] or not poi_data['name']:
                        continue

                    poi, created = PointOfInterest.objects.update_or_create(
                        external_id=poi_data['external_id'],
                        defaults=poi_data
                    )

                    if created:
                        imported_count += 1

                except (ValueError, KeyError):
                    continue

        return imported_count

    @transaction.atomic
    def import_json(self, file_path, filename):
        imported_count = 0

        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            try:
                data = json.load(jsonfile)
            except json.JSONDecodeError as e:
                raise CommandError(f'Invalid JSON file: {e}')

            if isinstance(data, dict):
                data = [data]

            for item in data:
                try:
                    coordinates = item.get('coordinates', {})
                    ratings = item.get('ratings', [])

                    poi_data = {
                        'external_id': str(item.get('id', '')).strip(),
                        'name': str(item.get('name', '')).strip(),
                        'latitude': float(coordinates.get('latitude', 0)),
                        'longitude': float(coordinates.get('longitude', 0)),
                        'category': str(item.get('category', '')).strip(),
                        'ratings_data': json.dumps(ratings) if ratings else '',
                        'description': str(item.get('description', '')).strip(),
                        'source_file': filename
                    }

                    if not poi_data['external_id'] or not poi_data['name']:
                        continue

                    poi, created = PointOfInterest.objects.update_or_create(
                        external_id=poi_data['external_id'],
                        defaults=poi_data
                    )

                    if created:
                        imported_count += 1

                except (ValueError, KeyError):
                    continue

        return imported_count

    @transaction.atomic
    def import_xml(self, file_path, filename):
        imported_count = 0

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            raise CommandError(f'Invalid XML file: {e}')

        # Look for DATA_RECORD elements (your XML format)
        poi_elements = root.findall("DATA_RECORD")

        # If not found, fallback for other formats (e.g., <record>)
        if not poi_elements:
            poi_elements = root.findall("record")

        for element in poi_elements:
            try:
                poi_data = {
                    'external_id': str(self.get_xml_text(element, 'pid')).strip(),
                    'name': str(self.get_xml_text(element, 'pname')).strip(),
                    'latitude': float(self.get_xml_text(element, 'platitude', '0')),
                    'longitude': float(self.get_xml_text(element, 'plongitude', '0')),
                    'category': str(self.get_xml_text(element, 'pcategory')).strip(),
                    'ratings_data': str(self.get_xml_text(element, 'pratings')).strip(),
                    'source_file': filename
                }

                if not poi_data['external_id'] or not poi_data['name']:
                    continue

                poi, created = PointOfInterest.objects.update_or_create(
                    external_id=poi_data['external_id'],
                    defaults=poi_data
                )

                if created:
                    imported_count += 1

            except (ValueError, AttributeError):
                continue

        return imported_count

    def get_xml_text(self, element, tag_name, default=''):
        child = element.find(tag_name)
        if child is not None and child.text:
            return child.text.strip()
        return default
