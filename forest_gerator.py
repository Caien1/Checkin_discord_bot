from PIL import Image

image = Image.open("test_.webp")
image2 = Image.open("./res/tree.png").resize((50,50))

image.paste(image2,(50,50),image2)

image.show("Image_test")


