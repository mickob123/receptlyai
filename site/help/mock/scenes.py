from mock import *

# ---------- shared: sending the key through our secure link (two phones) ----------
def send_step(n, what="key"):
    def sms():
        b=appbar("back","Receptly")
        b+=r(12,70,210,96,"#E9E8E3")+t(22,94,"Here's your secure link",13,600)+t(22,112,"for your "+what+". Paste it",13,400)+t(22,130,"in there, nowhere else.",13,400)
        b+=t(22,152,"receptlyai.com.au/connect",13,700,"#1a5fd0")+hl(16,138,200,22)
        return b
    def form():
        b=r(0,0,SW,48,BLK)+r(14,12,24,24,YEL)+t(26,30,"R",16,800,BLK,"middle")+t(48,30,"RECEPTLY",15,800,"#fff")
        b+=t(16,76,"Send us your "+what,16,700)
        b+=field(16,114,SW-32,"Business name","Dave's Plumbing")
        b+=field(16,176,SW-32,"Your software","ServiceM8 ▾" if what=="key" else "Your software ▾")
        b+=field(16,238,SW-32,"Paste it here","k9F2-••••••••••",hi=True)
        b+=r(16,296,SW-32,40,YEL)+t(SW/2,322,"Send securely",15,800,BLK,"middle")
        return b
    a=phone(n,sms(),"Tap the link we text you")
    c=phone(n,form(),"Paste it in. Send.")
    # combine two phones side by side
    return [a, c]

# ---------- Google Calendar on a computer ----------
def gcal_web():
    s1=sidebar(["Your name","Birthdays","Holidays"],0,170,"My calendars")+menu_list(180,30,200,["Display this only","Hide from list","Settings and sharing"],2)+note(200,180,"Hover, click the three dots")
    s2=head(24,40,"Share with specific people or groups")+button(24,64,"+ Add people and groups",hi=True,w=230,primary=False)+field(24,150,330,"Email","Receptly address",ph=True)
    s3=head(24,40,"Share with specific people")+field(24,80,300,"Email","Receptly address")+menu_list(24,130,330,["See only free/busy","See all event details","Make changes and see all event details","Make changes and manage sharing"],2)+button(380,276,"Send",hi=True,w=90)
    return [browser(1,"Settings and sharing","calendar.google.com",s1),
            browser(2,"Add people and groups","calendar.google.com",s2),
            browser(3,"Make changes, then Send","calendar.google.com",s3)]

# ---------- Outlook (via the Receptly settings login) ----------
def outlook():
    e1=head(24,40,"You're invited to your Receptly settings")+t(24,72,"Set a password to finish setting up your login.",14)+button(24,96,"Set your password",hi=True,w=180)
    e2=sidebar(["Business Profile","Calendars","Phone","Users"],1,170,"Settings")+t(200,40,"Calendars",18,700)
    for i,tb in enumerate(["Preferences","Availability","Connections"]):
        e2+=t(200+i*110,74,tb,14,700 if i==2 else 400)
    e2+=hl(414,56,104,26)
    e3=t(24,40,"Connections",18,700)+button(24,60,"+ Add New",w=110,primary=False)+menu_list(24,104,220,["Google","Outlook","Other"],1)
    e4=r(150,30,260,270,"#FFFFFF",G3,1)+t(170,70,"Sign in",20,700)+field(170,104,220,"Email","you@yourbusiness.com.au")+field(170,170,220,"Password","••••••••")+button(300,226,"Next",hi=True,w=90)+note(170,286,"Microsoft's own sign-in page")
    e5=r(110,20,340,290,"#FFFFFF",G3,1)+t(130,56,"Permissions requested",17,700)+t(130,86,"Read and add events to your calendars",13)+t(130,108,"Maintain access to data you've given",13)+t(130,130,"it access to",13)+button(240,250,"Cancel",w=90,primary=False)+button(340,250,"Accept",hi=True,w=90)
    return [browser(1,"Open our invite","your email",e1),browser(2,"Settings, Calendars, Connections","your Receptly settings",e2),
            browser(3,"Add New, then Outlook","your Receptly settings",e3),browser(4,"Sign in to Microsoft","Microsoft sign-in",e4),
            browser(5,"Click Accept. Done.","Microsoft sign-in",e5)]

# ---------- ServiceM8 ----------
def servicem8():
    side=lambda hi:sidebar(["Dispatch","Clients","Inbox","Reports","Settings"],hi,150)
    a=side(4)+note(180,60,"Your ServiceM8 web app, on a computer")
    b=sidebar(["Business","Staff","Online Booking","API Keys","Add-ons"],3,170,"Settings")
    c=head(24,40,"API Keys")+button(24,60,"+ Add API Key",hi=True,w=150)+field(24,140,300,"Name","Receptly")
    d=head(24,40,"Access")+menu_list(24,60,260,["Read only","Full Access"],1)+note(24,160,"It needs to create clients and jobs")
    e=head(24,40,"Receptly")+keybox(24,90,420)
    return [browser(1,"Open Settings","your ServiceM8 login",a),browser(2,"Click API Keys","your ServiceM8 login",b),
            browser(3,"Add API Key, call it Receptly","your ServiceM8 login",c),browser(4,"Choose Full Access","your ServiceM8 login",d),
            browser(5,"Copy the whole key","your ServiceM8 login",e),send_step(6)]

