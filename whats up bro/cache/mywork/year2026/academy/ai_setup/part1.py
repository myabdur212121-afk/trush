# -*- coding: utf-8 -*-
"""নিরীহ বাঙালি — পর্ব ১ (বই-পাতা + স্যারের বোর্ড লেআউট)
বাঁয়ে justified বইয়ের পাতা + reading bar; ডানে শিক্ষকের বোর্ড।"""
from manim import *

INK="#24231f"; DESK="#d7d0c3"; PAGE="#faf6ec"; MUTED="#6d685e"
ACCENT="#274c3d"; ACCENT2="#9b6239"; LINEC="#b8ad9a"; HL="#f5e6b8"; RED="#a33d2e"; GREEN="#2e6b45"
SERIF="Noto Serif Bengali"

def bn(s,size=24,color=INK,weight=NORMAL):
    return Text(s,font=SERIF,font_size=size,color=color,weight=weight)

_sp={}
def space_w(size):
    if size not in _sp:
        _sp[size]=bn("অ অ",size).width-bn("অঅ",size).width
    return _sp[size]

def make_paragraph(text,width,size=19,color=INK):
    words=[bn(w,size,color) for w in text.split()]
    sw=space_w(size)
    lines=[];cur=[];cur_w=0
    for wm in words:
        add=wm.width if not cur else wm.width+sw
        if cur and cur_w+add>width:
            lines.append(cur);cur=[wm];cur_w=wm.width
        else:
            cur.append(wm);cur_w+=add
    if cur:lines.append(cur)
    out=VGroup()
    for li,ws in enumerate(lines):
        last=(li==len(lines)-1)
        tot=sum(w.width for w in ws)
        gap=(width-tot)/(len(ws)-1) if (not last and len(ws)>1) else sw
        x=0;lg=VGroup()
        for w in ws:
            w.move_to([x+w.width/2,0,0]);x+=w.width+gap;lg.add(w)
        out.add(lg)
    out.arrange(DOWN,buff=0.15,aligned_edge=LEFT)
    return out

# ---------------- মূল টেক্সট (ছবি থেকে হুবহু) ----------------
BIO=("রোকেয়া সাখাওয়াত হোসেন ৯ই ডিসেম্বর, ১৮৮০ খ্রিষ্টাব্দে রংপুর জেলার পায়রাবন্দ গ্রামে জন্মগ্রহণ করেন। "
"তাঁর পিতা জহীরুদ্দিন মোহাম্মদ আবু আলী হায়দার সাবের সম্ভ্রান্ত ভূস্বামী ছিলেন। ছোটবেলায় বড় বোন করিমুন্নেসা "
"বেগম রোকেয়াকে বাংলা শিক্ষায় সাহায্য করেন। পরে তিনি বড় ভাই ইব্রাহিম সাবেরের তত্ত্বাবধানে ইংরেজি শেখেন। "
"বিহারের অন্তর্গত ভাগলপুরের সৈয়দ সাখাওয়াত হোসেনের সঙ্গে বিবাহের পর তিনি বেগম রোকেয়া সাখাওয়াত হোসেন "
"নামে পরিচিত হন। স্বামীর প্রেরণায় তিনি সাহিত্যচর্চা শুরু করেন। সমকালীন মুসলমান সমাজে প্রচলিত কুসংস্কারের "
"বিরুদ্ধে তিনি লেখনী ধারণ করেন। মুসলিম নারী জাগরণে তিনি অগ্রণী ভূমিকায় অবতীর্ণ হন। সাখাওয়াত মেমোরিয়াল "
"গার্লস স্কুল ও আনজুমান-ই-খাওয়াতীন-ই-ইসলাম প্রতিষ্ঠা করে তিনি মুসলমান নারীদের শিক্ষা ও সংস্কৃতির পথে "
"অগ্রসর হতে সাহায্য করেন। পদ্মরাগ, অবরোধবাসিনী, মতিচূর, সুলতানার স্বপ্ন ইত্যাদি তাঁর উল্লেখযোগ্য গ্রন্থ। "
"৯ই ডিসেম্বর, ১৯৩২ খ্রিষ্টাব্দে রোকেয়া সাখাওয়াত হোসেন মৃত্যুবরণ করেন।")

