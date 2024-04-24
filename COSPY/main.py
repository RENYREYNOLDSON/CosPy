########################
########################
########################  MAIN CODE FOR COSPY
######################## 
########################
########################

from tkinter import *
import customtkinter as CTk
import datetime
import threading
import os
import sdl2
from Render import *
from Robots import *
from Graphs import *
from customtkinter.windows.widgets.core_widget_classes.dropdown_menu import DropdownMenu
from tkinter.colorchooser import askcolor
from PIL import Image


class Menu(CTk.CTkFrame):
    #Constructor 
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        #FRAME SETUP
        # File
        var = CTk.StringVar(value="File")
        self.file=CTk.CTkOptionMenu(master=self,anchor="center",variable=var,values=["File"],width=100,corner_radius=0,bg_color="transparent")
        self.file.configure(button_color="#161616",fg_color="#161616")

        #menu_recent = DropdownMenu(self.file,values=["new"])
        self.file._dropdown_menu.add_command(label="New Test", accelerator="Ctrl+N")
        #self.file._dropdown_menu.insert_cascade(3,menu=menu_recent, label='Open Recent')
        self.file._dropdown_menu.add_command(label="Open Test", accelerator="Ctrl+O")
        self.file._dropdown_menu.add_command(label="Save Test", accelerator="Ctrl+S",command=master.save_test)
        self.file.pack(side="left")

        self.start_button = CTk.CTkButton(master=self,text="⟳",corner_radius=0,width=40,command=self.master.reset,fg_color="transparent")
        self.start_button.pack(side="right")
        self.record_button = CTk.CTkButton(master=self,text="⏺",corner_radius=0,width=40,fg_color="transparent",command=self.master.toggle_recording)
        self.record_button.pack(side="right")
        self.start_button = CTk.CTkButton(master=self,text="▶⏸",corner_radius=0,width=40,fg_color="transparent",command=self.master.set_running)
        self.start_button.pack(side="right")
        #Simulation speed
        self.speed_slider = CTk.CTkSlider(master=self,number_of_steps=3,command=master.update_speed)
        self.speed_slider.set(0)
        self.speed_slider.pack(side="right")
        self.speed_label = CTk.CTkLabel(master=self,text="Speed: x1")
        self.speed_label.pack(side="right")
        self.framerate_text = CTk.CTkLabel(master=self,text="Framerate: ",width=100,anchor="w",text_color="grey")
        self.framerate_text.pack(side="left",padx=(200,0))
        self.timestep_text = CTk.CTkLabel(master=self,text="Time Step: 0",text_color="grey")
        self.timestep_text.pack(side="left")

# FRAME SETUP FRAME
class Frame_Setup(CTk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2),weight=1,uniform="column")
        #Size
        self.size_text = CTk.CTkLabel(master=self,text="Size",padx=20,anchor="w",text_color="#a4a4a4")
        self.size_text.grid(row=0,column=0,sticky="NSWE")
        self.width = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.width.grid(row=0,column=1)
        self.width.insert(0,1960)#MAX SIZE 1960, MIN SIZE 400
        self.height = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.height.grid(row=0,column=2)
        self.height.insert(0,1460)#MAX SIZE 1460, MIN SIZE 400
        #Scale
        self.scale_text = CTk.CTkLabel(master=self,text="Scale",padx=20,anchor="w",text_color="#a4a4a4")
        self.scale_text.grid(row=1,column=0,sticky="NSEW")
        self.scale = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.scale.insert(0,0.25)
        self.scale.grid(row=1,column=1,columnspan=2,sticky="NSEW")

    def get_width(self):
        width = int(self.width.get())
        if width<400:
            width = 400
            self.width.delete(0,"end")
            self.width.insert(0,"400")
        elif width>1960:
            width=1960
            self.width.delete(0,"end")
            self.width.insert(0,"1960")
        return width
    
    def get_height(self):
        height = int(self.height.get())
        if height<400:
            height = 400
            self.height.delete(0,"end")
            self.height.insert(0,"400")
        elif height>1460:
            height=1460
            self.height.delete(0,"end")
            self.height.insert(0,"1460")
        return height

