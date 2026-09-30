import sys, json
sys.path.insert(0,"/home/claude/receptly")
from wp import call
from build_help import GUIDES, HUB, hub, guide
def upsert(slug, title, content, parent, seo_title, seo_desc):
    ex = call({"method":"GET","endpoint":"pages","query":{"slug":slug,"parent":parent,"status":"publish,draft","_fields":"id"}})["body"]
    payload={"slug":slug,"title":title,"content":content,"status":"publish","parent":parent,"template":"page-no-title","comment_status":"closed","ping_status":"closed"}
    r = call({"method":"POST","endpoint":"pages/%d"%ex[0]["id"] if ex else "pages","payload":payload})
    pid = r["body"]["id"] if isinstance(r.get("body"),dict) and "id" in r["body"] else None
    m = call({"method":"POST","endpoint":"updateMeta","namespace":"rankmath/v1","payload":{"objectType":"post","objectID":pid,"meta":{"rank_math_title":seo_title,"rank_math_description":seo_desc,"rank_math_focus_keyword":title}}}) if pid else {"status":None}
    print(r["status"], m["status"], pid, slug, r["body"].get("link") if isinstance(r["body"],dict) else r["body"])
    return pid
hid = upsert("help", HUB["title"], hub(), 0, HUB["seo_title"], HUB["seo_desc"])
for g in GUIDES:
    upsert(g["slug"], g["title"], guide(g), hid, g["seo_title"], g["seo_desc"])
