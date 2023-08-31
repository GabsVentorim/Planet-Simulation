import pygame 
import math

pygame.init()
WIDTH, HEIGHT = 800, 800 # Window size
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Window - pygame surface
pygame.display.set_caption("Planet Simulation") # Window title
WHITE = (255, 255, 255) # RGB color code for white
YELLOW = (255, 255, 0) # RGB color code for yellow

class Planet:
    AU = 149.6e6 * 1000 # in meters; AU -> Astronomical Unit
    G = 6.67408e-11 # Gravitational constant
    SCALE = 250 / AU # Scale for the simulation; 1 AU = 100 pixels
    TIMESTEP = 3600 * 24 # 1 day in seconds

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0 

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(win, self.color, (x, y), self.radius)

def main():
    run = True
    clock = pygame.time.Clock() # Clock object to control FPS

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30) # Sun object (even though it's not a planet :P)
    sun.sun = True

    planets = [sun]

    while run:
        clock.tick(60) # Set FPS to 60(max)
        # WIN.fill(WHITE) # Fill the window with white color
        

        for event in pygame.event.get(): # Check for events
            if event.type == pygame.QUIT:
                run = False # Quit if the user closes the window

        for planet in planets:
            planet.draw(WIN) 

        pygame.display.update() # Update the window
    
    pygame.quit() # Quit pygame

main()