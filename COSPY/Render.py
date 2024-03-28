########################
########################
########################  RENDER CODE FOR COSPY
######################## 
########################
########################


import sdl2
import sdl2.ext
import time
import random
import ctypes
import math
import numpy as np
from scipy.ndimage import convolve


class Renderer:
    def __init__(self,w,h,scale,embed,pheromone_size,pheromone_amount,evaporation_rate,diffusion_rate,wind_speed):
        self.w = w
        self.h = h
        self.scale=scale
        self.surfw = int(w*self.scale)
        self.surfh = int(h*self.scale)
        self.pheromone_size = pheromone_size
        self.pheromone_amount = pheromone_amount
        self.evaporation_rate = evaporation_rate#Number of ticks for each evaporation
        self.diffusion_rate = diffusion_rate
        self.wind_speed = wind_speed
        self.pheromone_colour = [0,0,1,0]
        self.pheromone_colour = [x * float(self.pheromone_amount) for x in self.pheromone_colour]
        self.show_walls = False
        self.start_time = time.time()
        self.frame_count = 0
        self.count=0
        self.running = True
        self.embed = embed
        self.framerate=0
        self.temperature_array = create_temperature_array(self.surfh,self.surfw)
        sdl2.ext.init()
        self.window = sdl2.ext.window.Window("d",(self.w,self.h))

        # Set the SDL_WINDOWID hint to embed the SDL window into the Tkinter frame
        if self.embed!=None:
            self.window.window = sdl2.SDL_CreateWindowFrom(embed)
        self.surf = sdl2.SDL_CreateRGBSurface(0,self.surfw,self.surfh,32,0,0,0,0)
        self.pixels = sdl2.ext.pixels3d(self.surf)
        #self.pixels+=self.temperature_array

        #Create environment surface!
        self.env_surf = sdl2.SDL_CreateRGBSurface(0,self.surfw,self.surfh,32,0,0,0,0)
        self.env_pixels = sdl2.ext.pixels3d(self.env_surf)

        self.window.show()
        # Mouse Position
        self.x, self.y = ctypes.c_int(0), ctypes.c_int(0) # Create two ctypes values
        # Create a kernel with values based on distance from the center
        self.render_robot=False

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
            elif event.type == sdl2.SDL_KEYDOWN:
                # Check if the pressed key is the spacebar
                if event.key.keysym.sym == sdl2.SDLK_SPACE:
                    pheromone_colour = [random.random(),random.random(),random.random()]

        buttonstate = sdl2.mouse.SDL_GetMouseState(ctypes.byref(self.x), ctypes.byref(self.y))
        self.x.value = int(self.x.value*self.scale)
        self.y.value = int(self.y.value*self.scale)

        # Blit the surface onto the window's surface
        # Scale the original surface to fit the window size
        scaled_surf = sdl2.SDL_CreateRGBSurface(0, self.w, self.h, 32, 0, 0, 0, 0)
        sdl2.SDL_BlitScaled(self.surf, None, scaled_surf, None)


        #### Draw The Robots
        if self.render_robot:
            for r in robots_array:
                # Define triangle vertices
                center = (r.x/self.scale, r.y/self.scale)
                # Define triangle color
                color = sdl2.ext.Color(r.colour[0],r.colour[1],r.colour[2])
                try:
                    draw_triangle(scaled_surf, center,100,r.angle,color)
                except:#Sometimes out of range so cannot draw!
                    pass
        else:
            try:
                pixels2 = sdl2.ext.pixels3d(scaled_surf)
                for r in robots_array:
                    pixels2[int(r.x/self.scale)][int(r.y/self.scale)]=[255,255,255,255]
            except Exception as e:
                print(e)

        # Blit the scaled surface onto the window surface
        sdl2.SDL_BlitSurface(scaled_surf, None, self.window.get_surface(), None)

        #sdl2.SDL_BlitSurface(self.surf, None, self.window.get_surface(), None)
        self.window.refresh()

        # Calculate framerate
        self.frame_count += 1
        if time.time() - self.start_time >= 1.0:  # Update every second
            self.framerate = self.frame_count / (time.time() - self.start_time)
            self.frame_count = 0
            self.start_time = time.time()

    def close(self):
        sdl2.ext.quit()

    def change_colour(self,e):
        self.pheromone_colour = [random.random(),random.random(),random.random(),0]
        self.pheromone_colour = [x * float(self.pheromone_amount) for x in self.pheromone_colour]
        print("Chnaged")

    def add_pheromone(self,x,y):
        r = int(self.pheromone_size/2)
        x_min = max(0,int(x)-r)
        x_max = min(self.w,int(x)+r)
        y_min = max(0,int(y)-r)
        y_max = min(self.h,int(y)+r)
        value_array = np.array(self.pheromone_colour, dtype=self.pixels.dtype)
        # Ensure addition won't exceed 255
        max_value = 255 - value_array
        add_region = self.pixels[x_min:x_max, y_min:y_max]
        add_region = np.minimum(add_region, max_value)
        # Add the value array to the specified region
        self.pixels[x_min:x_max, y_min:y_max] = add_region + value_array
        return




