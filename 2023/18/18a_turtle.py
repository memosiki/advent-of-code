# import turtle
from svg_turtle import SvgTurtle
from io import BytesIO

import numpy as np
from PIL import Image
from reportlab.graphics import renderPM

turtle = SvgTurtle(500, 500)

# pic_path = Path("turtle.eps")
# if not pic_path.exists():
map = {
    "U": lambda: turtle.setheading(90),
    "R": lambda: turtle.setheading(0),
    "D": lambda: turtle.setheading(270),
    "L": lambda: turtle.setheading(180),
}
turtle.penup()
turtle.hideturtle()
# turtle.begin_fill()
turtle.pendown()
# turtle.delay(0)
# turtle.setheading(90)
# turtle.forward(100)
print(turtle.position())
with open("input", "r") as fd:
    for line in fd:
        dir, steps, _ = line.split()
        map[dir]()
        turtle.forward((int(steps) + 1))
        print(turtle.position())
turtle.end_fill()
# eps = turtle.getcanvas().postscript(colormode="color")
# svglib.svglib.Image().png
png = BytesIO()
renderPM.drawToFile(turtle.to_svg(), png, "Png")
img = Image.open(png)
field = np.array(img)
img.save("debug.png")
input()
print("Non white pixels", np.sum(field[:, :, 0] != 255))
