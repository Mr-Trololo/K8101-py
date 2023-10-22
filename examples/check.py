import K8101

K8101.connect()
K8101.setInverted(0)
K8101.clearAll()
K8101.clearAll()
K8101.backlight(255)

K8101.drawPixel(0,0)
K8101.drawPixel(127,0)
K8101.drawPixel(0,63)
K8101.drawPixel(127,63)

for row in range (0,127,2):
    for column in range (0,63,2):
        K8101.drawPixel(row,column)

K8101.setInverted(1)