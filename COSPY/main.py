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
        self.alg_edit_button = CTk.CTkButton(master=self,text="Algorithm Editor",corner_radius=0,fg_color="transparent")
        self.alg_edit_button.pack(side="left")
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
        self.width.insert(0,1960)#MAX SIZE 1960, MIN SIZE 400
        self.height = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.height.grid(row=0,column=2,pady=(20,0))
        self.height.insert(0,1460)#MAX SIZE 1460, MIN SIZE 400
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
        self.deposit_size.insert(0,50)
        self.deposit_size.grid(row=2,column=1,columnspan=2,sticky="NSEW")
        #Deposit Rate
        self.deposit_text = CTk.CTkLabel(master=self,text="Deposit Rate",padx=20)
        self.deposit_text.grid(row=3,column=0)
        self.deposit_rate = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.deposit_rate.insert(0,2)
        self.deposit_rate.grid(row=3,column=1,columnspan=2,sticky="NSEW")
        
        #Evaporation Rate
        self.evap_text = CTk.CTkLabel(master=self,text="Evaporation Rate",padx=20)
        self.evap_text.grid(row=4,column=0)
        self.evaporation_rate = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.evaporation_rate.insert(0,4)
        self.evaporation_rate.grid(row=4,column=1,columnspan=2,sticky="NSEW")
        #Diffusion Rate
        self.diffusion_text = CTk.CTkLabel(master=self,text="Diffusion Rate",padx=20)
        self.diffusion_text.grid(row=5,column=0)
        self.diffusion = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.diffusion.insert(0,2)
        self.diffusion.grid(row=5,column=1,columnspan=2,sticky="NSEW")
        #Wind Rate
        self.wind_text = CTk.CTkLabel(master=self,text="Wind Rate",padx=20)
        self.wind_text.grid(row=6,column=0)
        self.windx = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.windx.grid(row=6,column=1)
        self.windx.insert(0,0)
        self.windy = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=0.0,border_width=1)
        self.windy.grid(row=6,column=2)
        self.windy.insert(0,0)

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
        
        #Boundary Function
        self.boundary_text = CTk.CTkLabel(master=self,text="Boundary Function",padx=20)
        self.boundary_text.grid(row=10,column=0)
        self.boundary_function = CTk.CTkOptionMenu(master=self,corner_radius=0,bg_color="transparent",values=["Bounce","Wrap","Stop"],command=self.master.set_boundary_function)
        self.boundary_function.grid(row=10,column=1,columnspan=2,sticky="NSEW")


        #Number of robots
        self.robot_text = CTk.CTkLabel(master=self,text="Robot Count",padx=20)
        self.robot_text.grid(row=11,column=0)
        self.robot_count = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=20,border_width=1)
        self.robot_count.insert(0,20)
        self.robot_count.grid(row=11,column=1,columnspan=2,sticky="EW")


        #Proportion of leader robots
        self.leader_text = CTk.CTkLabel(master=self,text="Leaders Proportion",padx=20)
        self.leader_text.grid(row=12,column=0)
        self.leader = CTk.CTkEntry(master=self,corner_radius=0,placeholder_text=20,border_width=1)
        self.leader.insert(0,0.1)
        self.leader.grid(row=12,column=1,columnspan=2,sticky="EW")


        #Render the robots?
        self.draw_robots = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="Show Robots",command=self.master.set_draw_robots)
        self.draw_robots.grid(row=13,column=1,columnspan=3,sticky="EW")

        #Multiple Leaders?
        self.multiple_leaders = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="Multiple Leaders",command=self.master.set_multiple_leaders)
        self.multiple_leaders.grid(row=14,column=1,columnspan=3,sticky="EW")
        #Leaders Follow?
        self.leaders_follow = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="Leaders Follow")
        self.leaders_follow.grid(row=15,column=1,columnspan=3,sticky="EW")
        #Threading Used?
        self.threading = CTk.CTkCheckBox(master=self,corner_radius=0,border_width=1,text="CPU Threading")
        self.threading.grid(row=16,column=1,columnspan=3,sticky="EW")

        #CosPy Logo
        font = ("Arial",100)
        self.logo = CTk.CTkLabel(master=self,text="CosPy",text_color="grey",font=font)
        self.logo.grid(row=20,column=0,columnspan=3,rowspan=20)

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
        self.options_frame.pack(side="right",fill="both")
        #############

        ############# ALGORITHM EDITOR FRAME
        self.algorithm_frame = Algorithm_Editor(master=self,corner_radius=0)
        #self.algorithm_frame.pack(side="right",fill="both")
        #############

        ############# RENDER AND GRAPHS TAB FRAME
        self.tabview = CTk.CTkTabview(master=self)
        self.tabview.pack(padx=10,pady=(0,10),fill="both",expand=True)
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
        scale = float(self.options_frame.scale.get())
        robot_count = int(self.options_frame.robot_count.get())
        draw_robots = self.options_frame.draw_robots.get()
        deposit_size = self.options_frame.deposit_size.get()
        deposit_amount = self.options_frame.deposit_rate.get()
        evaporation_rate = int(self.options_frame.evaporation_rate.get())
        diffusion_rate = int(self.options_frame.diffusion.get())
        wind_speed = (int(self.options_frame.windx.get()),int(self.options_frame.windy.get()))
        leaders = float(self.options_frame.leader.get())


        self.embed.destroy()
        self.embed = Frame(master=self.tabview.tab("Simulation"),width=width,height=height)
        self.embed.pack()
        self.graphs_embed.reset()
        self.renderer = Renderer(width,height,scale,self.embed.winfo_id(),int(deposit_size),deposit_amount,evaporation_rate,diffusion_rate,wind_speed)
        self.renderer.render_robot = draw_robots
        self.bind("<space>", self.renderer.change_colour)
        self.robots_array=[]
        for i in range(robot_count):
            self.robots_array.append(Robot(random.randint(50,int(width*scale)-50),random.randint(50,int(height*scale)-50)))
        if self.multiple_leaders:
            leaders = int(leaders*robot_count)
            for i in range(leaders):
                self.robots_array[i].leader = True

        else:
            self.robots_array[0].leader = True



    def set_draw_robots(self):
        self.renderer.render_robot = not self.renderer.render_robot

    def set_multiple_leaders(self):
        leaders = float(self.options_frame.leader.get())
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

#TODO
# Add FPS limit
# Fix wrap
# Add robot speed, angle speed, randomness
# ADD TEMPERATURE TOGGLE OPTION
# Add graphs
# Add show pheromone scanners
# Add create video mode
# Only render when shown? (quicker if not)
# Create a layer system to have multiple pheromones and envs
# LOOK at maths behind cosphi
# Add all variable options
# Add threading option for robots
# Test on smaller screen and make resizable
# Add saving
# FIX MULTIPLE LEADER SYSTEM