PARA1=("আমরা দুর্বল নিরীহ বাঙালি। এই বাঙালি শব্দে কেমন সুমধুর তরল কোমল ভাব প্রকাশ হয়। আহা! "
"এই অমিয়সিক্ত বাঙালি কোন বিধাতা গড়িয়াছিলেন? কুসুমের সৌকুমার্য, চন্দ্রের চন্দ্রিকা, মধুর মাধুরী, "
"যূথিকার সৌরভ, সুপ্তির নীরবতা, ভূধরের অচলতা, নবনীর কোমলতা, সলিলের তরলতা— এক কথায় "
"বিশ্বজগতের সমুদয় সৌন্দর্য এবং স্নিগ্ধতা লইয়া বাঙালি গঠিত হইয়াছে! আমাদের নামটি যেমন শ্রুতিমধুর "
"তদ্রূপ আমাদের সমুদয় ক্রিয়াকলাপও সহজ ও সরল।")

PARA2=("আমরা মূর্তিমতী কবিতা—যদি ভারতবর্ষকে ইংরেজি ধরনের একটি অট্টালিকা মনে করেন, তবে "
"বঙ্গদেশ তাহার বৈঠকখানা (drawing room) এবং বাঙালি তাহাতে সাজসজ্জা (drawing room suit)! "
"যদি ভারতবর্ষকে একটা সরোবর মনে করেন, তবে বাঙালি তাহাতে পদ্মিনী। যদি ভারতবর্ষকে একখানা "
"উপন্যাস মনে করেন, তবে বাঙালি তাহার নায়িকা! ভারতের পুরুষ সমাজে বাঙালি পুরুষিকা! অতএব "
"আমরা মূর্তিমান কাব্য।")

PAGE_W=6.9; PAGE_H=7.5; TEXT_W=6.2

def book_page(section, paras, sizes, page_label):
    page=RoundedRectangle(corner_radius=0.05,width=PAGE_W,height=PAGE_H,
        fill_color=PAGE,fill_opacity=1,stroke_color=LINEC,stroke_width=2)
    page.to_edge(LEFT,buff=0.25).set_y(0)
    head=bn("নিরীহ বাঙালি",24,ACCENT,BOLD)
    sub=bn("রোকেয়া সাখাওয়াত হোসেন",15,MUTED)
    sec=bn(section,18,ACCENT2,MEDIUM) if section else None
    pgs=[make_paragraph(t,TEXT_W,s) for t,s in zip(paras,sizes)]
    parts=[VGroup(head,sub).arrange(DOWN,buff=0.05)]
    if sec: parts.append(sec)
    parts+=pgs
    body=VGroup(*parts).arrange(DOWN,buff=0.26)
    for p in pgs: p.align_to(body,LEFT)
    if sec: sec.align_to(body,LEFT)
    body.move_to(page).align_to(page,UP).shift(DOWN*0.3)
    no=bn(page_label,12,MUTED).move_to(page.get_bottom()+UP*0.2)
    return VGroup(page,body,no), pgs

def board_title():
    t=bn("স্যারের বোর্ড",23,ACCENT,BOLD)
    sep=Line(ORIGIN,RIGHT*6.0,stroke_color=INK,stroke_width=1.5)
    g=VGroup(t,sep).arrange(DOWN,buff=0.12,aligned_edge=LEFT)
    g.move_to([7.2-6.0/2- (6.95-  (0.25+PAGE_W+0.4)) ,0,0])
    g.to_edge(RIGHT,buff=0.45).align_to([0,3.45,0],UP)
    return g

def vrow(a,b,size=21):
    return VGroup(bn(a,size,ACCENT2,MEDIUM),bn("→",int(size*0.85),MUTED),
                  bn(b,size,GREEN,MEDIUM)).arrange(RIGHT,buff=0.18)

