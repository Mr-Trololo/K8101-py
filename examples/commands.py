import K8101
from PIL import Image

# Connect to display first
K8101.connect()

# standard commands
K8101.clearAll()
image = Image.open('image.bmp')
K8101.drawBitmap(image)
K8101.clearForeground()
K8101.drawText("hewwo",1,1,10,6)
K8101.beep(1)
K8101.drawFilledRectangle(1,1,10,10)
K8101.drawHollowRectangle(11,11,10,10)
K8101.eraseFilledRectangle(1,1,10,10)
K8101.eraseHollowRectangle(11,11,10,10)
K8101.drawPixel(15,15)
K8101.erasePixel(15,15)
K8101.backlight(255) # 0-254s, 255 permanent
K8101.setContrast(150)
K8101.drawLine(20, 20, 25, 25)
K8101.eraseLine(20, 20, 25, 25)
K8101.setInverted(True)
K8101.setInverted(False)

# custom commands
K8101.waitForKey() # returns press or hold depending on action
K8101.drawHollowCircle(107,21,20,0.5)