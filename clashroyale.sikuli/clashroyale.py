import shutil
import os
import time

r = App.focusedWindow()
r2 = Region(r.x, r.y + 600, r.w, r.h - 600)
r.setAutoWaitTimeout(2)
r.highlight(2)

def scroll_down():
    # setting begin - end
    x1, y1 = (r.x + 230, r.y + 700)
    start = Location(x1, y1)
    # moving up
    stepY = 100
    run = start
    mouseMove(start); wait(0.5)
    mouseDown(Button.LEFT); wait(0.5)
    for i in range(4):
        run = run.above(stepY * i)
        mouseMove(run)
    mouseUp()

def scroll_up():
    # setting begin - end
    x1, y1 = (r.x + 230, r.y + 250)
    start = Location(x1, y1)
    # moving up
    stepY = 100
    run = start
    mouseMove(start); wait(0.5)
    mouseDown(Button.LEFT); wait(0.5)
    for i in range(4):
        run = run.below(stepY * i)
        mouseMove(run)
    mouseUp()

def find_trade():
    while r.exists("1540300646315.png"):
        dir = "D:\Skulix\Screenshots"
        img = capture(r)

        imgNew = "clashroyale"
        shutil.move(img, os.path.join(dir, imgNew + ".png"))

        click("1540307401692.png")
        click("1540319481238.png")
        click("1540319491461.png")

        scroll_down()

        if r.exists("1540320185273.png"):
            return

    if r2.exists("1540319994212.png"):
        r2.click("1540319994212.png")
        find_trade()
    
def leave_clan():
    if not r.exists("1540319732251.png"):
        r.click("1540319740979.png")
    r.click("1540319732251.png")
    r.click("1540319764194.png")
    r.click("1540319769646.png")
        
while r.exists("1540319785834.png"):
    if r.exists("1540319811275.png"):
        r.click("1540319821508.png")
        if r.exists("1540319843114.png"):
            r.click("1540319843114.png")
            wait("1540319865013.png")
            scroll_up()
            if r2.exists("1540319994212.png") or r.exists("1540300646315.png"):
                find_trade()
            leave_clan()
    else:
        leave_clan()