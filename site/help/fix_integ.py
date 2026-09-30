import sys; sys.path.insert(0,'/home/claude/receptly')
from wp import call
LINK = lambda s: '<a href="/help/%s/">Step-by-step guide</a>.' % s
EDITS = {
'servicem8': (82, [
 ("You generate it in ServiceM8 under Settings → API Keys and hand it over. Revoke it in one click, any time, and we stop.",
  "You make it in ServiceM8 under Settings → API Keys and send it through a secure link. Needs a paid ServiceM8 plan. Revoke it in one click, any time, and we stop."),
 ("In ServiceM8: Settings → API Keys → new key. That's the whole job on your side. Paste it into the setup form we send you, and it's stored encrypted.",
  "In ServiceM8: Settings → API Keys → Add API Key, Full Access. That's the whole job on your side, and it needs a paid ServiceM8 plan. Send it through the secure link we text you. " + LINK('servicem8')),
 ("Possibly, and you should know before you start. ServiceM8's own developer documentation flags that creating jobs through the API may incur account charges, depending on your plan. A job the receptionist creates counts the same as one you create by hand.",
  "No extra user: ServiceM8 doesn't charge per user, and a key isn't a user anyway. But each job the receptionist creates uses one job from your monthly ServiceM8 allowance, the same as a job you type in yourself."),
]),
'fergus': (85, [
 ("A personal access token gets you live today; we can move to OAuth later. Either way you can revoke it yourself.",
  "A personal access token gets you live today, through a login you already pay for. No extra user, and you can revoke it yourself."),
 ("In Fergus, generate a personal access token and paste it into the setup form we send. Stored encrypted, revocable by you at any time. If you'd rather use OAuth we'll set that up instead — it takes one extra step on the call.",
  "In Fergus: Settings → Integrations → Fergus API → generate a personal access token, from an Admin or Full User login you already have. Send it through the secure link we text you. Tokens last a year, and we remind you before it runs out. " + LINK('fergus')),
]),
'simpro': (86, [
 ("simPRO's API user is created inside your build by you.", "The API application is created inside your build by you."),
 ("You create the API user", "You create the API application"),
 ("In simPRO: System → Setup → API. Create an API user, generate the client ID and secret, and send them to us. We can't do this part for you — simPRO deliberately requires the build owner to do it, which is why you can revoke it whenever you like. We'll send a one-page walkthrough with screenshots.",
  "In Simpro: System → Setup → System Setup → API → Applications. Add an application for Receptly and send us the client ID and secret through the secure link we text you. We can't do this part for you — Simpro requires someone in your business with the API Applications permission, which is why you can revoke it whenever you like. Before anything is created, we check with you on the setup call that it won't add to your licence count. " + LINK('simpro')),
 ("Why do I have to create the API user myself?", "Why do I have to create the API application myself?"),
 ("We send a one-page walkthrough; it takes about five minutes.", 'The <a href="/help/simpro/">walkthrough</a> takes about ten minutes, and we stay on the phone for it.'),
]),
'aroflo': (87, [
 ("its API is properly built too — signed requests, per-account credentials, real webhooks.", "its API is properly built too, with credentials tied to your account."),
 ("AroFlo uses HMAC-SHA256 signing with credentials tied to your account, not ours. Strong, and yours to revoke.",
  "AroFlo credentials are tied to your account, not ours. Yours to revoke."),
 ("AroFlo credentials are generated against your account and stay tied to it. Send them through the setup form and they're stored encrypted.",
  "AroFlo keeps its API off until your primary contact asks for it, and we write that request for you. Then you make an access token in Site Administration and send it through the secure link we text you. " + LINK('aroflo')),
]),
'tradify': (88, [
 ("Tradify doesn't hand out API keys from a self-serve developer portal the way ServiceM8 and Fergus do — access is arranged with Tradify directly, and they confirm whether your plan allows it.",
  "Tradify doesn't hand out API keys the way ServiceM8 and Fergus do, and it doesn't publish an API we can connect to."),
 ("Tradify has a REST API and outbound webhooks. What it doesn't have is a public developer portal you can sign up to on a Tuesday afternoon. Access is requested through Tradify, they decide, and the documentation comes with the approval. That's their call to make and we're not going to pretend otherwise.",
  "Tradify doesn't publish an API, developer documentation or a Zapier connection that we can find. We've asked Tradify directly whether access is available. That's their call to make and we're not going to pretend otherwise."),
 ("Meanwhile you go live on day one with the receptionist booking into your calendar and texting you every call in full. Nothing waits.",
  "Meanwhile you go live on day one with the receptionist booking into your calendar and texting you every call in full. Nothing waits. On Tradify Pro or Plus we can also send each call to your Tradify enquiries address, so it lands in Tradify as an enquiry. " + '<a href="/help/tradify/">How that works</a>.'),
 ("Tradify approves API access per business and per plan.", "Whether Tradify offers API access at all is Tradify's call."),
 ("we'll give you exactly what to ask for — the endpoints and the use case, in a paragraph you can paste.", "we'll give you exactly what to ask for, in a paragraph you can paste."),
]),
}
dry = '--go' not in sys.argv
for slug,(pid,edits) in EDITS.items():
    raw = open(f'{slug}.orig.html').read(); new = raw
    for a,b in edits:
        n = new.count(a)
        if n != 1: print('!!', slug, n, a[:70]); continue
        new = new.replace(a,b)
    open(f'{slug}.new.html','w').write(new)
    print(slug, 'edits ok' if new!=raw else 'NO CHANGE')
    if not dry:
        r = call({'method':'POST','endpoint':f'pages/{pid}','payload':{'content':new}}); print('  ->', r['status'])
