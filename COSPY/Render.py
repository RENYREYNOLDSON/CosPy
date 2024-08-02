########################
########################
########################  RENDER CODE FOR COSPY
######################## 
########################
########################

import sdl2
import sdl2.ext
import sdl2.sdlgfx
import time
import random
import ctypes
import math
import numpy as np
from scipy.ndimage import convolve
import cv2

class Renderer:
    def __init__(self,
                 w,
                 h,
                 scale,
                 embed,
                 evaporation_rate,
                 diffusion_rate,
                 wind_speed,
                 use_temperature,
                 temperature_colour,
                 pheromone_colour,
                 aggregation_radius):
        self.w = w
        self.h = h
        self.scale=scale
        self.surfw = int(w*self.scale)
        self.surfh = int(h*self.scale)
        self.evaporation_rate = evaporation_rate#Number of ticks for each evaporation
        self.diffusion_rate = diffusion_rate
        self.wind_speed = wind_speed
        self.aggregation_radius = aggregation_radius
        self.show_walls = False
        self.start_time = time.time()
        self.frame_count = 0
        self.framerate=0
        self.count=0
        self.running = True
        self.render_robot=False
        self.embed = embed
        self.use_temperature = use_temperature
        self.temperature_array = create_temperature_array(self.surfh,self.surfw,temperature_colour)



        sdl2.ext.init()
        self.window = sdl2.ext.window.Window("d",(self.w,self.h))

        # Set the SDL_WINDOWID hint to embed the SDL window into the Tkinter frame
        if self.embed!=None:
            self.window.window = sdl2.SDL_CreateWindowFrom(embed)
        
        #Pheromone Surface
        self.surf = sdl2.SDL_CreateRGBSurface(0,self.surfw,self.surfh,32, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)
        self.pixels = sdl2.ext.pixels3d(self.surf)
        self.pixels[:]=pheromone_colour

        #Create environment surface!
        self.env_surf = sdl2.SDL_CreateRGBSurface(0,self.surfw,self.surfh,32, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)
        self.env_pixels = sdl2.ext.pixels3d(self.env_surf)
        self.env_pixels+=self.temperature_array

        #UI Surface
        self.UI_surf = sdl2.SDL_CreateRGBSurface(0,self.w,self.h,32, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)
        rend = sdl2.ext.Renderer(self.UI_surf)
        #Add circle on top
        sdl2.sdlgfx.circleRGBA(rend.sdlrenderer,int(self.w/2),int(self.h/2),aggregation_radius,0,0,0,255)
        rend.present()

        #Show Window
        self.window.show()



    def update_environment(self):

        #1. EVAPORATION
        if self.frame_count%self.evaporation_rate == 0:
            self.pixels = evaporate(self.pixels) 

        #2. DIFFUSION
        if self.frame_count%self.diffusion_rate == 0:
            self.pixels = diffuse(self.pixels)

        #3. WIND
        if self.wind_speed!=(0,0):
            self.pixels[0:self.surfw,0:self.surfh] = np.roll(self.pixels[0:self.surfw,0:self.surfh],self.wind_speed,axis=(0,1))
        
        return

    def refresh(self,robots_array):
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                self.running = False
                return 

        # Blit the surface onto the window's surface
        # Scale the original surface to fit the window size
        sdl2.SDL_FillRect(self.window.get_surface(),None,0x000000)
        if self.use_temperature:
            sdl2.SDL_BlitScaled(self.env_surf,None,self.window.get_surface(),None)


        sdl2.SDL_BlitScaled(self.surf,None,self.window.get_surface(),None)
        
        if self.use_temperature:
            sdl2.SDL_BlitSurface(self.UI_surf,None,self.window.get_surface(),None)


        #### Draw The Robots
        if self.render_robot:
            for r in robots_array:
                # Define triangle vertices
                center = (r.x/self.scale, r.y/self.scale)
                # Define triangle color
                color = sdl2.ext.Color(r.colour[0],r.colour[1],r.colour[2])
                try:
                    draw_triangle(self.window.get_surface(), center,100,r.angle,color)
                except:#Sometimes out of range so cannot draw!
                    pass
        else:
            try:
                pixels2 = sdl2.ext.pixels3d(self.window.get_surface())
                for r in robots_array:
                    pixels2[int(r.x/self.scale)][int(r.y/self.scale)]=[255,255,255,255]
            except Exception as e:
                print(e)

        self.window.refresh()


        # Calculate framerate
        self.frame_count += 1
        if time.time() - self.start_time >= 1.0:  # Update every second
            self.framerate = self.frame_count / (time.time() - self.start_time)
            self.frame_count = 0
            self.start_time = time.time()

    def close(self):
        sdl2.ext.quit()
        

    def add_pheromone_old(self,x,y,size,rate,colour):
        colour = [x * float(rate) for x in colour]
        colour = 1
        r = int(size/2)
        x_min = max(0,int(x)-r)
        x_max = min(self.w,int(x)+r)
        y_min = max(0,int(y)-r)
        y_max = min(self.h,int(y)+r)
        value_array = np.array(colour, dtype=self.pixels.dtype)
        # Ensure addition won't exceed 255
        max_value = 255 - value_array
        add_region = self.pixels[x_min:x_max, y_min:y_max]
        add_region = np.minimum(add_region, max_value)
        # Add the value array to the specified region
        self.pixels[x_min:x_max, y_min:y_max,3] = add_region + value_array
        return

    def add_pheromone(self,x,y,size,rate):
        if rate<1:#If rate less than one then only drop 1/x of the time
            val = random.random()
            if val<rate:
                rate=1
            else:
                rate=0

        r = int(size/2)
        x_min = max(0,int(x)-r)
        x_max = min(self.w,int(x)+r)
        y_min = max(0,int(y)-r)
        y_max = min(self.h,int(y)+r)
        # Ensure addition won't exceed 255
        max_value = 255 - rate
        add_region = self.pixels[x_min:x_max, y_min:y_max]
        add_region = np.minimum(add_region, max_value)
        # Add the value array to the specified region
        self.pixels[x_min:x_max, y_min:y_max] = add_region + [0,0,0,rate]
        return


