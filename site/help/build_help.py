# -*- coding: utf-8 -*-
"""Builds the /help/ hub and the seven connection guides as WordPress block markup.
Run: python3 build_help.py [--publish]. Facts sourced 30 Sep 2026 — see project doc
claude/connecting-client-systems.md. Anything unconfirmed is worded as such on the page."""
import json, sys
sys.path.insert(0, "/home/claude/receptly")

def esc(s): return s  # content is authored HTML; keep as-is

def section(inner, tone=""):
    cls = "rc-section" + (" rc-section--" + tone if tone else "")
    attrs = {"align": "full", "className": cls, "layout": {"type": "constrained"}}
    return ('<!-- wp:group %s -->\n<div class="wp-block-group alignfull %s">\n%s</div>\n<!-- /wp:group -->\n'
            % (json.dumps(attrs), cls, inner))

def eyebrow(t): return '<!-- wp:paragraph {"className":"rc-eyebrow"} -->\n<p class="rc-eyebrow">%s</p>\n<!-- /wp:paragraph -->\n' % t
def h1(t): return '<!-- wp:html -->\n<h1 class="wp-block-heading has-huge-font-size">%s</h1>\n<!-- /wp:html -->\n' % t
def h2(t): return '<!-- wp:heading -->\n<h2 class="wp-block-heading">%s</h2>\n<!-- /wp:heading -->\n' % t
def h3(t): return '<!-- wp:heading {"level":3} -->\n<h3 class="wp-block-heading">%s</h3>\n<!-- /wp:heading -->\n' % t
def lead(t): return '<!-- wp:paragraph {"className":"rc-lead","fontSize":"large"} -->\n<p class="rc-lead has-large-font-size">%s</p>\n<!-- /wp:paragraph -->\n' % t
def p(t): return '<!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph -->\n' % t
def muted(t): return '<!-- wp:paragraph {"className":"rc-muted"} -->\n<p class="rc-muted">%s</p>\n<!-- /wp:paragraph -->\n' % t
def html(t): return '<!-- wp:html -->\n%s\n<!-- /wp:html -->\n' % t
FIG_CSS = '<style>.rc-figs-help .rc-fig-n{font-size:clamp(2rem,4.2vw,2.75rem);line-height:1.05}</style>'
def figs(items): return html(FIG_CSS + '<div class="rc-figures rc-figs-help">' + "".join(
    '<div class="rc-fig"><span class="rc-fig-n">%s</span><span class="rc-fig-t">%s</span></div>' % i for i in items) + '</div>')
def ul(items): return html('<ul class="rc-list">' + "".join('<li>%s</li>' % i for i in items) + '</ul>')
def nope(items): return html('<ul class="rc-nope">' + "".join('<li>%s</li>' % i for i in items) + '</ul>')
SHOT_CSS = ('<style>.rc-shot{margin:14px 0 6px;max-width:520px}.rc-shot.phone{max-width:250px}'
            '.rc-shot svg{width:100%;height:auto;display:block}'
            '.rc-shot.duo{max-width:none;display:flex;flex-wrap:wrap;gap:14px}.rc-shot.duo svg{width:240px;max-width:100%}'
            '@media(max-width:600px){.rc-shot.wide{margin-left:calc(-1 * var(--rc-shot-pull,0px))}}</style>')
def _kind(svg):
    vb = svg.split('viewBox="0 0 ')[1].split('"')[0].split()
    w = float(vb[0])
    return "duo" if w > 560 else ("phone" if w < 400 else "wide")
def steps(items, shots=None):
    shots = shots or [None]*len(items)
    lis = []
    for (a, b), sv in zip(items, shots):
        if isinstance(sv, list):
            fig = '<figure class="rc-shot duo">%s</figure>' % "".join(sv)
        else:
            fig = ('<figure class="rc-shot %s">%s</figure>' % (_kind(sv), sv)) if sv else ''
        lis.append('<li><div><strong>%s</strong>%s%s</div></li>' % (a, b, fig))
    return html((SHOT_CSS if any(shots) else '') + '<ol class="rc-steps">' + "".join(lis) + '</ol>')
SHOT_NOTE = "Pictures are simplified. Your screen may look a little different."

HANDOVER = ("Send it through the secure link we text you. Don't email it, text it back or read it out "
            "over the phone. The link puts it straight into our locked system and nobody sees it in a message.")

