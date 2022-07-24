
import os

from PIL import Image, ImageDraw, ImageFont


def text_on_img(filename='0.jpg', text="Hello", size=12, color=(255, 255, 0)):
	# "Draw a text on an Image, saves it, show it"
    fnt = ImageFont.truetype("Chalkduster.ttf", 28)
    # 
    img = Image.open(filename)
    # create image
    draw = ImageDraw.Draw(img)
	# draw text
    draw.text((100, 250), text, font=fnt, fill=(255, 255, 255))
	# save file
    img.show()
    img.save(filename)


text_on_img(text="Text to write on img this is ar slf jkla sdjkl a", size=320)
