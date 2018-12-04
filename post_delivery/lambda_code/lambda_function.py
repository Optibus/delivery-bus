from __future__ import print_function
import googlemaps
from datetime import datetime
from math import sin, cos, sqrt, atan2, radians
from geopy.distance import geodesic

import json

print('Loading function')


def response(res=None):
    return {
        'statusCode': '200',
        'body': json.dumps(res),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

people_json = [{'id': '0526216383', 'stop': {'lat': '1.111', 'lon': '1.2323'}}]

people_json = {
  "deliverbizers": [
    {
    	"ID":100,
    	"name":"Joseph",
    	"locations":["Clay Tel Aviv-Yafo",
    	             "Helsinki Tel Aviv-Yafo",
    	             "Yoo Towers Tel Aviv-Yafo"]
    },
    {
      "ID":101,
    	"name":"David",
    	"locations":["Tashi Tel Aviv-Yafo",
    	             "Tuval  Tel Aviv-Yafo",
    	             "Brurya Tel Aviv-Yafo"]
    },
    {
      "ID":102,
    	"name":"Danny",
    	"locations":["Lessin Tel Aviv-Yafo",
    	             "HaTamar Tel Aviv-Yafo",
    	             "Harimon Tel Aviv-Yafo"]
    },
    {
      "ID":103,
    	"name":"Daniel",
    	"locations":["Bezalel  Tel Aviv-Yafo",
    	             "Ahaliav  Tel Aviv-Yafo",
    	             "Moshe Sharet  Tel Aviv-Yafo"]
    },
    {
      "ID":104,
    	"name":"Lavie",
    	"locations":["Ram Tel Aviv-Yafo",
    	             "Sderot Yehudit Tel Aviv-Yafo",
    	             "Yosef Karo Ram Tel Aviv-Yafo"]
    },
    {
      "ID":105,
    	"name":"Omer",
    	"locations":["Eliezer Kaplan Tel Aviv-Yafo",
    	             "Heftman Tel Aviv-Yafo",
    	             "Beit Hilel Tel Aviv-Yafo"]
    },
    {
      "ID":106,
    	"name":"Ariel",
    	"locations":["Shulman Tel Aviv-Yafo",
    	             "Yinon Tel Aviv-Yafo",
    	             "Yaniv Tel Aviv-Yafo"]
    },
    {
      "ID":107,
    	"name":"Noam",
    	"locations":["Sarona Market Tel Aviv-Yafo",
    	             "Ben Avigdor Tel Aviv-Yafo",
    	             "Meitav  Tel Aviv-Yafo"]
    },
    {
      "ID":108,
    	"name":"Adam",
    	"locations":["HaAvoda Tel Aviv-Yafo",
    	             "Sheinkin Tel Aviv-Yafo",
    	             "Brenner Tel Aviv-Yafo"]
    },
    {
      "ID":109,
    	"name":"Itai",
    	"locations":["Gordon Tel Aviv-Yafo",
    	             "Frishman Tel Aviv-Yafo",
    	             "Sderot Ben Gurion Tel Aviv-Yafo"]
    },
    {
      "ID":110,
    	"name":"Jonathan",
    	"locations":["Ben Ami Tel Aviv-Yafo",
    	             "HaAri Tel Aviv-Yafo",
    	             "Najara Tel Aviv-Yafo"]
    }]
}


def get_km_distance(lat1, lon1, lat2, lon2):

    return geodesic((lat1, lon1), (lat2, lon2)).km


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    gmaps = googlemaps.Client(key='AIzaSyA1vDfDUOgFDMrgpJYTT_y6LfhCq79fsfE')
    origin = event.get('origin')
    dest = event.get('destination')
    customer_id = event.get('customer_id')
    buses = []
    directions_result = gmaps.directions(origin,
                                         dest,
                                         mode="transit",
                                         departure_time=datetime.now(),
                                         transit_mode='bus',
                                         alternatives=True)

    all_directions = [a['legs'][0]['steps'] for a in directions_result]
    first_buses = {}
    for direction in all_directions:
        bus = []
        for step in direction:
            if step.get('transit_details'):
                bus.append(step)
        buses.append(bus)

    for bus in buses:
        if all(b['distance']['value'] > 20000 for b in bus):
            buses.remove(bus)

    for bus in buses:
        if bus[0]['distance']['value'] < 20000:
            first_buses[bus[0]['transit_details']['line']['short_name']] = {
                'arrival_stop': bus[0]['transit_details']['arrival_stop']['location'],
                'arrival_time': bus[0]['transit_details']['arrival_time']['value'],
                'departure_time': bus[0]['transit_details']['departure_time']['value'],
                'departure_stop': bus[0]['transit_details']['departure_stop']['location']}
        else:
            first_buses[bus[0]['transit_details']['line']['short_name']] = {
                'arrival_stop': bus[0]['transit_details']['arrival_stop']['location'],
                'arrival_time': bus[0]['transit_details']['arrival_time']['value']}

    result_dict = {}
    for key, value in first_buses.items():
        relevant_people = []
        lat1 = value['departure_stop']['lat']
        lon1 = value['departure_stop']['lng']
        lat2 = value['arrival_stop']['lat']
        lon2 = value['arrival_stop']['lng']
        for person in people_json['deliverbizers']:
            person['google_locations'] = []
            for x in person['locations']:
                google_geocode = gmaps.geocode(x)
                person['google_locations'].append(google_geocode)
            for loc in person['google_locations']:
                if loc:
                    lot = loc[0]['geometry']['location']['lat']
                    lan = loc[0]['geometry']['location']['lng']
                    if get_km_distance(lat1, lon1, lot, lan) < 1:
                        relevant_people.append(person['ID'])
                        break
        result_dict[key] = relevant_people

    return response(result_dict)



