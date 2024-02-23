from tkinter import *
import customtkinter as CTk
import os
import sdl2
from Render import *
from Robots import *
from customtkinter.windows.widgets.core_widget_classes.dropdown_menu import DropdownMenu

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
        self.file._dropdown_menu.add_command(label="Save Test", accelerator="Ctrl+S")


        #self.file._dropdown_menu.insert_separator(1)
        #self.file._dropdown_menu.insert_separator(7)
        #self.file._dropdown_menu.insert_separator(10)
        #self.file._dropdown_menu.insert_separator(15)
        self.file.pack(side="left")

        self.start_button = CTk.CTkButton(master=self,text="Reset",corner_radius=0,command=self.master.reset)
        self.start_button.pack(side="right")
        self.start_button = CTk.CTkButton(master=self,text="Stop",corner_radius=0)
        self.start_button.pack(side="right")
        self.start_button = CTk.CTkButton(master=self,text="Pause",corner_radius=0)
        self.start_button.pack(side="right")
        self.start_button = CTk.CTkButton(master=self,text="Start",corner_radius=0)
        self.start_button.pack(side="right")


        self.framerate_text = CTk.CTkLabel(master=self,text="Framerate: ")
        self.framerate_text.pack(side="right")



class Options(CTk.CTkFrame):
    #Constructor 
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2),weight=1)
        #FRAME SETUP
        #Size
        self.size_text = CTk.CTkLabel(master=self,text="Size")
        self.size_text.grid(row=0,column=0,pady=(20,0))
        self.width = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.width.grid(row=0,column=1,pady=(20,0))
        self.width.insert(0,2000)
        self.height = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.height.grid(row=0,column=2,pady=(20,0))
        self.height.insert(0,1550)
        #Scale
        self.scale_text = CTk.CTkLabel(master=self,text="Scale",padx=20)
        self.scale_text.grid(row=1,column=0)
        self.scale = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.scale.insert(0,0.25)
        self.scale.grid(row=1,column=1,columnspan=2,sticky="NSEW")
        #Deposit Size
        self.deposit_text = CTk.CTkLabel(master=self,text="Deposit Size",padx=20)
        self.deposit_text.grid(row=2,column=0)
        self.deposit_size = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.deposit_size.grid(row=2,column=1,columnspan=2,sticky="NSEW")
        #Deposit Rate
        self.deposit_text = CTk.CTkLabel(master=self,text="Deposit Rate",padx=20)
        self.deposit_text.grid(row=3,column=0)
        self.deposit_rate = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.deposit_rate.grid(row=3,column=1,columnspan=2,sticky="NSEW")
        #Evaporation Rate
        self.evap_text = CTk.CTkLabel(master=self,text="Evaporation Rate",padx=20)
        self.evap_text.grid(row=4,column=0)
        self.evaporation_rate = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.evaporation_rate.grid(row=4,column=1,columnspan=2,sticky="NSEW")
        #Diffusion Rate
        self.diffusion_text = CTk.CTkLabel(master=self,text="Diffusion Rate",padx=20)
        self.diffusion_text.grid(row=5,column=0)
        self.diffusion = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.diffusion.grid(row=5,column=1,columnspan=2,sticky="NSEW")
        #Wind Rate
        self.wind_text = CTk.CTkLabel(master=self,text="Wind Rate",padx=20)
        self.wind_text.grid(row=6,column=0)
        self.windx = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.windx.grid(row=6,column=1)
        self.windy = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.windy.grid(row=6,column=2)

        #Blending Mode
        self.blending_text = CTk.CTkLabel(master=self,text="Blending Mode",padx=20)
        self.blending_text.grid(row=7,column=0)
        self.blending = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["RGBA"])
        self.blending.grid(row=7,column=1,columnspan=2,sticky="NSEW")

        #Robot Algorithm
        self.algorithm_text = CTk.CTkLabel(master=self,text="Robot Algorithm",padx=20)
        self.algorithm_text.grid(row=8,column=0)
        self.algorithm = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["Ant"])
        self.algorithm.grid(row=8,column=1,columnspan=2,sticky="NSEW")

        #Starting formations
        self.formation_text = CTk.CTkLabel(master=self,text="Starting Formation",padx=20)
        self.formation_text.grid(row=9,column=0)
        self.formation = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["Random","Grid"])
        self.formation.grid(row=9,column=1,columnspan=2,sticky="NSEW")


        #Number of robots
        self.robot_text = CTk.CTkLabel(master=self,text="Robot Count",padx=20)
        self.robot_text.grid(row=10,column=0)
        self.robot_count = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=20,border_width=1)
        self.robot_count.insert(0,20)
        self.robot_count.grid(row=10,column=1,columnspan=2,sticky="EW")

        #Render the robots?
        self.draw_robots = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="Show Robots",command=self.master.set_draw_robots)
        self.draw_robots.grid(row=11,column=1,columnspan=3,sticky="EW")

        #Multiple Leaders?
        self.multiple_leaders = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="Multiple Leaders",command=self.master.set_draw_robots)
        self.multiple_leaders.grid(row=12,column=1,columnspan=3,sticky="EW")
        #Leaders Follow?
        self.leaders_follow = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="Leaders Follow",command=self.master.set_draw_robots)
        self.leaders_follow.grid(row=13,column=1,columnspan=3,sticky="EW")
        #Threading Used?
        self.threading = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="CPU Threading",command=self.master.set_draw_robots)
        self.threading.grid(row=14,column=1,columnspan=3,sticky="EW")



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
            self.robots_array.append(Robot(random.randint(20,400),random.randint(20,400)))
        self.robots_array[0].leader = True

        ############# MENU FRAME
        self.bar_frame = Menu(master=self,corner_radius=0,fg_color="#161616")
        self.bar_frame.pack(padx=0,pady=0,fill="both")
        #############


        ############# OPTIONS FRAME
        self.options_frame = Options(master=self,corner_radius=0)
        self.options_frame.pack(side="right",fill="both")
        #############



        ############# RENDER FRAME
        self.embed = Frame(master=self,width=2000,height=1550)
        #self.embed.grid(columnspan = (2000), rowspan = 1600) # Adds grid
        self.embed.pack(side="left",padx=30)
        self.renderer = Renderer(2000,1550,0.25,self.embed.winfo_id())
        self.bind("<space>", self.renderer.change_colour)
        ##############


    def refresh(self):
        #Update Robots
        for r in self.robots_array:
            r.deposit(self.renderer)
            r.move(self.renderer.pixels)

        #Update the screen
        self.renderer.refresh(self.robots_array)
        #Update framerate text
        self.bar_frame.framerate_text.configure(text="Framerate: "+str(self.renderer.framerate))

    def close(self):
        self.renderer.close()
        self.destroy()

    def reset(self):
        #GET VARIABLES FROM OPTIONS
        width = int(self.options_frame.width.get())
        height = int(self.options_frame.height.get())
        scale = float(self.options_frame.scale.get())
        robot_count = int(self.options_frame.robot_count.get())
        draw_robots = self.options_frame.draw_robots.get()

        self.embed.destroy()
        self.embed = Frame(master=self,width=width,height=height)
        self.embed.pack(side="left",padx=30)
        self.renderer = Renderer(width,height,scale,self.embed.winfo_id())
        self.renderer.render_robot = draw_robots
        self.bind("<space>", self.renderer.change_colour)
        self.robots_array=[]
        for i in range(robot_count):
            self.robots_array.append(Robot(random.randint(50,int(width*scale)-50),random.randint(50,int(height*scale)-50)))
        self.robots_array[0].leader = True

    def set_draw_robots(self):
        self.renderer.render_robot = not self.renderer.render_robot

if __name__ == "__main__":
    title_font = ("David",20,"bold")
    normal_font = ("David",16)
    CTk.set_appearance_mode("dark")
    if os.path.exists("theme.json"):
        CTk.set_default_color_theme("theme.json")
    app=App()
    app.after(0, lambda:app.state('zoomed'))
    while True:
        app.refresh()
        app.update()


#TODO
# Optimize drawing of pheromones so that the size can be changed
# Add all variable options
# Add robots
# Add popout window
# Add threading option for robots
