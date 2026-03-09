"""pong"""
import ctypes
import os
os.environ["SDL_MAIN_USE_CALLBACKS"] = "1"
os.environ["SDL_RENDER_DRIVER"] = "opengl"
import sdl3 # pylint: disable=wrong-import-position

RENDERER = ctypes.POINTER(sdl3.SDL_Renderer)()
WINDOW = ctypes.POINTER(sdl3.SDL_Window)()
LEFT_RACKET_KEYS = { "up": False, "down": False }
RIGHT_RACKET_KEYS = { "up": False, "down": False }
TEXTCOLOR = sdl3.SDL_Color(255, 255, 255)
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 200
RACKET_WIDTH = 10
RACKET_HEIGHT = 80
RACKET_SPEED = 190
RACKET_LEFT_X = 10
RACKET_RIGHT_X = CANVAS_WIDTH - RACKET_WIDTH - 10
BALL_SIZE = 8
BALL_SPEED = 125

GLOBAL_DATA = {
    "font" : None,
    "scoreLeft" : 0,
    "scoreRight" : 0,
    "racketLeftY" : 50,
    "racketRightY" : 50,
    "lastTime" : 0,
    "ballPosX" : CANVAS_WIDTH / 2,
    "ballPosY" : CANVAS_HEIGHT / 2,
    "ballDirX" : -1,
    "ballDirY" : 0
}

