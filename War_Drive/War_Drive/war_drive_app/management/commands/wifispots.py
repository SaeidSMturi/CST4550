# import csv
# from django.conf import settings
# from django.core.management.base import BaseCommand
# from war_drive_app.models import EVChargingLocation


# class Command(BaseCommand):
#     help = 'Load data from EV Station file'

#     def handle(self, *args, **kwargs):
#         data_file = settings.BASE_DIR / 'data' / 'EV_Charging_Stations.csv'
#         keys = ('Station Name', 'New Georeferenced Column')  # the CSV columns we will gather data from.
        
#         records = []
#         with open(data_file, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 records.append({k: row[k] for k in keys})

#         # extract the latitude and longitude from the Point object
#         for record in records:
#             longitude, latitude = record['New Georeferenced Column'].split("(")[-1].split(")")[0].split()
#             record['longitude'] = float(longitude)
#             record['latitude'] = float(latitude)

#             # add the data to the database
#             EVChargingLocation.objects.get_or_create(
#                 station_name=record['Station Name'],
#                 latitude=record['latitude'],
#                 longitude=record['longitude']
#             )


# load_stations.py
# app/management/commands/load_stations.py
import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from war_drive_app.models import WiFi  # Adjust if your app name is different

# class Command(BaseCommand):
#     help = 'Load data from EV Charging Stations CSV file'

#     def handle(self, *args, **kwargs):
#         # Construct the full path to the CSV file.
#         data_file = os.path.join(settings.BASE_DIR, 'data', 'EV_Charging_Stations.csv')
#         # Only gather these columns (modify if you need additional columns)
#         keys = ('Station Name', 'New Georeferenced Column')
        
#         records = []
#         try:
#             with open(data_file, 'r', encoding='utf-8-sig') as csvfile:
#                 reader = csv.DictReader(csvfile)
#                 for row in reader:
#                     # Gather only the keys we want
#                     records.append({k: row[k] for k in keys})
#         except Exception as e:
#             self.stderr.write(f"Error reading CSV file: {e}")
#             return

#         # Extract latitude and longitude from the "POINT (lng lat)" string
#         for record in records:
#             try:
#                 # Expecting format like: POINT (-73.4764687 41.072882)
#                 point_text = record['New Georeferenced Column']
#                 # Remove the "POINT (" prefix and ")" suffix then split
#                 parts = point_text.strip().lstrip("POINT (").rstrip(")").split()
#                 if len(parts) != 2:
#                     self.stderr.write(f"Unexpected format for point: {point_text}")
#                     continue
#                 # Note: the CSV stores longitude first, then latitude.
#                 longitude, latitude = parts
#                 record['longitude'] = float(longitude)
#                 record['latitude'] = float(latitude)
#             except Exception as e:
#                 self.stderr.write(f"Error processing record {record}: {e}")
#                 continue

#             # Create or update the database record
#             obj, created = EVChargingLocation.objects.get_or_create(
#                 station_name=record['Station Name'],
#                 defaults={
#                     'latitude': record['latitude'],
#                     'longitude': record['longitude']
#                 }
#             )
#             if not created:
#                 # Optionally update the record if it already exists.
#                 obj.latitude = record['latitude']
#                 obj.longitude = record['longitude']
#                 obj.save()

#         self.stdout.write("CSV data imported successfully.")




# class Command(BaseCommand):
#     help = 'Load data from EV Station CSV file using the new format'

#     def handle(self, *args, **kwargs):
#         # Build the full file path. Assumes the CSV file is in a folder named "data" at the project root.
#         data_file = os.path.join(settings.BASE_DIR, 'data', 'EV_Charging_Stations.csv')
#         records = []

#         # Open the CSV file with the correct encoding (utf-8-sig handles a BOM, if present)
#         try:
#             with open(data_file, 'r', encoding='utf-8-sig') as csvfile:
#                 reader = csv.DictReader(csvfile)
#                 for row in reader:
#                     records.append(row)
#         except Exception as e:
#             self.stderr.write(f"Error reading CSV file: {e}")
#             return

#         # Process each record
#         for row in records:
#             # Determine station name: if SSID is provided (non-empty), use it; otherwise, use MAC.
#             station_name = row['SSID'].strip() if row['SSID'].strip() != '' else row['MAC'].strip()
            
#             # Parse latitude and longitude from the provided columns.
#             try:
#                 latitude = float(row['CurrentLatitude'])
#                 longitude = float(row['CurrentLongitude'])
#             except Exception as e:
#                 self.stderr.write(f"Error parsing latitude/longitude for {station_name}: {e}")
#                 continue

#             # Add the station to the database if it doesn't already exist.
#             EVChargingLocation.objects.get_or_create(
#                 station_name=station_name,
#                 defaults={
#                     'latitude': latitude,
#                     'longitude': longitude,
#                 }
#             )

#         self.stdout.write("CSV data imported successfully.")



class Command(BaseCommand):
    help = 'Load data from WiFi Spots CSV file (only records with Type WIFI)'

    def handle(self, *args, **kwargs):
        # Build full path to the CSV file
        data_file = os.path.join(settings.BASE_DIR, 'data', 'WigleWifi_20250327014237.csv')
        records = []

        try:
            # Use utf-8-sig encoding to handle any Byte-Order Mark (BOM)
            with open(data_file, 'r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Filter: only keep records where the Type column equals 'WIFI'
                    if row['Type'].strip().upper() == 'WIFI':
                        records.append(row)
        except Exception as e:
            self.stderr.write(f"Error reading CSV file: {e}")
            return

        # for row in records:
        #     # Determine SSID: use the SSID if available; otherwise, use MAC.
        #     SSID = row['SSID'].strip() if row['SSID'].strip() != '' else row['MAC'].strip()



        for row in records:
            # Process only those records where SSID is available.
            ssid_value = row['SSID'].strip()
            if ssid_value == '':
                # Skip records that don't have an SSID
                continue

            SSID = ssid_value  # Use SSID as is; do not fall back to MAC
            
            try:
                # Parse latitude and longitude from the CSV fields (they are provided as separate columns)
                latitude = float(row['CurrentLatitude'])
                longitude = float(row['CurrentLongitude'])
            except Exception as e:
                self.stderr.write(f"Error parsing coordinates for {SSID}: {e}")
                continue

            # Create or update the record based on the SSID.
            obj, created = WiFi.objects.get_or_create(
                SSID=SSID,
                defaults={
                    'latitude': latitude,
                    'longitude': longitude,
                }
            )
            if not created:
                # Update the record if it already exists (optional)
                obj.latitude = latitude
                obj.longitude = longitude
                obj.save()

        self.stdout.write("CSV data imported successfully (only WIFI records).")


