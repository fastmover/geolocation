from flask import Flask, json, render_template, request
from math import cos, asin, sqrt, pi
import csv

app = Flask(__name__)

@app.route('/locations', methods=['post'])
def closest_location():
    if request.method == 'POST':
        latitude = request.json['latitude']
        longitude = request.json['longitude']
        return calcDistance(float(latitude), float(longitude))

@app.route("/")
def home():
    return render_template('./index.html')

def calcDistance(lat, long):
    with open('pharmacies.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        pharmacies = []
        for row in csv_reader:
            pharmacy = {
                "name": row["name"],
                "address": row["address"],
                "distance": distance(lat, long, float(row["latitude"]), float(row["longitude"])),
            }
            pharmacies.append(pharmacy)
    pharmacies.sort(key= lambda x:x['distance'])
    closestPharmacy = pharmacies.pop(0)
    closestPharmacy["distance"] = round(closestPharmacy["distance"], 1)
    return json.dumps(closestPharmacy)

def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return (12742 * asin(sqrt(a))) * 0.621371

if __name__ == '__main__':
    app.run()