def redline(t,size=19):
    m=bn(t,size,RED,MEDIUM)
    if m.width>6.1: m.scale_to_fit_width(6.1)
    return m

def qbox(lines,w=6.15):
    title=bn("প্রশ্ন-পয়েন্ট:",18,ACCENT,BOLD)
    items=[bn(l,16.5,INK) for l in lines]
    for it in items:
        if it.width>w-0.5: it.scale_to_fit_width(w-0.5)
    g=VGroup(title,*items).arrange(DOWN,buff=0.11,aligned_edge=LEFT)
    bg=RoundedRectangle(corner_radius=0.08,width=w,height=g.height+0.4,
        fill_color=HL,fill_opacity=1,stroke_color=ACCENT2,stroke_width=1.4)
    g.move_to(bg).align_to(bg,LEFT).shift(RIGHT*0.22)
    return VGroup(bg,g)

class P1(Scene):
    T=30.0
    def construct(self):
        self.camera.background_color=DESK
        self.el=0.0
        self.body()
        pad=self.T-self.el
        if pad>0:self.wait(pad)
    def p(self,*a,rt=0.7):
        self.play(*a,run_time=rt);self.el+=rt
    def w(self,t):
        if t>0:self.wait(t);self.el+=t
    def upto(self,t):
        self.w(t-self.el)
    # reading: lines-এর ওপর bar/highlight চালানো
    def read_lines(self, lines, t_start, t_end):
        weights=[sum(len(w.text) for w in lg) for lg in lines]
        total=sum(weights)
        span=t_end-t_start
        cur=lines[0]
        hl=SurroundingRectangle(cur,fill_color=HL,fill_opacity=0.55,stroke_width=0,buff=0.04)
        bar=Rectangle(width=cur.width+0.1,height=0.055,fill_color=ACCENT2,fill_opacity=1,stroke_width=0)
        bar.next_to(cur,DOWN,buff=0.03)
        self.upto(t_start)
        self.p(FadeIn(hl),FadeIn(bar),rt=0.3)
        self.bring_to_back(hl)
        t=t_start
        for i,lg in enumerate(lines):
            dur=span*weights[i]/total
            t+=dur
            if i<len(lines)-1:
                nxt=lines[i+1]
                nhl=SurroundingRectangle(nxt,fill_color=HL,fill_opacity=0.55,stroke_width=0,buff=0.04)
                nbar=Rectangle(width=nxt.width+0.1,height=0.055,fill_color=ACCENT2,fill_opacity=1,stroke_width=0)
                nbar.next_to(nxt,DOWN,buff=0.03)
                self.upto(t-0.25)
                self.p(Transform(hl,nhl),Transform(bar,nbar),rt=0.25)
                self.bring_to_back(hl)
        self.upto(t_end)
        self.p(FadeOut(hl),FadeOut(bar),rt=0.4)