def evaporate(pixels):
    pixels[...,0] = (pixels[..., 0] - 1) % 255  # Red channel
    #pixels[...,1] = (pixels[..., 1] - 1) % 255  # Red channel
    pixels[...,2] = (pixels[..., 2] - 1) % 255  # Red channel
    return pixels


def gaussian_kernel(size, sigma):
    """Generate a Gaussian kernel."""
    kernel = np.fromfunction(
        lambda x, y: (1/(2*np.pi*sigma**2)) * np.exp(-((x-size//2)**2 + (y-size//2)**2) / (2*sigma**2)),
        (size, size)
    )
    return kernel / np.sum(kernel)

def diffusion_kernel(size):
    """Generate a diffusion kernel."""
    kernel = np.zeros((size, size))
    center = size // 2
    for i in range(size):
        for j in range(size):
            kernel[i, j] = 1.0 / (1 + np.sqrt((i - center)**2 + (j - center)**2))
    return kernel / np.sum(kernel)


def diffuse(pixels):
    # Define a blur kernel
    # Define the size and sigma for the Gaussian kernel
    kernel_size = 3  # Adjust this according to the desired kernel size
    sigma = 1.0     # Adjust this according to the desired standard deviation

    # Generate a Gaussian kernel
    blur_kernel = gaussian_kernel(kernel_size, sigma)
    # Generate a diffusion kernel
    diff_kernel = diffusion_kernel(kernel_size)

    for i in [0,2]:  # Loop over RGB channels
        pixels[:, :, i] = convolve(pixels[:, :, i], diff_kernel, mode='constant', cval=0.0)

    return pixels


def apply_colour_kernel(array,kernel,x,y,colour):

    """
    Apply a kernel centered at position (x, y) within the array.
    """

    kernel_height, kernel_width = kernel.shape
    array_height, array_width = array.shape[:2]

    # Calculate the starting and ending indices for the kernel
    start_x = max(0, x - kernel_width // 2)
    start_y = max(0, y - kernel_height // 2)
    end_x = min(array_width, x + (kernel_width + 1) // 2)
    end_y = min(array_height, y + (kernel_height + 1) // 2)

    # Apply the kernel to the specified region
    for i in range(3):
        conv_result = convolve(array[start_y:end_y, start_x:end_x, i], kernel)
        scaled_result = conv_result * colour[i]*100
        print(scaled_result)
        array[start_y:end_y, start_x:end_x, i] += scaled_result.astype(array.dtype)
        #print(array[start_y:end_y, start_x:end_x, i])

    return array#np.clip(result, 0, 255).astype(np.uint8) 



def rotate_point(center, point, angle):
    """
    Rotate a point around a center by a given angle (in degrees).
    """
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

def create_temperature_array(w,h):
    # Calculate center coordinates
    center_x = (w - 1) / 2
    center_y = (h - 1) / 2

    # Create meshgrid for distances from center
    Y, X = np.mgrid[:h, :w]
    distances = np.sqrt((X - center_x)**2 + (Y - center_y)**2)

    # Normalize distances
    max_distance = np.sqrt(center_x**2 + center_y**2)
    normalized_distances = 1 - distances / max_distance

    # Ensure values are within [0, 1] range
    normalized_distances = np.clip(normalized_distances, 0, 1)

    # Create gradient array
    gradient_array = np.zeros((h, w, 4), dtype=np.uint8)
    gradient_array[:, :, 1] = 100  *normalized_distances# Green channel
    gradient_array[:, :, 3] = 255  # Alpha channel
    return gradient_array


if __name__ == "__main__":
    r = Renderer(1000,800,0.25,None)
    while True:
        r.refresh()