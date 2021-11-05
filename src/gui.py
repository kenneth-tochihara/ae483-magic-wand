from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from copy import deepcopy

class Applet(Tk):

    def __init__(self, client):

        # initialize applet parent object
        super(Applet, self).__init__()
        self.client = client
        
        # top level properties
        self.title("Magic Wand")
        self.minsize(width=500, height=400)

        # drawing section
        self.canvasFrame = ttk.Frame(self)
        self.canvasFrame.grid(column=0, row=0)
        self.canvasFrame.canvas = Canvas(self, width=500, height=300)
        self.canvasFrame.canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        self.canvasFrame.canvas.bind("<Button-1>", self.savePosn)
        self.canvasFrame.canvas.bind("<B1-Motion>", self.addLine)
        self.canvasFrame.canvas.bind("<ButtonRelease-1>", self.onRelease)
        self.coordinates = []
        
        # run flight button
        self.flightButtonFrame = ttk.Frame(self)
        self.button = ttk.Button(text="Fucking fly", command=self.runFlight)
        self.button.place(x=250, y=350)
    
    def runFlight(self):
        self.canvasFrame.canvas.delete('all')
        print('shheesh')

    # action when mouse click is released
    def onRelease(self, event):
        self.client.get_coordinates(self.coordinates)
        self.coordinates = []
        
    # action when mouse is clicked
    def savePosn(self, event):
        global lastx, lasty
        lastx, lasty = event.x, event.y
        self.coordinates.append((event.x, event.y))

    # action when mouse is dragged
    def addLine(self, event):
        self.canvasFrame.canvas.create_line((lastx, lasty, event.x, event.y))
        self.savePosn(event)
        

if __name__ == '__main__':
    app = Applet()
    app.mainloop()

        
