from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from copy import deepcopy
import numpy as np
import time
from client import *
from threading import Thread

# sizing properties
window_width  = 500
window_height = 400
canvas_width = 300
canvas_height = 300

# padding properties
overall_padding = 5

class Applet(Tk):

    def __init__(self):

        # initialize applet parent object
        super(Applet, self).__init__()
        
        # top level properties
        self.title("Magic Wand")
        self.minsize(width=window_width, height=window_height)
        self.configure(background='grey')
        self.coordinates = []
        self.flight_coordinates = []
        self.dts = []
        self.prev_time = time.time()
        self.abort = False
        
        # create all the objects
        self.createCanvas()
        self.createFlightControl()
        self.createModeSelection()
        self.createPlaneSelection()
        self.createClear()
        
        # create client
        self.client = SimpleClient(use_controller=False, use_observer=False, channel=self.channel.get())
        
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
    
        # create flight button
        self.flightButton = ttk.Button(self.flightControlFrame, text="Run Flight", command=self.runFlight)
        self.flightButton.grid(column=0, row=0, padx=overall_padding, pady=overall_padding)
        
        # create abort button
        self.abortButton = ttk.Button(self.flightControlFrame, text="Abort", command=self.abortFlight)
        self.abortButton.grid(column=0, row=1, padx=overall_padding, pady=overall_padding)

        # create connect button
        self.connectButton = ttk.Button(self.flightControlFrame, text="Connect", command=self.connectClient)
        self.connectButton.grid(column=1, row=0, padx=overall_padding, pady=overall_padding)
        
        # text input for channel selection
        self.channel_label = ttk.Label(self.flightControlFrame, text="Channel")
        self.channel_label.grid(column=2, row=0, padx=overall_padding, pady=overall_padding)
        self.channel = IntVar(value=58)
        ttk.Entry(self.flightControlFrame, textvariable=self.channel).grid(column=3, row=0, padx=overall_padding, pady=overall_padding)
        
        # text input for square width
        self.flight_zone_label = ttk.Label(self.flightControlFrame, text="Flight Zone (m)")
        self.flight_zone_label.grid(column=2, row=1, padx=overall_padding, pady=overall_padding)
        self.flight_zone = StringVar(value='2.5')
        ttk.Entry(self.flightControlFrame, textvariable=self.flight_zone).grid(column=3, row=1, padx=overall_padding, pady=overall_padding)
        
        # text input for connection status
        self.is_connected = StringVar()
        self.is_connected.set(str(False))
        self.connection_status_label = ttk.Label(self.flightControlFrame, textvariable=self.is_connected)
        self.connection_status_label.grid(column=4, row=0, padx=overall_padding, pady=overall_padding)
 
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
    
    # action when 'Connect' button is clicked
    def connectClient(self):
        self.client = SimpleClient(use_controller=False, use_observer=False, channel=self.channel.get())
        self.is_connected.set(str(self.client.is_connected))
        self.client.connect()
        self.is_connected.set(str(self.client.is_connected))

    # convert from world coordinates to canvas pixels
    def convert_pixel_to_world(self):
        self.flight_coordinates = np.divide(self.coordinates, canvas_width/float(self.flight_zone.get()))

    # convert from canvas pixels to world coordinates, typecast as integers as well
    def convert_world_to_pixel(self):
        self.flight_data = np.divide(self.flight_data, float(self.flight_zone.get())/canvas_width)
        self.flight_data = [(int(x[1]), int(x[0])) for x in self.flight_data]

    # action when 'Flight' button is clicked
    def runFlight(self):
        
        # make sure we got coordinates and are connected
        if (len(self.flight_coordinates) == 0) or (not self.client.is_connected):
            return
        
        # run the flight thread
        self.flight_thread = Thread(target = self.client.flight, args = (self.flight_coordinates, self.dts))
        self.flight_thread.start()        
        self.flight_thread.join()
        self.dts = []
        
        # check if flight aborted
        if self.abort:
            return
        
        # run post-flight procedures
        self.postFlight()
        self.abort = False
    
    # action when 'Abort' button is clicked
    def abortFlight(self):
        self.client.cf.close_link()
        self.flight_thread.join()
        self.abort = True
        
    # action after landing
    def postFlight(self):
        
        # make sure flight wasn't aborted
        if self.abort:
            return
        
        # convert to flight coordinates tuples
        self.flight_data = []
        for idx in range(len(self.client.data['stateEstimate.x']['data'])):
            
            # record data if timestamp is within plotted location
            if self.client.data['start_time'] < self.client.data['stateEstimate.x']['time'][idx] < self.client.data['end_time']:
                self.flight_data.append((self.client.data['stateEstimate.x']['data'][idx], self.client.data['stateEstimate.y']['data'][idx]))
        
        # obtain o_x, o_y and convert to pixels
        self.convert_world_to_pixel()
                
        # plot data onto canvas
        lastx, lasty = self.flight_data[0][0], self.flight_data[0][1]
        for coord in self.flight_data[1:]:
            self.canvas.create_line(lastx, lasty, coord[0], coord[1], fill='green')
            lastx, lasty = coord[0], coord[1]
        
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
        self.canvas.create_line(lastx, lasty, event.x, event.y)
        self.savePosn(event)


if __name__ == '__main__':
    app = Applet()
    app.mainloop()

        
