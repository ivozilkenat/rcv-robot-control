import pygame
import math
from abc import ABC, abstractmethod

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
TRIANGLE_SIZE = 50
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 0)
COLORS = [WHITE, BLACK, GRAY]
CIRCLE_BAND_WIDTH = 20

# Initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Controllable Triangle with Sensors")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)


class Corner:
    """Class to represent a corner of the triangle."""
    def __init__(self, label):
        self.label = label
        self.x = 0
        self.y = 0
        self.sensor_reading = (0, 0, 0)  # Default color (black)
        self.has_changed = False

    def check_color(self, background_surface):
        """Update the sensor reading and check if the color has changed."""
        x, y = int(self.x), int(self.y)
        if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
            new_color = background_surface.get_at((x, y))[:3]
        else:
            new_color = (0, 0, 0)  # Default to black if out of bounds

        self.has_changed = new_color != self.sensor_reading
        self.sensor_reading = new_color

    def draw(self, screen):
        """Draw the label of the corner."""
        text = font.render(self.label, True, BLUE)
        screen.blit(text, (self.x - 10, self.y - 10))


class ConcentricCircles:
    """Class to manage the background pattern."""
    def __init__(self, center, band_width, colors):
        self.center = center
        self.band_width = band_width
        self.colors = colors

    def draw(self, screen):
        """Draw concentric circles cycling through colors."""
        max_radius = int(math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2))
        radius = max_radius
        color_index = 0
        while radius > 0:
            pygame.draw.circle(screen, self.colors[color_index], self.center, radius)
            radius -= self.band_width
            color_index = (color_index + 1) % len(self.colors)


class Triangle:
    """Class to represent and control the triangle."""
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.A = Corner("A")
        self.B = Corner("B")
        self.C = Corner("C")
        self.corners = [self.A, self.B, self.C]
        self.update_positions()

    def update_positions(self):
        """Update the positions of the corners based on the triangle's center."""
        points = self.get_points()
        for corner, point in zip(self.corners, points):
            corner.x, corner.y = point

    def get_points(self):
        """Get the coordinates of the triangle's vertices."""
        points = []
        for i in range(3):
            angle = (2 * math.pi * i) / 3  # Equilateral triangle angles
            px = self.x + self.size * math.cos(angle)
            py = self.y + self.size * math.sin(angle)
            points.append((px, py))
        return points

    def move(self, dx, dy):
        """Move the triangle by dx and dy."""
        self.x += dx
        self.y += dy
        self.update_positions()

    def draw(self, screen):
        """Draw the triangle and its corners."""
        points = self.get_points()
        pygame.draw.polygon(screen, RED, points, 3)

        # Let corners draw themselves
        for corner in self.corners:
            corner.draw(screen)

    def update_sensor_colors(self, background_surface):
        """Update sensor readings for all corners."""
        for corner in self.corners:
            corner.check_color(background_surface)


class UserLogic(ABC):
    """Abstract base class for user-defined logic."""
    def __init__(self, triangle):
        self.triangle = triangle

    @abstractmethod
    def execute_logic(self):
        """Abstract method for user-defined logic."""
        pass


class CustomLogic(UserLogic):
    """Example implementation of custom user logic."""
    def execute_logic(self):
        # Example: Move towards the center if color at 'A' is black
        if self.triangle.A.sensor_reading == BLACK:
            self.triangle.move(0, 2)
        elif self.triangle.B.sensor_reading == WHITE:
            self.triangle.move(-2, 0)
        elif self.triangle.C.sensor_reading == GRAY:
            self.triangle.move(2, 0)


class Simulation:
    """Main simulation class to handle the game loop."""
    def __init__(self):
        self.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.background = ConcentricCircles(self.center, CIRCLE_BAND_WIDTH, COLORS)

        # Create a background surface for sampling colors
        self.background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.draw(self.background_surface)

        self.triangle = Triangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, TRIANGLE_SIZE)
        self.user_logic = CustomLogic(self.triangle)
        self.running = True

    def handle_input(self):
        """Handle user input to move the triangle."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.triangle.move(0, -5)
        if keys[pygame.K_DOWN]:
            self.triangle.move(0, 5)
        if keys[pygame.K_LEFT]:
            self.triangle.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            self.triangle.move(5, 0)

    def run(self):
        """Main simulation loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Handle input
            self.handle_input()

            # Update sensors and execute user logic
            self.triangle.update_sensor_colors(self.background_surface)
            self.user_logic.execute_logic()

            # Drawing
            screen.fill((0, 0, 0))
            self.background.draw(screen)
            self.triangle.draw(screen)

            # Read and print sensor data
            for corner in self.triangle.corners:
                print(f"{corner.label}: ({corner.x:.2f}, {corner.y:.2f}) Sensor: {corner.sensor_reading} Changed: {corner.has_changed}")

            # Update display
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()
