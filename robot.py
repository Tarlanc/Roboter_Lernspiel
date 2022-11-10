
import time
import math
import random

from tkinter import *
random.seed()


class Anzeige(Frame):
    def __init__(self, master=None, width = 900, height=600):        
        Frame.__init__(self,master)
        top=self.winfo_toplevel() #Flexible Toplevel of the window
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.grid(sticky=N+S+W+E)
        self.width = width
        self.height = height

        #self.title("Spielfeld")
        self.set_window()

    def set_window(self):

        settings = {'Width':self.width,
                    'Height':self.height}

        self.coords = StringVar()
        self.coords.set("hallo")

        self.feld = Canvas(self,bg="#ffffff",height=settings['Height'],width=settings['Width'])
        self.feld.grid(row=1,column=1)
        self.feld.bind("<Motion>",self.show_coord)
        self.feld.bind("<Leave>",self.hide_coord)

        self.cleg = Label(self,textvariable=self.coords)
        self.cleg.grid(row=3,column=1,sticky=E)
        self.xlin = Canvas(self,width=settings['Width'],height=17,bg="#eeeeff")
        self.xlin.grid(row=2,column=1,sticky=N,columnspan=3)
        self.ylin = Canvas(self,width=30,height=settings['Height'],bg="#eeeeff")
        self.ylin.grid(row=1,column=0,sticky=E)

        for tick in range(0,settings['Width'],50):
            a = self.xlin.create_line(tick,0,tick,5,fill="#000000")
        for tick in range(100,settings['Width'],100):
            a = self.xlin.create_line(tick,0,tick,10,fill="#000000")
            a = self.xlin.create_text(tick,13,text=str(tick))

        for tick in range(0,settings['Height'],50):
            a = self.ylin.create_line(30,tick,25,tick,fill="#000000")
        for tick in range(100,settings['Height'],100):
            a = self.ylin.create_line(30,tick,20,tick,fill="#000000")
            a = self.ylin.create_text(3,tick,anchor=W,text=str(tick))

    def leeren(self):
        self.feld.delete("all")


    def show_coord(self,event=''):
        x = event.x
        y = event.y
        #print(x,y)
        self.coords.set("X: "+str(x)+" / Y: "+str(y))

    def hide_coord(self,event=''):
        self.coords.set("")



class Roboter():
    def __init__(self,master=None,x=250,y=250,richtung=0,farbe=None):
        self.xpos = x
        self.ypos = y
        self.size = 10
        self.direction = richtung*2*math.pi/360
        self.winkel=richtung
        self.master = master
        self.stiftpos = [int(self.xpos),int(self.ypos)]
        if farbe==None:
            self.farbe = regenbogen(random.random())
        else:
            self.farbe = farbe
        self.line = True
        self.kinder = []
        self.dicke = 1

        self.draw()

    def malen(self):
        self.line = not self.line


    def position(self):
        pos = [int(self.xpos),int(self.ypos)]
        pos.append(round(self.xpos+self.size*math.cos(self.direction)))
        pos.append(round(self.ypos+self.size*math.sin(self.direction)))

        for k in self.kinder:
            k.xpos=self.xpos
            k.ypos=self.ypos

        return pos
    

    def draw(self):
        p = self.position()
        self.id = self.master.feld.create_oval(p[0]-self.size,
                                          p[1]-self.size,
                                          p[0]+self.size,
                                          p[1]+self.size,
                                          fill=self.farbe,
                                          outline="#000000",
                                          width=1)
        
        self.id2 = self.master.feld.create_oval(p[2],p[3],p[2],p[3],
                                          fill="#000000",
                                          outline="#000000",
                                          width=6)
        self.master.feld.update()

    def zeichnen(self):
        p = self.position()

        self.master.feld.coords(self.id,[p[0]-self.size,
                                          p[1]-self.size,
                                          p[0]+self.size,
                                          p[1]+self.size])
        self.master.feld.coords(self.id2,[p[2],p[3],p[2],p[3]])
        self.master.feld.itemconfigure(self.id,fill=self.farbe)
                                          
        if self.line:
            l = self.master.feld.create_line(self.stiftpos[0],self.stiftpos[1],p[0],p[1],
                                             fill = self.farbe, width=int(self.dicke))
        self.stiftpos = [p[0],p[1]]
        self.master.feld.update()

        for k in self.kinder:
            k.zeichnen()


    def lauf(self,weg=50,delay=.01):
        schritt = 5
        schritte = int(weg/schritt)
        if schritte < 1:
            schritte = 1
        schritt = weg/schritte
        
        for t in range(schritte):
            self.xpos += schritt*math.cos(self.direction)
            self.ypos += schritt*math.sin(self.direction)
            self.zeichnen()
            time.sleep(delay)

    def spring(self,weg=50,delay=0.0):
        self.xpos += weg*math.cos(self.direction)
        self.ypos += weg*math.sin(self.direction)
        self.zeichnen()
        time.sleep(delay)

    def links(self,winkel=90):
        self.direction -= winkel*2*math.pi/360
        self.winkel-=winkel
        self.zeichnen()
        

    def rechts(self,winkel=90):
        self.direction += winkel*2*math.pi/360
        self.winkel += winkel
        self.zeichnen()
        

    def stirb(self):
        self.master.feld.delete(self.id)
        self.master.feld.delete(self.id2)

        for k in self.kinder:
            k.stirb()


