from Tkinter import Tk, Label, Button


from Tkinter import *


fields = ['hour', 'day']
OPTIONS = [['2', '3'], ['2', '3']]


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

 

def reset_station():
     listbox.delete(0, END)
     #listbox.insert(END, '')        
            
if __name__ == '__main__':
    root = Tk()
    listbox = Listbox(root)
    listbox.pack()
    ents = makeform(root, fields, OPTIONS)
    root.bind('<Return>', (lambda event, e=ents: fetch(e))) 
    global vals
    vals = fetch(ents)
    print vals
    
    b1 = Button(root, text='Show', command=(lambda e=ents: fetch(e)))
    b1.pack(side=LEFT, padx=5, pady=5)
    lb = Listbox(root)
    
    b = Button(root, text="Reset",
           command=reset_station)
    b.pack(side=LEFT, padx=5, pady=5)

    root.mainloop()