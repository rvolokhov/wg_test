from Shape import Shape
from Circle import Circle
from tkinter import Canvas

canvas = Canvas(width=400, height=400, bg="white")

def test_shape_text_negative():
    Shape.change_color("black")
    circle = Circle(0,0,0)
    assert "Selected color is" not in circle.draw_text(canvas), "wrong text, it has not contain substr 'Selected color is'"

def test_shape_text_positive():
    Shape.change_color("blue")
    circle = Circle(0,0,0)
    assert "Selected color is" in circle.draw_text(canvas), "wrong text, it has to contain substr 'Selected color is'"