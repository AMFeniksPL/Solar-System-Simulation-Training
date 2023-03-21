# Potrzebne importy
import math

import pygame

from pygame.constants import *
from pygame.locals import *

class Planet:

    counter = 0
    listOfPlanets = []

    AU = 149.6e9
    G = 6.67428e-11
    SCALE = 250 / AU
    TIMESTEP = 3600 * 24

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.isSun = False

        self.velX = self.velY = 0

        if len(Planet.listOfPlanets) > 0:
            sunMass = Planet.listOfPlanets[0].mass
            self.velY = (Planet.G * sunMass / self.x) ** 0.5


        Planet.counter += 1
        Planet.listOfPlanets.append(self)

    def count_gravity_force(self):

        sumForceX = sumForceY = 0

        for planet in Planet.listOfPlanets:
            if planet == self:
                continue

            distance = ((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2) ** 0.5

            force = Planet.G * self.mass * planet.mass / (distance ** 2)

            angle = math.atan2(planet.y - self.y, planet.x - self.x)

            forceX = force * math.cos(angle)
            forceY = force * math.sin(angle)

            sumForceX += forceX * Planet.TIMESTEP
            sumForceY += forceY * Planet.TIMESTEP

        return sumForceX, sumForceY

    def apply_forces(self):
        forceX, forceY = self.count_gravity_force()

        self.velX += forceX / self.mass
        self.velY += forceY / self.mass

        self.x += self.velX * Planet.TIMESTEP
        self.y += self.velY * Planet.TIMESTEP

    def draw(self):
        x = self.x * Planet.SCALE + SCREEN_WIDTH / 2
        y = self.y * Planet.SCALE + SCREEN_HEIGHT / 2

        scaledRadius = self.radius * Planet.SCALE / (250/Planet.AU)

        pygame.draw.circle(screen, self.color, (x, y), scaledRadius)


    @staticmethod
    def draw_all_planets():
        for planet in Planet.listOfPlanets:
            planet.draw()

    @staticmethod
    def update_all_planets():
        print(Planet.SCALE)
        for planet in Planet.listOfPlanets:
            planet.apply_forces()

    @staticmethod
    def change_scale(coefficient):
        Planet.SCALE *= 1.03 ** coefficient


# Odpalenie modułów pygame
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Parametry Screena
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def main():
    # Zegar kontrolujący FPS-y
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 20, (255, 255, 0), 2.0e30)

    mercury = Planet(0.42 * Planet.AU, 0, 10, (0, 0, 200), 0.330e24)
    venus = Planet(0.72 * Planet.AU, 0, 10, (0, 0, 200), 4.87e24)
    earth = Planet(1 * Planet.AU, 0, 10, (0, 0, 200), 5.97e24)
    mars = Planet(1.63 * Planet.AU, 0, 10, (0, 0, 200), 0.642e24)

    # Pętla gry
    running = True
    while running:
        # LOGIKA GRY (w przyszłości):
        Planet.update_all_planets()


        # RYSOWANIE GRAFIKI:
        # Wypełnienie okienka kolorem
        screen.fill((0, 0, 0))

        # Rysowanie kształtów w PyGame
        Planet.draw_all_planets()


        # Czekanie na kolejną klatkę
        clock.tick(60)

        #Aktualizacja gry
        pygame.display.flip()

        # Te cztery linijki pozwalają nam normalnie zamknąć program
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                Planet.change_scale(event.y)


            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()

main()
