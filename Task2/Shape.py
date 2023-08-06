from abc import ABC, abstractmethod
from tkinter import *

# parent class for figures
class Shape(ABC):
    color = "black"

    @abstractmethod
    def draw(self, c: Canvas):
        pass

    @abstractmethod
    def draw_text(self, c: Canvas):
        pass

    @staticmethod
    def change_color(c) -> None:
        Shape.color = c