# ---------- Fergus ----------
def fergus():
    a=sidebar(["Jobs","Schedule","Customers","Quotes","Settings"],4,150)
    b=sidebar(["Company","Users","Integrations"],2,170,"Settings")+menu_list(190,60,220,["Xero","MYOB","Fergus API"],2)
    c=head(24,40,"Fergus API")+t(24,70,"Personal access token",14)+button(24,90,"Generate token",hi=True,w=170)
    d=head(24,40,"Your token")+keybox(24,90,420,"Personal access token")
    return [browser(1,"Open Settings","your Fergus login",a),browser(2,"Integrations, then Fergus API","your Fergus login",b),
            browser(3,"Generate a token","your Fergus login",c),browser(4,"Copy the whole token","your Fergus login",d),send_step(5,"token")]

# ---------- Simpro ----------
def simpro():
    a=sidebar(["Jobs","Quotes","People","System"],3,150)+menu_list(160,128,200,["Setup","System Setup"],1)
    b=head(24,40,"System Setup")
    for i,tb in enumerate(["Defaults","Security","API"]): b+=t(24+i*110,78,tb,14,700 if i==2 else 400)
    b+=hl(234,60,50,26)+menu_list(220,100,200,["Applications","Logs"],0)
    c=head(24,40,"Applications")+button(24,60,"+ Add Application",hi=True,w=180)+field(24,140,300,"Name","Receptly")
    d=head(24,40,"Receptly")+keybox(24,80,440,"Client ID")+keybox(24,160,440,"Client secret")
    return [browser(1,"System, Setup, System Setup","your Simpro login",a),browser(2,"API tab, then Applications","your Simpro login",b),
            browser(3,"Add one, call it Receptly","your Simpro login",c),browser(4,"Copy the ID and secret","your Simpro login",d),
            send_step(5,"details")]

# ---------- AroFlo ----------
def aroflo():
    p1=head(24,40,"New support request")+field(24,80,480,"Subject","Please enable APIv2 on our account")+r(24,130,480,110,"#FFFFFF",G3,1)+t(36,156,"Hi AroFlo support, please enable APIv2 on",13)+t(36,176,"our account. We're connecting Receptly.",13)+button(414,260,"Send",hi=True,w=90)
    p2=head(24,40,"Inbox")+r(24,60,500,60,"#FFFFFF",G3,1)+t(36,84,"AroFlo Support",14,700)+t(36,106,"APIv2 is now enabled on your account",13)+hl(24,60,500,60)
    a=sidebar(["Site Administration","Settings"],1,190,"Admin")
    b=sidebar(["General","AroFlo API"],1,170,"Settings")+menu_list(190,70,180,["APIv1","APIv2"],1)
    c=head(24,40,"APIv2")+button(24,60,"Create Personal Access Token",hi=True,w=270)+keybox(24,150,440,"Personal access token",False)
    return ([browser(1,"Primary contact asks AroFlo","your email",p1),browser(2,"Wait for AroFlo's yes","your email",p2)],
            [browser(1,"Site Administration, Settings","your AroFlo login",a),browser(2,"AroFlo API, then APIv2","your AroFlo login",b),
             browser(3,"Create the token, copy it","your AroFlo login",c),send_step(4,"token")])

# ---------- Tradify ----------
def tradify():
    a=sidebar(["Jobs","Schedule","Customers","Settings"],3,150)+menu_list(160,128,190,["Enquiries","Users"],0)
    b=head(24,40,"Enquiries")+field(24,90,420,"Your enquiries email address","daves-plumbing@enquiries…")+hl(24,90,420,34)
    c=head(24,40,"Give it to us")+t(24,72,"Read it out on the setup call, or email it to",14)+t(24,94,"contact@receptlyai.com.au. It isn't a password.",14)
    d=sidebar(["My profile","Sign out"],0,170,"Your name")
    e=head(24,40,"My profile")+button(24,64,"Connect Google Calendar",hi=True,w=230)+note(24,140,"Sign in with the Google account you shared with us")
    return ([browser(1,"Settings, then Enquiries","your Tradify login",a),browser(2,"Set up the address","your Tradify login",b),browser(3,"Send us the address","",c)],
            [browser(1,"Open your profile","your Tradify login",d),browser(2,"Connect Google Calendar","your Tradify login",e)])