# ENVIRONMENT SETUP FRAME
class Environment_Setup(CTk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2),weight=1,uniform="column")
        #Evaporation Rate
        self.evap_text = CTk.CTkLabel(master=self,text="Evaporation Rate",padx=20,anchor="w",text_color="#a4a4a4")
        self.evap_text.grid(row=4,column=0,sticky="NSWE")
        self.evaporation_rate = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.evaporation_rate.insert(0,4)
        self.evaporation_rate.grid(row=4,column=1,columnspan=2,sticky="NSEW")
        #Diffusion Rate
        self.diffusion_text = CTk.CTkLabel(master=self,text="Diffusion Rate",padx=20,anchor="w",text_color="#a4a4a4")
        self.diffusion_text.grid(row=5,column=0,sticky="NSWE")
        self.diffusion = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.diffusion.insert(0,2)
        self.diffusion.grid(row=5,column=1,columnspan=2,sticky="NSEW")
        #Wind Rate
        self.wind_text = CTk.CTkLabel(master=self,text="Wind Rate",padx=20,anchor="w",text_color="#a4a4a4")
        self.wind_text.grid(row=6,column=0,sticky="NSWE")
        self.windx = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.windx.grid(row=6,column=1)
        self.windx.insert(0,0)
        self.windy = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.windy.grid(row=6,column=2)
        self.windy.insert(0,0)
        #Boundary Function
        self.boundary_text = CTk.CTkLabel(master=self,text="Boundary Function",padx=20,anchor="w",text_color="#a4a4a4")
        self.boundary_text.grid(row=10,column=0,sticky="NSWE")
        self.boundary_function = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["Bounce","Wrap","Stop"],command=master.master.master.master.set_boundary_function)
        self.boundary_function.grid(row=10,column=1,columnspan=2,sticky="NSEW")
        #Temperature?
        text = CTk.CTkLabel(master=self,text="Temperature",padx=20,anchor="w",text_color="#a4a4a4")
        text.grid(row=11,column=0,sticky="NSEW")
        self.temperature = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="",command=self.master.master.master.master.set_temperature)
        self.temperature.grid(row=11,column=1,columnspan=3,sticky="EW")
        """
        #Temp Strength
        text = CTk.CTkLabel(master=self,text="Temp Strength",padx=20,anchor="w",text_color="#a4a4a4")
        text.grid(row=12,column=0,sticky="NSWE")
        self.strength = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.strength.insert(0,2)
        self.strength.grid(row=12,column=1,columnspan=2,sticky="NSEW")
        """
        #Temperature Colour
        text = CTk.CTkLabel(master=self,text="Temp Colour",padx=20,anchor="w",text_color="#a4a4a4")
        text.grid(row=13,column=0,sticky="NSEW")
        self.colour = CTk.CTkButton(master=self,corner_radius=0,border_width=0,text="#00FF00",fg_color="#00FF00",command=self.change_colour)
        self.colour.grid(row=13,column=1,columnspan=2,sticky="EW")
        #Aggregation Size
        self.aggregation_text = CTk.CTkLabel(master=self,text="Aggregation R",padx=20,anchor="w",text_color="#a4a4a4")
        self.aggregation_text.grid(row=14,column=0,sticky="NSWE")
        self.aggregation = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.aggregation.insert(0,400)
        self.aggregation.grid(row=14,column=1,columnspan=2,sticky="NSEW")


    #Open the text colour picker
    def change_colour(self):
        colors = askcolor(title="Temoerature Color Chooser")
        if colors!=None:
            self.colour.configure(fg_color=colors[1],text=str(colors[1]))

    def get_colour(self):
        hex_code = self.colour.cget("text")
        # Remove '#' if present
        hex_code=hex_code.replace("#","")
        # Convert hex to RGBA
        r = int(hex_code[0:2], 16) 
        g = int(hex_code[2:4], 16) 
        b = int(hex_code[4:6], 16) 
        return [b, g, r, 255]
    
    def get_boundary_function(self):
        return self.boundary_function.get()
    
    def get_use_temperature(self):
        return self.temperature.get()

