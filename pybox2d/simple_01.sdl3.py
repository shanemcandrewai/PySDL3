"""Box2D simple example convert from pygame backend to PySDL3
based on
https://github.com/pybox2d/pybox2d/blob/master/library/Box2D/examples/simple/simple_01.py"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ctypes
import os
import Box2D  # pylint: disable=unused-import
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, staticBody, dynamicBody)
os.environ["SDL_MAIN_USE_CALLBACKS"] = "1"
os.environ["SDL_RENDER_DRIVER"] = "opengl"
import sdl3 # pylint: disable=wrong-import-position

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

# --- pygame setup ---
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# pygame.display.set_caption('Simple pygame example')
# clock = pygame.time.Clock()
RENDERER = ctypes.POINTER(sdl3.SDL_Renderer)()
WINDOW = ctypes.POINTER(sdl3.SDL_Window)()


# --- pybox2d world setup ---
# Create the world
world = world(gravity=(0, -10), doSleep=True)

# And a static body to hold the ground shape
ground_body = world.CreateStaticBody(
    position=(0, 1),
    shapes=polygonShape(box=(50, 5)),
)

# Create a dynamic body
dynamic_body = world.CreateDynamicBody(position=(10, 15), angle=15)

# And add a box fixture onto it (with a nonzero density, so it will move)
box = dynamic_body.CreatePolygonFixture(box=(2, 1), density=1, friction=0.3)

colors = {
    staticBody: (255, 255, 255, 255),
    dynamicBody: (127, 127, 127, 255),
}

@sdl3.SDL_AppInit_func
def SDL_AppInit(appstate, argc, argv):# pylint: disable=invalid-name, unused-argument
    """SDL_AppInit"""
    if not sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO):
        sdl3.SDL_Log("Couldn't initialize SDL: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE
    window_title = "Draw Box2D colliders using line segments, PySDL3".encode()
    if not sdl3.SDL_CreateWindowAndRenderer(
    window_title, SCREEN_WIDTH, SCREEN_HEIGHT, 0, WINDOW, RENDERER):
        sdl3.SDL_Log("Couldn't create window/renderer: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE
    sdl3.SDL_SetRenderVSync(RENDERER, 1) # Turn on vertical sync
    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppEvent_func
def SDL_AppEvent(appstate, event):# pylint: disable=invalid-name, unused-argument
    """SDL_AppEvent"""
    if sdl3.SDL_DEREFERENCE(event).type == sdl3.SDL_EVENT_QUIT:
        return sdl3.SDL_APP_SUCCESS
    return sdl3.SDL_APP_CONTINUE

class Box2Ddraw:
    """Box2D_draw"""
    def __init__(self, renderer, ppm):
        self.renderer = renderer
        self.ppm = ppm

    def draw_polygon(self, color, vertices):
        """draw_polygon"""
        # r = int(color.r * 255)
        # g = int(color.g * 255)
        # b = int(color.b * 255)
        # sdl3.SDL_SetRenderDrawColor(self.renderer, r, g, b, sdl3.SDL_ALPHA_OPAQUE)

        sdl3.SDL_SetRenderDrawColor(
        self.renderer, color[0], color[1], color[2], sdl3.SDL_ALPHA_OPAQUE)

        x0 = vertices[0][0] * self.ppm
        y0 = vertices[0][1] * self.ppm
        x1 = vertices[1][0] * self.ppm
        y1 = vertices[1][1] * self.ppm
        # sdl3.SDL_RenderLine(self.renderer, x0, y0, x1, y1)
        sdl3.SDL_RenderRect(self.renderer, sdl3.SDL_FRect(x0, y0, x1, y1))

        x1 = vertices[1][0] * self.ppm
        y1 = vertices[1][1] * self.ppm
        x2 = vertices[2][0] * self.ppm
        y2 = vertices[2][1] * self.ppm
        sdl3.SDL_RenderLine(self.renderer, x1, y1, x2, y2)

        x2 = vertices[2][0] * self.ppm
        y2 = vertices[2][1] * self.ppm
        x3 = vertices[3][0] * self.ppm
        y3 = vertices[3][1] * self.ppm
        sdl3.SDL_RenderLine(self.renderer, x2, y2, x3, y3)

        x3 = vertices[3][0] * self.ppm
        y3 = vertices[3][1] * self.ppm
        x0 = vertices[0][0] * self.ppm
        y0 = vertices[0][1] * self.ppm
        sdl3.SDL_RenderLine(self.renderer, x3, y3, x0, y0)

    def draw_circle(self, center, radius):
        """draw circle"""


@sdl3.SDL_AppIterate_func
def SDL_AppIterate(appstate):# pylint: disable=invalid-name, unused-argument
    """SDL_AppIterate"""


# --- main game loop ---
# running = True
# while running:
    # Check the event queue
    # for event in pygame.event.get():
        # if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # The user closed the window or pressed escape
            # running = False

    # screen.fill((0, 0, 0, 0))
    sdl3.SDL_SetRenderDrawColor(RENDERER, 100, 0, 0, sdl3.SDL_ALPHA_OPAQUE)
    sdl3.SDL_RenderClear(RENDERER) # Start with a blank canvas
    # Draw the world
    for body in (ground_body, dynamic_body):  # or: world.bodies
        # The body gives us the position and angle of its shapes
        for fixture in body.fixtures:
            # The fixture holds information like density and friction,
            # and also the shape.
            shape = fixture.shape

            # Naively assume that this is a polygon shape. (not good normally!)
            # We take the body's transform and multiply it with each
            # vertex, and then convert from meters to pixels with the scale
            # factor.
            vertices = [(body.transform * v) * PPM for v in shape.vertices]

            # But wait! It's upside-down! Pygame and Box2D orient their
            # axes in different ways. Box2D is just like how you learned
            # in high school, with positive x and y directions going
            # right and up. Pygame, on the other hand, increases in the
            # right and downward directions. This means we must flip
            # the y components.
            vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]

            # pygame.draw.polygon(screen, colors[body.type], vertices)
            box2ddraw = Box2Ddraw(RENDERER, PPM)
            box2ddraw.draw_polygon(colors[body.type], vertices)

    # Make Box2D simulate the physics of our world for one step.
    # Instruct the world to perform a single step of simulation. It is
    # generally best to keep the time step and iterations fixed.
    # See the manual (Section "Simulating the World") for further discussion
    # on these parameters and their implications.
    world.Step(TIME_STEP, 10, 10)

    # Flip the screen and try to keep at the target FPS
    # pygame.display.flip()
    # clock.tick(TARGET_FPS)
    sdl3.SDL_RenderPresent(RENDERER)
    return sdl3.SDL_APP_CONTINUE


@sdl3.SDL_AppQuit_func
def SDL_AppQuit(appstate, result):# pylint: disable=invalid-name, unused-argument
    """SDL_AppQuit"""
    sdl3.SDL_Log("SDL quit".encode())
