import pygame
import math

from core.constants import *

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
        text = font.render(self.label, True, C_BLUE)
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
        self.control_corner = self.A  # Default control corner
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

    def move_in_normal_direction(self, step):
        """Move the triangle in the direction of the normal of the vector
        formed by the two non-control corners."""
        non_control_corners = [c for c in self.corners if c != self.control_corner]
        c1, c2 = non_control_corners

        # Vector difference between the two non-control corners
        vector = (c2.x - c1.x, c2.y - c1.y)

        # Normal vector (perpendicular)
        normal = (-vector[1], vector[0])  # Rotate 90 degrees counterclockwise

        # Normalize the normal vector
        magnitude = math.sqrt(normal[0] ** 2 + normal[1] ** 2)
        if magnitude != 0:
            normal = (normal[0] / magnitude, normal[1] / magnitude)

        # Apply movement in the normal direction
        self.move(normal[0] * step, normal[1] * step)  # Scale the movement by a factor of 5

    def draw(self, screen):
        """Draw the triangle and its corners."""
        points = self.get_points()
        pygame.draw.polygon(screen, C_RED, points, 3)

        # Let corners draw themselves
        for corner in self.corners:
            corner.draw(screen)

    def update_sensor_colors(self, background_surface):
        """Update sensor readings for all corners."""
        for corner in self.corners:
            corner.check_color(background_surface)


class Simulation:
    """Main simulation class to handle the game loop."""
    def __init__(
            self,
            user_logic,
            allow_manuel_override=True,
            band_width=CIRCLE_BAND_WIDTH,
            triangle_size=TRIANGLE_SIZE,
            screen_width=SCREEN_WIDTH,
            screen_height=SCREEN_HEIGHT
    ):
        self.center = (screen_width // 2, screen_height // 2)
        self.background = ConcentricCircles(self.center, band_width, BAND_COLORS)

        # Create a background surface for sampling colors
        self.background_surface = pygame.Surface((screen_width, screen_height))
        self.background.draw(self.background_surface)

        self.triangle = Triangle(screen_width // 2, screen_height // 4, triangle_size)
        self.user_logic = user_logic(self.triangle)
        self.running = True
        self.controller_running = False
        self.allow_manuel_override = allow_manuel_override

    def handle_input(self):
        """Handle user input to move the triangle."""
        keys = pygame.key.get_pressed()

        # TODO: make this more sophisticated?
        self.controller_running = keys[pygame.K_SPACE]

        if self.allow_manuel_override:
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
            if self.controller_running:
                self.user_logic.loop()

            # Drawing
            screen.fill(C_WHITE)
            self.background.draw(screen)
            self.triangle.draw(screen)

            # Read and print sensor data
            # for corner in self.triangle.corners:
            #     print(f"{corner.label}: ({corner.x:.2f}, {corner.y:.2f}) Sensor: {corner.sensor_reading} Changed: {corner.has_changed}")

            # Update display
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()