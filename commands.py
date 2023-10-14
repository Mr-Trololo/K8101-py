import k8101

# standard commands
k8101.clearAll()
k8101.clearForeground()
k8101.drawText("hewwo",1,1,10,6)
k8101.beep(1)
k8101.drawFilledRectangle(1,1,10,10)
k8101.drawHollowRectangle(11,11,10,10)
k8101.eraseFilledRectangle(1,1,10,10)
k8101.eraseHollowRectangle(11,11,10,10)
k8101.drawPixel(15,15)
k8101.erasePixel(15,15)
k8101.backlight(255) # 0-254s, 255 permanent
k8101.setContrast(150)
k8101.drawLine(20, 20, 25, 25)
k8101.eraseLine(20, 20, 25, 25)
k8101.setInverted(True)
k8101.setInverted(False)

# custom commands
k8101.waitForKey() # returns press or hold depending on action
k8101.drawCircle(107,21,20,0.5)