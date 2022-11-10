
from tkinter import *
import robot

root = Tk()
spielfeld = robot.Anzeige(root)
###########################################


kerni = robot.Roboter(spielfeld,x=350,y=300, farbe="blue")
arm = robot.Arm(spielfeld,anker=kerni,laenge=100)

kerni.malen()
arm.malen()

for runde in range(10):
    arm.farbe=robot.regenbogen(runde/10)
    for i in range(6):
        arm.malen()
        arm.kreis(360,schnell=True)
        arm.malen()
        
        kerni.links(60)
        kerni.lauf(100,delay=0)
    arm.wachsen(-10,schnell=True)

kerni.stirb()
    

heini = robot.Roboter(spielfeld,x=550,y=400, farbe="black")

for i in range(120):
    heini.farbe=robot.regenbogen(i/120)
    heini.lauf(100+i,delay=0)
    heini.links(123)

kerni.stirb()




#############################################
root.mainloop()

