from tkinter import *

from Shape import Shape
from Square import Square
from Circle import Circle
from Triangle import Triangle
import random

# instance of tkinter
root = Tk()
# creating canvas
canvas = Canvas(width=400, height=400, bg="white")
# list of figures (shapes)
figures = []
# list of colors, they will be selected randomly by clicking on canvas
colors = ['red', 'green', 'blue']

#callback func for clicking
def callback(event):
    Shape.change_color(colors[random.randint(0,2)])
    draw(canvas)

def init():
    canvas.bind("<Button-1>", callback)
    canvas.pack()
    # creating figures and add them to the list
    figures.append(Square(50, 220, 50, 75))
    figures.append(Circle(120, 70, 50))
    figures.append(Triangle(50, 50, 120, 20, 20, 120))
    draw(canvas)
    root.mainloop()


def draw(c):
    # clear canvas
    c.delete("all")
    # go through all figures and draw them
    for figure in figures:
        figure.draw(c)
        figure.draw_text(c)

# entry point
init()