class Arm():
    def __init__(self,master=None,x=400,y=250, laenge = 100, richtung=0, unterarm = 0, anker=None, farbe=None):
        if anker == None:
            self.xpos = x
            self.ypos = y
        else:
            self.xpos = anker.stiftpos[0]
            self.ypos = anker.stiftpos[1]
            anker.kinder.append(self)
            if farbe==None:
                farbe = anker.farbe
        self.oberarm = laenge
        self.unterarm = unterarm
        self.anker = anker
        self.winkel = [richtung*2*math.pi/360,richtung*2*math.pi/360]
        self.master = master
        if farbe == None:
            farbe=regenbogen(random.random())
        else:
            self.farbe = farbe
        self.line = True
        self.schritt = math.pi/180 ## Ein Kreis ist 360
        self.kinder = []
        self.dicke = 1

        self.draw() ## Recompute positions. Important step after each movement

    def malen(self):
        self.line = not self.line

    def position(self):
        x1 = self.xpos
        y1 = self.ypos

        x2 = round(self.xpos + math.cos(self.winkel[0])*self.oberarm)
        y2 = round(self.ypos + math.sin(self.winkel[0])*self.oberarm)

        x3 = round(x2 + math.cos(self.winkel[1])*self.unterarm)
        y3 = round(y2 + math.sin(self.winkel[1])*self.unterarm)

        self.stiftpos = [x3,y3]
        for k in self.kinder:
            k.xpos=x3
            k.ypos=y3

        return [x1,y1,x2,y2,x3,y3]


    def draw(self):
        p = self.position()
        self.arm1 = self.master.feld.create_line(p[0],p[1],p[2],p[3],
                                            fill="#aaaaaa",
                                            width=3)
        self.arm2 = self.master.feld.create_line(p[2],p[3],p[4],p[5],
                                            fill="#aaaaaa",
                                            width=3)
        self.ellenbogen = self.master.feld.create_oval(p[2]-3,p[3]-3,p[2]+3,p[3]+3,
                                            fill="#aaaaaa",
                                            width=1)
        self.stift = self.master.feld.create_oval(p[4]-3,p[5]-3,p[4]+3,p[5]+3,
                                            fill=self.farbe,
                                            width=1)
        self.master.feld.update()

    def zeichnen(self):
        prev = list(self.stiftpos)
        p = self.position()
        curr = list(self.stiftpos)
        self.master.feld.coords(self.arm1,[p[0],p[1],p[2],p[3]])
        self.master.feld.coords(self.arm2,[p[2],p[3],p[4],p[5]])
        self.master.feld.coords(self.ellenbogen,[p[2]-3,p[3]-3,p[2]+3,p[3]+3])
        self.master.feld.coords(self.stift,[p[4]-3,p[5]-3,p[4]+3,p[5]+3])

        self.master.feld.itemconfigure(self.stift,fill=self.farbe)

        if self.line:
            l = self.master.feld.create_line(prev[0],prev[1],curr[0],curr[1],
                                            fill=self.farbe, width=int(self.dicke))

        for k in self.kinder:
            k.zeichnen()
            
        self.master.feld.update()

    def drehen(self,step=10):
        #time.sleep(.0005)
        self.winkel[0]+=self.schritt*step
        self.winkel[1]+=self.schritt*step
        
    def biegen(self,step=10):
        #time.sleep(.0005)
        self.winkel[1]+=self.schritt*step

    def strecken(self,step=10,ober=True,unter=False):
        if ober and self.oberarm*1000>step:
            self.oberarm += step/1000
        if unter and self.unterarm*1000 > step:
            self.unterarm += step/1000

    def stirb(self):
        self.master.feld.delete(self.arm1)
        self.master.feld.delete(self.arm2)
        self.master.feld.delete(self.ellenbogen)
        self.master.feld.delete(self.stift)

        for k in self.kinder:
            k.stirb()

        if not self.anker == None:
            self.anker.kinder.remove(self)


    def drehmuster(self,step1=10,step2=0,strecken=0,unter=True,ober=True,dauer=2000, schnell=False):
        for i in range(dauer):
            if not schnell: time.sleep(.005)
            self.drehen(step1)
            self.biegen(step2)
            self.strecken(strecken,ober=ober,unter=unter)
            self.zeichnen()

    def kreis(self, bogen=90,schnell=False, delay=0.03):
        if bogen>0:
            schritt = 5
        else:
            schritt = -5
        schritte = int(bogen/schritt)
        if schritte <1: schritte = 1
        schritt = bogen/schritte
        for i in range(schritte):
            if not schnell: time.sleep(delay)
            self.drehen(schritt)
            self.zeichnen()

    def kreis2(self, bogen=90,schnell=False):
        if bogen>0:
            schritt = 5
        else:
            schritt = -5
        schritte = int(bogen/schritt)
        if schritte <1: schritte = 1
        schritt = bogen/schritte
        for i in range(schritte):
            if not schnell: time.sleep(.01)
            self.biegen(schritt)
            self.zeichnen()

    def wachsen(self, laenge=10, schnell=False):
        if laenge>0:
            schritt = 2
        else:
            schritt = -2
            
        schritte = int(laenge/schritt)
        if schritte <1: schritte = 1
        schritt = laenge/schritte
        for i in range(schritte):
            if not schnell: time.sleep(.05)
            self.strecken(schritt*1000)
            self.zeichnen()

    def bewegen(self, x=100, y=100,schnell=False):
        if x > 0:
            xstep = 5
        else:
            xstep = -5

        if y > 0:
            ystep = 5
        else:
            ystep = -5

        xs = int(x/xstep)
        ys = int(y/ystep)
        schritte = max(xs,ys)
        if schritte > 0:
            xstep = x/schritte
            ystep = y/schritte
            for i in range(schritte):
                if not schnell: time.sleep(.05)
                self.xpos+=xstep
                self.ypos+=ystep
                self.zeichnen()

    def bewege_zu(self, zux=100, zuy=100,schnell=False):
        x = zux-self.xpos
        y = zuy-self.ypos
        if x > 0:
            xstep = 5
        else:
            xstep = -5

        if y > 0:
            ystep = 5
        else:
            ystep = -5

        xs = int(x/xstep)
        ys = int(y/ystep)
        schritte = max(xs,ys)
        if schritte > 0:
            xstep = x/schritte
            ystep = y/schritte
            for i in range(schritte):
                if not schnell: time.sleep(.05)
                self.xpos+=xstep
                self.ypos+=ystep
                self.zeichnen()