class Robot_Setup(CTk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2),weight=1,uniform="column")
        #Robot Speed
        self.speed_text = CTk.CTkLabel(master=self,text="Robot Speed",padx=20,anchor="w",text_color="#a4a4a4")
        self.speed_text.grid(row=0,column=0,sticky="NSEW")
        self.speed = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.speed.insert(0,0.5)
        self.speed.grid(row=0,column=1,columnspan=2,sticky="NSEW")
        #Angle Change Rate
        self.angle_rate_text = CTk.CTkLabel(master=self,text="Turn Speed",padx=20,anchor="w",text_color="#a4a4a4")
        self.angle_rate_text.grid(row=1,column=0,sticky="NSEW")
        self.angle_rate = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.angle_rate.insert(0,0.4)
        self.angle_rate.grid(row=1,column=1,columnspan=2,sticky="NSEW")
        #Randomness
        self.randomness_text = CTk.CTkLabel(master=self,text="Randomness",padx=20,anchor="w",text_color="#a4a4a4")
        self.randomness_text.grid(row=2,column=0,sticky="NSEW")
        self.randomness = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.randomness.insert(0,0.4)
        self.randomness.grid(row=2,column=1,columnspan=2,sticky="NSEW")
        #Deposit Size
        self.deposit_text = CTk.CTkLabel(master=self,text="Deposit Size",padx=20,anchor="w",text_color="#a4a4a4")
        self.deposit_text.grid(row=3,column=0,sticky="NSEW")
        self.deposit_size = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.deposit_size.insert(0,50)
        self.deposit_size.grid(row=3,column=1,columnspan=2,sticky="NSEW")
        #Deposit Rate
        self.deposit_text = CTk.CTkLabel(master=self,text="Deposit Rate",padx=20,anchor="w",text_color="#a4a4a4")
        self.deposit_text.grid(row=4,column=0,sticky="NSEW")
        self.deposit_rate = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.deposit_rate.insert(0,2)
        self.deposit_rate.grid(row=4,column=1,columnspan=2,sticky="NSEW")
        #Pheromone Detection Distance
        self.pheromone_dist_text = CTk.CTkLabel(master=self,text="Detect Radius",padx=20,anchor="w",text_color="#a4a4a4")
        self.pheromone_dist_text.grid(row=5,column=0,sticky="NSEW")
        self.pheromone_dist = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.pheromone_dist.insert(0,25)
        self.pheromone_dist.grid(row=5,column=1,columnspan=2,sticky="NSEW")
        #Robot Detection Distance
        self.robot_dist_text = CTk.CTkLabel(master=self,text="Collide Radius",padx=20,anchor="w",text_color="#a4a4a4")
        self.robot_dist_text.grid(row=6,column=0,sticky="NSEW")
        self.robot_dist = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.robot_dist.insert(0,10)
        self.robot_dist.grid(row=6,column=1,columnspan=2,sticky="NSEW")
       #Number of robots
        self.robot_text = CTk.CTkLabel(master=self,text="Robot Count",padx=20,anchor="w",text_color="#a4a4a4")
        self.robot_text.grid(row=7,column=0,sticky="NSEW")
        self.robot_count = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=20,border_width=1)
        self.robot_count.insert(0,20)
        self.robot_count.grid(row=7,column=1,columnspan=2,sticky="EW")
        #Proportion of leader robots
        self.leader_text = CTk.CTkLabel(master=self,text="Leader Proportion",padx=20,anchor="w",text_color="#a4a4a4")
        self.leader_text.grid(row=8,column=0,sticky="NSEW")
        self.leader = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=20,border_width=1)
        self.leader.insert(0,0.1)
        self.leader.grid(row=8,column=1,columnspan=2,sticky="EW")
        #Pheromone Colour
        self.colour_text = CTk.CTkLabel(master=self,text="Pheromone Colour",padx=20,anchor="w",text_color="#a4a4a4")
        self.colour_text.grid(row=9,column=0,sticky="NSEW")
        self.colour = CTk.CTkButton(master=self,corner_radius=0,border_width=1,fg_color="#FF0000",text="#FF0000",command=self.change_colour)
        self.colour.grid(row=9,column=1,columnspan=2,sticky="EW")
        #Collisions
        self.collisions_text = CTk.CTkLabel(master=self,text="Collisions",padx=20,anchor="w",text_color="#a4a4a4")
        self.collisions_text.grid(row=10,column=0,sticky="NSEW")
        self.collisions = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["Ignore","Stop","Stop linear to temperature","Stop exponential to temperature"])
        self.collisions.grid(row=10,column=1,columnspan=2,sticky="NSEW")
        #Collision Stop Time
        self.stop_text = CTk.CTkLabel(master=self,text="Stop Time",padx=20,anchor="w",text_color="#a4a4a4")
        self.stop_text.grid(row=11,column=0,sticky="NSEW")
        self.stop_time = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=20,border_width=1)
        self.stop_time.insert(0,100)
        self.stop_time.grid(row=11,column=1,columnspan=2,sticky="EW")
        #Collision IMMUNE Time
        self.immune_text = CTk.CTkLabel(master=self,text="Immune Time",padx=20,anchor="w",text_color="#a4a4a4")
        self.immune_text.grid(row=12,column=0,sticky="NSEW")
        self.immune_time = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=20,border_width=1)
        self.immune_time.insert(0,20)
        self.immune_time.grid(row=12,column=1,columnspan=2,sticky="EW")
        #Multiple Leaders?
        text = CTk.CTkLabel(master=self,text="Multiple Leaders",padx=20,anchor="w",text_color="#a4a4a4")
        text.grid(row=13,column=0,sticky="NSEW")
        self.multiple_leaders = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="",command=master.master.master.master.set_multiple_leaders)
        self.multiple_leaders.grid(row=13,column=1,columnspan=3,sticky="EW")
        #Leaders Follow?
        text = CTk.CTkLabel(master=self,text="Leaders Follow",padx=20,anchor="w",text_color="#a4a4a4")
        text.grid(row=14,column=0,sticky="NSEW")
        self.leaders_follow = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="")
        self.leaders_follow.grid(row=14,column=1,columnspan=3,sticky="EW")

    #Open the text colour picker
    def change_colour(self):
        colors = askcolor(title="Pheromone Color Chooser")
        if colors!=None:
            self.colour.configure(fg_color=colors[1],text=str(colors[1]))
    
    def get_speed(self):
        return float(self.speed.get())
    def get_angle_rate(self):
        return float(self.angle_rate.get())
    def get_randomness(self):
        return float(self.randomness.get())
    def get_deposit_size(self):
        return float(self.deposit_size.get())
    def get_deposit_rate(self):
        return float(self.deposit_rate.get())
    def get_pheromone_dist(self):
        return float(self.pheromone_dist.get())
    def get_robot_dist(self):
        return float(self.robot_dist.get())
    def get_robot_count(self):
        return int(self.robot_count.get())
    def get_leader(self):
        return float(self.leader.get())
    def get_colour(self):
        hex_code = self.colour.cget("text")
        # Remove '#' if present
        hex_code=hex_code.replace("#","")
        # Convert hex to RGBA
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16) 
        return [r, g, b, 0]
    def get_algorithm(self):
        return self.algorithm.get()
    def get_formation(self):
        return self.formation.get()
    def get_leaders_follow(self):
        return self.leaders_follow.get()
    def get_stop_time(self):
        return float(self.stop_time.get())
    def get_immune_time(self):
        return float(self.immune_time.get())