def evaporate(pixels):
    #pixels[...,0] = (pixels[..., 0] - 1) % 255  # Red channel
    #pixels[...,1] = (pixels[..., 1] - 1) % 255  # Red channel
    #pixels[...,2] = (pixels[..., 2] - 1) % 255  # Red channel
    pixels[...,3] = (pixels[..., 3] - 1) % 255  # Alpha channel
    return pixels


def diffusion_kernel(size):
    """Generate a diffusion kernel."""
    kernel = np.zeros((size, size))
    center = size // 2
    for i in range(size):
        for j in range(size):
            kernel[i, j] = 1 / (1 + np.sqrt((i - center)**2 + (j - center)**2))
    return kernel / np.sum(kernel)


def diffuse(pixels):
    # Define a blur kernel
    # Define the size and sigma for the Gaussian kernel
    kernel_size = 3  # Adjust this according to the desired kernel size
    # Generate a diffusion kernel
    diff_kernel = diffusion_kernel(kernel_size)
    pixels[:, :, 3] = convolve(pixels[:, :, 3], diff_kernel, mode='constant', cval=0.0)
    return pixels

def rotate_point(center, point, angle):
    #Rotate a point around a center by a given angle (in degrees).
    cx, cy = center
    px, py = point
    angle_rad = angle+math.pi/2
    qx = cx + math.cos(angle_rad) * (px - cx) - math.sin(angle_rad) * (py - cy)
    qy = cy + math.sin(angle_rad) * (px - cx) + math.cos(angle_rad) * (py - cy)
    return int(qx), int(qy)


def draw_triangle(surface, center, size, angle, color):
    # Calculate the coordinates of the vertices of the equilateral triangle
    base_len = size / math.sqrt(3)
    half_base = base_len / 2
    height = size * math.sqrt(3) / 2
    top_vertex = (center[0], center[1] - height / 2)
    left_vertex = (center[0] - half_base, center[1] + height / 2)
    right_vertex = (center[0] + half_base, center[1] + height / 2)
    # Rotate the vertices by the given angle around the center
    top_vertex = rotate_point(center, top_vertex, angle)
    left_vertex = rotate_point(center, left_vertex, angle)
    right_vertex = rotate_point(center, right_vertex, angle)
    # Draw lines to form the triangle
    sdl2.ext.line(surface, color, (top_vertex[0],top_vertex[1],left_vertex[0],left_vertex[1]), width=1)
    sdl2.ext.line(surface, color, (left_vertex[0],left_vertex[1],right_vertex[0],right_vertex[1]), width=1)
    sdl2.ext.line(surface, color, (right_vertex[0],right_vertex[1],top_vertex[0],top_vertex[1]), width=1)

def create_temperature_array(w,h,colour):
    # Calculate center coordinates
    center_x = (w - 1) / 2
    center_y = (h - 1) / 2
    #Create meshgrid for distances from center
    Y, X = np.mgrid[:h, :w]
    distances = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
    #Normalize distances
    max_distance = np.sqrt(center_x**2 + center_y**2)
    normalized_distances = 1 - distances / max_distance
    #Ensure values are within [0, 1] range
    normalized_distances = np.clip(normalized_distances, 0, 1)
    #Create gradient array
    gradient_array = np.zeros((h, w, 4), dtype=np.uint8)
    gradient_array[:, :, 0] = colour[0]
    gradient_array[:, :, 1] = colour[1]
    gradient_array[:, :, 2] = colour[2]
    gradient_array[:, :, 3] = 255*normalized_distances  # Alpha channel
    return gradient_array

