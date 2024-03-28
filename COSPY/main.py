########################
########################
########################  MAIN CODE FOR COSPY
######################## 
########################
########################


from tkinter import *
import customtkinter as CTk
import os
import sdl2
from Render import *
from Robots import *
from Graphs import *
from customtkinter.windows.widgets.core_widget_classes.dropdown_menu import DropdownMenu




def distance_between_robots(robot1, robot2):
    return np.sqrt((robot1.x - robot2.x)**2 + (robot1.y - robot2.y)**2)


class Algorithm_Editor(CTk.CTkFrame):
    #Constructor 
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        #FRAME SETUP

        

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


        #self.file._dropdown_menu.insert_separator(1)
        #self.file._dropdown_menu.insert_separator(7)
        #self.file._dropdown_menu.insert_separator(10)
        #self.file._dropdown_menu.insert_separator(15)
        self.file.pack(side="left")

        # Editor Buttons
        #self.alg_edit_button = CTk.CTkButton(master=self,text="Algorithm Editor",corner_radius=0,fg_color="transparent")
        #self.alg_edit_button.pack(side="left")
        #self.env_edit_button = CTk.CTkButton(master=self,text="Environment Editor",corner_radius=0,fg_color="transparent")
        #self.env_edit_button.pack(side="left")

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
        self.leaders_follow = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="")
        self.leaders_follow.grid(row=11,column=1,columnspan=3,sticky="EW")
        #Temp Strength
        text = CTk.CTkLabel(master=self,text="Temp Strength",padx=20,anchor="w",text_color="#a4a4a4")
        text.grid(row=12,column=0,sticky="NSWE")
        self.strength = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.strength.insert(0,2)
        self.strength.grid(row=12,column=1,columnspan=2,sticky="NSEW")
        #Temperature Colour
        text = CTk.CTkLabel(master=self,text="Temp Colour",padx=20,anchor="w",text_color="#a4a4a4")
        text.grid(row=13,column=0,sticky="NSEW")
        self.colour = CTk.CTkButton(master=self,corner_radius=0,border_width=0)
        self.colour.grid(row=13,column=1,columnspan=2,sticky="EW")


