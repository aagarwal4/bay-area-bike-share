import requests
import csv
import geopy.distance
import pandas as pd
from Tkinter import Tk, Label, Button
import urllib
import simplejson

address = raw_input("Enter your address: ")
#address = "101 Howard Street, San Francisco"
api_key = ***
api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
api_response_dict = api_response.json()

if api_response_dict['status'] == 'OK':
    latitude = api_response_dict['results'][0]['geometry']['location']['lat']
    longitude = api_response_dict['results'][0]['geometry']['location']['lng']

mylist = []
with open('station.csv','rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        mylist.append(tuple(row[1:4]))

station_google_info = pd.DataFrame(columns = ['station_name','distance','duration', 'distance_value'])
for station in mylist[1:]:
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={0}&destinations={1}&key={2}&mode=walking'.format(str(latitude)+','+str(longitude), str(station[1])+','+str(station[2]), api_key)
    distance_response_dict = simplejson.load(urllib.urlopen(url))

    if distance_response_dict['status'] == 'OK':
        station_google_info = station_google_info.append({'station_name': station[0], 'distance': distance_response_dict['rows'][0]['elements'][0]['distance']['text'],
                                    'duration':distance_response_dict['rows'][0]['elements'][0]['duration']['text'],
                                    'distance_value': distance_response_dict['rows'][0]['elements'][0]['distance']['value']}, ignore_index=True)

def prediction_lookup(stations_df, date, hour):
    df = pd.read_csv("predictions.csv")
    filtered_df = df[(df['station_name'].isin(stations_df['station_name'])) & (df['hour'] == hour) & (df['date'] == date)]
    filtered_df = filtered_df.join(stations_df.set_index('station_name'), on = 'station_name').sort_values('metric', ascending = 0)
    filtered_df['rank'] = range(1,len(filtered_df)+1)
    return filtered_df[['rank', 'station_name', 'distance', 'duration', 'metric']]

date = '18-01-2018'
hour = 1
print prediction_lookup(station_google_info.sort_values('distance_value', ascending = 1).head(), date, hour)
    
