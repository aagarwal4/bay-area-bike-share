import requests
import csv
import geopy.distance

address = raw_input("Enter your address: ")
#address = "101 Howard Street, San Francisco"
api_key = "AIzaSyArR8tSLIxffYvFWBtM5Xyu_3nQXwog5uA"
api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
api_response_dict = api_response.json()

if api_response_dict['status'] == 'OK':
    latitude = api_response_dict['results'][0]['geometry']['location']['lat']
    longitude = api_response_dict['results'][0]['geometry']['location']['lng']
#    print 'Latitude:', latitude
#    print 'Longitude:', longitude

mylist = []
distances = []
mycoords = (latitude, longitude)

with open('station.csv','rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        mylist.append(tuple(row[1:4]))

#for station in mylist[1:]:
#    distances.append((station[0], geopy.distance.vincenty(mycoords, (station[1],station[2]))))

#distance_sorted = sorted(distances, key = lambda x: x[1])

#print("The nearest stations are: ")
#i = 1
#for station in distance_sorted[0:5]:
#    print "Nearest " + str(i) + " station is " + station[0]
#    print "Distance is " + str(station[1])
#    i = i + 1
 
#Using distance matrix API

new_distances = []
for station in mylist[1:]:
    distance_response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={0}&destinations={1}&key={2}'.format(str(latitude)+','+str(longitude), str(station[1])+','+str(station[2]), api_key))
    distance_response_dict = distance_response.json()

    if distance_response_dict['status'] == 'OK':
        distance = distance_response_dict['rows'][0]['elements'][0]['distance']['text']
        distance_value = distance_response_dict['rows'][0]['elements'][0]['distance']['value']
	duration = distance_response_dict['rows'][0]['elements'][0]['duration']['text']
	duration_value = distance_response_dict['rows'][0]['elements'][0]['duration']['value']
        new_distances.append((station[0],distance,distance_value,duration,duration_value))
    
distance_sorted = sorted(new_distances, key = lambda x: x[2])
duration_sorted = sorted(new_distances, key = lambda x: x[4])

print("The nearest stations by distance are: ")
i = 1
for station in distance_sorted[0:5]:
    print "Nearest " + str(i) + " station is " + station[0]
    print "Distance is " + station[1]
    print "Duration is " + station[3]
    print "\n"
    i = i + 1    

print("\n\nThe nearest stations by duration are: ")
i = 1      
for station in duration_sorted[0:5]:
    print "Nearest " + str(i) + " station is " + station[0]
    print "Duration is " + station[3]
    print "Distance is " + station[1]
    print "\n"
    i = i + 1