# ---------------------------------------------------------------- S1 ভূমিকা
class P1S01(P1):
    T=37.9
    def body(self):
        t1=bn("নিরীহ বাঙালি",58,ACCENT,BOLD)
        t2=bn("রোকেয়া সাখাওয়াত হোসেন",30,INK)
        t3=bn("পর্ব ১ — লেখক-পরিচিতি ও গল্পের শুরু",22,ACCENT2)
        g=VGroup(t1,t2,t3).arrange(DOWN,buff=0.3).move_to(UP*1.6)
        self.p(FadeIn(t1,shift=UP*0.2),rt=1.0)
        self.upto(2.0);self.p(FadeIn(t2),rt=0.7)
        # লেআউট ব্যাখ্যা
        pg=RoundedRectangle(corner_radius=0.06,width=2.6,height=2.6,fill_color=PAGE,fill_opacity=1,stroke_color=LINEC,stroke_width=2)
        pl=VGroup(*[Line(ORIGIN,RIGHT*2.0,stroke_color=MUTED,stroke_width=2) for _ in range(4)]).arrange(DOWN,buff=0.3).move_to(pg)
        bar=Rectangle(width=2.0,height=0.06,fill_color=ACCENT2,fill_opacity=1,stroke_width=0).move_to(pl[1]).shift(DOWN*0.14)
        lab1=bn("বইয়ের পাতা",19,ACCENT,MEDIUM).next_to(pg,DOWN,buff=0.15)
        left=VGroup(pg,pl,bar,lab1).move_to(LEFT*2.9+DOWN*1.3)
        bd=RoundedRectangle(corner_radius=0.06,width=2.6,height=2.6,fill_color="#ece5d4",fill_opacity=1,stroke_color=ACCENT,stroke_width=2)
        bl=VGroup(bn("শব্দার্থ",16,GREEN,MEDIUM),bn("ব্যাখ্যা",16,RED,MEDIUM),bn("★★★ প্রশ্ন",16,ACCENT2,MEDIUM)).arrange(DOWN,buff=0.25).move_to(bd)
        lab2=bn("স্যারের বোর্ড",19,ACCENT,MEDIUM).next_to(bd,DOWN,buff=0.15)
        right=VGroup(bd,bl,lab2).move_to(RIGHT*2.9+DOWN*1.3)
        self.upto(7.0);self.p(FadeIn(left,shift=UP*0.15),rt=0.8)
        self.upto(13.0);self.p(FadeIn(right,shift=UP*0.15),rt=0.8)
        legend=bn("★ সাধারণ    ★★ গুরুত্বপূর্ণ    ★★★ পরীক্ষার জন্য অবশ্যই",20,INK,MEDIUM).move_to(DOWN*3.2)
        self.upto(20.0);self.p(FadeIn(legend),rt=0.7)
        self.upto(30.0);self.p(FadeIn(t3),rt=0.7)

# ---------------------------------------------------------------- S2 লেখক-পরিচিতি পড়া
class P1S02(P1):
    T=71.1
    def body(self):
        grp,pgs=book_page("লেখক-পরিচিতি",[BIO],[17],"পৃষ্ঠা ৩৮")
        bt=board_title()
        note=bn("মন দিয়ে শোনো — বই খুলে সাথে মেলাও",17,MUTED).next_to(bt,DOWN,buff=0.35).align_to(bt,LEFT)
        self.p(FadeIn(grp,shift=RIGHT*0.2),FadeIn(bt),rt=0.9)
        self.p(FadeIn(note),rt=0.4)
        self.read_lines(list(pgs[0]),3.0,self.T-1.2)

# ---------------------------------------------------------------- S3 লেখক-পরিচিতি বোর্ড
class P1S03(P1):
    T=59.9
    def body(self):
        grp,pgs=book_page("লেখক-পরিচিতি",[BIO],[17],"পৃষ্ঠা ৩৮")
        grp[1].set_opacity(0.45)
        bt=board_title()
        self.add(grp,bt)
        items=[]
        r1=VGroup(bn("১. জন্ম: ৯ই ডিসে. ১৮৮০ · পায়রাবন্দ, রংপুর",19,INK),
                  bn("   মৃত্যু: ৯ই ডিসে. ১৯৩২",19,INK)).arrange(DOWN,buff=0.06,aligned_edge=LEFT)
        c1=qbox(["★★★ জন্ম-মৃত্যু একই তারিখ! — MCQ · সংক্ষিপ্ত · ক"])
        r2=bn("২. বাংলা: বোন করিমুন্নেসা · ইংরেজি: ভাই ইব্রাহিম সাবের",17.5,INK)
        r2b=redline("উল্টে দিয়ে ভুল অপশন হয় — সাবধান! ★★",17)
        r3=bn("৩. গ্রন্থ: পদ্মরাগ · অবরোধবাসিনী · মতিচূর · সুলতানার স্বপ্ন",17,INK)
        r3b=redline("‘কোনটি তাঁর রচনা নয়’ — MCQ ★★★",17)
        r4=bn("৪. প্রতিষ্ঠান: সাখা. মেমো. গার্লস স্কুল · আনজুমান-ই-খাওয়াতীন-ই-ইসলাম",15.5,INK)
        r5=bn("৫. মুসলিম নারী জাগরণের অগ্রণী — খ ★★",17.5,INK)
        col=VGroup(r1,c1,r2,r2b,r3,r3b,r4,r5).arrange(DOWN,buff=0.2,aligned_edge=LEFT)
        for m in col:
            if m.width>6.2: m.scale_to_fit_width(6.2)
        col.next_to(bt,DOWN,buff=0.3).align_to(bt,LEFT)
        times=[4.0,12.5,20.0,25.5,30.5,36.0,41.5,48.0]
        for m,t in zip(col,times):
            self.upto(t);self.p(FadeIn(m,shift=UP*0.1),rt=0.55)

