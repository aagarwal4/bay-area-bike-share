from Tkinter import Tk, Label, Button
'''
class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
'''

from Tkinter import *
'''
def printSomething():

    label = Label(root, text= "<a>Hey, I printed you!</a><a>Hey, I printed you!</a>")
    label.pack() 

root = Tk()
button = Button(root, text="Show me the nearest stations", command=printSomething) 
button.pack()

root.mainloop()
'''

'''
master = Tk()

listbox = Listbox(master)
listbox.pack()

listbox.insert(END, "Nearest stations:")

for item in ["one", "two", "three", "four"]:
    listbox.insert(END, item)


mainloop()
'''



fields = 'Location', 'hour', 'day'


def fetch(entries):
    #global entries
    vals = []
    for entry in entries:
        field = entry[0]
        text = entry[1].get()
        print('%s: "%s"' % (field, text)) 
        vals.append(text)
    if str(vals[0]) == '101':
        for item in ["one", "zero", "one"]:
            listbox.insert(END, item)
    elif str(vals[0]) == '102':
        for item in ["one", "zero", "two"]:
            listbox.insert(END, item) 
#    else:
#        for item in ["zero", "zero", "zero"]:
#            listbox.insert(END, item)    
    return vals
      

def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries

def stations_nearby(vals):
    if str(vals[0]) == '101':
        for item in ["one", "zero", "one"]:
            listbox.insert(END, item)
    elif str(vals[0]) == '102':
        for item in ["one", "zero", "two"]:
            listbox.insert(END, item) 
    else:
        for item in ["zero", "zero", "zero"]:
            listbox.insert(END, item) 
        
        
'''            
def stations_nearby():
    for item in items:
        listbox.insert(END, item)
'''    

def print_station(item):
     istbox.insert(END, item)        
            
if __name__ == '__main__':
    root = Tk()
    listbox = Listbox(root)
    listbox.pack()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e))) 
    global vals
    vals = fetch(ents)
    print vals 
    b1 = Button(root, text='Show', command=(lambda e=ents: fetch(e)))
    b1.pack(side=LEFT, padx=5, pady=5)
    #b2 = Button(root, text='Quit', command=root.quit)
    #b2.pack(side=LEFT, padx=5, pady=5)
    #button = Button(root, text="Show me the nearest stations", command=(lambda v=vals: stations_nearby(v))) 
    #button.pack(side=LEFT, padx=5, pady=5)
    root.mainloop()