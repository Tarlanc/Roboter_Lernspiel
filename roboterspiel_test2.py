
from tkinter import *
import robot

root = Tk()
spielfeld = robot.Anzeige(root)
###########################################

def mach_dreieck(roboter,gross=1):
    roboter.lauf(100*gross)
    roboter.links(120)
    roboter.lauf(100*gross)
    roboter.links(120)
    roboter.lauf(100*gross)
    roboter.links(120)

hansli = robot.Roboter(spielfeld, farbe="blue")

for i in range(20):
    mach_dreieck(hansli,i/10)
    hansli.links(18)




#############################################
root.mainloop()

