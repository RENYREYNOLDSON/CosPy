
import sdl2
import sdl2.ext
import time
import random
import ctypes
import math
import numpy as np
from scipy.ndimage import convolve


class Renderer:
    def __init__(self,w,h,scale,embed):
        self.w = w
        self.h = h
        self.scale=scale
        self.surfw = int(w*self.scale)
        self.surfh = int(h*self.scale)
        self.pheromone_size = 50
        self.evaporation_rate = 4 #Number of ticks for each evaporation
        self.pheromone_colour = [0.5,0.4,1]
        self.start_time = time.time()
        self.frame_count = 0
        self.count=0
        self.running = True
        self.embed = embed
        self.framerate=0
        sdl2.ext.init()
        self.window = sdl2.ext.window.Window("d",(self.w,self.h))
        # Set the SDL_WINDOWID hint to embed the SDL window into the Tkinter frame
        if self.embed!=None:
            self.window.window = sdl2.SDL_CreateWindowFrom(embed)
        #self.renderer = sdl2.SDL_CreateRenderer(self.window, -1, 0)
        self.surf = sdl2.SDL_CreateRGBSurface(0,self.surfw,self.surfh,32,0,0,0,0)
        self.pixels = sdl2.ext.pixels3d(self.surf)
        self.window.show()
        # Mouse Position
        self.x, self.y = ctypes.c_int(0), ctypes.c_int(0) # Create two ctypes values

    def refresh(self):
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

        for hoz in range(int(self.x.value-self.pheromone_size/2),int(self.x.value+self.pheromone_size/2)):
            for ver in range(int(self.y.value-self.pheromone_size/2),int(self.y.value+self.pheromone_size/2)):
                if ver>0 and ver<self.surfh and hoz>0 and hoz<self.surfw:
                    dist = math.sqrt((self.x.value-hoz)**2+(self.y.value-ver)**2)
                    if dist<self.pheromone_size/2:
                        pix = self.pixels[hoz][ver]
                        if dist==0:
                            add=100
                        else:
                            add = 100/dist
                        self.pixels[hoz][ver]=[min(255*self.pheromone_colour[0],pix[0]+add*self.pheromone_colour[0]),min(255*self.pheromone_colour[1],pix[1]+add*self.pheromone_colour[1]),min(255*self.pheromone_colour[2],pix[2]+add*self.pheromone_colour[2]),pix[3]]
        #EVAPORATION
        if self.frame_count%self.evaporation_rate == 0:
            self.pixels = evaporate(self.pixels) 
            pass

        self.pixels = diffuse(self.pixels)

        # Blit the surface onto the window's surface
        # Scale the original surface to fit the window size
        scaled_surf = sdl2.SDL_CreateRGBSurface(0, self.w, self.h, 32, 0, 0, 0, 0)
        sdl2.SDL_BlitScaled(self.surf, None, scaled_surf, None)

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
        self.pheromone_colour = [random.random(),random.random(),random.random()]
        print("Chnaged")


def evaporate(pixels):
    pixels[...,0] = (pixels[..., 0] - 1) % 255  # Red channel
    pixels[...,1] = (pixels[..., 1] - 1) % 255  # Red channel
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
    blur_kernel = np.array([[1, 1, 1],
                            [1, 1, 1],
                            [1, 1, 1]]) / 9.0  # Averaging kernel
    
        # Define the size and sigma for the Gaussian kernel
    kernel_size = 3  # Adjust this according to the desired kernel size
    sigma = 1.0     # Adjust this according to the desired standard deviation

    # Generate a Gaussian kernel
    blur_kernel = gaussian_kernel(kernel_size, sigma)
    # Generate a diffusion kernel
    diff_kernel = diffusion_kernel(kernel_size)

    for i in range(3):  # Loop over RGB channels
        pixels[:, :, i] = convolve(pixels[:, :, i], diff_kernel, mode='constant', cval=0.0)

    return pixels

if __name__ == "__main__":
    r = Renderer(1000,800,0.25,None)
    while True:
        r.refresh()