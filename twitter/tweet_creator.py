import datetime
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pytrends.request import TrendReq

ASSETS_DIRPATH = Path(__file__).parent.parent.resolve() / "assets"
DATE_TO_FR = {
    "DAY": {
        "Monday": "lundi",
        "Tuesday": "mardi",
        "Wednesday": "mercredi",
        "Thursday": "jeudi",
        "Friday": "vendredi",
        "Saturday": "samedi",
        "Sunday": "dimanche",
    },
    "MONTH": [
        "",
        "janvier",
        "f\u00e9vrier",
        "mars",
        "avril",
        "mai",
        "juin",
        "juillet",
        "ao\u00fbt",
        "septembre",
        "octobre",
        "novembre",
        "d\u00e9cembre",
    ],
}


def CreateStatus(date: datetime) -> str:
    """
    Create the status which will be posted with media.

    :return: Status including date in french format.
    """
    # Update date to french format
    day_nb = "1er" if date.strftime("%d") == "01" else date.strftime("%d")

    # Create textual date in french format
    date_fr_long = (
        f"{DATE_TO_FR['DAY'][date.strftime('%A')]} "
        f"{day_nb} {DATE_TO_FR['MONTH'][int(date.strftime('%m'))]} "
        f"{date.strftime('%Y')}"
    )

    # Create status
    status = (
        f"Top des recherches Google en France du {date_fr_long} "
        f"{date.strftime('(%d/%m/%Y) à %Hh')}"
    )

    return status


def CreateMedia() -> BytesIO:
    """
    Create the media to post on Twitter.

    :return: Stream of media to post.
    """
    # Get the top 10 trends in France
    trends = TrendReq().today_searches(pn="FR").head(10)

    # Load the template
    template_filepath = ASSETS_DIRPATH / "template.jpeg"
    media = Image.open(template_filepath)

    # Load the font
    font_filepath = ASSETS_DIRPATH / "Calibri.ttf"
    font = ImageFont.truetype(str(font_filepath), 50)

    # Draw the trends on the media
    x, y = 600, 420
    draw = ImageDraw.Draw(media)
    for research in trends:
        draw.text((x, y), ("·    " + research), font=font, fill=(130, 130, 130))
        y += 65

    # Save the media as a stream
    output_stream = BytesIO()
    media.save(output_stream, "JPEG")
    output_stream.seek(0)

    return output_stream
