import shutil
import os
import time
import random
import json
from time import gmtime, strftime

count = 1
badclans = []

with open('D:\Scripts\SikuliRoyale\clashroyale.sikuli\clans.json') as json_data:
    clans = json.load(json_data)

r = App.focusedWindow()
r2 = Region(r.x, r.y + 150, r.w - 400, r.h - 800)
r3 = Region(r.x, r.y + 185, r.w, 480)
r.highlight(2)
r.setAutoWaitTimeout(1)

def scroll_up():
    x1, y1 = (r.x + 230, r.y + 200)
    start = Location(x1, y1)
    stepY = 200
    run = start
    mouseMove(start)
    mouseDown(Button.LEFT); wait(0.5)
    run = run.below(stepY)
    mouseMove(run)
    mouseUp()


def center_shift(button):
    start = button.getCenter()
    stop = Location(start.getX(), r.getCenter().getY())
    mouseMove(start)
    mouseDown(Button.LEFT); wait(0.5)
    mouseMove(stop)
    mouseUp()

def capture_trade():
    dir = "D:\Skulix\Screenshots"
    img = capture(r3)

    imgNew = "clashroyale"
    shutil.move(img, os.path.join(dir, imgNew + ".png"))

def send_trade(clan):
    click("1540555920427.png")

    embed = 'payload_json:{{    "embeds": [{{        "title": "Trade Found",        "description": "{}/100",        "fields": [{{            "name": "Clan",            "value": "{} ([{}](https://royaleapi.com/clan/{}))"        }},{{            "name": "Time",            "value": "{}"        }}],        "color": 14177041,        "footer": {{            "text": "Bot by GR8 | Titan",            "icon_url": "https://i.imgur.com/TP8GXZb.png"        }}    }}]}}'
    embed = embed.format(count, clans[clan], clan, clan.strip("#"), strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()))

    click("1541750450407.png")
    type("a", Key.CTRL)
    paste(embed)
    click("1540319481238.png")
    click("1540319491461.png")
    

def find_trade(clan):
    if r.exists("TradeButton.png"):
        trade = r.getLastMatch()
        center_shift(trade)
        capture_trade()
        send_trade(clan)
    if r2.exists("1541321891125.png"):
        r2.click("1541321891125.png")
        wait(0.5)
        find_trade(clan)
    
def leave_clan():
    if r.exists("PurpleTrophy.png"):
        r.click("PurpleTrophy.png")
        r.click("LeaveButton.png")
        r.click("YesButton.png")

def search_clan(clan):
    if r.exists("1540557093477.png"):
            r.click("1540557093477.png")
    r.paste("1540555777035.png" ,clan)
    r.click("1540555791644.png")

tags = clans.keys()
random.shuffle(tags)
for clan in tags:
    if count > 100:
        print(badclans)
        break

    search_clan(clan)
    wait(1)
    if r.exists("YellowTrophy.png"):
        r.click("YellowTrophy.png")
    else:
        badclans.append(clan)
        continue
    if r.exists("JoinButton.png"):
        r.click("JoinButton.png")
        if r.exists("1540564325650.png"):
            r.click("1540564340338.png")
            r.click("1540556749121.png")
            badclans.append(clan)
            continue
        if not exists("PageDownButton.png"):
            badclans.append(clan)
            continue
        else:
            click("PageDownButton.png")
        wait(1)
        count += 1
        if r.exists("TradeButton.png"):
            trade = r.getLastMatch()
            center_shift(trade)
            capture_trade()
            send_trade(clan)
            scroll_up()
            scroll_up()
        else:
            scroll_up()
        if r2.exists("1541321891125.png") or r.exists("TradeButton.png"):
            find_trade(clan)
        leave_clan()
    else:
        r.click("1540556749121.png")