def footer_block():
    return section(
        h2("Stuck on a step?") +
        p("Stop where you are and tell us on the setup call. We'll walk you through it on the phone while you tap. "
          "Or email <a href=\"mailto:contact@receptlyai.com.au\">contact@receptlyai.com.au</a> with the step number you're on.") +
        muted('<a href="/help/">All connection guides</a> · <a href="/integrations/">Everything Receptly works with</a>'),
        "base")

def guide(g):
    out = section(eyebrow("Help · " + g["name"]) + h1(g["h1"]) + lead(g["lead"]) + figs(g["facts"]))
    out += section(eyebrow("Before you start") + h2(g.get("before_h", "What you need")) + ul(g["before"]), "surface")
    for i, blk in enumerate(g["steps"]):
        out += section(eyebrow(blk["eyebrow"]) + h2(blk["h2"]) + (p(blk["intro"]) if blk.get("intro") else "")
                       + steps(blk["items"], blk.get("shots"))
                       + (muted(SHOT_NOTE) if blk.get("shots") else "")
                       + (muted(blk["after"]) if blk.get("after") else ""),
                       "" if i % 2 == 0 else "surface")
    out += section(eyebrow("What it costs you") + h2(g["cost_h"]) + "".join(p(x) for x in g["cost"]), "surface")
    if g.get("nope"):
        out += section(eyebrow("Why we do it this way") + h2(g.get("nope_h", "What we won't ask you for")) + nope(g["nope"]))
    out += section(eyebrow("Switching it off") + h2("You can cut us off yourself, any time") + "".join(p(x) for x in g["off"]), "surface")
    if g.get("faq"):
        out += section(eyebrow("Questions") + h2("Straight answers") + "".join(h3(q) + p(a) for q, a in g["faq"]))
    out += footer_block()
    return out

NO_PASSWORD = [
    "Your password. Not for any of your accounts, not ever. If someone says they're from Receptly and asks for one, it isn't us.",
    "A login of our own inside your software. Most job software charges per user, so that would put your bill up, and some of them ban shared logins outright.",
]

