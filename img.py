from PIL import Image

sizes = [(16, 16), (32, 32)]

img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
img.save('img/blank.ico', sizes=sizes)
