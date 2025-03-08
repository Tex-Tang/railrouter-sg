from opencage.geocoder import OpenCageGeocode
import json, os, re, pprint

BASE_DIR = os.path.dirname(__file__)
json_path = os.path.join(BASE_DIR, "shengsiong-locations.json")

key = 'XXX'
geocoder = OpenCageGeocode(key)

with open(json_path, "r") as f:
    shengsiong_list = json.load(f)

cleaned_shengsiong_list = []
error_shengsiong_list = []

for idx, shop in enumerate(shengsiong_list):
    full_address, time, phone = shop["address"], shop["time"], shop["phone"]
    
    cleaned_json = {}
    
    cleaned_json['is24Hour'] = re.search(r'24', time) is not None
    cleaned_json['postal_code'] = re.search(r'Singapore (\d+)', full_address).group(1)
    cleaned_json['address1'] = re.split(r'#', full_address)[0].strip()
    
    results = geocoder.geocode(f'{cleaned_json['address1']}, Singapore')
    if results:
        long, lat = results[0]['geometry']['lng'], results[0]['geometry']['lat']
        
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

output_file = os.path.join(BASE_DIR, "cleaned_shengsiong_locations.json")
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(cleaned_shengsiong_list, outfile, indent=4)

error_file = os.path.join(BASE_DIR, "error_shengsiong_locations.json")
with open(error_file, "w", encoding="utf-8") as outfile:
    json.dump(error_shengsiong_list, outfile, indent=4)