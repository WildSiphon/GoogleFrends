from PIL import ImageFont,ImageDraw,Image
from datetime import *
from pytrends.request import TrendReq
from modules.twitter_wrapper import WrapperTwitter

DAY_FR = {"Monday" : "lundi", "Tuesday" : "mardi", "Wednesday" : "mercredi", "Thursday" : "jeudi", "Friday" : "vendredi", "Saturday" : "samedi", "Sunday" : "dimanche"}
MONTH_FR = ["","janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]

#PATH="/home/pi/Bots/GoogleFrends/"
PATH="./"

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

def createStatus(date):
    day_nb = "1er" if date.strftime("%d")=="01" else date.strftime("%d")
    date_fr_long = f"{DAY_FR[date.strftime('%A')]} {day_nb} {MONTH_FR[int(date.strftime('%m'))]} {date.strftime('%Y')}"
    status = f"Top des recherches Google en France du {date_fr_long} {date.strftime('(%d/%m/%Y) à %Hh')}"
    return status

def main():
    date = datetime.now()
    status = createStatus(date=date)
    try:
        createImage()
        twitter = WrapperTwitter(debug=False)
        twitter.postImage(status=status)
        print(f"{date.strftime('%Y-%m-%d %H:%M:%S')}: Success")
    except Exception as e:
        print(f"{date.strftime('%Y-%m-%d %H:%M:%S')}: Fail, {e}")

if __name__ == "__main__":
    main()