@sdl3.SDL_AppInit_func
def SDL_AppInit(appstate, argc, argv):# pylint: disable=invalid-name, unused-argument
    """SDL_AppInit"""
    if not sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO):
        sdl3.SDL_Log("Couldn't initialize SDL: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    # Initialize the TTF library
    if not sdl3.TTF_Init():
        sdl3.SDL_Log("Couldn't initialize TTF: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    if not sdl3.SDL_CreateWindowAndRenderer(
    "Pong NoobTuts using PySDL3".encode(), CANVAS_WIDTH,
    CANVAS_HEIGHT, 0, WINDOW, RENDERER):
        sdl3.SDL_Log("Couldn't create window/renderer: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    sdl3.SDL_SetRenderVSync(RENDERER, 1) # Turn on vertical sync
    GLOBAL_DATA["font"] = sdl3.TTF_OpenFont("C:/Windows/Fonts/arial.ttf".encode(), 26)
    if not GLOBAL_DATA["font"]:
        sdl3.SDL_Log("Error: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppEvent_func
def SDL_AppEvent(appstate, event):# pylint: disable=invalid-name, unused-argument
    """SDL_AppEvent"""
    if sdl3.SDL_DEREFERENCE(event).type == sdl3.SDL_EVENT_QUIT:
        return sdl3.SDL_APP_SUCCESS
    if sdl3.SDL_DEREFERENCE(event).type == sdl3.SDL_EVENT_KEY_DOWN:
        if sdl3.SDL_DEREFERENCE(event).key.scancode == sdl3.SDL_SCANCODE_W:
            LEFT_RACKET_KEYS["up"] = True
        if sdl3.SDL_DEREFERENCE(event).key.scancode == sdl3.SDL_SCANCODE_S:
            LEFT_RACKET_KEYS["down"] = True
        if sdl3.SDL_DEREFERENCE(event).key.scancode == sdl3.SDL_SCANCODE_UP:
            RIGHT_RACKET_KEYS["up"] = True
        if sdl3.SDL_DEREFERENCE(event).key.scancode == sdl3.SDL_SCANCODE_DOWN:
            RIGHT_RACKET_KEYS["down"] = True
    elif sdl3.SDL_DEREFERENCE(event).type == sdl3.SDL_EVENT_KEY_UP:
        if sdl3.SDL_DEREFERENCE(event).key.scancode == sdl3.SDL_SCANCODE_W:
            LEFT_RACKET_KEYS["up"] = False
        if sdl3.SDL_DEREFERENCE(event).key.scancode == sdl3.SDL_SCANCODE_S:
            LEFT_RACKET_KEYS["down"] = False
        if sdl3.SDL_DEREFERENCE(event).key.scancode == sdl3.SDL_SCANCODE_UP:
            RIGHT_RACKET_KEYS["up"] = False
        if sdl3.SDL_DEREFERENCE(event).key.scancode == sdl3.SDL_SCANCODE_DOWN:
            RIGHT_RACKET_KEYS["down"] = False

    return sdl3.SDL_APP_CONTINUE

def keyboard(delta_time):
    """keyboard"""
    # Left racket
    if LEFT_RACKET_KEYS["up"]:
        GLOBAL_DATA["racketLeftY"] -= RACKET_SPEED * delta_time
    if LEFT_RACKET_KEYS["down"]:
        GLOBAL_DATA["racketLeftY"] += RACKET_SPEED * delta_time

    # Right racket
    if RIGHT_RACKET_KEYS["up"]:
        GLOBAL_DATA["racketRightY"] -= RACKET_SPEED * delta_time
    if RIGHT_RACKET_KEYS["down"]:
        GLOBAL_DATA["racketRightY"] += RACKET_SPEED * delta_time

def update_ball(delta_time):
    """update_ball"""
    # Fly the ball a bit
    GLOBAL_DATA["ballPosX"] += GLOBAL_DATA["ballDirX"] * BALL_SPEED * delta_time
    GLOBAL_DATA["ballPosY"] += GLOBAL_DATA["ballDirY"] * BALL_SPEED * delta_time

    # Hit by left racket?
    if (
            GLOBAL_DATA["ballPosX"] < RACKET_LEFT_X + RACKET_WIDTH and
            GLOBAL_DATA["ballPosX"] > RACKET_LEFT_X and
            GLOBAL_DATA["ballPosY"] < GLOBAL_DATA["racketLeftY"] +
            RACKET_HEIGHT and GLOBAL_DATA["ballPosY"] > GLOBAL_DATA["racketLeftY"]
        ):
        # Set the fly direction depending on where it hit the racket
        # t is 0.5 if hit at top, 0 at center, -0.5 at bottom
        t = ((GLOBAL_DATA["ballPosY"] - GLOBAL_DATA["racketLeftY"]) / RACKET_HEIGHT) - 0.5
        GLOBAL_DATA["ballDirX"] = abs(GLOBAL_DATA["ballDirX"]) # Force it to be positive
        GLOBAL_DATA["ballDirY"] = t
        print(t)

    # Hit by right racket?
    if (
            GLOBAL_DATA["ballPosX"] < RACKET_RIGHT_X + RACKET_WIDTH and
            GLOBAL_DATA["ballPosX"] > RACKET_RIGHT_X and
            GLOBAL_DATA["ballPosY"] < GLOBAL_DATA["racketRightY"] + RACKET_HEIGHT and
            GLOBAL_DATA["ballPosY"] > GLOBAL_DATA["racketRightY"]
        ):
        # Set the fly direction depending on where it hit the racket
        # t is 0.5 if hit at top, 0 at center, -0.5 at bottom
        t = ((GLOBAL_DATA["ballPosY"] - GLOBAL_DATA["racketRightY"]) / RACKET_HEIGHT) - 0.5
        GLOBAL_DATA["ballDirX"] = -abs(GLOBAL_DATA["ballDirX"]) # Force it to be negative
        GLOBAL_DATA["ballDirY"] = t
        print(t)

    # Hit left wall?
    if GLOBAL_DATA["ballPosX"] < 0:
        GLOBAL_DATA["scoreRight"] += 1
        GLOBAL_DATA["ballPosX"] = CANVAS_WIDTH / 2
        GLOBAL_DATA["ballPosY"] = CANVAS_HEIGHT / 2
        GLOBAL_DATA["ballDirX"] = abs(GLOBAL_DATA["ballDirX"]) # Force it to be positive
        GLOBAL_DATA["ballDirY"] = 0

    # Hit right wall?
    if GLOBAL_DATA["ballPosX"] > CANVAS_WIDTH:
        GLOBAL_DATA["scoreLeft"] += 1
        GLOBAL_DATA["ballPosX"] = CANVAS_WIDTH / 2
        GLOBAL_DATA["ballPosY"] = CANVAS_HEIGHT / 2
        GLOBAL_DATA["ballDirX"] = -abs(GLOBAL_DATA["ballDirX"]) # Force it to be negative
        GLOBAL_DATA["ballDirY"] = 0

    # Hit top wall?
    if GLOBAL_DATA["ballPosY"] < 0:
        GLOBAL_DATA["ballDirY"] = abs(GLOBAL_DATA["ballDirY"]) # Force to be positive

    # Hit bottom wall?
    if GLOBAL_DATA["ballPosY"] > CANVAS_HEIGHT:
        GLOBAL_DATA["ballDirY"] = -abs(GLOBAL_DATA["ballDirY"]) # Force bot negativef

@sdl3.SDL_AppIterate_func
def SDL_AppIterate(appstate):# pylint: disable=invalid-name, unused-argument
    """SDL_AppIterate"""
    # Delta time
    current_time = sdl3.SDL_GetTicks()
    delta_time = (current_time - GLOBAL_DATA["lastTime"]) / 1000
    GLOBAL_DATA["lastTime"] = current_time

    # Input handling
    keyboard(delta_time)

    # Update the ball
    update_ball(delta_time)

    sdl3.SDL_SetRenderDrawColor(RENDERER, 0, 0, 0, sdl3.SDL_ALPHA_OPAQUE)
    sdl3.SDL_RenderClear(RENDERER)

    # Draw the left racket
    sdl3.SDL_SetRenderDrawColor(RENDERER, 255, 255, 255, sdl3.SDL_ALPHA_OPAQUE)
    rect = sdl3.SDL_FRect(RACKET_LEFT_X, GLOBAL_DATA["racketLeftY"],
    RACKET_WIDTH, RACKET_HEIGHT)
    sdl3.SDL_RenderFillRect(RENDERER, rect)

    # Draw the right racket
    sdl3.SDL_SetRenderDrawColor(RENDERER, 255, 255, 255, sdl3.SDL_ALPHA_OPAQUE)
    rect = sdl3.SDL_FRect(RACKET_RIGHT_X, GLOBAL_DATA["racketRightY"],
    RACKET_WIDTH, RACKET_HEIGHT)
    sdl3.SDL_RenderFillRect(RENDERER, rect)

    # Draw the ball
    sdl3.SDL_SetRenderDrawColor(RENDERER, 255, 255, 255, sdl3.SDL_ALPHA_OPAQUE)
    rect = sdl3.SDL_FRect(GLOBAL_DATA["ballPosX"] - BALL_SIZE / 2, GLOBAL_DATA["ballPosY"] -
    BALL_SIZE / 2, BALL_SIZE, BALL_SIZE)
    sdl3.SDL_RenderFillRect(RENDERER, rect)

    score_text = "%d:%d".encode() % (GLOBAL_DATA["scoreLeft"], GLOBAL_DATA["scoreRight"])
    surface = sdl3.TTF_RenderText_Blended(GLOBAL_DATA["font"], score_text, len(score_text),
    TEXTCOLOR)
    text_texture = sdl3.SDL_CreateTextureFromSurface(RENDERER, surface)
    sdl3.SDL_DestroySurface(surface)

    width, height = ctypes.c_float(), ctypes.c_float()
    sdl3.SDL_GetTextureSize(text_texture, ctypes.byref(width), ctypes.byref(height))
    rect = sdl3.SDL_FRect(CANVAS_WIDTH / 2 - 18, 5, width.value, height.value)
    sdl3.SDL_RenderTexture(RENDERER, text_texture, None, rect)

    sdl3.SDL_RenderPresent(RENDERER)
    sdl3.SDL_DestroyTexture(text_texture)
    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppQuit_func
def SDL_AppQuit(appstate, result):# pylint: disable=invalid-name, unused-argument
    """SDL_AppQuit"""
