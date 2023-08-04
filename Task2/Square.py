from Shape import Shape
from tkinter import *


class Square(Shape):
    def __init__(self, pos_x, pos_y, sideA, sideB) -> None:
        self.position_x = pos_x
        self.position_y = pos_y
        self.sideA = sideA
        self.sideB = sideB

    def draw(self, c: Canvas):
        c.create_rectangle(self.position_x, self.position_y, self.position_x+self.sideA, self.position_y+self.sideB, outline=self.color, width=2)

    def draw_text(self, c:Canvas) -> str:
        text = "Drawing a square ("+str(self.position_x)+", "+str(self.position_y)+") with sides are "+str(self.sideA)+" and "+str(self.sideB)
        if Shape.color != 'black':
            text = text + "\nSelected color is "+Shape.color
        c.create_text(self.position_x, self.position_y, text=text, fill="black", font="Helvetica 8 normal", anchor=SW)
        return text
