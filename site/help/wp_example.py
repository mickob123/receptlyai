import json, subprocess
URL="https://n8n.agentivegroup.ai/webhook/<temporary-helper-path>"  # a temp n8n workflow using the "Receptly WP App Password" credential; create, use, delete
def call(req):
    r=subprocess.run(["curl","-sS","--retry","2","-X","POST",URL,"-H","Content-Type: application/json","--data-binary","@-"],input=json.dumps(req),capture_output=True,text=True)
    try: return json.loads(r.stdout)
    except Exception: return {"status":None,"raw":r.stdout[:500],"err":r.stderr[:300]}
