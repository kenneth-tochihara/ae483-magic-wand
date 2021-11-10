from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from copy import deepcopy
# import main

# sizing properties
window_width  = 500
window_height = 400
canvas_width = 500
canvas_height = 300

# padding properties
overall_padding = 5

# flags
ob_flag = False

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
        
        # create all the objects
        self.createCanvas()
        self.createFlightButton()
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
        
    # create flight button
    def createFlightButton(self):
        self.flightButton = ttk.Button(self, text="Run Flight", command=self.runFlight)
        self.flightButton.place(x=0, y=0)
        self.flightButton.grid(column=1, row=2, padx=overall_padding, pady=overall_padding)
    
    # create mode selection dropdown
    def createModeSelection(self):
        
        # create mode selection frame
        self.modeSelectionFrame = ttk.LabelFrame(self, text="Mode Selection",)
        self.modeSelectionFrame.grid(column=0, row=0, padx=overall_padding, pady=overall_padding)
        
        # set default mode
        self.modes = ["copycat", "spellcaster", "live"]
        self.mode = StringVar()
        self.mode.set(self.modes[0])
        
        # create dropdown menu
        ttk.OptionMenu(self.modeSelectionFrame, self.mode, *self.modes).pack()
    
    # create plane selection
    def createPlaneSelection(self):
        
        # create plane selection frame
        self.planeSelectionFrame = ttk.LabelFrame(self, text="Plane Selection")
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
    
    # action when 'Flight' button is clicked
    def runFlight(self):
        # normalize based on the window size
        self.coordinates = np.divide(self.coordinates, canvas_width)
        # rescale to whatever relevant physical situation
        flight_zone = 1.5 # client.move interprets meters
        self.coordinates *= flight_zone
        # client.move smooth returns home in client code!
        new_coordinates = self.coordinates
        return new_coordinates

    # action when 'Clear' button is clicked
    def clearFlight(self):
        self.canvas.delete('all')
        print('shheesh')

    # action when mouse click is released
    def onRelease(self, event):
        global ob_flag
        
        if ob_flag: 
            ob_flag = False
        else:
            self.client.get_coordinates(self.coordinates)
            print(self.coordinates)
            self.coordinates = []
        
    # action when mouse is clicked
    def savePosn(self, event):
        global lastx, lasty, ob_flag
        
        # verify position is in canvas
        if (0 < event.x < canvas_width + (overall_padding*2) - 1) and (0 < event.y < canvas_height + (overall_padding*2) - 1):
            lastx, lasty = event.x, event.y
            self.coordinates.append((event.x, event.y))
        else:
            self.onRelease(None)
            ob_flag = True

    # action when mouse is dragged
    def addLine(self, event):
        self.canvas.create_line((lastx, lasty, event.x, event.y))
        self.savePosn(event)
        

if __name__ == '__main__':
    app = Applet()
    app.mainloop()

        
