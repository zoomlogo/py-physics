from functools import reduce
from math import atan2
from vector import vector
import pyglet

class Circle:
    def __init__(self, x, y, mass=1):
        self.pos = vector(x, y)
        self.vel = vector(0, 0)
        self.acc = vector(0, 0)

        self.mass = mass
        if self.mass == 0:
            self.inv_mass = 0
        else:
            self.inv_mass = 1 / mass
        self.radius = mass * 10

        self.color = (255, 255, 255)
        self.shape = pyglet.shapes.Circle(self.pos.x, self.pos.y, self.radius)

        self.coefficient_of_restitution = 1

    def apply_forces(self, *forces):
        if not forces:
            return
        self.acc += reduce(lambda x, y: x + y, forces) * self.mass

    def border_collide(self):
        if self.pos.x <= self.radius:
            self.vel.x *= -1 * self.coefficient_of_restitution
        elif self.pos.x >= (1024 - self.radius):
            self.vel.x *= -1 * self.coefficient_of_restitution

        if self.pos.y <= self.radius:
            self.vel.y *= -1 * self.coefficient_of_restitution
        elif self.pos.y >= (512 - self.radius):
            self.vel.y *= -1 * self.coefficient_of_restitution

    def collide(self, other):
        if type(other) == Circle:
            if abs(self.pos - other.pos) <= self.radius + other.radius:
                penetration_depth = other.pos - self.pos
                collision_normal = penetration_depth.normal()

                self.vel.x += -1 * other.coefficient_of_restitution * collision_normal.x * self.inv_mass
                self.vel.y += -1 * other.coefficient_of_restitution * collision_normal.y * self.inv_mass

    def update(self, dt):
        self.pos += self.vel * dt
        self.vel += self.acc * dt
        self.acc *= 0 # Reset

        # Update shape
        self.shape.x = self.pos.x
        self.shape.y = self.pos.y
        self.shape.color = self.color

    def draw(self):
        self.shape.draw()

