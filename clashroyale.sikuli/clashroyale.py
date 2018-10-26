import shutil
import os
import time

clans = [ "#8V8CC2", "#2999R82R", "#PPC8QPY9", "#89GLVGGC", "#98QYCVVQ", "#QRCVRJY", "#8RVVU8RY", "#2QJR8G2G", "#8V2V2GLJ", "#UJGR90R", "#29RR9Q00", "#80JR9CY8", "#2LG00R", "#9RVPU8CC", "#9GJLUJP2", "#2VP2UP", "#JUGYLQG", "#PVUJQQ9", "#9CYYJR0G", "#98P22CYQ", "#YCVUR2", "#99PRPCJ2", "#9CYYC2RC", "#8Y2P0Y8", "#P88P9VRY", "#2QPVJ0L9", "#9PURUQGL", "#9UJRCC08", "#JYYQ0G", "#9CY92C92", "#CQJY8RP", "#9JP2CL2Y", "#PU988Q0", "#9ULPC080", "#292J8QV", "#9JL0ULC9", "#2JV0VL8", "#99GJJJGC", "#9PVY28R", "#2VUVU2U", "#P0GCGGJC", "#2V9C0YYQ", "#RPLQV2P", "#8290GQ90", "#8YCCVU0", "#G2PJURR", "#82PRP29C", "#PL299P", "#CL8CP0", "#P8GYCGYR", "#LGRJ9G", "#8GGRG0VY", "#8GLGPPLL", "#8R9JY9UC", "#JRCQRY" ]

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

        click("1540555920427.png")
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
        
for clan in clans:
    if r.exists("SearchButton.png"):
        r.type("1540555777035.png" ,clan)
        r.click("1540555791644.png")
        wait(1)
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