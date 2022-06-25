from turtle import *
from datetime import datetime


class ClockHand(object):
    def __init__(self, color, size, thickness, angleDiv=60, arrowToggle=True):
        self.thickness = thickness
        self.color = color
        # Size has to be between 0 and 1, 0: Don't draw - 1: Draw to the edge of the clock
        self.size = size
        self.angleDiv = angleDiv
        self.val = 0
        self.arrow = arrowToggle
        self.arrow_size = min(ARROW_SIZE * ((1/self.size)), ARROW_MAX)

    def draw(self, pen):
        pen.pen(pencolor=self.color, pensize=self.thickness)
        pen.up()
        pen.goto(0, 0)
        pen.setheading(90)  # Face up / 12 O'clock
        pen.rt(self.val / self.angleDiv * 360)
        pen.down()
        pen.fd(self.size * clock_radius)
        if self.arrow:
            self.drawArrow(pen)

    def drawArrow(self, pen):
        pen.color(self.color)
        pen.begin_fill()
        pen.rt(90)
        pen.bk(self.arrow_size/2)
        pen.fd(self.arrow_size)
        pen.lt(120)
        pen.fd(self.arrow_size)
        pen.lt(120)
        pen.fd(self.arrow_size)
        pen.end_fill()
        pen.up()


# Define Constants and Variables
START_ANIMATION = True

WIDTH = 800
HEIGHT = 800

ARROW_MAX = 20
ARROW_SIZE = 10

BACKGROUND_COLOR = 'black'
CLOCK_COLOR = 'maroon'
INNER_CLOCK_COLOR = 'black'

hour_hand = ClockHand('chocolate', 0.25, 4, 12)
minute_hand = ClockHand('cyan', 0.65, 2)
second_hand = ClockHand('lightgreen', 0.8, 1)

HOUR_LINE_SIZE = 20
MINUTE_LINE_SIZE = 10

SMOOTH = True

clock_radius = min(WIDTH, HEIGHT)/4

# Initilize Screen
screen = Screen()
screen.bgcolor(BACKGROUND_COLOR)
screen.setup(WIDTH, HEIGHT)
title('Clock')


# Initilize Turtle
pen = Turtle()
pen.hideturtle()
pen.speed(0)


# Initlize Functions
def invert_smooth(x, y):
    global SMOOTH
    SMOOTH = not SMOOTH


def drawClock(pen):
    # Draw main circle
    pen.up()
    pen.setheading(0)
    pen.pen(pencolor=CLOCK_COLOR, fillcolor=INNER_CLOCK_COLOR, pensize=5)
    pen.begin_fill()
    pen.goto(0, -clock_radius)
    pen.down()
    pen.circle(clock_radius)
    pen.end_fill()
    pen.up()

    # Draw small lines
    def small_clock_lines(pensize, pencolor, amnt, linesize):
        pen.color(pencolor)
        pen.pensize(pensize)
        for _ in range(amnt):
            pen.goto(0, 0)
            pen.fd(clock_radius-linesize)
            pen.down()
            pen.fd(linesize)
            pen.up()
            pen.rt(360/amnt)

    small_clock_lines(5, CLOCK_COLOR, 12, HOUR_LINE_SIZE)
    small_clock_lines(3, CLOCK_COLOR, 60, MINUTE_LINE_SIZE)


def drawHands(pen):
    minute_hand.draw(pen)
    hour_hand.draw(pen)
    second_hand.draw(pen)


def updateClock():
    now = datetime.now()
    second_hand.val = now.second
    minute_hand.val = now.minute
    hour_hand.val = now.hour
    if SMOOTH:
        second_hand.val += now.microsecond / 10 ** 6
        minute_hand.val += second_hand.val / 60
        hour_hand.val += minute_hand.val / 60


def writeTime():
    pen.up()
    pen.color('white')
    pen.pensize(10)
    pen.setheading(0)

    pen.goto(0, (clock_radius/2 + (HEIGHT/4)) * -1)
    pen.write(datetime.now().strftime("%H:%M:%S"),
              align='center', font=('Arial', 30, 'normal'))


# Draw Everything
screen.onclick(invert_smooth)
if not START_ANIMATION:
    screen.tracer(0)

while True:
    drawClock(pen)
    updateClock()
    drawHands(pen)
    pen.goto(0, 0)
    pen.dot(clock_radius/15, CLOCK_COLOR)
    writeTime()
    screen.update()
    screen.tracer(0)
    pen.clear()

# Run Loop
screen.mainloop()
