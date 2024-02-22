from sdl2 import *
import tkinter as tk
from tkinter import *
import random, ctypes
import customtkinter as CTk

def draw():
    global renderer
    x1 = ctypes.c_int(random.randrange(0, 600))
    y1 = ctypes.c_int(random.randrange(0, 500))
    x2 = ctypes.c_int(random.randrange(0, 600))
    y2 = ctypes.c_int(random.randrange(0, 500))
    r = ctypes.c_ubyte(random.randrange(0, 255))
    g = ctypes.c_ubyte(random.randrange(0, 255))
    b = ctypes.c_ubyte(random.randrange(0, 255))
    SDL_SetRenderDrawColor(renderer, r, g, b, ctypes.c_ubyte(255))
    SDL_RenderDrawLine(renderer, x1, y1, x2, y2)

def sdl_update():
    global window, event, renderer
    SDL_RenderPresent(renderer);
    if SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == SDL_QUIT:
            SDL_DestroyRenderer(renderer)
            SDL_DestroyWindow(window)
            SDL_Quit()

# tkinter stuff #
root = CTk.CTk()
embed = tk.Frame(root, width = 500, height = 500) #creates embed frame for pygame window
embed.grid(columnspan = (600), rowspan = 500) # Adds grid
embed.pack(side = LEFT) #packs window to the left
buttonwin = CTk.CTkFrame(root, width = 75, height = 500)
buttonwin.pack(side = LEFT)
button1 = Button(buttonwin,text = 'Draw',  command=draw)
button1.pack(side=LEFT)
root.update()
#################################
# SDL window stuff #
SDL_Init(SDL_INIT_VIDEO)
window = SDL_CreateWindowFrom(embed.winfo_id())
renderer = SDL_CreateRenderer(window, -1, 0)
SDL_SetRenderDrawColor(renderer, ctypes.c_ubyte(255), ctypes.c_ubyte(255), 
                                ctypes.c_ubyte(255), ctypes.c_ubyte(255))
SDL_RenderClear(renderer)
event = SDL_Event()
draw()

while True:
    sdl_update()
    root.update()