import json, os, importlib
from playwright.sync_api import sync_playwright
if os.path.exists("crop.json"): os.remove("crop.json")
import mock, scenes; importlib.reload(mock); importlib.reload(scenes)
allsv=[]
for f in ["gcal_web","outlook","servicem8","fergus","simpro"]: allsv+=getattr(scenes,f)()
for a,b in [scenes.aroflo(),scenes.tradify()]: allsv+=a+b
allsv=[x for x in allsv if isinstance(x,str)]
html='<!doctype html><body>'+"".join(allsv)+'</body>'
crop={}
with sync_playwright() as p:
    br=p.chromium.launch(executable_path="/opt/pw-browsers/chromium"); pg=br.new_page()
    pg.set_content(html)
    res=pg.evaluate("""()=>[...document.querySelectorAll('svg[data-k]')].map(s=>{let R=0,B=0;for(const el of s.querySelector('g.c').querySelectorAll('rect:not([data-bg]),text,circle')){const b=el.getBBox();R=Math.max(R,b.x+b.width);B=Math.max(B,b.y+b.height)}return [s.dataset.k,R,B]})""")
    br.close()
for k,rx,by in res:
    crop[k]=(int(min(560,max(340,rx+28))), int(min(330,max(150,by+28))))
json.dump(crop,open("crop.json","w"),indent=0); print(len(crop))
