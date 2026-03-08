"""pong"""
import ctypes
import os

os.environ["SDL_MAIN_USE_CALLBACKS"] = "1"
os.environ["SDL_RENDER_DRIVER"] = "opengl"

import sdl3 # pylint: disable=wrong-import-position

class GlobalData():
    """global data"""
    RENDERER = ctypes.POINTER(sdl3.SDL_Renderer)()
    WINDOW = ctypes.POINTER(sdl3.SDL_Window)()

    LEFT_RACKET_KEYS = { "up": False, "down": False }
    RIGHT_RACKET_KEYS = { "up": False, "down": False }

    font = None
    TEXTCOLOR = sdl3.SDL_Color(255, 255, 255)

    scoreLeft = 0
    scoreRight = 0

    CANVAS_WIDTH = 500
    CANVAS_HEIGHT = 200

    # Rackets in general
    RACKET_WIDTH = 10
    RACKET_HEIGHT = 80
    RACKET_SPEED = 190

    # Left racket position
    RACKET_LEFT_X = 10
    racketLeftY = 50

    # Right racket position
    RACKET_RIGHT_X = CANVAS_WIDTH - RACKET_WIDTH - 10
    racketRightY = 50

    lastTime = 0

    ballPosX = CANVAS_WIDTH / 2
    ballPosY = CANVAS_HEIGHT / 2
    ballDirX = -1
    ballDirY = 0
    BALL_SIZE = 8
    BALL_SPEED = 125

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
    "Pong NoobTuts using PySDL3".encode(), GlobalData.CANVAS_WIDTH,
    GlobalData.CANVAS_HEIGHT, 0, GlobalData.WINDOW, GlobalData.RENDERER):
        sdl3.SDL_Log("Couldn't create window/renderer: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    sdl3.SDL_SetRenderVSync(GlobalData.RENDERER, 1) # Turn on vertical sync
    GlobalData.font = sdl3.TTF_OpenFont("C:/Windows/Fonts/arial.ttf".encode(), 26)
    if not GlobalData.font:
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
            GlobalData.LEFT_RACKET_KEYS["up"] = True
        if sdl3.SDL_DEREFERENCE(event).key.scancode == sdl3.SDL_SCANCODE_S:
            GlobalData.LEFT_RACKET_KEYS["down"] = True
        if sdl3.SDL_DEREFERENCE(event).button.button == sdl3.SDL_SCANCODE_UP:
            GlobalData.RIGHT_RACKET_KEYS["up"] = True
        if sdl3.SDL_DEREFERENCE(event).button.button == sdl3.SDL_SCANCODE_DOWN:
            GlobalData.RIGHT_RACKET_KEYS["down"] = True
    elif sdl3.SDL_DEREFERENCE(event).type == sdl3.SDL_EVENT_KEY_UP:
        if sdl3.SDL_DEREFERENCE(event).key.scancode == sdl3.SDL_SCANCODE_W:
            GlobalData.LEFT_RACKET_KEYS["up"] = False
        if sdl3.SDL_DEREFERENCE(event).key.scancode == sdl3.SDL_SCANCODE_S:
            GlobalData.LEFT_RACKET_KEYS["down"] = False
        if sdl3.SDL_DEREFERENCE(event).button.button == sdl3.SDL_SCANCODE_UP:
            GlobalData.RIGHT_RACKET_KEYS["up"] = False
        if sdl3.SDL_DEREFERENCE(event).button.button == sdl3.SDL_SCANCODE_DOWN:
            GlobalData.RIGHT_RACKET_KEYS["down"] = False

    return sdl3.SDL_APP_CONTINUE

def keyboard(delta_time):
    """keyboard"""
    # Left racket
    if GlobalData.LEFT_RACKET_KEYS["up"]:
        GlobalData.racketLeftY -= GlobalData.RACKET_SPEED * delta_time
    if GlobalData.LEFT_RACKET_KEYS["down"]:
        GlobalData.racketLeftY += GlobalData.RACKET_SPEED * delta_time

    # Right racket
    if GlobalData.RIGHT_RACKET_KEYS["up"]:
        GlobalData.racketRightY -= GlobalData.RACKET_SPEED * delta_time
    if GlobalData.RIGHT_RACKET_KEYS["down"]:
        GlobalData.racketRightY += GlobalData.RACKET_SPEED * delta_time

def update_ball(delta_time):
    """update_ball"""
    # Fly the ball a bit
    GlobalData.ballPosX += GlobalData.ballDirX * GlobalData.BALL_SPEED * delta_time
    GlobalData.ballPosY += GlobalData.ballDirY * GlobalData.BALL_SPEED * delta_time

    # Hit by left racket?
    if (
            GlobalData.ballPosX < GlobalData.RACKET_LEFT_X + GlobalData.RACKET_WIDTH and
            GlobalData.ballPosX > GlobalData.RACKET_LEFT_X and
            GlobalData.ballPosY < GlobalData.racketLeftY +
            GlobalData.RACKET_HEIGHT and GlobalData.ballPosY > GlobalData.racketLeftY
        ):
        # Set the fly direction depending on where it hit the racket
        # t is 0.5 if hit at top, 0 at center, -0.5 at bottom
        t = ((GlobalData.ballPosY - GlobalData.racketLeftY) / GlobalData.RACKET_HEIGHT) - 0.5
        GlobalData.ballDirX = abs(GlobalData.ballDirX) # Force it to be positive
        GlobalData.ballDirY = t
        print(t)

    # Hit by right racket?
    if (
            GlobalData.ballPosX < GlobalData.RACKET_RIGHT_X + GlobalData.RACKET_WIDTH and
            GlobalData.ballPosX > GlobalData.RACKET_RIGHT_X and
            GlobalData.ballPosY < GlobalData.racketRightY + GlobalData.RACKET_HEIGHT and
            GlobalData.ballPosY > GlobalData.racketRightY
        ):
        # Set the fly direction depending on where it hit the racket
        # t is 0.5 if hit at top, 0 at center, -0.5 at bottom
        t = ((GlobalData.ballPosY - GlobalData.racketRightY) / GlobalData.RACKET_HEIGHT) - 0.5
        GlobalData.ballDirX = -abs(GlobalData.ballDirX) # Force it to be negative
        GlobalData.ballDirY = t
        print(t)

    # Hit left wall?
    if GlobalData.ballPosX < 0:
        GlobalData.scoreRight += 1
        GlobalData.ballPosX = GlobalData.CANVAS_WIDTH / 2
        GlobalData.ballPosY = GlobalData.CANVAS_HEIGHT / 2
        GlobalData.ballDirX = abs(GlobalData.ballDirX) # Force it to be positive
        GlobalData.ballDirY = 0

    # Hit right wall?
    if GlobalData.ballPosX > GlobalData.CANVAS_WIDTH:
        GlobalData.scoreLeft += 1
        GlobalData.ballPosX = GlobalData.CANVAS_WIDTH / 2
        GlobalData.ballPosY = GlobalData.CANVAS_HEIGHT / 2
        GlobalData.ballDirX = -abs(GlobalData.ballDirX) # Force it to be negative
        GlobalData.ballDirY = 0

    # Hit top wall?
    if GlobalData.ballPosY < 0:
        GlobalData.ballDirY = abs(GlobalData.ballDirY) # Force to be positive

    # Hit bottom wall?
    if GlobalData.ballPosY > GlobalData.CANVAS_HEIGHT:
        GlobalData.ballDirY = -abs(GlobalData.ballDirY) # Force bot negativef

@sdl3.SDL_AppIterate_func
def SDL_AppIterate(appstate):# pylint: disable=invalid-name, unused-argument
    """SDL_AppIterate"""
    # Delta time
    current_time = sdl3.SDL_GetTicks()
    delta_time = (current_time - GlobalData.lastTime) / 1000
    GlobalData.lastTime = current_time

    # Input handling
    keyboard(delta_time)

    # Update the ball
    update_ball(delta_time)

    sdl3.SDL_SetRenderDrawColor(GlobalData.RENDERER, 0, 0, 0, sdl3.SDL_ALPHA_OPAQUE)
    sdl3.SDL_RenderClear(GlobalData.RENDERER)

    # Draw the left racket
    sdl3.SDL_SetRenderDrawColor(GlobalData.RENDERER, 255, 255, 255, sdl3.SDL_ALPHA_OPAQUE)
    rect = sdl3.SDL_FRect(GlobalData.RACKET_LEFT_X, GlobalData.racketLeftY,
    GlobalData.RACKET_WIDTH, GlobalData.RACKET_HEIGHT)
    sdl3.SDL_RenderFillRect(GlobalData.RENDERER, rect)

    # Draw the right racket
    sdl3.SDL_SetRenderDrawColor(GlobalData.RENDERER, 255, 255, 255, sdl3.SDL_ALPHA_OPAQUE)
    rect = sdl3.SDL_FRect(GlobalData.RACKET_RIGHT_X, GlobalData.racketRightY,
    GlobalData.RACKET_WIDTH, GlobalData.RACKET_HEIGHT)
    sdl3.SDL_RenderFillRect(GlobalData.RENDERER, rect)

    # Draw the ball
    sdl3.SDL_SetRenderDrawColor(GlobalData.RENDERER, 255, 255, 255, sdl3.SDL_ALPHA_OPAQUE)
    rect = sdl3.SDL_FRect(GlobalData.ballPosX - GlobalData.BALL_SIZE / 2, GlobalData.ballPosY -
    GlobalData.BALL_SIZE / 2, GlobalData.BALL_SIZE, GlobalData.BALL_SIZE)
    sdl3.SDL_RenderFillRect(GlobalData.RENDERER, rect)

    score_text = "%d:%d".encode() % (GlobalData.scoreLeft, GlobalData.scoreRight)
    surface = sdl3.TTF_RenderText_Blended(GlobalData.font, score_text, len(score_text),
    GlobalData.TEXTCOLOR)
    GlobalData.textTexture = sdl3.SDL_CreateTextureFromSurface(GlobalData.RENDERER, surface)
    sdl3.SDL_DestroySurface(surface)

    width, height = ctypes.c_float(), ctypes.c_float()
    sdl3.SDL_GetTextureSize(GlobalData.textTexture, ctypes.byref(width), ctypes.byref(height))
    rect = sdl3.SDL_FRect(GlobalData.CANVAS_WIDTH / 2 - 18, 5, width.value, height.value)
    sdl3.SDL_RenderTexture(GlobalData.RENDERER, GlobalData.textTexture, None, rect)

    sdl3.SDL_RenderPresent(GlobalData.RENDERER)
    sdl3.SDL_DestroyTexture(GlobalData.textTexture)
    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppQuit_func
def SDL_AppQuit(appstate, result):# pylint: disable=invalid-name, unused-argument
    """SDL_AppQuit"""