GUIDES = [
dict(slug="google-calendar", name="Google Calendar", title="Connect Google Calendar to Receptly",
 seo_title="Share your Google Calendar with Receptly | Help", seo_desc="How to let Receptly book jobs into your Google Calendar from your phone in about a minute. No password, nothing to install, and you can switch it off yourself.",
 h1="Let Receptly book jobs into your Google Calendar",
 lead="About a minute on your phone. You share your calendar with us the same way you'd share it with an office manager. We do the rest.",
 facts=[("1 min","On your phone or a computer. Nothing to install."),("You","Whoever owns the Google account your jobs go into."),("Free","Sharing a calendar costs nothing.")],
 before=["The Google Calendar app on your phone, or a computer with calendar.google.com open.",
         "Signed in to the Google account that holds your work calendar.",
         "The Receptly address we give you on the setup call. It doesn't need to be in your contacts. Type it in and it works.",
         "If your email ends in your business name and someone else runs it, they may have blocked sharing outside the business. If a step below won't let you add us, that's why. Tell us and we'll sort it with them."],
 steps=[dict(eyebrow="On your phone", h2="Share it from the Google Calendar app", items=[
    ("Open the menu","Open Google Calendar and tap the three lines, top left."),
    ("Go to Settings","Scroll to the bottom of the menu and tap Settings."),
    ("Pick the calendar","Under your email address, tap the calendar your jobs should land in. For most people that's the one with your own name on it."),
    ("Add us","Tap Shared with, then Add people or groups. Type the Receptly address."),
    ("Set the permission","Choose <em>Make changes and see all event details</em>. The default is view only, and we can't book a job into a calendar we can only look at."),
    ("Save","Tap Save. That's it.")]),
  dict(eyebrow="On a computer", h2="Or share it from calendar.google.com", items=[
    ("Find the calendar","On the left, under My calendars, hover over your calendar and click the three dots, then Settings and sharing."),
    ("Add us","Under Share with specific people or groups, click Add people and groups and type the Receptly address."),
    ("Set the permission","Choose <em>Make changes and see all event details</em>, then Send.")])],
 cost_h="Nothing", cost=["Sharing a Google Calendar is free. There's no extra account for you to pay for."],
 nope=NO_PASSWORD,
 off=["Go back to the same screen: Settings, your calendar, Shared with. Tap the cross next to our address and save. Bookings stop that moment.",
      "Jobs already in your calendar stay where they are. They're yours."],
 faq=[("Why does it need to see event details?","So it doesn't book a job on top of something you've already got on. It checks when you're busy before it offers a time."),
      ("Can it see my personal stuff?","It sees the calendar you share and nothing else. Keep a separate calendar for family things and don't share that one."),
      ("I use Outlook, not Google.","Different steps. See <a href=\"/help/outlook/\">connecting Outlook</a>.")]),

dict(slug="outlook", name="Outlook", title="Connect Outlook or Microsoft 365 to Receptly",
 seo_title="Connect Outlook or Microsoft 365 to Receptly | Help", seo_desc="How to connect an Outlook, Hotmail or Microsoft 365 calendar to Receptly so it can book jobs in. One sign-in on a computer, about two minutes.",
 h1="Let Receptly book jobs into your Outlook calendar",
 lead="Microsoft doesn't let you share an editable calendar with anyone outside your business, so Outlook works differently from Google. You sign in once and click Accept. About two minutes on a computer.",
 facts=[("2 min","On a computer. Easier than on a phone."),("You","Whoever owns the Outlook or Microsoft 365 account."),("Free","No extra Microsoft licence.")],
 before=["A computer. You'll sign in to your Microsoft account once.",
         "The email invite we send you after the setup call. It gives you a login to your Receptly settings, for this one job.",
         "If someone else runs your business Microsoft 365, they may need to approve the connection. If you see <em>Need admin approval</em>, forward it to them."],
 steps=[dict(eyebrow="Steps", h2="Connect it once", items=[
    ("Open the invite","Click the link in our email and set a password for your Receptly login."),
    ("Go to Connections","Click Settings, then Calendars, then the Connections tab."),
    ("Add Outlook","Click Add New and choose Outlook."),
    ("Sign in to Microsoft","Sign in with the account your work calendar lives in."),
    ("Accept","Click Accept. You're done. We set up which calendar it books into.")],
    after="If your screen doesn't show Settings, click your initials in the corner, then Profile, then Calendar settings. Same Outlook button from there. Outlook.com, Hotmail, Live and Microsoft 365 accounts all work this way. An on-site Exchange server doesn't. If that's you, say so on the setup call.")],
 cost_h="Nothing", cost=["There's no charge from us or from Microsoft to connect it."],
 nope=NO_PASSWORD,
 off=["Log in and go back to Settings, Calendars, Connections, and remove Outlook. Or tell us and we'll remove it the same day.",
      "Jobs already in your calendar stay where they are."],
 faq=[("Why can't I just share it like Google?","Microsoft 365 only allows view-only sharing with people outside your business. We need to add bookings, so view-only won't do."),
      ("Will I have to log in again?","Only if the connection drops, for example after you change your Microsoft password. If that happens we'll tell you.")]),

dict(slug="servicem8", name="ServiceM8", title="Connect ServiceM8 to Receptly",
 seo_title="How to create a ServiceM8 API key for Receptly | Help", seo_desc="Step by step: create a ServiceM8 API key so Receptly can put jobs from your calls straight into ServiceM8. Five minutes, no extra user, revoke it yourself any time.",
 h1="Connect ServiceM8 in five minutes",
 lead="You make a key in ServiceM8 and send it to us. The key lets Receptly create clients and jobs from your calls. No extra user, no password.",
 facts=[("5 min","On a computer. The ServiceM8 web app, not the phone app."),("You","The account owner, or whoever looks after your ServiceM8 settings."),("No extra user","ServiceM8 doesn't charge per user. The key isn't a user anyway.")],
 before=["A paid ServiceM8 plan. The free plan doesn't include API keys.",
         "Your ServiceM8 login, on a computer.",
         "The secure link we text you after the setup call."],
 steps=[dict(eyebrow="Steps", h2="Make the key", items=[
    ("Open Settings","Log in to ServiceM8 on a computer and go to Settings."),
    ("Find API Keys","Click API Keys."),
    ("Add a key","Click Add API Key and call it Receptly, so you know what it is later."),
    ("Choose Full Access","It needs to create clients and jobs. Read only can't do that."),
    ("Copy the key","Copy the whole key."),
    ("Send it to us","" + HANDOVER)])],
 cost_h="No extra user. Jobs count like any other job.",
 cost=["ServiceM8 charges by jobs per month, not by user, and a key isn't a user. So there's nothing extra to pay for the connection itself.",
       "Each job Receptly creates uses one job from your monthly allowance, the same as a job you type in yourself. That's why it only creates a job when the call passes the rules you set. A tyre-kicker outside your rules gets a callback promise and a text to you, not a job."],
 nope=NO_PASSWORD,
 off=["In ServiceM8, go to Settings, API Keys, and delete the Receptly key. The connection stops that second. You don't have to ring us first.",
      "Everything it did shows in each job's diary under the key's name, so you can always see what it touched."],
 faq=[("Does it change my existing jobs?","No. It creates new clients and jobs. It doesn't edit, invoice or delete anything."),
      ("What does Receptly do in ServiceM8?","See <a href=\"/integrations/servicem8/\">Receptly and ServiceM8</a> for what lands in ServiceM8 after a call.")]),

dict(slug="fergus", name="Fergus", title="Connect Fergus to Receptly",
 seo_title="How to create a Fergus access token for Receptly | Help", seo_desc="Step by step: generate a Fergus personal access token so Receptly can lodge calls as enquiries or jobs. No extra user, and you can revoke it yourself.",
 h1="Connect Fergus in five minutes",
 lead="You generate a token in Fergus and send it to us. It works through a login you already pay for, so there's no extra user.",
 facts=[("5 min","On a computer."),("You","An Admin or Full User in Fergus."),("No extra user","The token hangs off a user you already have.")],
 before=["An Admin or Full User login in Fergus. Timesheet users can't do this.",
         "The secure link we text you after the setup call.",
         "Fergus allows one token per user. If you've already made one for something else, like Zapier, have another Full User make ours, or tell us on the setup call."],
 steps=[dict(eyebrow="Steps", h2="Generate the token", items=[
    ("Open Settings","Log in to Fergus and go to Settings."),
    ("Find the Fergus API","Click Integrations, then Fergus API."),
    ("Generate","Generate a personal access token."),
    ("Copy it","Copy the whole token."),
    ("Send it to us","" + HANDOVER)])],
 cost_h="No extra user",
 cost=["A Fergus Full User is a paid seat, which is exactly why we don't ask for one. The token works through a login you already have.",
       "Fergus doesn't list a fee for using its API."],
 nope=NO_PASSWORD,
 off=["In Fergus, go to Settings, Integrations, Fergus API, and remove the token. The connection stops straight away.",
      "It also stops if the person whose login made the token is removed or moved down from a Full User. If you're changing staff around, tell us first."],
 faq=[("Does the token run out?","Yes. Fergus tokens last a year. We'll remind you before it runs out, and making a new one takes two minutes."),
      ("Whose name shows in Fergus?","Whatever Receptly creates shows as done by the person whose login made the token. Worth making it from the office login rather than a tradie's."),
      ("What does Receptly do in Fergus?","See <a href=\"/integrations/fergus/\">Receptly and Fergus</a>.")]),

dict(slug="simpro", name="Simpro", title="Connect Simpro to Receptly",
 seo_title="How to set up Simpro API access for Receptly | Help", seo_desc="How to create a Simpro API application so Receptly can create jobs from your calls, and what to check about licences before you start.",
 h1="Connect Simpro",
 lead="Simpro makes the account owner create the connection, which is the right way round: the credentials are yours to switch off. About ten minutes on a computer, and we'll be on the phone for it.",
 facts=[("10 min","On a computer, with us on the phone."),("You","Someone with the API Applications permission, usually the owner or admin."),("Licences","We check this with you before anything is set up.")],
 before=["A Simpro login with the <em>API Applications</em> permission. If you can't see the API tab in the steps below, that's the missing piece.",
         "Your Simpro web address, the one you log in at.",
         "The secure link we text you after the setup call."],
 steps=[dict(eyebrow="Steps", h2="Create the API application", items=[
    ("Open System Setup","Go to System, then Setup, then System Setup."),
    ("Find the API tab","Click the API tab, then Applications."),
    ("Add an application","Add a new application and call it Receptly."),
    ("Copy the details","Copy the client ID and the client secret it gives you."),
    ("Send them to us","Send both, plus your Simpro web address. " + HANDOVER)],
    after="Simpro's screens change from build to build. If yours doesn't match, stop and we'll find it together on the call.")],
 cost_h="We confirm licences with you first",
 cost=["Simpro doesn't publish its pricing, and it hasn't told us yet whether an API application uses one of your user licences. We've asked. Until it confirms, we check your licence count with you on the setup call, and nothing gets set up that adds a licence without you saying yes first.",
       "What we won't do is ask you for a Simpro login of our own. Simpro user licences are shared across your staff, so a Receptly login could lock one of your people out at the wrong moment."],
 nope=NO_PASSWORD,
 off=["In Simpro, go back to System Setup, API, Applications, and delete the Receptly application. The connection stops.",],
 faq=[("What does Receptly do in Simpro?","See <a href=\"/integrations/simpro/\">Receptly and Simpro</a>.")]),

dict(slug="aroflo", name="AroFlo", title="Connect AroFlo to Receptly",
 seo_title="How to turn on AroFlo API access for Receptly | Help", seo_desc="How to get AroFlo API access switched on and create an access token so Receptly can create tasks from your calls. What it costs and how to switch it off.",
 h1="Connect AroFlo",
 lead="AroFlo keeps its API switched off until you ask for it. So there are two parts: a quick request to AroFlo, then a token you make and send to us.",
 facts=[("1–2 days","Mostly waiting for AroFlo to switch it on. Your part is about ten minutes."),("You","Your AroFlo primary contact makes the request."),("No extra user","We use a token, not a login.")],
 before=["The primary contact on your AroFlo account. AroFlo only takes the request from them.",
         "Access to Site Administration in AroFlo, for part two.",
         "The secure link we text you after the setup call."],
 steps=[dict(eyebrow="Part one", h2="Ask AroFlo to switch the API on", items=[
    ("Contact AroFlo support","Your primary contact raises a support request asking for APIv2 to be enabled on your account. We can write the request for you. Just forward it."),
    ("Wait for the yes","AroFlo tells you when it's on.")]),
  dict(eyebrow="Part two", h2="Make the token", items=[
    ("Open Site Administration","In AroFlo, go to Site Administration, then Settings."),
    ("Find the API","Click AroFlo API, then APIv2."),
    ("Create a token","Create a Personal Access Token and copy it."),
    ("Send it to us","" + HANDOVER)])],
 cost_h="No extra user. We confirm the rest with AroFlo.",
 cost=["An extra AroFlo user starts at $80 a month, so we never ask to be added as one.",
       "AroFlo's own help page says API usage may be charged for in future. It doesn't charge today as far as we can find, and we've asked AroFlo to confirm. If that changes, we'll tell you before it costs you anything."],
 nope=NO_PASSWORD,
 off=["In AroFlo, go back to Site Administration, Settings, AroFlo API, and delete the token. The connection stops."],
 faq=[("What does Receptly do in AroFlo?","See <a href=\"/integrations/aroflo/\">Receptly and AroFlo</a>.")]),

dict(slug="tradify", name="Tradify", title="Receptly and Tradify: what connects today",
 seo_title="Using Receptly with Tradify: what connects today | Help", seo_desc="Tradify doesn't publish an API we can connect to. Here's what works today: bookings in your calendar and new jobs as Tradify enquiries, with no extra user.",
 h1="Tradify: what connects today",
 lead="Tradify doesn't publish an API we can plug into, and we won't pretend otherwise. Two things do work today, and neither needs an extra user.",
 facts=[("Enquiries","On Tradify Pro or Plus, each call can land in Tradify as an enquiry."),("Calendar","Bookings go in your Google Calendar, which Tradify can show."),("No extra user","We never ask to be added to Tradify.")],
 before=["For enquiries: Tradify Pro or Plus. The Lite plan doesn't have an enquiries address.",
         "For the calendar: a Google Calendar. Set that up first with the <a href=\"/help/google-calendar/\">Google Calendar guide</a>."],
 steps=[dict(eyebrow="Part one", h2="Turn on your enquiries address", intro="Every email sent to this address becomes an enquiry in Tradify. We send each call there, with the caller's details and what they need.", items=[
    ("Open Settings","In Tradify, go to Settings, then Enquiries."),
    ("Create the address","Set up your enquiries email address."),
    ("Give it to us","Read it out on the setup call or email it to us. It isn't a password, so it doesn't need the secure link.")]),
  dict(eyebrow="Part two", h2="Show your bookings in Tradify", intro="Receptly books into your Google Calendar. Tradify can pull that calendar in, so the bookings show up in your Tradify schedule.", items=[
    ("Open your profile","In Tradify, open your own profile."),
    ("Connect Google Calendar","Click Connect Google Calendar and sign in to the same Google account you shared with us.")],
    after="It's one way: Google into Tradify. Jobs you add in Tradify don't flow back to Google.")],
 cost_h="Nothing extra",
 cost=["Both of these use features already in your Tradify plan.",
       "What we won't do is ask to be added as a Tradify user. That's $48 to $62 a month on your bill, and Tradify's terms don't allow sharing logins with anyone outside your business."],
 nope=NO_PASSWORD,
 off=["Enquiries: change or switch off the enquiries address in Tradify's Settings. Calendar: remove our address from your Google Calendar sharing."],
 faq=[("Will you connect properly if Tradify opens an API?","Yes, at no extra cost. We've asked Tradify directly and we'll tell you the answer, whatever it is.")]),
]