class Render_Setup(CTk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2),weight=1,uniform="column")

        #Render the robots?
        self.draw_text = CTk.CTkLabel(master=self,text="Show Robots",padx=20,anchor="w",text_color="#a4a4a4")
        self.draw_text.grid(row=0,column=0,sticky="NSEW")
        self.draw_robots = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="",command=master.master.master.master.set_draw_robots)
        self.draw_robots.grid(row=0,column=1,columnspan=1,sticky="EW")
        #Threading Used?
        self.thread_text = CTk.CTkLabel(master=self,text="CPU Threading",padx=20,anchor="w",text_color="#a4a4a4")
        self.thread_text.grid(row=1,column=0,sticky="NSEW")
        self.threading = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="")
        self.threading.grid(row=1,column=1,columnspan=1,sticky="EW")


class Graph_Setup(CTk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2),weight=1,uniform="column")
        """
        #Graph 1
        self.graph1_text = CTk.CTkLabel(master=self,text="Graph 1",padx=20,anchor="w",text_color="#a4a4a4")
        self.graph1_text.grid(row=0,column=0,sticky="NSEW")
        self.graph1 = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["Cohesion","# in pheromone","Pheromone Cover","# robots Stopped"])
        self.graph1.grid(row=0,column=1,columnspan=2,sticky="NSEW")
        #Graph 2
        self.graph2_text = CTk.CTkLabel(master=self,text="Graph 2",padx=20,anchor="w",text_color="#a4a4a4")
        self.graph2_text.grid(row=1,column=0,sticky="NSEW")
        self.graph2 = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["Cohesion","# in pheromone","Pheromone Cover","# robots Stopped"])
        self.graph2.grid(row=1,column=1,columnspan=2,sticky="NSEW")
        #Graph 3
        self.graph3_text = CTk.CTkLabel(master=self,text="Graph 3",padx=20,anchor="w",text_color="#a4a4a4")
        self.graph3_text.grid(row=2,column=0,sticky="NSEW")
        self.graph3 = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["Cohesion","# in pheromone","Pheromone Cover","# robots Stopped"])
        self.graph3.grid(row=2,column=1,columnspan=2,sticky="NSEW")
        #Graph 4
        self.graph4_text = CTk.CTkLabel(master=self,text="Graph 4",padx=20,anchor="w",text_color="#a4a4a4")
        self.graph4_text.grid(row=3,column=0,sticky="NSEW")
        self.graph4 = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["Cohesion","# in pheromone","Pheromone Cover","# robots Stopped"])
        self.graph4.grid(row=3,column=1,columnspan=2,sticky="NSEW")
        """
        #Colour scheme
        self.colour_scheme_text = CTk.CTkLabel(master=self,text="Colour Scheme",padx=20,anchor="w",text_color="#a4a4a4")
        self.colour_scheme_text.grid(row=4,column=0,sticky="NSEW")
        self.colour_scheme = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["default","dark_background"],command=master.master.master.master.toggle_graph_theme)
        self.colour_scheme.grid(row=4,column=1,columnspan=2,sticky="NSEW")
        """
        #Reset Graphs?
        self.on_reset_text = CTk.CTkLabel(master=self,text="On Reset",padx=20,anchor="w",text_color="#a4a4a4")
        self.on_reset_text.grid(row=5,column=0,sticky="NSEW")
        self.on_reset = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["Clear","Combine Plots","Average"])
        self.on_reset.grid(row=5,column=1,columnspan=2,sticky="NSEW")
        #Show axis?
        self.axis_text = CTk.CTkLabel(master=self,text="Show Axis",padx=20,anchor="w",text_color="#a4a4a4")
        self.axis_text.grid(row=6,column=0,sticky="NSEW")
        self.show_axis = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="")
        self.show_axis.grid(row=6,column=1,columnspan=1,sticky="EW")
        #Fixed axis?
        self.fix_axis_text = CTk.CTkLabel(master=self,text="Fix Axis",padx=20,anchor="w",text_color="#a4a4a4")
        self.fix_axis_text.grid(row=7,column=0,sticky="NSEW")
        self.fix_axis = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="")
        self.fix_axis.grid(row=7,column=1,columnspan=1,sticky="EW")
        """

class Recording_Setup(CTk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.directory = ""
        self.grid_columnconfigure((0,1,2),weight=1,uniform="column")
        #File Destination
        self.file_text = CTk.CTkLabel(master=self,text="File Location",padx=20,anchor="w",text_color="#a4a4a4")
        self.file_text.grid(row=0,column=0,sticky="NSEW")
        self.file = CTk.CTkButton(master=self,corner_radius=0,border_width=0,command=self.select_folder)
        self.file.grid(row=0,column=1,columnspan=2,sticky="EW")
        #Name
        self.name_text = CTk.CTkLabel(master=self,text="Name",padx=20,anchor="w",text_color="#a4a4a4")
        self.name_text.grid(row=1,column=0,sticky="NSEW")
        self.name = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text="Robot Test 1",border_width=1)
        self.name.grid(row=1,column=1,columnspan=2,sticky="EW")

        #Save quality
        #Autorecord length
        #File destination
        #Name
        #Stop after x
        #Number of tests to run
        #Reset on record start?
        #Save video?
        #Record with graphs ATTACTHED?
        #Record with graphs also?
        #Record with logs also?
        
    #Select the save file
    def select_folder(self):
        # Select a folder and save name
        filename=CTk.filedialog.askdirectory(title="Select Output Directory")
        if filename=="":
            return
        self.directory = filename
        self.file.configure(text=filename[-20:])

