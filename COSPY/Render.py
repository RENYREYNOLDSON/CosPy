
import sdl2
import sdl2.ext
import time

WIDTH,HEIGHT=1000,800

sdl2.ext.init()

window = sdl2.ext.Window("Rendered Image", size=(WIDTH, HEIGHT))
window.show()

surf = sdl2.SDL_CreateRGBSurface(0,WIDTH,HEIGHT,32,0,0,0,0)

pixels = sdl2.ext.PixelView(surf)



# Initialize variables for framerate calculation
start_time = time.time()
frame_count = 0
count=0
# Main loop
running = True
while running:
    for event in sdl2.ext.get_events():
        if event.type == sdl2.SDL_QUIT:
            running = False

    # Enable alpha blending
    sdl2.SDL_SetSurfaceAlphaMod(surf, sdl2.SDL_ALPHA_OPAQUE)  # Reset alpha modulation
    sdl2.SDL_SetSurfaceBlendMode(surf, sdl2.SDL_BLENDMODE_BLEND)  # Enable blending

    for i in range(50+count):
        pixels[40][i]=(255, 0, 0, 255) 
        pixels[i][i]=(255, 255, 0, 255) 
    count+=1
    # Blit the surface onto the window's surface
    sdl2.SDL_BlitSurface(surf, None, window.get_surface(), None)

    # Update the window
    window.refresh()

    # Calculate framerate
    frame_count += 1
    if time.time() - start_time >= 1.0:  # Update every second
        framerate = frame_count / (time.time() - start_time)
        window.title = f"Rendered Image - FPS: {framerate:.2f}"
        frame_count = 0
        start_time = time.time()

# Clean up
sdl2.ext.quit()