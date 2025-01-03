from PIL import Image,ImageDraw
from res import backgrounds
from io import BytesIO
import requests

def trees_required(points):
    points_to_tree_val =5
    trees = points//points_to_tree_val
    return trees


async def send_imag(avatar_image_url,points):
    trees = trees_required(points)
   # print(trees)
    image = Image.open(backgrounds.get("level")[0])
    tree_image = Image.open(backgrounds.get("trees")[0]).resize((64,64))
    mask = tree_image.split()[3]
   # image.paste(tree_image,(0,0),mask=mask)
   
    while trees>=0:
        x_coord = (trees//10)*64
        y_coord = (trees%10)*64
        image.paste(tree_image,(x_coord,y_coord),mask=mask)
        trees = trees -1

    image_bin=BytesIO();
    image.save(image_bin,format="PNG")
    image_bin.seek(0)

    return image_bin


