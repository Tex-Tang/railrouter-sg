from opencage.geocoder import OpenCageGeocode
import googlemaps
import json, os, re, pprint

BASE_DIR = os.path.dirname(__file__)
json_path = os.path.join(BASE_DIR, "shengsiong-locations.json")

key = 'key'
gmaps = googlemaps.Client(key)

with open(json_path, "r") as f:
    shengsiong_list = json.load(f)

cleaned_shengsiong_list = []
error_shengsiong_list = []

for idx, shop in enumerate(shengsiong_list):
    full_address, postal_code, is24Hour = shop["address1"], shop["postal_code"], shop["is24Hour"]
    
    cleaned_json = {}
    
    cleaned_json['is24Hour'] = is24Hour
    cleaned_json['postal_code'] = postal_code
    cleaned_json['address1'] = full_address
    
    results = gmaps.geocode(f'{cleaned_json['address1']}, Singapore')
    if results:
        long, lat = results[0]['geometry']['location']['lng'], results[0]['geometry']['location']['lat']
        
        if not(1.15 <= lat <= 1.48 and 103.60 <= long <= 104.10):
            cleaned_json['error'] = 'Coordinates Out of Bound'
            error_shengsiong_list.append(cleaned_json)
        else:
            cleaned_json['lat'], cleaned_json['long'] = lat, long
            cleaned_shengsiong_list.append(cleaned_json)
    else: 
        cleaned_json['error'] = 'Coordinate Missing'
        error_shengsiong_list.append(cleaned_json)
        
    print(f'{idx+1}: {cleaned_json['address1']}')

BASE_DIR = os.path.dirname(__file__)

output_file = os.path.join(BASE_DIR, "new-shengsiong-locations.json")
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(cleaned_shengsiong_list, outfile, indent=4)

error_file = os.path.join(BASE_DIR, "error-shengsiong-locations.json")
with open(error_file, "w", encoding="utf-8") as outfile:
    json.dump(error_shengsiong_list, outfile, indent=4)