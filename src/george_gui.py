import tkinter as tk
from tkinter import messagebox as tkMessageBox
class Display:
    def __init__(self):
        self.app = tk.Tk()
        

        self.canvas = tk.Canvas(self.app,width=400,height=400,bg='black')
        self.canvas.pack()
        
        self.button = tk.Button(text="FLY BABY")
        self.button.place(x=200, y=200)
        
        def get_x_and_y(event):
            global lasx, lasy
            lasx, lasy = event.x, event.y
        
        self.coordinates = []
        def draw_smth(event):
            self.coordinates_entryx = {}
            self.corrdinates_entryy = {}
            global lasx, lasy
            self.canvas.create_line((lasx, lasy, event.x, event.y), 
                            fill='white', 
                            width=2)
            lasx, lasy = event.x, event.y
            self.coordinates_entry = [lasx,lasy]
            
            
            if self.coordinates_entry[0] in range(190,210):
                if self.coordinates_entry[1] in range(195,205):
                    print('BULGARIA NUMBER 1')
                    self.canvas.delete('all') 
                    
            self.coordinates.append(self.coordinates_entry)
            return self.coordinates 
        
            
                     
            

        def release(event):
            print(self.coordinates)
            self.coordinates = []

        
        self.canvas.bind("<Button-1>", get_x_and_y)
        self.canvas.bind("<B1-Motion>", draw_smth)
        self.canvas.bind("<ButtonRelease>", release)
        
        
        
        self.app.mainloop()

display = Display()