class Options(CTk.CTkScrollableFrame):
    #Constructor 
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0),weight=1)

        #CosPy Logo
        font = ("Arial",100)
        self.logo = CTk.CTkLabel(master=self,text="CosPy",text_color="grey",font=font)
        self.logo.grid(row=0,column=0,columnspan=3)

        self.logo = CTk.CTkLabel(master=self,text="Version 0.5",text_color="grey",font=("Arial",20))
        self.logo.grid(row=1,column=0,columnspan=3)

        #Buttom for each section which will enable/disable it
        #Sections:

        #1. Frame
        self.frame_setup = Frame_Setup(master=self)
        self.frame_setup_button = CTk.CTkButton(master=self,
                                          text="▶ Frame Setup",
                                          fg_color="transparent",
                                          corner_radius=0,
                                          anchor="w",
                                          hover=False,
                                          command=self.toggle_frame_setup)
        self.frame_setup_button.grid(padx=(10,0),sticky="ew",row=2)

        #2. Environment
        self.environment_setup = Environment_Setup(master=self)
        self.environment_setup_button = CTk.CTkButton(master=self,
                                          text="▶ Environment Setup",
                                          fg_color="transparent",
                                          corner_radius=0,
                                          anchor="w",
                                          hover=False,
                                          command=self.toggle_environment_setup)
        self.environment_setup_button.grid(padx=(10,0),sticky="ew",row=4)
        
        #3. Robots
        self.robots_setup = Robot_Setup(master=self)
        self.robots_setup_button = CTk.CTkButton(master=self,
                                          text="▶ Robots",
                                          fg_color="transparent",
                                          corner_radius=0,
                                          anchor="w",
                                          hover=False,
                                          command=self.toggle_robots_setup)
        self.robots_setup_button.grid(padx=(10,0),sticky="ew",row=6)

        #4. Render Settings
        self.render_setup = Render_Setup(master=self)
        self.render_setup_button = CTk.CTkButton(master=self,
                                          text="▶ Render Settings",
                                          fg_color="transparent",
                                          corner_radius=0,
                                          anchor="w",
                                          hover=False,
                                          command=self.toggle_render_setup)
        self.render_setup_button.grid(padx=(10,0),sticky="ew",row=8)

        #5. Recording Settings
        self.recording_setup = Recording_Setup(master=self)
        self.recording_setup_button = CTk.CTkButton(master=self,
                                          text="▶ Recording Settings",
                                          fg_color="transparent",
                                          corner_radius=0,
                                          anchor="w",
                                          hover=False,
                                          command=self.toggle_recording_setup)
        self.recording_setup_button.grid(padx=(10,0),sticky="ew",row=10)

        #6. Graph Options
        self.graph_setup = Graph_Setup(master=self)
        self.graph_setup_button = CTk.CTkButton(master=self,
                                          text="▶ Graphing & Logging Settings",
                                          fg_color="transparent",
                                          corner_radius=0,
                                          anchor="w",
                                          hover=False,
                                          command=self.toggle_graph_setup)
        self.graph_setup_button.grid(padx=(10,0),sticky="ew",row=12)
    
    def toggle_frame_setup(self):
        if self.frame_setup.winfo_ismapped():
            self.frame_setup.grid_forget()
            self.frame_setup_button.configure(text="▶ Frame Setup")
        else:
            self.frame_setup.grid(row=3,sticky="ew",columnspan=1,padx=(10,0))
            self.frame_setup_button.configure(text="▼ Frame Setup")
    
    def toggle_environment_setup(self):
        if self.environment_setup.winfo_ismapped():
            self.environment_setup.grid_forget()
            self.environment_setup.configure(text="▶ Environment Setup")
        else:
            self.environment_setup.grid(row=5,sticky="ew",columnspan=1,padx=(10,0))
            self.environment_setup.configure(text="▼ Environment Setup")

    def toggle_robots_setup(self):
        if self.robots_setup.winfo_ismapped():
            self.robots_setup.grid_forget()
            self.robots_setup.configure(text="▶ Robots")
        else:
            self.robots_setup.grid(row=7,sticky="ew",columnspan=1,padx=(10,0))
            self.robots_setup.configure(text="▼ Robots")

    def toggle_render_setup(self):
        if self.render_setup.winfo_ismapped():
            self.render_setup.grid_forget()
            self.render_setup.configure(text="▶ Render Settings")
        else:
            self.render_setup.grid(row=9,sticky="ew",columnspan=1,padx=(10,0))
            self.render_setup.configure(text="▼ Render Settings")

    def toggle_recording_setup(self):
        if self.recording_setup.winfo_ismapped():
            self.recording_setup.grid_forget()
            self.recording_setup.configure(text="▶ Recording Settings")
        else:
            self.recording_setup.grid(row=11,sticky="ew",columnspan=1,padx=(10,0))
            self.recording_setup.configure(text="▼ Recording Settings")

    def toggle_graph_setup(self):
        if self.graph_setup.winfo_ismapped():
            self.graph_setup.grid_forget()
            self.graph_setup.configure(text="▶ Graphing & Logging Settings")
        else:
            self.graph_setup.grid(row=13,sticky="ew",columnspan=1,padx=(10,0))
            self.graph_setup.configure(text="▼ Graphing & Logging Settings")



