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
    while r.exists("TradeButton.png"):
        dir = "D:\Skulix\Screenshots"
        img = capture(r)

        imgNew = "clashroyale"
        shutil.move(img, os.path.join(dir, imgNew + ".png"))

        click("1540307401692.png")
        click("1540319481238.png")
        click("1540319491461.png")

        scroll_down()

        if r.exists("GR8.png"):
            return

    if r2.exists("UpperNotification.png"):
        r2.click("UpperNotification.png")
        find_trade()
    
def leave_clan():
    if not r.exists("PurpleTrophy.png"):
        r.click("SocialTab.png")
    r.click("PurpleTrophy.png")
    r.click("LeaveButton.png")
    r.click("YesButton.png")
        
while r.exists("ShopTab.png"):
    if r.exists("SearchButton.png"):
        r.click("YellowTrophy.png")
        if r.exists("JoinButton.png"):
            r.click("JoinButton.png")
            wait("PageDownButton.png")
            scroll_up()
            if r2.exists("UpperNotification.png") or r.exists("TradeButton.png"):
                find_trade()
            leave_clan()
    else:
        leave_clan()