from Tkinter import Tk, Label, Button

from Tkinter import *
import requests
import csv
import geopy.distance
import pandas as pd
import urllib
import simplejson

fields = ['hour', 'day']
OPTIONS = [[1, 2], ['18-01-2018', '19-01-2018']]

def app_lookup(vals):

    #address = raw_input("Enter your address: ")
    #address = "101 Howard Street, San Francisco"
    address = vals[0]
    api_key = "AIzaSyBe81O8VCU4EVkDJ5oBbEHbBn6kXeFZQJE"
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
    df = pd.read_csv("predictions.csv")
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
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        w = OptionMenu(root, variable, *OPTIONS[i])
        w.pack()
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
        global car_header
        global car_list
        car_header = df.columns.get_values()
        car_list = [tuple(row) for row in df.rows()[1]]

        root.title("Multicolumn Treeview/Listbox")
        listbox = MultiColumnListbox()
    '''
    if vals[0] != "":
        df=app_lookup(vals)

        x = df.to_string(header=True,
                  index=False,
                  index_names=False).split("\n")
        vals = [ele for ele in x]
        #print df
        for item in vals:
           # print item
            listbox.insert(END, item)
             
    if str(vals[0]) == '101':
        for item in ["one", "zero", "one"]:
            listbox.insert(END, item)
    elif str(vals[0]) == '102':
        for item in ["one", "zero", "two"]:
            listbox.insert(END, item)
    '''
#    else:
#        for item in ["zero", "zero", "zero"]:
#            listbox.insert(END, item)    
    return vals

try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk

class MultiColumnListbox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()

    def _setup_widgets(self):
        s = """\click on header to sort by that column
to change width of column drag boundary
        """
        msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
            padding=(10, 2, 10, 6), text=s)
        msg.pack(fill='x')
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=car_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def _build_tree(self):
        for item in car_list:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(car_header[ix],width=None)<col_w:
                    self.tree.column(car_header[ix], width=col_w)


def reset_station():
     listbox.delete(0, END)
     #listbox.insert(END, '')        
            
if __name__ == '__main__':
    root = Tk()
 #   listbox = Listbox(root, width = 150, height = 10)
#    listbox.pack(expand = True)
    ents = makeform(root, fields, OPTIONS)
    root.bind('<Return>', (lambda event, e=ents: fetch(e))) 
    global vals
    vals = fetch(ents)
    print vals
    
    b1 = Button(root, text='Show', command=(lambda e=ents: fetch(e)))
    b1.pack(side=LEFT, padx=5, pady=5)
 #   lb = Listbox(root)
    
    b = Button(root, text="Reset",
           command=reset_station)
    b.pack(side=LEFT, padx=5, pady=5)

    
    root.mainloop()

