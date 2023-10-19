import K8101
from PIL import Image

K8101.connect()
K8101.clearAll()
K8101.clearAll()

image = Image.open('image.bmp')
K8101.drawBitmap(image)