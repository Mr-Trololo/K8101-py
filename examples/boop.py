import K8101

K8101.connect()
K8101.clearAll()
K8101.clearAll()
K8101.backlight(255)

K8101.drawText("Pat me :3",35,25,128,6)

K8101.waitForKey()

K8101.clearAll()
K8101.drawText("OwO",55,25,128,6)
K8101.backlight(20)