import sys as _s; _s.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__file__), "mock"))
import scenes as _sc
from google import SHOTS as _gphone
_G = {g["slug"]: g for g in GUIDES}
_G["google-calendar"]["steps"][0]["shots"] = _gphone
_G["google-calendar"]["steps"][1]["shots"] = _sc.gcal_web()
_G["outlook"]["steps"][0]["shots"] = _sc.outlook()
_G["servicem8"]["steps"][0]["shots"] = _sc.servicem8()
_G["fergus"]["steps"][0]["shots"] = _sc.fergus()
_G["simpro"]["steps"][0]["shots"] = _sc.simpro()
_a1, _a2 = _sc.aroflo(); _G["aroflo"]["steps"][0]["shots"] = _a1; _G["aroflo"]["steps"][1]["shots"] = _a2
_t1, _t2 = _sc.tradify(); _G["tradify"]["steps"][0]["shots"] = _t1; _G["tradify"]["steps"][1]["shots"] = _t2
for _g in GUIDES:
    for _b in _g["steps"]:
        if _b.get("shots"): assert len(_b["shots"]) == len(_b["items"]), (_g["slug"], len(_b["shots"]), len(_b["items"]))

HUB = dict(slug="help", title="Connect your calendar and job software",
 seo_title="Connect your calendar and job software | Receptly help", seo_desc="Step-by-step guides to connect Google Calendar, Outlook, ServiceM8, Fergus, Simpro, AroFlo and Tradify to Receptly. No passwords, no extra users.")

