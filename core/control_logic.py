from abc import ABC, abstractmethod
from core.sim import Triangle

class ControlLogic(ABC):
    """Abstract base class for user-defined logic."""
    def __init__(self, triangle: Triangle):
        self.triangle = triangle

    @abstractmethod
    def loop(self):
        """Abstract method for user-defined logic."""
        robot = self.triangle
