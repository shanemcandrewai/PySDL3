import ctypes
import os

os.environ["SDL_MAIN_USE_CALLBACKS"] = "1"
os.environ["SDL_RENDER_DRIVER"] = "opengl"

import sdl3

renderer = ctypes.POINTER(sdl3.SDL_Renderer)()
window = ctypes.POINTER(sdl3.SDL_Window)()

leftRacketKeys = { "up": False, "down": False }
rightRacketKeys = { "up": False, "down": False }

font = None
textColor = sdl3.SDL_Color(255, 255, 255)

scoreLeft = 0
scoreRight = 0

canvasWidth = 500
canvasHeight = 200

# Rackets in general
racketWidth = 10
racketHeight = 80
racketSpeed = 190

# Left racket position
racketLeftX = 10
racketLeftY = 50

# Right racket position
racketRightX = canvasWidth - racketWidth - 10
racketRightY = 50

lastTime = 0

ballPosX = canvasWidth / 2
ballPosY = canvasHeight / 2
ballDirX = -1
ballDirY = 0
ballSize = 8
ballSpeed = 125

@sdl3.SDL_AppInit_func
def SDL_AppInit(appstate, argc, argv):
    global font
    global canvasWidth
    global canvasHeight

    if not sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO):
        sdl3.SDL_Log("Couldn't initialize SDL: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    # Initialize the TTF library
    if not sdl3.TTF_Init():
        sdl3.SDL_Log("Couldn't initialize TTF: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    if not sdl3.SDL_CreateWindowAndRenderer("Pong NoobTuts using PySDL3".encode(), canvasWidth, canvasHeight, 0, window, renderer):
        sdl3.SDL_Log("Couldn't create window/renderer: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    sdl3.SDL_SetRenderVSync(renderer, 1) # Turn on vertical sync

    font = sdl3.TTF_OpenFont("C:/Windows/Fonts/arial.ttf".encode(), 26)
    if not font:
        sdl3.SDL_Log("Error: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppEvent_func
def SDL_AppEvent(appstate, event):
    if sdl3.SDL_DEREFERENCE(event).type == sdl3.SDL_EVENT_QUIT:
        return sdl3.SDL_APP_SUCCESS
    elif sdl3.SDL_DEREFERENCE(event).type == sdl3.SDL_EVENT_KEY_DOWN:
        if sdl3.SDL_DEREFERENCE(event).key.scancode == sdl3.SDL_SCANCODE_W:
            leftRacketKeys["up"] = True
        if sdl3.SDL_DEREFERENCE(event).key.scancode == sdl3.SDL_SCANCODE_S:
            leftRacketKeys["down"] = True
        if sdl3.SDL_DEREFERENCE(event).button.button == sdl3.SDL_SCANCODE_UP:
            rightRacketKeys["up"] = True
        if sdl3.SDL_DEREFERENCE(event).button.button == sdl3.SDL_SCANCODE_DOWN:
            rightRacketKeys["down"] = True
    elif sdl3.SDL_DEREFERENCE(event).type == sdl3.SDL_EVENT_KEY_UP:
        if sdl3.SDL_DEREFERENCE(event).key.scancode == sdl3.SDL_SCANCODE_W:
            leftRacketKeys["up"] = False
        if sdl3.SDL_DEREFERENCE(event).key.scancode == sdl3.SDL_SCANCODE_S:
            leftRacketKeys["down"] = False
        if sdl3.SDL_DEREFERENCE(event).button.button == sdl3.SDL_SCANCODE_UP:
            rightRacketKeys["up"] = False
        if sdl3.SDL_DEREFERENCE(event).button.button == sdl3.SDL_SCANCODE_DOWN:
            rightRacketKeys["down"] = False

    return sdl3.SDL_APP_CONTINUE

def keyboard(deltaTime):
    global racketLeftY
    global racketRightY

    # Left racket
    if leftRacketKeys["up"]:
        racketLeftY -= racketSpeed * deltaTime
    if leftRacketKeys["down"]:
        racketLeftY += racketSpeed * deltaTime

    # Right racket
    if rightRacketKeys["up"]:
        racketRightY -= racketSpeed * deltaTime
    if rightRacketKeys["down"]:
        racketRightY += racketSpeed * deltaTime

def updateBall(deltaTime):
    global ballDirX
    global ballDirY
    global ballPosX
    global ballPosY
    global scoreRight
    global scoreLeft

    # Fly the ball a bit
    ballPosX += ballDirX * ballSpeed * deltaTime
    ballPosY += ballDirY * ballSpeed * deltaTime

    # Hit by left racket?
    if (
            ballPosX < racketLeftX + racketWidth and ballPosX > racketLeftX and
            ballPosY < racketLeftY + racketHeight and ballPosY > racketLeftY
        ):
        # Set the fly direction depending on where it hit the racket
        # t is 0.5 if hit at top, 0 at center, -0.5 at bottom
        t = ((ballPosY - racketLeftY) / racketHeight) - 0.5
        ballDirX = abs(ballDirX) # Force it to be positive
        ballDirY = t
        print(t)

    # Hit by right racket?
    if (
            ballPosX < racketRightX + racketWidth and ballPosX > racketRightX and
            ballPosY < racketRightY + racketHeight and ballPosY > racketRightY
        ):
        # Set the fly direction depending on where it hit the racket
        # t is 0.5 if hit at top, 0 at center, -0.5 at bottom
        t = ((ballPosY - racketRightY) / racketHeight) - 0.5
        ballDirX = -abs(ballDirX) # Force it to be negative
        ballDirY = t
        print(t)

    # Hit left wall?
    if ballPosX < 0:
        scoreRight += 1
        ballPosX = canvasWidth / 2
        ballPosY = canvasHeight / 2
        ballDirX = abs(ballDirX) # Force it to be positive
        ballDirY = 0

    # Hit right wall?
    if ballPosX > canvasWidth:
        scoreLeft += 1
        ballPosX = canvasWidth / 2
        ballPosY = canvasHeight / 2
        ballDirX = -abs(ballDirX) # Force it to be negative
        ballDirY = 0

    # Hit top wall?
    if ballPosY < 0:
        ballDirY = abs(ballDirY) # Force to be positive

    # Hit bottom wall?
    if ballPosY > canvasHeight:
        ballDirY = -abs(ballDirY) # Force bot negativef

@sdl3.SDL_AppIterate_func
def SDL_AppIterate(appstate):
    global lastTime

    # Delta time
    currentTime = sdl3.SDL_GetTicks()
    deltaTime = (currentTime - lastTime) / 1000
    lastTime = currentTime

    # Input handling
    keyboard(deltaTime)

    # Update the ball
    updateBall(deltaTime)

    sdl3.SDL_SetRenderDrawColor(renderer, 0, 0, 0, sdl3.SDL_ALPHA_OPAQUE)
    sdl3.SDL_RenderClear(renderer)

    # Draw the left racket
    sdl3.SDL_SetRenderDrawColor(renderer, 255, 255, 255, sdl3.SDL_ALPHA_OPAQUE)
    rect = sdl3.SDL_FRect(racketLeftX, racketLeftY, racketWidth, racketHeight)
    sdl3.SDL_RenderFillRect(renderer, rect)

    # Draw the right racket
    sdl3.SDL_SetRenderDrawColor(renderer, 255, 255, 255, sdl3.SDL_ALPHA_OPAQUE)
    rect = sdl3.SDL_FRect(racketRightX, racketRightY, racketWidth, racketHeight)
    sdl3.SDL_RenderFillRect(renderer, rect)

    # Draw the ball
    sdl3.SDL_SetRenderDrawColor(renderer, 255, 255, 255, sdl3.SDL_ALPHA_OPAQUE)
    rect = sdl3.SDL_FRect(ballPosX - ballSize / 2, ballPosY - ballSize / 2, ballSize, ballSize)
    sdl3.SDL_RenderFillRect(renderer, rect)

    scoreText = "%d:%d".encode() % (scoreLeft, scoreRight)
    surface = sdl3.TTF_RenderText_Blended(font, scoreText, len(scoreText), textColor)
    textTexture = sdl3.SDL_CreateTextureFromSurface(renderer, surface)
    sdl3.SDL_DestroySurface(surface)

    width, height = ctypes.c_float(), ctypes.c_float()
    sdl3.SDL_GetTextureSize(textTexture, ctypes.byref(width), ctypes.byref(height))
    rect = sdl3.SDL_FRect(canvasWidth / 2 - 18, 5, width.value, height.value)
    sdl3.SDL_RenderTexture(renderer, textTexture, None, rect)

    sdl3.SDL_RenderPresent(renderer)
    sdl3.SDL_DestroyTexture(textTexture)
    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppQuit_func
def SDL_AppQuit(appstate, result):
    ... # SDL will clean up the window/renderer for us