class Robot_Setup(CTk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2),weight=1,uniform="column")
        #Robot Speed
        self.deposit_text = CTk.CTkLabel(master=self,text="Robot Speed",padx=20,anchor="w",text_color="#a4a4a4")
        self.deposit_text.grid(row=0,column=0,sticky="NSEW")
        self.deposit_size = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.deposit_size.insert(0,50)
        self.deposit_size.grid(row=0,column=1,columnspan=2,sticky="NSEW")
        #Angle Change Rate
        self.deposit_text = CTk.CTkLabel(master=self,text="Turn Speed",padx=20,anchor="w",text_color="#a4a4a4")
        self.deposit_text.grid(row=1,column=0,sticky="NSEW")
        self.deposit_size = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.deposit_size.insert(0,50)
        self.deposit_size.grid(row=1,column=1,columnspan=2,sticky="NSEW")
        #Randomness
        self.deposit_text = CTk.CTkLabel(master=self,text="Randomness",padx=20,anchor="w",text_color="#a4a4a4")
        self.deposit_text.grid(row=2,column=0,sticky="NSEW")
        self.deposit_size = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.deposit_size.insert(0,50)
        self.deposit_size.grid(row=2,column=1,columnspan=2,sticky="NSEW")
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
       #Number of robots
        self.robot_text = CTk.CTkLabel(master=self,text="Robot Count",padx=20,anchor="w",text_color="#a4a4a4")
        self.robot_text.grid(row=5,column=0,sticky="NSEW")
        self.robot_count = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=20,border_width=1)
        self.robot_count.insert(0,20)
        self.robot_count.grid(row=5,column=1,columnspan=2,sticky="EW")
        #Proportion of leader robots
        self.leader_text = CTk.CTkLabel(master=self,text="Leader Proportion",padx=20,anchor="w",text_color="#a4a4a4")
        self.leader_text.grid(row=6,column=0,sticky="NSEW")
        self.leader = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=20,border_width=1)
        self.leader.insert(0,0.1)
        self.leader.grid(row=6,column=1,columnspan=2,sticky="EW")
        #Pheromone Colour
        self.leader_text = CTk.CTkLabel(master=self,text="Pheromone Colour",padx=20,anchor="w",text_color="#a4a4a4")
        self.leader_text.grid(row=7,column=0,sticky="NSEW")
        self.colour = CTk.CTkButton(master=self,corner_radius=0,border_width=0)
        self.colour.grid(row=7,column=1,columnspan=2,sticky="EW")
        #Robot Algorithm
        self.algorithm_text = CTk.CTkLabel(master=self,text="Robot Algorithm",padx=20,anchor="w",text_color="#a4a4a4")
        self.algorithm_text.grid(row=8,column=0,sticky="NSEW")
        self.algorithm = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["Ant"])
        self.algorithm.grid(row=8,column=1,columnspan=2,sticky="NSEW")
        #Starting formations
        self.formation_text = CTk.CTkLabel(master=self,text="Starting Formation",padx=20,anchor="w",text_color="#a4a4a4")
        self.formation_text.grid(row=9,column=0,sticky="NSEW")
        self.formation = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["Random","Grid","Centre"])
        self.formation.grid(row=9,column=1,columnspan=2,sticky="NSEW")
        #Collisions
        self.formation_text = CTk.CTkLabel(master=self,text="Collisions",padx=20,anchor="w",text_color="#a4a4a4")
        self.formation_text.grid(row=10,column=0,sticky="NSEW")
        self.collisions = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["Ignore","Stop","Stop proportional to temperature"])
        self.collisions.grid(row=10,column=1,columnspan=2,sticky="NSEW")

        #Multiple Leaders?
        text = CTk.CTkLabel(master=self,text="Multiple Leaders",padx=20,anchor="w",text_color="#a4a4a4")
        text.grid(row=11,column=0,sticky="NSEW")
        self.multiple_leaders = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="",command=master.master.master.master.set_multiple_leaders)
        self.multiple_leaders.grid(row=11,column=1,columnspan=3,sticky="EW")
        #Leaders Follow?
        text = CTk.CTkLabel(master=self,text="Leaders Follow",padx=20,anchor="w",text_color="#a4a4a4")
        text.grid(row=12,column=0,sticky="NSEW")
        self.leaders_follow = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="")
        self.leaders_follow.grid(row=12,column=1,columnspan=3,sticky="EW")

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
        #Colour scheme
        self.colour_scheme_text = CTk.CTkLabel(master=self,text="Colour Scheme",padx=20,anchor="w",text_color="#a4a4a4")
        self.colour_scheme_text.grid(row=4,column=0,sticky="NSEW")
        self.colour_scheme = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["Light","Dark"])
        self.colour_scheme.grid(row=4,column=1,columnspan=2,sticky="NSEW")
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


