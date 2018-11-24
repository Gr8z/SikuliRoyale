import shutil
import os
import time
import random
import json
from time import gmtime, strftime

count = 1
badclans = []

filterGiveCards = ["edrag.png"]
filterGetCards = ["lavahound.png","sparky.png","clone.png"]

with open('D:\Scripts\SikuliRoyale\clashroyale.sikuli\clans.json') as json_data:
    clans = json.load(json_data)

app_region = App.focusedWindow()
top_region = Region(app_region.x, app_region.y + 150, app_region.w - 400, app_region.h - 800)

app_region.highlight(2)
app_region.setAutoWaitTimeout(1)
top_region.setAutoWaitTimeout(1)

def scroll_up():
    x1, y1 = (app_region.x + 230, app_region.y + 200)
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
    stop = Location(start.getX(), app_region.getCenter().getY())

    if abs(app_region.getCenter().getY() - button.getCenter().getY()) > 10:
        mouseMove(start)
        mouseDown(Button.LEFT); wait(0.5)
        mouseMove(stop)
        mouseUp()

def capture_trade(region):
    dir = "D:\Skulix\Screenshots"
    img = capture(region)

    imgNew = "clashroyale"
    shutil.move(img, os.path.join(dir, imgNew + ".png"))

def send_trade(clan):
    click("postman.png")

    embed = 'payload_json:{{    "embeds": [{{        "title": "Trade Found",        "description": "{}/100",        "fields": [{{            "name": "Clan",            "value": "{} ([{}](https://royaleapi.com/clan/{}))"        }},{{            "name": "Time",            "value": "{}"        }}],        "color": 14177041,        "footer": {{            "text": "Bot by GR8 | Titan",            "icon_url": "https://i.imgur.com/TP8GXZb.png"        }}    }}]}}'
    embed = embed.format(count, clans[clan], clan, clan.strip("#"), strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()))

    click("payload_json.png")
    type("a", Key.CTRL)
    paste(embed)
    click("send.png")
    click("nox.png")
    

def find_trade(clan):
    if app_region.exists("TradeButton.png"):
        trade = app_region.getLastMatch()
        center_shift(trade)
        wait(0.2)

        trades = findAll("TradeButton.png")
        sorted_trades = sorted(trades, key=lambda m:m.y)

        for page_trade in sorted_trades:
            filter = True
            trade_region = Region(page_trade.x - 300, page_trade.y - 30, page_trade.w + 170, page_trade.h + 70)
            trade_give = Region(trade_region.x, trade_region.y, trade_region.w/2, trade_region.h)
            trade_get = Region(trade_give.x+trade_give.w, trade_give.y, trade_give.w, trade_give.h) 
            
            for give in filterGiveCards:
                if trade_give.exists(give, 0.5):
                    filter = False

            for want in filterGetCards:
                if trade_get.exists(want, 0.5):
                    filter = False

            if filter:
                capture_trade(trade_region)
                send_trade(clan)
    if top_region.exists("NotiUp.png"):
        top_region.click("NotiUp.png")
        wait(0.5)
        find_trade(clan)
    
def leave_clan():
    if app_region.exists("PurpleTrophy.png"):
        app_region.click("PurpleTrophy.png")
        app_region.click("LeaveButton.png")
        app_region.click("YesButton.png")

def search_clan(clan):
    if app_region.exists("crossButton.png"):
            app_region.click("crossButton.png")
    app_region.paste("clanSearch.png" ,clan)
    app_region.click("searchButton.png")

tags = clans.keys()
random.shuffle(tags)
for clan in tags:
    if count >= 100:
        print(badclans)
        break

    search_clan(clan)
    wait(1)
    if app_region.exists("YellowTrophy.png"):
        app_region.click("YellowTrophy.png")
    else:
        badclans.append(clan)
        continue
    if app_region.exists("JoinButton.png"):
        app_region.click("JoinButton.png")
        if app_region.exists("RequestTitle.png"):
            app_region.click("cancelButton.png")
            app_region.click("redCross.png")
            badclans.append(clan)
            continue
        if not app_region.exists("PageDownButton.png"):
            badclans.append(clan)
            continue
        else:
            click("PageDownButton.png")
        wait(1)
        count += 1
        if app_region.exists("TradeButton.png"):
            trade = app_region.getLastMatch()
            center_shift(trade)
            wait(0.2)
            trade_region = Region(trade.x - 300, trade.y - 30, trade.w + 170, trade.h + 70)
            capture_trade(trade_region)
            send_trade(clan)
            scroll_up()
            scroll_up()
        else:
            scroll_up()
        if top_region.exists("NotiUp.png") or app_region.exists("TradeButton.png"):
            find_trade(clan)
        leave_clan()
    else:
        app_region.click("redCross.png")