from Shape import Shape
from tkinter import *


class Triangle(Shape):
    def __init__(self, pos_x1, pos_y1, pos_x2, pos_y2, pos_x3, pos_y3) -> None:
        self.position_x1 = pos_x1
        self.position_y1 = pos_y1
        self.position_x2 = pos_x2
        self.position_y2 = pos_y2
        self.position_x3 = pos_x3
        self.position_y3 = pos_y3

    def draw(self, c: Canvas):
        c.create_line(self.position_x1, self.position_y1, self.position_x2, self.position_y2, fill=Shape.color, width=2)
        c.create_line(self.position_x2, self.position_y2, self.position_x3, self.position_y3, fill=Shape.color, width=2)
        c.create_line(self.position_x3, self.position_y3, self.position_x1, self.position_y1, fill=Shape.color, width=2)

    def draw_text(self, c: Canvas):
        text = "Drawing a triangle with points ("+str(self.position_x1)+", "+str(self.position_y1)+"), ("+str(self.position_x2)+", "+str(self.position_y2)+"), ("+str(self.position_x3)+", "+str(self.position_y3)+")"
        if Shape.color != "black":
            text = text + "\nSelected color is " + Shape.color
        c.create_text(self.position_x1, self.position_y1, text=text, fill="black", font="Helvetica 8 normal", anchor=SW)