class Recording_Setup(CTk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2),weight=1,uniform="column")
        #File Destination
        self.file_text = CTk.CTkLabel(master=self,text="File Location",padx=20,anchor="w",text_color="#a4a4a4")
        self.file_text.grid(row=0,column=0,sticky="NSEW")
        self.file = CTk.CTkButton(master=self,corner_radius=0,border_width=0)
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



    def get_width(self):
        width = int(self.frame_setup.width.get())
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
        height = int(self.frame_setup.height.get())
        if height<400:
            height = 400
            self.height.delete(0,"end")
            self.height.insert(0,"400")
        elif height>1460:
            height=1460
            self.height.delete(0,"end")
            self.height.insert(0,"1460")
        return height
    
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
        self.robots_array=[]
        for i in range(10):
            self.robots_array.append(Robot(random.randint(20,400),random.randint(20,300)))
        self.robots_array[0].leader = True
        self.multiple_leaders=False
        self.leaders_follow=False
        self.running=False
        self.recording=False
        self.simulation_speed = 1
        self.time_step=0

        ############# MENU FRAME
        self.bar_frame = Menu(master=self,corner_radius=0,fg_color="#161616")
        self.bar_frame.pack(padx=0,pady=0,fill="both")
        #############

        ############# OPTIONS FRAME
        self.options_frame = Options(master=self,corner_radius=0)
        self.options_frame.pack(side="right",fill="both",expand=True)
        #############

        ############# ALGORITHM EDITOR FRAME
        self.algorithm_frame = Algorithm_Editor(master=self,corner_radius=0)
        #self.algorithm_frame.pack(side="right",fill="both")
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
        if self.running:

            #UPDATE THE ROBOTS
            for r in self.robots_array:
                r.deposit(self.renderer)
                r.move(self.renderer.pixels)

            #UPDATE THE ENVIRONEMNT
            self.renderer.update_environment()

            #UPDATE THE GRAPHS PAGE
            if self.time_step%120==0:
                # Convert each instance into a NumPy array
                positions = np.array([np.array(instance) for instance in self.robots_array])
                #Find how many are in center-x
                centre_x = self.renderer.surfw/2
                centre_y = self.renderer.surfh/2
                distance_threshold = 50 # Specify the distance threshold
                num_points_at_distance = count_points_at_distance(positions, centre_x, centre_y, distance_threshold)
                #Find directional accuracy of the swarm as a whole
                #Find how many are following!

                # Calculate pairwise distances using broadcasting
                #distances = np.sqrt(np.sum((positions[:, np.newaxis, :] - positions[np.newaxis, :, :])**2, axis=-1))
                """
                # Set threshold distance
                threshold_distance = 5
                # Find indices of near robots
                near_indices = np.where((distances > 0) & (distances < threshold_distance))
                # Concatenate the arrays
                all_near_indices = np.concatenate(near_indices)
                # Convert the result to a list
                near_indices_list = all_near_indices.tolist()

                for i in near_indices_list:
                    self.robots_array[i].encounter(self.renderer.pixels)
                """
                self.graphs_embed.update_graphs(self.time_step,num_points_at_distance,3,4)
                if self.tabview.get()=="Graphs":
                    self.bar_frame.framerate_text.configure(text="Framerate: "+str("N/A"))
            #UPDATE TIME STEP
            self.time_step+=1

        #UPDATE THE ACTUAL SCREEN
        if self.time_step%self.simulation_speed==0 and self.tabview.get()=="Simulation":
            #Refresh the render
            if self.running:
                self.renderer.refresh(self.robots_array)
            #Update framerate text
            self.bar_frame.framerate_text.configure(text="Framerate: "+str(int(self.renderer.framerate)))
        #Update time step text
        self.bar_frame.timestep_text.configure(text="Time Step: "+str(self.time_step))

        return


    def close(self):
        self.running=True
        self.renderer.close()
        self.destroy()

    def reset(self):
        #GET VARIABLES FROM OPTIONS
        self.time_step = 0
        width = self.options_frame.get_width()
        height = self.options_frame.get_height()
        scale = 0.2#float(self.options_frame.scale.get())
        robot_count = int(self.options_frame.robots_setup.robot_count.get())
        draw_robots = self.options_frame.render_setup.draw_robots.get()
        deposit_size = self.options_frame.robots_setup.deposit_size.get()
        deposit_amount = self.options_frame.robots_setup.deposit_rate.get()
        evaporation_rate = int(self.options_frame.environment_setup.evaporation_rate.get())
        diffusion_rate = int(self.options_frame.environment_setup.diffusion.get())
        wind_speed = (int(self.options_frame.environment_setup.windx.get()),int(self.options_frame.environment_setup.windy.get()))
        leaders = float(self.options_frame.robots_setup.leader.get())


        self.embed.destroy()
        self.embed = Frame(master=self.tabview.tab("Simulation"),width=width,height=height)
        self.embed.pack()
        self.graphs_embed.reset()
        self.renderer = Renderer(width,height,scale,self.embed.winfo_id(),int(deposit_size),deposit_amount,evaporation_rate,diffusion_rate,wind_speed)
        self.renderer.render_robot = draw_robots
        self.bind("<space>", self.renderer.change_colour)
        self.robots_array=[]
        for i in range(robot_count):
            self.robots_array.append(Robot(random.randint(1,int(width*scale)-2),random.randint(1,int(height*scale)-2)))
        if self.multiple_leaders:
            leaders = int(leaders*robot_count)
            for i in range(leaders):
                self.robots_array[i].leader = True

        else:
            self.robots_array[0].leader = True



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
        else:
            self.bar_frame.record_button._fg_color="red"

        self.recording = not self.recording

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

#DONE
# Optimize drawing of pheromones so that the size can be changed
# Add robots
# Add simulation speed
# Add Bounce
# Add wrap around
# Make it move 1 frame when paused!
# Make the options a scrollable frame with dropdown sections
# FIX MULTIPLE LEADER SYSTEM
#Make graphs stay big! 


#NOW
#Add all options into menu
#Create a new reset function, make it so saving and loading will be easy



#TODO
# Dont render so much whilst paused, FIX THIS GLITCHING! Then it'll run well
# Fix pheromones not working properly when on graphs page
# Add FPS limit
# Add limit ram
# Fix wrap
# Add show pheromone scanners
# Add create video mode
# Create a layer system to have multiple pheromones and envs
# LOOK at maths behind cosphi
# Add saving