def hub():
    rows = [
      ("/help/google-calendar/","Google Calendar","1 minute on your phone. Free."),
      ("/help/outlook/","Outlook and Microsoft 365","2 minutes on a computer. Free."),
      ("/help/servicem8/","ServiceM8","5 minutes. Needs a paid ServiceM8 plan. No extra user."),
      ("/help/fergus/","Fergus","5 minutes. Admin or Full User. No extra user."),
      ("/help/simpro/","Simpro","10 minutes, with us on the phone. We check licences with you first."),
      ("/help/aroflo/","AroFlo","AroFlo switches the API on first, then 10 minutes. No extra user."),
      ("/help/tradify/","Tradify","What connects today, without an extra user."),
    ]
    lst = html('<ul class="rc-list">' + "".join('<li><strong><a href="%s">%s</a></strong> %s</li>' % r for r in rows) + '</ul>')
    out = section(eyebrow("Help") + h1("Connect your calendar and job software") +
                  lead("We set up almost everything. One step has to be you, because only the owner of an account can let someone in. Each guide below is that one step, and we'll be on the phone for it if you want."))
    out += section(eyebrow("Pick yours") + h2("Guides") + lst, "surface")
    out += section(eyebrow("How we connect") + h2("What we'll never ask you for") + nope(NO_PASSWORD + [
        "Anything you can't take back. Every connection here can be switched off by you, in your own software, without ringing us."]))
    out += footer_block()
    return out

if __name__ == "__main__":
    import os
    os.makedirs("out", exist_ok=True)
    open("out/help.html","w").write(hub())
    for g in GUIDES: open("out/%s.html" % g["slug"],"w").write(guide(g))
    print("built", 1 + len(GUIDES))