def spirograph(muster, dauer=1000):
    for t in range(dauer):
        for m in muster:
            m[0].drehen(m[1])
            if len(m)>2:
                m[0].strecken(m[2])

        muster[0][0].zeichnen()

def regenbogen(x):
    if x >1:x=1
    if x <0:x=0
    red = math.cos(x*2*math.pi)+0.5
    green = math.cos((x+.66)*2*math.pi)+.05
    blue = math.cos((x+.33)*2*math.pi)+0.5

    outstr = '#'

    for v in [red,green,blue]:
        if v > 1:
            outstr+="ff"
        elif v < 0:
            outstr+="00"
        else:
            h = hex(int(v*255)).split('x')[-1]
            if len(h)==1:
                outstr+="0"+h
            else:
                outstr+=h

    return outstr

       
if __name__ == "__main__":  ##If it is just called as a module, don't start the GUI
    root = Tk()
    spielfeld = Anzeige(root)

    for i in range(100):
        bug = Roboter(spielfeld,x=500,y=300,farbe=regenbogen(0))
        bug.malen()
        drehen = random.random()*180
        schritte = 400
        arm = Arm(spielfeld,anker=bug,laenge=30,richtung=drehen-90,farbe=regenbogen(0))
        arm.dicke=random.random()*3+1
        extend = random.random()*3+.3
        for i in range(schritte):
            arm.farbe=regenbogen(i/schritte)
            bug.rechts(drehen)
            bug.spring(0+i*extend,0)
            #arm.malen()
            arm.kreis(drehen,schnell=True)
            arm.oberarm+=60/schritte
            #arm.malen()
        bug.stirb()
        spielfeld.leeren()
            



##    chef = Arm(spielfeld,x=450,y=300,laenge=140,farbe="#000000")
##    chef.line=False
##    blau = Arm(spielfeld,laenge=60,farbe="#0000ff",anker=chef)
##    rot = Arm(spielfeld,laenge=40,farbe="#ff0000",anker=blau)
##    gruen = Arm(spielfeld,laenge=20,farbe="#00ff00",anker=rot)
##
##    spirograph([(chef,6),(blau,-4,-20),(rot,-4),(gruen,-4)],dauer=900)
##    chef.stirb()
    
##
##
##    chef = Arm(spielfeld,y=400,unterarm=0,farbe="#000000")
##    chef.line=False
##    chef.kreis(-250)
##
##    blau = Arm(spielfeld,unterarm=50,farbe="#0000ff",anker=chef)
##    blau.line=False
##    blau.kreis(-500)
##    blau.line=True
##
##    rot = Arm(spielfeld,unterarm=50,farbe="#ff0000",anker=chef)
##    rot.line=False
##    rot.kreis(-250)
##    rot.line=True
##
##    gruen = Arm(spielfeld,unterarm=50,farbe="#00ff00",anker=rot)
##
##    chef.kreis(1000)
##
##    blau.kreis(250)
##    rot.kreis(250)
##    gruen.kreis(500)
##
##    for kreis in [blau,rot,gruen]:
##        kreis.line=False
##
##    chef.bewegen(0,-100)
##
##    for kreis in [blau,rot,gruen]:
##        kreis.line=True
##
##    chef.kreis(1000)
   
    #r.drehmuster(10,12,10,dauer=2000)
    #r.stirb()
    root.mainloop()
    