# ---------------------------------------------------------------- S4 প্যারা-১ পড়া
class P1S04(P1):
    T=45.7
    def body(self):
        grp,pgs=book_page(None,[PARA1,PARA2],[19,19],"পৃষ্ঠা ৩৮")
        bt=board_title()
        self.p(FadeIn(grp,shift=RIGHT*0.2),FadeIn(bt),rt=0.9)
        self.read_lines(list(pgs[0]),4.5,self.T-1.0)

# ---------------------------------------------------------------- S5 প্যারা-১ বোর্ড
class P1S05(P1):
    T=58.6
    def body(self):
        grp,pgs=book_page(None,[PARA1,PARA2],[19,19],"পৃষ্ঠা ৩৮")
        pgs[1].set_opacity(0.35)
        bt=board_title()
        self.add(grp,bt)
        rows=VGroup(
            vrow("সৌকুমার্য","সৌন্দর্য",19),vrow("চন্দ্রিকা","জ্যোৎস্না",19),
            vrow("যূথিকা","জুঁই ফুল",19),vrow("ভূধর","পর্বত",19),
            vrow("নবনী","মাখন",19),vrow("সলিল","পানি",19),
            vrow("অমিয়সিক্ত","অমৃতে ভেজানো",19),
        ).arrange(DOWN,buff=0.12,aligned_edge=LEFT)
        vb=VGroup(redline("ভাবার্থ: প্রশংসা নয় — খোঁচা!",19),
                  bn("কোমলতা = দুর্বলতা · অলসতা · তেজহীনতা",17,INK)).arrange(DOWN,buff=0.07,aligned_edge=LEFT)
        qb=qbox(["★★★ শব্দার্থ — MCQ · সংক্ষিপ্ত · ক",
                 "★★ ‘ভূধরের অচলতা’ কী বোঝায় — খ",
                 "★ প্রথম লাইন: ‘আমরা দুর্বল নিরীহ বাঙালি’"])
        col=VGroup(rows,vb,qb).arrange(DOWN,buff=0.28,aligned_edge=LEFT)
        col.next_to(bt,DOWN,buff=0.28).align_to(bt,LEFT)
        for i,t in enumerate([3.5,6.5,9.5,12.0,14.5,17.0,20.0]):
            self.upto(t);self.p(FadeIn(rows[i],shift=UP*0.08),rt=0.45)
        self.upto(27.0);self.p(FadeIn(vb,shift=UP*0.1),rt=0.6)
        self.upto(40.0);self.p(FadeIn(qb,scale=1.03),rt=0.7)

# ---------------------------------------------------------------- S6 প্যারা-২ পড়া
class P1S06(P1):
    T=37.3
    def body(self):
        grp,pgs=book_page(None,[PARA1,PARA2],[19,19],"পৃষ্ঠা ৩৮")
        pgs[0].set_opacity(0.35)
        bt=board_title()
        self.add(grp,bt)
        self.read_lines(list(pgs[1]),2.5,self.T-1.0)

