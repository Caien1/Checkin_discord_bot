from PIL import Image
from res import backgrounds
from io import BytesIO
import requests


async def level_selector():
    pass

async def send_imag(avatar_image_url):
    image = Image.open(backgrounds.get("level")[3]).resize((400,400))

    response =  requests.get(avatar_image_url)
    avatar = BytesIO(response.content)
    avatar = Image.open(avatar).resize((75,75))
    avatar.thumbnail((100,100))
    image.paste(avatar,(0,0))


    image_bin=BytesIO();
    image.save(image_bin,format="PNG")
    image_bin.seek(0)

    return image_bin


