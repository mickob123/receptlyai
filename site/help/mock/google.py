from mock import *
def s1():
    b=appbar("menu","October",hl_left=True)
    days="M T W T F S S".split()
    for i,d in enumerate(days): b+=t(18+i*38,72,d,12,600,G3,"middle")
    for wk in range(4):
        for i in range(7): b+=t(18+i*38,100+wk*30,str(1+wk*7+i),13,400,TXT,"middle")
    b+=r(12,230,SW-24,34,"#DDE8F8")+t(22,252,"Blocked drain, Penrith",13,600)
    b+=r(12,272,SW-24,34,"#DDE8F8")+t(22,294,"Quote, Blacktown",13,600)
    b+=t(16,350,"Tap the three lines",14,600,G3)
    return phone(1,b,"Open the menu")
def s2():
    b=r(0,0,210,480,"#FFFFFF")+r(210,0,SW-210,480,"#00000055")
    for i,x in enumerate(["Schedule","Day","3 days","Week","Month"]): b+=t(20,40+i*40,x,15)
    b+=r(0,230,210,1,G2)+t(20,262,"Your work calendar",14,400,G3)
    b+=r(0,400,210,1,G2)+t(20,436,"Settings",15,700)+hl(10,414,150,34)
    return phone(2,b,"Scroll down, tap Settings")
def s3():
    b=appbar("back","Settings")+row(49,"General")
    b+=t(16,124,"you@yourbusiness.com.au",12,600,G3)
    b+=row(134,"Your name","Your work calendar",52,True)+hl(6,134,SW-12,52)
    b+=row(187,"Birthdays")+row(232,"Holidays in Australia")
    return phone(3,b,"Tap your work calendar")
def s4():
    b=appbar("back","Your name")+row(49,"Notifications")+row(94,"Colour")
    b+=t(16,166,"SHARED WITH",12,700,G3)
    b+=r(0,176,SW,50,"#FFFFFF")+t(16,206,"+  Add people or groups",15,700,"#1a5fd0")+hl(6,180,SW-12,42)
    b+=r(12,262,SW-24,40,"#FFFFFF",G3,1)+t(22,287,"Type the Receptly address",13,400,G3)
    return phone(4,b,"Add the Receptly address")
def s5():
    b=appbar("back","Permission")
    opts=["See only free/busy","See all event details","Make changes and see all event details","Make changes and manage sharing"]
    y=60
    for i,o in enumerate(opts):
        lines=[o] if len(o)<26 else [o[:o.rfind(' ',0,26)], o[o.rfind(' ',0,26)+1:]]
        h=30+18*len(lines)
        b+=r(0,y,SW,h,"#FFFFFF")+r(0,y+h,SW,1,G2)
        b+=f'<circle cx="26" cy="{y+h/2}" r="8" fill="{"#1a5fd0" if i==2 else "#fff"}" stroke="{"#1a5fd0" if i==2 else G3}" stroke-width="2"/>'
        for j,l in enumerate(lines): b+=t(46,y+24+j*18,l,14,700 if i==2 else 400)
        if i==2: b+=hl(6,y+2,SW-12,h-4)
        y+=h+1
    return phone(5,b,"Pick “Make changes…”")
def s6():
    b=appbar("back","Share with","Save",hl_right=True)
    b+=r(12,70,SW-24,40,"#FFFFFF",G3,1)+t(22,95,"Receptly address",13,600)
    b+=r(12,124,SW-24,56,"#FFFFFF",G3,1)+t(22,148,"Make changes and see",13,600)+t(22,166,"all event details",13,600)
    return phone(6,b,"Tap Save. Done.")
SHOTS=[s1(),s2(),s3(),s4(),s5(),s6()]
