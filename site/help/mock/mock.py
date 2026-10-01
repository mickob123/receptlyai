# Simplified, logo-free UI mock-ups for the /help/ guides. Receptly palette, square corners.
BLK="#0A0A0A"; INK="#141414"; YEL="#F2C300"; G1="#F4F4F2"; G2="#E2E1DC"; G3="#9A9890"; TXT="#1C1C1C"
W,H=300,560  # phone
def esc(s): return s.replace("&","&amp;").replace("<","&lt;")
def t(x,y,s,size=15,w=400,fill=TXT,anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="Barlow,Arial,sans-serif" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>'
def r(x,y,w,h,fill,stroke=None,sw=0):
    s=f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{s}/>'
def hl(x,y,w,h): # yellow target box
    return r(x-4,y-4,w+8,h+8,"none",YEL,4)
def phone(n, body, title):
    sx,sy=14,40  # screen origin
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H+40}" role="img" aria-label="Step {n}: {esc(title)}">',
         r(0,0,W,H,BLK), r(sx,sy,W-28,H-80,G1), r(W/2-30,16,60,8,"#2a2a2a"), r(W/2-40,H-28,80,6,"#3a3a3a"),
         f'<g transform="translate({sx},{sy})">{body}</g>',
         r(0,H,44,40,YEL), t(22,H+28,str(n),22,800,BLK,"middle"), r(44,H,W-44,40,"#2B2B2B"), t(56,H+26,title,15,600,"#FFFFFF"),
         '</svg>']
    return "".join(out)
SW=W-28
def appbar(left="", title="", right="", hl_left=False, hl_right=False):
    b=r(0,0,SW,48,"#FFFFFF")+r(0,48,SW,1,G2)
    if left=="menu":
        b+="".join(r(14,15+i*8,20,3,TXT) for i in range(3))
        if hl_left: b+=hl(10,10,28,28)
    elif left=="back": b+=t(14,31,"←",22,500)
    b+=t(48 if left else 14,31,title,17,600)
    if right:
        b+=t(SW-14,31,right,16,700,"#1a5fd0","end")
        if hl_right: b+=hl(SW-62,12,52,26)
    return b
def row(y,label,sub=None,h=44,bold=False,col=TXT):
    s=r(0,y,SW,h,"#FFFFFF")+r(0,y+h,SW,1,G2)+t(16,y+(26 if not sub else 20),label,15,600 if bold else 400,col)
    if sub: s+=t(16,y+37,sub,12,400,G3)
    return s

# ---------- browser frame ----------
BW,BH=560,330   # content area
import json as _json, os as _os
_CROP_F = _os.path.join(_os.path.dirname(__file__), "crop.json")
CROP = _json.load(open(_CROP_F)) if _os.path.exists(_CROP_F) else {}
def browser(n, caption, where, body):
    key = "%s|%s" % (where, caption)
    cw, ch = CROP.get(key, (BW, BH))
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cw} {ch+76}" role="img" aria-label="Step {n}: {esc(caption)}" data-k="{esc(key)}">',
         r(0,0,cw,36,BLK)]
    out+= [r(12+i*14,14,8,8,"#555") for i in range(3)]
    out+= [r(60,8,cw-72,20,"#2a2a2a"), t(70,23,where,12,500,"#cfcfcf")] if where else []
    out+= [r(0,36,cw,ch,G1), f'<g class="c" transform="translate(0,36)" clip-path="none">{body}</g>',
           r(0,ch+36,44,40,YEL), t(22,ch+64,str(n),22,800,BLK,"middle"),
           r(44,ch+36,cw-44,40,"#2B2B2B"), t(56,ch+62,caption,15,600,"#FFFFFF"), '</svg>']
    return "".join(out)
def sidebar(items, hi=None, w=150, title=None):
    s=r(0,0,w,BH,"#FFFFFF").replace("<rect","<rect data-bg=\"1\"")+r(w,0,1,BH,G2).replace("<rect","<rect data-bg=\"1\"")
    y=18
    if title: s+=t(16,y+10,title,13,700,G3); y+=26
    for i,it in enumerate(items):
        bold = i==hi
        s+=t(16,y+16,it,14,700 if bold else 400)
        if bold: s+=hl(8,y-2,w-16,28)
        y+=34
    return s
def head(x,y,txt,size=20): return t(x,y,txt,size,700)
def button(x,y,label,hi=False,w=None,primary=True):
    w=w or 16+len(label)*8.2
    s=r(x,y,w,34,"#1C1C1C" if primary else "#FFFFFF","#1C1C1C",1)+t(x+w/2,y+22,label,14,700,"#FFFFFF" if primary else TXT,"middle")
    return s+(hl(x,y,w,34) if hi else "")
def field(x,y,w,label,value="",hi=False,ph=False):
    s=t(x,y-8,label,12,600,G3)+r(x,y,w,34,"#FFFFFF",G3,1)+t(x+10,y+22,value,14,400 if not ph else 400,G3 if ph else TXT)
    return s+(hl(x,y,w,34) if hi else "")
def menu_list(x,y,w,opts,hi):
    s=r(x,y,w,len(opts)*32+8,"#FFFFFF",G3,1)
    for i,o in enumerate(opts):
        s+=t(x+12,y+26+i*32,o,14,700 if i==hi else 400)
        if i==hi: s+=hl(x+4,y+6+i*32,w-8,28)
    return s
def keybox(x,y,w,label="Your key",hi_copy=True):
    s=t(x,y-8,label,12,600,G3)+r(x,y,w,38,"#FFFFFF",G3,1)+t(x+10,y+25,"k9F2-••••••••••••-7Qx3",14,500,"#555")
    bx=x+w-70; s+=r(bx,y+5,62,28,"#1C1C1C")+t(bx+31,y+24,"Copy",13,700,"#fff","middle")
    return s+(hl(bx,y+5,62,28) if hi_copy else "")
def note(x,y,txt): return t(x,y,txt,13,600,G3)
