#!/usr/bin/env python3

import json
import time
import tweepy

from PIL import ImageFont,ImageDraw,Image
from datetime import datetime,date
from pytrends.request import TrendReq

#PATH="/home/pi/Bots/GoogleFrends/"
PATH="./"

def connect():
    global api
    with open(f"{PATH}credentials.json","r") as f:
        token = json.load(f)

    consumer_key = token["API_KEY"]
    consumer_secret = token["API_SECRET_KEY"]
    access_token = token["ACCESS_TOKEN"]
    access_token_secret = token["ACCESS_TOKEN_SECRET"]
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

def createImage():
    pytrend = TrendReq()
    df = pytrend.today_searches(pn="FR")

    image = Image.open(f"{PATH}assets/template.jpeg")
    draw = ImageDraw.Draw(image)  
       
    font = ImageFont.truetype(f"{PATH}Calibri.ttf", 50)  

    x = 600
    y = 420
    for r in df.head(10):
        draw.text((x, y), ("·    " + r), font=font, fill=(130,130,130))  
        y += 65
    image.save(f"{PATH}assets/output.png")

def postImage():
    
    connect()
    
    try:
        Tdate = date.today()
        day_fr = {"Monday" : "Lundi", "Tuesday" : "Mardi", "Wednesday" : "Mercredi", "Thursday" : "Jeudi", "Friday" : "Vendredi", "Saturday" : "Samedi", "Sunday" : "Dimanche"}
        month_fr = ["","Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]

        if Tdate.strftime("%d") == "01":
            day = "1er"
        else:
            day = Tdate.strftime("%d")
        date_today = day_fr[Tdate.strftime("%A")] + " " + day + " " + month_fr[int(Tdate.strftime("%m"))] + " " + Tdate.strftime("%Y")

        status = "Top des recherches Google en France du " + date_today + " (" + Tdate.strftime("%d/%m/%Y") + ") à " + datetime.now().strftime("%H") + "h"
        filename = f"{PATH}assets/output.png"
         
        api.update_with_media(filename, status)

        print(str(Tdate) + " " + datetime.now().strftime("%H:%M:%S") + " : Success")
    except Exception as e:
        print(str(Tdate) + " " + datetime.now().strftime("%H:%M:%S") + " : Fail")
        print(e)

def main():
    createImage()
    #postImage()

if __name__ == "__main__":
    main()