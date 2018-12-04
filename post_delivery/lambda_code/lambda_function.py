from __future__ import print_function
import googlemaps
from datetime import datetime
from math import sin, cos, sqrt, atan2, radians
from geopy.distance import geodesic


import json

from send_sms import SMS

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
      "ID":102,
    	"name":"Danny",
    	"locations":["Menachem Begin 23 Tel Aviv"]
    },
    {
      "ID":103,
    	"name":"Daniel",
    	"locations":["Menachem Begin 23 Tel Aviv"]
    },
    {
      "ID":107,
    	"name":"Noam",
    	"locations":["Menachem Begin 23 Tel Aviv"]
    },
    {
      "ID":108,
    	"name":"Adam",
    	"locations":["Begin 23 Jerusalem"]
    },
    {
      "ID":110,
    	"name":"Jonathan",
    	"locations":["Begin 23 Jerusalem"]
    }]
}


def get_km_distance(lat1, lon1, lat2, lon2):

    return geodesic((lat1, lon1), (lat2, lon2)).km


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    event = {'origin': 'Menachem Begin 23 tel aviv', 'destination': 'Ben Gurion university', 'customer_id': 100}

    gmaps = googlemaps.Client(key='AIzaSyA1vDfDUOgFDMrgpJYTT_y6LfhCq79fsfE')
    origin = event.get('origin')
    dest = event.get('destination')
    customer_id = event.get('customer_id')
    buses = []
    directions_result = gmaps.directions(origin,
                                         dest,
                                         mode="transit",
                                         departure_time=1544003400,
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
        for person in people_json['deliverbizers']:
            person['google_locations'] = []
            for x in person['locations']:
                google_geocode = gmaps.geocode(x)
                person['google_locations'].append(google_geocode)
            for loc in person['google_locations']:
                if loc:
                    lot = loc[0]['geometry']['location']['lat']
                    lan = loc[0]['geometry']['location']['lng']
                    if get_km_distance(lat1, lon1, lot, lan) < 10:
                        relevant_people.append(person['ID'])
                        break
        result_dict[key] = relevant_people

    print(result_dict)
    print(directions_result[2]['legs'][0]['steps'])
    res = []
    for bus in directions_result[2]['legs'][0]['steps']:
        if bus['distance']['value'] < 1000:
            continue
        else:
            res.append({'name_of_the_stop': bus['transit_details']['departure_stop']['name'],
                        'line_number': bus['transit_details']['line']['short_name'],
                        'departure_time': bus['transit_details']['departure_time']['text'],
                        'duration': bus['duration']['text']})

    SMS().send_sms('Use line 238 or 669 to deliver and earn some money!\nClick here to accept: https://tinyurl.com/ybbcuvxs')


    return response(res)

lambda_handler([], [])
