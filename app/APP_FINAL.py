from Tkinter import Tk, Label, Button

from Tkinter import *
import requests
import csv
import geopy.distance
import pandas as pd
import urllib
import simplejson
try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
    
fields = ['Hour', 'Date']
OPTIONS = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ,12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
           ['01-19-2018', '01-20-2018', '01-21-2018', '01-22-2018', '01-23-2018', '01-24-2018', '01-25-2018', '01-26-2018']]

def app_lookup(vals):

    #address = raw_input("Enter your address: ")
    #address = "101 Howard Street, San Francisco"
    address = vals[0]
    api_key = "AIzaSyD8Jpw9ibPED4v1pwUygH4tP4IuYG4kiUw"
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

    stations_df = station_google_info.sort_values('distance_value', ascending = 1).head()
    df = pd.read_csv("nearest_station_df.csv")
    filtered_df = df[(df['station_name'].isin(stations_df['station_name'])) & (df['hour'] == int(vals[1])) & (df['date'] == vals[2])]
    filtered_df = filtered_df.join(stations_df.set_index('station_name'), on = 'station_name').sort_values('metric', ascending = 0)
    filtered_df['rank'] = range(1,len(filtered_df)+1)

    return filtered_df[['rank', 'station_name', 'distance', 'duration', 'metric']]

def makeform(root, fields, OPTIONS):
    entries = []
    row = Frame(root)
    lab = Label(row, width=15, text='Location', anchor='w')
    ent = Entry(row)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    lab.pack(side=LEFT)
    ent.pack(side=RIGHT, expand=YES, fill=X)
    entries.append(('Location', ent))
    for i in range(0, 2):        
        variable = StringVar(root)
        variable.set(OPTIONS[i][0]) # default value
        row = Frame(root)
        lab = Label(row, width=15, text=fields[i], anchor='w')
        lab.pack(side=LEFT)
        w = OptionMenu(row, variable, *OPTIONS[i])
        w.pack(side=LEFT)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        entries.append((fields[i], variable))
        #val = variable.get()
    return entries   


def fetch(entries):
    #global entries
    vals = []
    for entry in entries:
        field = entry[0]
        text = entry[1].get()
        print('%s: "%s"' % (field, text)) 
        vals.append(text)

    
    if vals[0] != "":
        df = app_lookup(vals)
        print vals[0]
 #       car_header = list(df.columns.values)
        print df
        car_list = [tuple(row[1]) for row in df.iterrows()]
        for col in car_header:
            tree.heading(col, text=col.title())
        for item in car_list:
            tree.insert('', 'end', values=item)   
    return vals



def reset_station():
#     listbox.delete(0, END)
     #listbox.insert(END, '')
    tree.delete(*tree.get_children())
            
if __name__ == '__main__':
    root = Tk()
 #   listbox = Listbox(root, width = 150, height = 10)
#    listbox.pack(expand = True)
    ents = makeform(root, fields, OPTIONS)
    root.bind('<Return>', (lambda event, e=ents: fetch(e))) 
    global vals
    vals = fetch(ents)
    print vals

    fm = Frame(root)
    b1 = Button(fm, text='Show', command=(lambda e=ents: fetch(e)))
    b1.pack(side=LEFT, padx=5, pady=5)
 #   lb = Listbox(root)
    
    b = Button(fm, text="Reset",
           command=reset_station)
    b.pack(side=LEFT, padx=5, pady=5)
    fm.pack(fill=BOTH, expand = YES)
    car_header = ['rank', 'station_name', 'distance', 'duration', 'metric']
    root.title("GoBike Station Recommendation")
    container = ttk.Frame()
    container.pack(fill='both', expand=True)
    tree = ttk.Treeview(columns=car_header, show="headings")
    tree.grid(column=0, row=0, sticky='nsew', in_=container)
    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)
    
    root.mainloop()