class App(CTk.CTk):#MAIN APP WINDOW
    def __init__(self):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.title("COSPY - Swarm Robotics Tool")
        self.minsize(1600,900)
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.multiple_leaders=False
        self.leaders_follow=False
        self.collide_mode="Ignore"
        self.running=False
        self.recording=False
        self.simulation_speed = 1
        self.time_step=0
        self.save_img=False

        ############# MENU FRAME
        self.bar_frame = Menu(master=self,corner_radius=0,fg_color="#161616")
        self.bar_frame.pack(padx=0,pady=0,fill="both")
        #############

        ############# OPTIONS FRAME
        self.options_frame = Options(master=self,corner_radius=0)
        self.options_frame.pack(side="right",fill="both",expand=True)
        #############


        ############# RENDER AND GRAPHS TAB FRAME
        self.tabview = CTk.CTkTabview(master=self,width=1020)
        self.tabview.pack(padx=20,pady=(0,10),fill="both",expand=True)
        self.tabview.add("Simulation")  # add tab at the end
        self.tabview.add("Graphs")  # add tab at the end

        ############# RENDER FRAME
        self.embed = Frame(master=self.tabview.tab("Simulation"),width=2000,height=1550)
        self.embed.pack()
        ##############

        ############# GRAPH FRAME
        self.graphs_embed = Graph_Frame(master=self.tabview.tab("Graphs"))
        self.graphs_embed.pack(fill="both",expand=True)
        #############

        self.reset()


    def refresh(self):
        #time.sleep(0.01)
        if self.running:
            if self.collide_mode!="Ignore":
                #1. IF COLLISIONS STOP IS ON
                positions = np.array([np.array(instance) for instance in self.robots_array])
                # Define a threshold for closeness
                threshold = self.robots_array[0].robot_dist# Adjust this value according to your needs
                # Calculate pairwise Euclidean distances
                distances = np.sqrt(np.sum((positions[:, np.newaxis] - positions[np.newaxis, :]) ** 2, axis=-1))
                # Mask of values that are close
                close_mask = distances < threshold
                # Indices of close points
                close_indices = np.argwhere(np.sum(close_mask, axis=1)>1)
                if self.collide_mode=="Stop":#Stop for x time frames
                    for i in close_indices:
                        self.robots_array[i[0]].encounter()
                elif self.collide_mode=="Stop linear to temperature":#Stop relative to temperature
                    for i in close_indices:
                        self.robots_array[i[0]].temperature_linear_encounter(self.renderer.env_pixels)
                else:
                    for i in close_indices:
                        self.robots_array[i[0]].temperature_exponential_encounter(self.renderer.env_pixels)

            #UPDATE THE ROBOTS
            if self.options_frame.render_setup.threading.get():
                # Main loop
                for r in self.robots_array:
                    # Create a thread for each robot and start it
                    thread = threading.Thread(target=process_robot, args=(r, self.renderer))
                    thread.start()

                # Wait for all threads to finish
                for thread in threading.enumerate():
                    if thread != threading.current_thread():
                        thread.join()
            else:
                for r in self.robots_array:
                    r.deposit(self.renderer)
                    r.move(self.renderer.pixels)

            #UPDATE THE ENVIRONEMNT
            self.renderer.update_environment()

            #RECORDING
            if self.recording:
                #COMBINE THE GRAPHS AND SURFACE INTO ONE BGR IMAGE!
                img_tl = graph_to_BGR(self.graphs_embed.canvas1)
                img_bl = graph_to_BGR(self.graphs_embed.canvas3)
                img_left = np.vstack((img_tl, img_bl))  

                img_tr = graph_to_BGR(self.graphs_embed.canvas2)
                img_br = graph_to_BGR(self.graphs_embed.canvas4)
                img_right = np.vstack((img_tr,img_br))

                #Get the pysdl2 surface
                img_surface = sdl2.ext.surface_to_ndarray(self.renderer.window.get_surface())[:, :, [2, 1, 0]]
                img_surface = cv2.cvtColor(img_surface, cv2.COLOR_RGBA2BGR)  # Convert RGBA to BGR for OpenCV
                width = int(self.renderer.w*(img_right.shape[0]/self.renderer.h))
                img_surface = cv2.resize(img_surface,(width,img_right.shape[0]))

                combined_img = np.hstack((img_left,img_surface,img_right))
                self.video_writer.write(combined_img)


            #UPDATE THE GRAPHS PAGE
            if self.time_step%100==0 or self.time_step==1:
                if self.save_img and (self.time_step%1000==0 or self.time_step==1):
                    sdl2.ext.image.save_bmp(self.renderer.window.get_surface(),path=str(self.directory)+str(self.log_name)+str(self.time_step)+".bmp",overwrite=True)

                # Convert each instance into a NumPy array
                positions = np.array([np.array(instance) for instance in self.robots_array])

                #FIND ROBOTS X DISTANCE FROM CENTER
                centre_x = self.renderer.surfw/2
                centre_y = self.renderer.surfh/2
                distance_threshold = self.renderer.aggregation_radius*self.renderer.scale # Specify the distance threshold
                num_points_at_distance = count_points_at_distance2(positions, centre_x, centre_y, distance_threshold)

                #FIND NUMBER OF ROBOTS WAITING
                robots_waiting = 0
                #GET ROBOTS IN PHEROMONE
                robots_in_pheromone = 0
                for i in self.robots_array:
                    if i.in_pheromone(self.renderer.pixels):
                        robots_in_pheromone+=1
                    if i.waiting>0:
                        robots_waiting+=1

                #Proportion of robots in pheromone!!!!!
                robots_in_pheromone = robots_in_pheromone/len(self.robots_array)

                #FIND DISTANCES BETWEEN ROBOTS
                positions = np.array([np.array(instance) for instance in self.robots_array])
                # Calculate pairwise Euclidean distances
                distances = np.sqrt(np.sum((positions[:, np.newaxis] - positions[np.newaxis, :]) ** 2, axis=-1))
                avg_distance = np.mean(distances)

                #UPDATE GRAPH EMBEDS
                self.graphs_embed.update_graphs(robots_waiting,num_points_at_distance,robots_in_pheromone,avg_distance)
                log_path = str(self.directory)+str(self.log_name)
                self.graphs_embed.update_log(log_path,robots_waiting,num_points_at_distance,robots_in_pheromone,avg_distance)
            #UPDATE TIME STEP
            self.time_step+=1

        #UPDATE THE ACTUAL SCREEN
        if self.time_step%self.simulation_speed==0:
            #Refresh the render
            if self.running:
                self.renderer.refresh(self.robots_array)
            #Update framerate text
            self.bar_frame.framerate_text.configure(text="Framerate: "+str(int(self.renderer.framerate)))
        #Update time step text
        self.bar_frame.timestep_text.configure(text="Time Step: "+str(self.time_step))

        return


    def close(self):
        try:
            self.video_writer.release()
        except:
            pass
        self.running=True
        self.renderer.close()
        self.destroy()

    def reset(self):

        #1. GET VARIABLES FROM OPTIONS
        self.time_step = 0
        #Frame
        width = self.options_frame.frame_setup.get_width()
        height = self.options_frame.frame_setup.get_height()
        scale = float(self.options_frame.frame_setup.scale.get())
        #Environment
        evaporation_rate = int(self.options_frame.environment_setup.evaporation_rate.get())
        diffusion_rate = int(self.options_frame.environment_setup.diffusion.get())
        use_temperature = self.options_frame.environment_setup.temperature.get()
        wind_speed = (int(self.options_frame.environment_setup.windx.get()),int(self.options_frame.environment_setup.windy.get()))
        temperature_colour = self.options_frame.environment_setup.get_colour()
        aggregation_radius = int(self.options_frame.environment_setup.aggregation.get())
        #Robots
        leaders = self.options_frame.robots_setup.get_leader()
        leaders_follow = self.options_frame.robots_setup.get_leaders_follow()
        robot_count = self.options_frame.robots_setup.get_robot_count()
        self.collide_mode = self.options_frame.robots_setup.collisions.get()
        pheromone_colour=self.options_frame.robots_setup.get_colour()
        #Logs
        self.log_name = self.options_frame.recording_setup.name.get()
        if self.log_name=="":
            self.log_name="default"
        self.directory = self.options_frame.recording_setup.directory
        if self.directory!="":
            self.directory+="/"


        #2. CREATE NEW RENDERER
        self.embed.destroy()
        self.embed = Frame(master=self.tabview.tab("Simulation"),width=width,height=height)
        self.embed.pack()
        self.graphs_embed.reset()
        self.renderer = Renderer(width,height,scale,self.embed.winfo_id(),evaporation_rate,diffusion_rate,wind_speed,use_temperature,temperature_colour,pheromone_colour,aggregation_radius)
        self.renderer.render_robot = self.options_frame.render_setup.draw_robots.get()


        
        #3. CREATE ROBOTS ARRAY
        self.robots_array=[]
        for i in range(robot_count):
            self.robots_array.append(Robot(x=random.randint(1,int(width*scale)-2),
                                           y=random.randint(1,int(height*scale)-2),
                                           speed=self.options_frame.robots_setup.get_speed(),
                                           angle_speed=self.options_frame.robots_setup.get_angle_rate(),
                                           randomness=self.options_frame.robots_setup.get_randomness(),
                                           deposit_size=self.options_frame.robots_setup.get_deposit_size(),
                                           deposit_rate=self.options_frame.robots_setup.get_deposit_rate(),
                                           pheromone_dist=self.options_frame.robots_setup.get_pheromone_dist(),
                                           robot_dist=self.options_frame.robots_setup.get_robot_dist(),
                                           boundary_function=self.options_frame.environment_setup.get_boundary_function(),
                                           stop_time=self.options_frame.robots_setup.get_stop_time(),
                                           immune_time=self.options_frame.robots_setup.get_immune_time(),
                                           use_temperature=self.options_frame.environment_setup.get_use_temperature(),
                                           leaders_follow=leaders_follow))
            
        #4. ASSIGN LEADER ROLES
        if self.multiple_leaders:
            leaders = int(leaders*robot_count)
            for i in range(leaders):
                self.robots_array[i].leader = True

        else:
            self.robots_array[0].leader = True

        # RETURN
        return 

    def set_draw_robots(self):
        self.renderer.render_robot = not self.renderer.render_robot

    def set_multiple_leaders(self):
        leaders = float(self.options_frame.robots_setup.leader.get())
        if self.multiple_leaders:
            #Now only 1 leader#
            for r in self.robots_array:
                r.leader=False
            self.robots_array[0].leader=True
        else:
            #Now multiple leaders
            leaders = int(leaders*len(self.robots_array))
            for i in range(leaders):
                self.robots_array[i].leader = True
        self.multiple_leaders = not self.multiple_leaders

    def set_temperature(self):
        self.renderer.use_temperature = not self.renderer.use_temperature

    def set_leaders_follow(self):
        self.leaders_follow = not self.leaders_follow
        for r in self.robots_array:
            r.leaders_follow = self.leaders_follow

    def set_running(self):
        self.running = not self.running

    #Sets the boundary function for the agents
    def set_boundary_function(self,event):
        for r in self.robots_array:
            r.edge_mode = event

    #Updates the speed by using the slider
    def update_speed(self,event):
        thresholds = [0.25,0.5,0.75,1]
        self.simulation_speed = [1, 2, 4, 8][next(i for i, v in enumerate(thresholds) if event <= v)]
        self.bar_frame.speed_label.configure(text="Speed: x"+str(self.simulation_speed))

    #Toggle the recording
    def toggle_recording(self):
        if self.recording:
            self.bar_frame.record_button._fg_color="transparent"
            #Save video
            self.video_writer.release()
        else:
            self.bar_frame.record_button._fg_color="red"
            # Initialize video writer
            #vid_w,vid_h = self.graphs_embed.canvas1.get_width_height()
            width2 = int(self.renderer.w*(960/self.renderer.h))
            self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')  #Codec for MPEG-4
            #Add time into name of file, if name not set
            current_time = datetime.datetime.now().strftime("%H%M%S")
            name = str(self.directory)+str(self.log_name)+str(current_time)+'.mp4'
            self.video_writer = cv2.VideoWriter(name, self.fourcc, 60.0, (1280+width2, 960))

        self.recording = not self.recording

    def toggle_graph_theme(self,theme):
        self.graphs_embed.toggle_theme(theme)


        

    #Save the Test
    def save_test(self):
        pass
        #Open file saver
        #Create save class
        #Save pickle file

    #Load the Test
    def load_test(self):
        pass
        #Open file explorer 
        #Get file contents
        #Set input values and refresh
        
    
