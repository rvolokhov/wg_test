from Shape import Shape
from tkinter import *


class Circle(Shape):
    def __init__(self, pos_x, pos_y, radius) -> None:
        self.position_x = pos_x
        self.position_y = pos_y
        self.radius = radius

    def draw(self, c: Canvas):
        c.create_oval(self.position_x, self.position_y, self.position_x+self.radius*2, self.position_y+self.radius*2, outline=Shape.color, width=2)

    def draw_text(self, c:Canvas) -> str:
        text = "Drawing a circle: ("+str(self.position_x)+", "+str(self.position_y)+") with radius "+str(self.radius)
        if Shape.color != "black":
            text = text + "\nSelected color is " + Shape.color
        c.create_text(self.position_x+self.radius, self.position_y+self.radius, text=text, fill="black", font="Helvetica 8 normal", anchor=SW)
        return text
