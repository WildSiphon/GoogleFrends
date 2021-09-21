import json

from PIL import ImageFont,ImageDraw,Image
from datetime import *
from pytrends.request import TrendReq
from modules.twitter_wrapper import WrapperTwitter

#PATH="/home/pi/Bots/GoogleFrends/"
PATH="./"
DATE_FR = json.load(open(f"{PATH}date_fr.json", "r"))

def createImage():
    pytrend = TrendReq()
    trends  = pytrend.today_searches(pn="FR")

    image = Image.open(f"{PATH}assets/template.jpeg")
    draw  = ImageDraw.Draw(image)  
    font  = ImageFont.truetype(f"{PATH}assets/Calibri.ttf", 50)  

    x,y = 600,420
    for r in trends.head(10):
        draw.text(
            (x,y),
            ("·    " + r),
            font=font,
            fill=(130,130,130)
        )  
        y += 65
    image.save(f"{PATH}assets/output.png")

def createStatus(date):
    day_nb = "1er" if date.strftime("%d")=="01" else date.strftime("%d")
    date_fr_long = f"{DATE_FR['DAY'][date.strftime('%A')]} {day_nb} {DATE_FR['MONTH'][int(date.strftime('%m'))]} {date.strftime('%Y')}"
    status = f"Top des recherches Google en France du {date_fr_long} {date.strftime('(%d/%m/%Y) à %Hh')}"
    return status

def main():
    date = datetime.now()
    status = createStatus(date=date)
    try:
        createImage()
        twitter = WrapperTwitter(debug=False)
        twitter.postImage(
            status=status,
            filename=f"{PATH}assets/output.png",
        )
        print(f"{date.strftime('%Y-%m-%d %H:%M:%S')}: Success")
    except Exception as e:
        print(f"{date.strftime('%Y-%m-%d %H:%M:%S')}: Fail, {e}")

if __name__ == "__main__":
    main()