def count_points_at_distance(points, center_x, center_y, distance_threshold):
    center = np.array([center_x, center_y])
    distances = np.linalg.norm(points - center, axis=1)
    num_points_at_distance = np.sum(distances <= distance_threshold)
    return num_points_at_distance

def count_points_at_distance2(points, center_x, center_y, distance_threshold):
    num_points_at_distance = 0 
    for p in points:
        if math.sqrt((center_x-p[0])**2+(center_y-p[1])**2)<=distance_threshold:
            num_points_at_distance+=1
    return num_points_at_distance

#Used for CPU threading of robots
def process_robot(robot, renderer):
    robot.deposit(renderer)
    robot.move(renderer.pixels)

def graph_to_BGR(canvas):
    buffer = canvas.buffer_rgba()
    img = np.array(buffer)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)  # Convert RGBA to BGR for OpenCV
    return img

if __name__ == "__main__":
    title_font = ("David",20,"bold")
    normal_font = ("David",16)
    CTk.set_appearance_mode("dark")
    if os.path.exists("theme.json"):
        CTk.set_default_color_theme("theme.json")
    app=App()
    icon_path = os.path.join(os.path.dirname(__file__) , "icon.ico")
    app.iconbitmap(icon_path)
    app.after(0, lambda:app.state('zoomed'))
    while True:
        app.refresh()
        app.update()

# DONE:
# Optimize drawing of pheromones so that the size can be changed
# Add robots
# Add simulation speed
# Add Bounce
# Add wrap around
# Make it move 1 frame when paused!
# Make the options a scrollable frame with dropdown sections
# FIX MULTIPLE LEADER SYSTEM
# Make graphs stay big! 
# Add pheromone detection distance
# Make temp on it's own layer and change colour
# Add robot detection distance
# Dont render so much whilst paused, FIX THIS GLITCHING! Then it'll run well
# Fix pheromones not working properly when on graphs page
# Fix robot movement
# Add recording system
# Add CPU threading
# Add aggregation area size option
# Make all exports go to same file
# Make exporting of logs and stuff use correct names!   
#FUTURE 
# Add hover tooltips
# Add way more options into the menu





