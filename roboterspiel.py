
from tkinter import *
import robot

root = Tk()
spielfeld = robot.Anzeige(root)
###########################################





hansli = robot.Roboter(spielfeld)
hansli.lauf(100)
hansli.links()
hansli.lauf(50)
hansli.rechts()
hansli.lauf(100)
hansli.stirb()
hansli.links()
hansli.lauf()










#############################################
root.mainloop()

