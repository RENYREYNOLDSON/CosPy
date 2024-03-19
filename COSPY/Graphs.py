import matplotlib.animation as animation
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as CTk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


#GRAPHS TO SHOW
#Cohesion
#% in pheromone
#Global pheromone amount
#Pheromone cover
#Amount in area
#Number of robots stopped

class Graph_Frame(CTk.CTkFrame):
    #Constructor 
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        # Have 4 graphs in a grid! These can be changed
        self.data1=[]
        self.data2=[]
        self.data3=[]
        self.data4=[]
        # Configure grid weights to make rows and columns expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # Create matplotlib figures and subplots
        self.fig1, self.ax1 = plt.subplots()
        self.fig2, self.ax2 = plt.subplots()
        self.fig3, self.ax3 = plt.subplots()
        self.fig4, self.ax4 = plt.subplots()
        
        # Create a canvas for each subplot
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self)
        self.canvas3 = FigureCanvasTkAgg(self.fig3, master=self)
        self.canvas4 = FigureCanvasTkAgg(self.fig4, master=self)
        
        # Draw the canvases
        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()
        self.canvas4.draw()
        
        # Pack the canvases into the frame
        self.canvas1.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.canvas2.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        self.canvas3.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        self.canvas4.get_tk_widget().grid(row=1, column=1, sticky="nsew")

    def update_graphs(self,value1,value2,value3,value4):
        self.data1.append(value1)
        self.data2.append(value2)
        self.data3.append(value3)
        self.data4.append(value4)

        x_values=[120 * i for i in range(len(self.data1))]

        # Clear existing plots and plot new data
        self.ax1.clear()
        self.ax1.plot(x_values,self.data1)
        self.canvas1.draw()
        
        self.ax2.clear()
        self.ax2.plot(x_values,self.data2)
        self.canvas2.draw()
        
        self.ax3.clear()
        self.ax3.plot(x_values,self.data3)
        self.canvas3.draw()
        
        self.ax4.clear()
        self.ax4.plot(x_values,self.data4)
        self.canvas4.draw()

