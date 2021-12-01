from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from copy import deepcopy
import numpy as np
import time
import json

# sizing properties
window_width  = 500
window_height = 400
canvas_width = 300
canvas_height = 300
flight_zone = 2.5 # m

# padding properties
overall_padding = 5

class Applet(Tk):

    def __init__(self, client):

        # initialize applet parent object
        super(Applet, self).__init__()
        self.client = client
        
        # top level properties
        self.title("Magic Wand")
        self.minsize(width=window_width, height=window_height)
        self.configure(background='grey')
        self.coordinates = []
        self.dts = []
        self.prev_time = time.time()
        
        # create all the objects
        self.createCanvas()
        self.createFlightControl()
        self.createModeSelection()
        self.createPlaneSelection()
        self.createClear()
        
    # create canvas section
    def createCanvas(self):
        self.canvas = Canvas(self, width=canvas_width, height=canvas_height)
        self.canvas.grid(column=1, row=0, sticky=(N, W, E, S), padx=overall_padding, pady=overall_padding, rowspan=2)
        self.canvas.bind("<Button-1>", self.savePosn)
        self.canvas.bind("<B1-Motion>", self.addLine)
        self.canvas.bind("<ButtonRelease-1>", self.onRelease)
        
    # create flight control buttons
    def createFlightControl(self):
        
        # create flight control frame
        self.flightControlFrame = ttk.Frame(self)
        self.flightControlFrame.grid(column=1, row=2, padx=overall_padding, pady=overall_padding)
        
        # create connect button
        self.connectButton = ttk.Button(self.flightControlFrame, text="Connect", command=self.client.connect)
        self.connectButton.grid(column=0, row=0, padx=overall_padding, pady=overall_padding)
    
        # create flight button
        self.flightButton = ttk.Button(self.flightControlFrame, text="Run Flight", command=self.runFlight)
        self.flightButton.grid(column=0, row=1, padx=overall_padding, pady=overall_padding)
        
        # create abort button
        self.abortButton = ttk.Button(self.flightControlFrame, text="Abort")
        self.abortButton.grid(column=0, row=2, padx=overall_padding, pady=overall_padding)
    
    # create mode selection dropdown
    def createModeSelection(self):
        
        # create mode selection frame
        self.modeSelectionFrame = ttk.LabelFrame(self, text="Mode Selection", labelanchor="n")
        self.modeSelectionFrame.grid(column=0, row=0, padx=overall_padding, pady=overall_padding)
        
        # set default mode
        self.modes = ["", "Copycat", "Spellcaster", "Live"]
        self.mode = StringVar()
        self.mode.set(self.modes[1])
        
        # create dropdown menu
        self.modeSelectionOptionMenu = ttk.OptionMenu(self.modeSelectionFrame, self.mode, *self.modes)
        self.modeSelectionOptionMenu.pack()
        self.modeSelectionOptionMenu.configure(width=len(max(self.modes, key=len)))
    
    # create plane selection
    def createPlaneSelection(self):
        
        # create plane selection frame
        self.planeSelectionFrame = ttk.LabelFrame(self, text="Plane Selection", labelanchor="n")
        self.planeSelectionFrame.grid(column=0, row=1, padx=overall_padding, pady=overall_padding)
        
        # set default plane
        planes = ['XY', 'XZ', 'YZ']
        self.plane = StringVar()
        self.plane.set(planes[0])
        
        # create radio buttons
        ttk.Radiobutton(self.planeSelectionFrame, text=planes[0], variable=self.plane, value=planes[0]).pack()
        ttk.Radiobutton(self.planeSelectionFrame, text=planes[1], variable=self.plane, value=planes[1]).pack()
        ttk.Radiobutton(self.planeSelectionFrame, text=planes[2], variable=self.plane, value=planes[2]).pack()
        
    # create clear button
    def createClear(self):
        self.clearSelectionButton = ttk.Button(self, text="Clear", command=self.clearFlight)
        self.clearSelectionButton.place(x=0, y=0)
        self.clearSelectionButton.grid(column=0, row=2, padx=overall_padding, pady=overall_padding)
    
    # create data saving interface
    def createDataSave(self):
        pass
    
    def convert_pixel_to_world(self):
        # call to the gui for translated coordinates
        # run get_coordinates
        self.flight_coordinates = np.divide(self.coordinates, canvas_width)
        # rescale to whatever relevant physical situation
        flight_zone = 2.5 # client.move interprets meters
        self.flight_coordinates *= flight_zone
        # client.move smooth returns home in client code!
        
    def convert_world_to_pixel(self):
        
        # convert from canvas pixels to world coordinates
        self.flight_coordinates = np.divide(self.coordinates, canvas_width/flight_zone)

    # action when 'Flight' button is clicked
    def runFlight(self):
        self.client.flight(self.flight_coordinates, self.dts)
        self.dts = []
        # print(type(self.client.data['stateEstimate.x']))
        print(self.client.data['stateEstimate.x']['data'])
        self.postFlight()
        
    def postFlight(self):
        
        # convert to flight coordinates tuples
        self.flight_coordinates = []
        for idx in range(len(self.client.data['stateEstimate.x']['data'])):
            self.flight_coordinates.append((self.client.data['stateEstimate.x']['data'][idx], 
                                            self.client.data['stateEstimate.y']['data'][idx]))
        
        # obtain o_x, o_y and convert to pixels
        self.flight_coordinates = np.divide(self.flight_coordinates, flight_zone/canvas_width) 
        self.flight_coordinates = [(int(x[0]), int(x[1])) for x in self.flight_coordinates]
        print(self.flight_coordinates)
        
        # plot data onto canvas
        lastx, lasty = self.flight_coordinates[0][0], self.flight_coordinates[0][1]
        for coord in self.flight_coordinates[1:]:
            self.canvas.create_line((lastx, lasty, coord[0], coord[1]))
            
        
        pass
        
    # action when 'Clear' button is clicked
    def clearFlight(self):
        self.canvas.delete('all')
        self.coordinates = []

    # action when mouse click is released
    def onRelease(self, event):
        
        # convert coordinates and flush pixel coordinates
        self.convert_pixel_to_world()
        self.coordinates = []
        
    # action when mouse is clicked
    def savePosn(self, event):
        global lastx, lasty
            
        # verify position is in canvas
        lastx, lasty = event.x, event.y
        self.coordinates.append((event.x, event.y))
        self.dts.append(time.time()-self.prev_time)                         
        
        # get the time between each event
        self.prev_time = time.time()

    # action when mouse is dragged
    def addLine(self, event):
        
        # boundary check, x
        if overall_padding > event.x: event.x = overall_padding
        elif event.x > canvas_width: event.x = canvas_width
        
        # boundary check, y
        if overall_padding > event.y: event.y = overall_padding
        elif event.y > canvas_height: event.y = canvas_height
        
        # draw line and save position
        self.canvas.create_line((lastx, lasty, event.x, event.y))
        self.savePosn(event)

    def json_load(filename):
    # load raw data
        with open(filename, 'r') as f:
            data = json.load(f)

        # convert lists to numpy arrays
        for val in data.values():
            for key in val.keys():
                val[key] = np.array(val[key])

    def graph_data(self):
        print(self.client.data)
        # t = data['time']

        # # states
        # o_x = data['stateEstimate.x']
        # o_y = data['stateEstimate.y']

        # i = 0
        # for i in range(len(o_x)):

        #     self.canvas.create_line(o_x[i],o_y[i],o_x[i+1],o_y[i+1])
        #     i += 1

if __name__ == '__main__':
    app = Applet()
    app.mainloop()

        
