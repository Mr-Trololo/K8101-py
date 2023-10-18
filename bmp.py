import K8101
from PIL import Image

K8101.clearAll()
K8101.clearAll()



image = Image.open("image.bmp") # Open the image


K8101.drawBitmap(image)