# ---------------------------------------------------------------- S7 প্যারা-২ বোর্ড
class P1S07(P1):
    T=59.5
    def body(self):
        grp,pgs=book_page(None,[PARA1,PARA2],[19,19],"পৃষ্ঠা ৩৮")
        pgs[0].set_opacity(0.35)
        bt=board_title()
        self.add(grp,bt)
        rows=VGroup(
            vrow("অট্টালিকা → বৈঠকখানা","সাজসজ্জা (drawing room suit)",17),
            vrow("সরোবর","বাঙালি পদ্মিনী",19),
            vrow("উপন্যাস","বাঙালি নায়িকা",19),
            vrow("পুরুষ সমাজ","বাঙালি পুরুষিকা!",19),
        ).arrange(DOWN,buff=0.13,aligned_edge=LEFT)
        ins=redline("সব উপমাই নারীবাচক ও শোভার — দেখতে সুন্দর, কাজের নয়!",16.5)
        con=bn("∴ আমরা মূর্তিমান কাব্য",23,ACCENT,BOLD)
        conbox=RoundedRectangle(corner_radius=0.08,width=con.width+0.5,height=con.height+0.35,
            fill_color=HL,fill_opacity=1,stroke_color=ACCENT2,stroke_width=1.5)
        cong=VGroup(conbox,con.move_to(conbox))
        qb=qbox(["★★★ কাকে ‘মূর্তিমান কাব্য’? — বাঙালিকে (বইয়ের MCQ)",
                 "★★★ কেন বলেছেন? — খ (বইয়ের CQ)",
                 "★★ ‘পুরুষিকা’-র ইঙ্গিত — খ · গ",
                 "★★ drawing room suit — সংক্ষিপ্ত"])
        col=VGroup(rows,ins,cong,qb).arrange(DOWN,buff=0.24,aligned_edge=LEFT)
        for m in col:
            if m.width>6.25: m.scale_to_fit_width(6.25)
        col.next_to(bt,DOWN,buff=0.28).align_to(bt,LEFT)
        for i,t in enumerate([3.0,9.0,12.5,15.5]):
            self.upto(t);self.p(FadeIn(rows[i],shift=UP*0.08),rt=0.5)
        self.upto(21.0);self.p(FadeIn(ins,shift=UP*0.1),rt=0.6)
        self.upto(28.5);self.p(FadeIn(cong,scale=1.05),rt=0.7)
        self.upto(34.0);self.p(FadeIn(qb,scale=1.03),rt=0.7)

# ---------------------------------------------------------------- S8 রিক্যাপ
class P1S08(P1):
    T=27.4
    def body(self):
        t=bn("পর্ব ১ শেষ!",46,ACCENT,BOLD).move_to(UP*2.4)
        self.p(FadeIn(t,scale=1.1),rt=0.8)
        items=VGroup(
            bn("✓ লেখক-পরিচিতির পরীক্ষা-পয়েন্ট",24,INK),
            bn("✓ প্রথম দুই অনুচ্ছেদ + ৭টি শব্দার্থ",24,INK),
            bn("✓ ‘মূর্তিমান কাব্য’-এর আসল মানে",24,INK),
        ).arrange(DOWN,buff=0.3,aligned_edge=LEFT).move_to(UP*0.5)
        for i,tt in enumerate([3.5,6.5,10.0]):
            self.upto(tt);self.p(FadeIn(items[i],shift=UP*0.1),rt=0.5)
        nxt=bn("পরের পর্বে: খাদ্য · পোশাক · বাণিজ্য · পাস বিক্রয়",23,ACCENT2,MEDIUM)
        nb=RoundedRectangle(corner_radius=0.1,width=nxt.width+0.6,height=nxt.height+0.45,
            fill_color=HL,fill_opacity=1,stroke_color=ACCENT2,stroke_width=1.5)
        g=VGroup(nb,nxt.move_to(nb)).move_to(DOWN*1.6)
        self.upto(15.5);self.p(FadeIn(g,shift=UP*0.15),rt=0.8)
        bye=bn("দেখা হবে পর্ব ২-এ — আল্লাহ হাফেজ!",22,MUTED).move_to(DOWN*3.0)
        self.upto(21.5);self.p(FadeIn(bye),rt=0.6)
