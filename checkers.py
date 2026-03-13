"""SDL3 test"""
import ctypes
import os
os.environ["SDL_MAIN_USE_CALLBACKS"] = "1"
# os.environ["SDL_RENDER_DRIVER"] = "opengl"
import sdl3 # pylint: disable=wrong-import-position

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

@sdl3.SDL_AppInit_func
def SDL_AppInit(appstate, argc, argv):# pylint: disable=invalid-name, unused-argument
    """SDL_AppInit"""
    if not sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO):
        sdl3.SDL_Log("Couldn't initialize SDL: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE
    sdl3.SDL_Log("SDL initialized".encode())

    window = ctypes.POINTER(sdl3.SDL_Window)()
    renderer = ctypes.POINTER(sdl3.SDL_Renderer)()
    if not sdl3.SDL_CreateWindowAndRenderer("Draw outline rectangles using PySDL3".encode(),
    WINDOW_WIDTH, WINDOW_HEIGHT, sdl3.SDL_WINDOW_RESIZABLE, window, renderer):
        sdl3.SDL_Log("Couldn't create window/renderer: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    # load image into texture
    tex_black = sdl3.IMG_LoadTexture(renderer, "./blender/black.ortho.png".encode())
    if not tex_black:
        sdl3.SDL_Log("Error: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE
    tex_white = sdl3.IMG_LoadTexture(renderer, "./blender/white.ortho.png".encode())
    if not tex_white:
        sdl3.SDL_Log("Error: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    sdl3.SDL_SetRenderLogicalPresentation(renderer, WINDOW_WIDTH, WINDOW_HEIGHT,
    sdl3.SDL_LOGICAL_PRESENTATION_LETTERBOX)
    sdl3.SDL_SetRenderVSync(renderer, 1) # Turn on vertical sync

    # add textures and renderer to appstate
    appstate[0] = ctypes.cast(
    ctypes.pointer(ctypes.py_object({
    "renderer" : renderer,
    "tex_black" : tex_black,
    "tex_white" : tex_white
    })), ctypes.c_void_p)

    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppEvent_func
def SDL_AppEvent(appstate, event):# pylint: disable=invalid-name, unused-argument
    """SDL_AppEvent"""
    if sdl3.SDL_DEREFERENCE(event).type == sdl3.SDL_EVENT_QUIT:
        return sdl3.SDL_APP_SUCCESS
    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppIterate_func
def SDL_AppIterate(appstate):# pylint: disable=invalid-name, unused-argument
    """SDL_AppIterate"""

    # retrieve renderer from appstate
    renderer = ctypes.cast(appstate, ctypes.POINTER(ctypes.py_object)).contents.value["renderer"]

    # As you can see from this, rendering draws over whatever was drawn before it
    sdl3.SDL_SetRenderDrawColor(renderer, 255, 255, 255, sdl3.SDL_ALPHA_OPAQUE)
    sdl3.SDL_RenderClear(renderer) # Start with a blank canvas
    sdl3.SDL_SetRenderDrawColor(renderer, 255, 0, 0, sdl3.SDL_ALPHA_OPAQUE)
    sdl3.SDL_RenderDebugText(renderer, 272, 100, "Hello world!".encode())

    # First rectangle
    sdl3.SDL_SetRenderDrawColor(renderer, 255, 0, 0, sdl3.SDL_ALPHA_OPAQUE)
    sdl3.SDL_RenderRect(renderer, sdl3.SDL_FRect(160, 70, 160, 20))

    # Second rectangle
    sdl3.SDL_SetRenderDrawColor(renderer, 0, 255, 0, sdl3.SDL_ALPHA_OPAQUE)
    sdl3.SDL_RenderRect(renderer, sdl3.SDL_FRect(20, 180, 160, 20))

    # Third rectangle
    sdl3.SDL_SetRenderDrawColor(renderer, 0, 0, 255, sdl3.SDL_ALPHA_OPAQUE)
    sdl3.SDL_RenderRect(renderer, sdl3.SDL_FRect(135, 290, 200, 20))

    # retrieve itextures from appstate
    tex_black = ctypes.cast(appstate, ctypes.POINTER(ctypes.py_object)).contents.value["tex_black"]
    tex_white = ctypes.cast(appstate, ctypes.POINTER(ctypes.py_object)).contents.value["tex_white"]
    width = 90
    height = 90
    blackx = 30
    whitex =100

    for row in range(6):
        for col in range(3):
            for bw in ((blackx, tex_black), (whitex, tex_white)):
                sdl3.SDL_RenderTexture(renderer, bw[1],
                None, sdl3.SDL_FRect(bw[0] + col * 140 + row * 35, 140 + row * 12, width, height))

    # sdl3.SDL_RenderTexture(renderer, tex_black, None, sdl3.SDL_FRect(90, 140, 90, 60))
    # sdl3.SDL_RenderTexture(renderer, tex_white, None, sdl3.SDL_FRect(160, 140, 90, 60))
    # sdl3.SDL_RenderTexture(renderer, tex_black, None, sdl3.SDL_FRect(230, 140, 90, 60))
    # sdl3.SDL_RenderTexture(renderer, tex_white, None, sdl3.SDL_FRect(300, 140, 90, 60))

    # sdl3.SDL_RenderTexture(renderer, tex_black, None, sdl3.SDL_FRect(125, 152, 90, 60))
    # sdl3.SDL_RenderTexture(renderer, tex_white, None, sdl3.SDL_FRect(195, 152, 90, 60))
    # sdl3.SDL_RenderTexture(renderer, tex_black, None, sdl3.SDL_FRect(265, 152, 90, 60))
    # sdl3.SDL_RenderTexture(renderer, tex_white, None, sdl3.SDL_FRect(335, 152, 90, 60))

    sdl3.SDL_RenderPresent(renderer)
    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppQuit_func
def SDL_AppQuit(appstate, result):# pylint: disable=invalid-name, unused-argument
    """SDL_AppQuit"""
    sdl3.SDL_Log("SDL quit".encode())
