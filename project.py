import pygame 
import math

pygame.init()
WIDTH, HEIGHT = 800, 800 # Window size
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Window - pygame surface
pygame.display.set_caption("Planet Simulation") # Window title
WHITE = (255, 255, 255) # RGB color code for white
YELLOW = (255, 255, 0) # RGB color code for yellow
BLUE = (100, 149, 237) # RGB color code for blue
RED = (188, 39, 50) # RGB color code for red
DARK_GREY = (80, 78, 81) # RGB color code for dark grey

FONT = pygame.font.SysFont("comicsans", 16) # Font for the text

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

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)   

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)} km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y))

    def attration(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2 # Gravitational force between the two planets
        theta = math.atan2(distance_y, distance_x) # Angle between the two planets
        force_x = math.cos(theta) * force # X component of the force
        force_y = math.sin(theta) * force # Y component of the force
        return force_x, force_y
    
    def update_position(self, planets):
        total_force_x = total_force_y = 0
        for planet in planets:
            if self == planet: 
                continue 
            fx, fy = self.attration(planet)
            total_force_x += fx
            total_force_y += fy
        
        self.x_vel += total_force_x / self.mass * self.TIMESTEP # F = ma -> a = F/m
        self.y_vel += total_force_y / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))



def main():
    run = True
    clock = pygame.time.Clock() # Clock object to control FPS

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30) # Sun object (even though it's not a planet :P)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24) # Earth object
    earth.y_vel = 29.783 * 1000

    mars = Planet(- 1.524 * Planet.AU, 0, 12, RED, 6.38 * 10**23) # Mars object
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23) # Mercury object
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24) # Venus object
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60) # Set FPS to 60(max)
        WIN.fill((0, 0, 0)) # Fill the window with white color
        

        for event in pygame.event.get(): # Check for events
            if event.type == pygame.QUIT:
                run = False # Quit if the user closes the window

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN) 


        pygame.display.update() # Update the window
    
    pygame.quit() # Quit pygame

main()
