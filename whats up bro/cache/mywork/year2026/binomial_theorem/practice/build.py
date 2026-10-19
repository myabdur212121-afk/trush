"""Build ~/practice/index.html — a clean, mobile-first reading page of the EXACT
narration text used for the TTS voice (~/project/narration/*.txt)."""
import base64, html, pathlib

HERE = pathlib.Path(__file__).parent
NAR = pathlib.Path('/home/user/project/narration')
BN_DIG = str.maketrans('0123456789', '০১২৩৪৫৬৭৮৯')

PARTS = [
    ("p1", ["s1a", "s1b", "s2", "s3", "s4"], "ভূমিকা", "Intro"),
    ("p2", [f"{i:02d}" for i in range(1, 18)], "Combination", "অধ্যায় ১"),
    ("p3", [f"{i:02d}" for i in range(1, 18)], "Binomial Theorem", "অধ্যায় ২"),
    ("p4", [f"{i:02d}" for i in range(1, 20)], "Pascal's Triangle ও Summary", "অধ্যায় ৩ · সারাংশ"),
]


def font(name):
    return base64.b64encode((HERE / 'fonts' / name).read_bytes()).decode()


def bn(n):
    return str(n).translate(BN_DIG)


tabs, body = [], []
total = 0
for pi, (pre, ids, title, sub) in enumerate(PARTS, 1):
    tabs.append(f'<a href="#part{pi}" data-p="{pi}"><b>{bn(pi)}</b>{html.escape(title)}</a>')
    clips = []
    for ci, i in enumerate(ids, 1):
        cid = f"{pre}_{i}"
        lines = [l.strip() for l in (NAR / f"{cid}.txt").read_text(encoding='utf-8').splitlines() if l.strip()]
        ps = "".join(f"<p>{html.escape(l)}</p>" for l in lines)
        clips.append(
            f'<article class="clip" id="{cid}"><div class="ch"><span class="n">ক্লিপ {bn(f"{ci:02d}")}</span>'
            f'<span class="id">{cid}</span></div><div class="tx">{ps}</div></article>')
        total += 1
    body.append(
        f'<section class="part" id="part{pi}" data-p="{pi}"><header class="ph">'
        f'<div class="pk">Part {pi} <span>·</span> {html.escape(sub)}</div>'
        f'<h2>{html.escape(title)}</h2><div class="pm">{bn(len(ids))}টি ক্লিপ</div></header>'
        + "".join(clips) + '</section>')

page = f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#F4F1EA">
<title>Binomial Theorem — Narration Script</title>
<style>
@font-face{{font-family:"CM";src:url(data:font/woff2;base64,{font('cm-Regular.woff2')}) format("woff2");font-weight:400;unicode-range:U+0020-007E,U+00A0,U+00B7,U+2013-2014,U+2018-201D,U+2026}}
@font-face{{font-family:"CM";src:url(data:font/woff2;base64,{font('cm-Bold.woff2')}) format("woff2");font-weight:600 700;unicode-range:U+0020-007E,U+00A0,U+00B7,U+2013-2014,U+2018-201D,U+2026}}
@font-face{{font-family:"BN";src:url(data:font/woff2;base64,{font('bn-Regular.woff2')}) format("woff2");font-weight:400}}
@font-face{{font-family:"BN";src:url(data:font/woff2;base64,{font('bn-SemiBold.woff2')}) format("woff2");font-weight:600 700}}
:root{{--paper:#F4F1EA;--ink:#151515;--mute:#6E6A62;--rule:#DAD4C8;--card:#FBF9F4;--fs:21px}}
html.dark{{--paper:#141414;--ink:#EEEAE2;--mute:#9A958B;--rule:#2C2B29;--card:#1B1B1A}}
*{{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}}
html{{scroll-behavior:smooth;scroll-padding-top:120px}}
body{{background:var(--paper);color:var(--ink);font-family:"CM","BN",serif;-webkit-text-size-adjust:100%;transition:background .3s,color .3s}}
.top{{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--paper) 92%,transparent);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--rule);padding-top:env(safe-area-inset-top)}}
.bar{{max-width:760px;margin:auto;display:flex;align-items:center;gap:8px;padding:10px 16px 6px}}
.ttl{{flex:1;min-width:0}}
.ttl b{{display:block;font-size:17px;font-weight:700;letter-spacing:.2px}}
.ttl small{{display:block;font-size:12.5px;color:var(--mute);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.bt{{border:1px solid var(--rule);background:var(--card);color:var(--ink);font:600 15px "CM","BN",serif;height:38px;min-width:42px;border-radius:10px;padding:0 10px;cursor:pointer}}
.bt:active{{transform:scale(.95)}}
.tabs{{max-width:760px;margin:auto;display:flex;gap:6px;overflow-x:auto;padding:4px 16px 10px;scrollbar-width:none}}
.tabs::-webkit-scrollbar{{display:none}}
.tabs a{{flex:none;text-decoration:none;color:var(--mute);border:1px solid var(--rule);border-radius:999px;padding:6px 13px;font-size:14px;white-space:nowrap;transition:.2s}}
.tabs a b{{margin-right:6px;font-weight:700}}
.tabs a.on{{background:var(--ink);color:var(--paper);border-color:var(--ink)}}
main{{max-width:760px;margin:auto;padding:8px 16px 90px}}
.ph{{padding:40px 0 14px;border-bottom:2px solid var(--ink);margin-bottom:6px}}
.pk{{font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:var(--mute)}}
.pk span{{margin:0 4px}}
h2{{font-size:30px;font-weight:700;line-height:1.35;margin:4px 0 2px}}
.pm{{font-size:14px;color:var(--mute)}}
.clip{{padding:22px 0 20px;border-bottom:1px solid var(--rule)}}
.ch{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:10px}}
.n{{font-size:14px;font-weight:700;letter-spacing:.3px}}
.id{{font-size:13px;color:var(--mute);letter-spacing:.5px}}
.tx p{{font-size:var(--fs);line-height:1.9;margin:0 0 .55em;padding-left:14px;border-left:2px solid transparent;transition:border-color .2s}}
.tx p:active,.tx p.mk{{border-left-color:var(--ink)}}
.end{{text-align:center;color:var(--mute);font-size:15px;padding:40px 0 10px}}
#up{{position:fixed;right:16px;bottom:calc(18px + env(safe-area-inset-bottom));width:46px;height:46px;border-radius:50%;border:1px solid var(--rule);background:var(--ink);color:var(--paper);font-size:20px;opacity:0;pointer-events:none;transition:.3s;cursor:pointer}}
#up.show{{opacity:.9;pointer-events:auto}}
#sz{{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);background:var(--ink);color:var(--paper);padding:10px 18px;border-radius:12px;font-size:16px;opacity:0;pointer-events:none;transition:opacity .25s;z-index:20}}
#sz.show{{opacity:.92}}
</style>
</head>
<body>
<div class="top">
  <div class="bar">
    <div class="ttl"><b>Narration Script</b><small>Binomial Theorem — সংখ্যাগুলো আসলে কোথা থেকে আসে?</small></div>
    <button class="bt" id="minus" aria-label="ছোট লেখা">A−</button>
    <button class="bt" id="plus" aria-label="বড় লেখা">A+</button>
    <button class="bt" id="theme" aria-label="রং বদল"><svg width="18" height="18" viewBox="0 0 24 24" style="vertical-align:middle"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg></button>
  </div>
  <nav class="tabs">{''.join(tabs)}</nav>
</div>
<main>
{''.join(body)}
<div class="end">— সমাপ্ত · মোট {bn(total)}টি ক্লিপ —</div>
</main>
<button id="up" aria-label="উপরে">↑</button>
<div id="sz"></div>
<script>
(function(){{
  var K='bt_script_v1',st={{}};try{{st=JSON.parse(localStorage.getItem(K))||{{}}}}catch(e){{}}
  function save(){{try{{localStorage.setItem(K,JSON.stringify(st))}}catch(e){{}}}}
  var R=document.documentElement,fs=st.fs||21,sz=document.getElementById('sz'),t;
  function bn(n){{return String(n).replace(/[0-9]/g,function(d){{return '০১২৩৪৫৬৭৮৯'[d]}})}}
  function setFs(v,show){{fs=Math.max(15,Math.min(34,v));R.style.setProperty('--fs',fs+'px');st.fs=fs;save();
    if(show){{sz.textContent='লেখার আকার '+bn(fs);sz.classList.add('show');clearTimeout(t);t=setTimeout(function(){{sz.classList.remove('show')}},700)}}}}
  function setTheme(d){{R.classList.toggle('dark',d);st.dark=d;save();
    document.querySelector('meta[name=theme-color]').content=d?'#141414':'#F4F1EA'}}
  setFs(fs,false);setTheme(!!st.dark);
  document.getElementById('minus').onclick=function(){{setFs(fs-1,true)}};
  document.getElementById('plus').onclick=function(){{setFs(fs+1,true)}};
  document.getElementById('theme').onclick=function(){{setTheme(!R.classList.contains('dark'))}};
  [].forEach.call(document.querySelectorAll('.tabs a'),function(a){{a.onclick=function(e){{e.preventDefault();
    var el=document.querySelector(a.getAttribute('href'));window.scrollTo({{top:el.getBoundingClientRect().top+window.scrollY-110,behavior:'smooth'}})}}}});
  var up=document.getElementById('up');up.onclick=function(){{window.scrollTo({{top:0}})}};
  // tap a line to keep a small marker (where you stopped)
  document.querySelector('main').addEventListener('click',function(e){{var p=e.target.closest('.tx p');if(!p)return;
    var o=document.querySelector('.tx p.mk');if(o&&o!==p)o.classList.remove('mk');p.classList.toggle('mk')}});
  var tabs=[].slice.call(document.querySelectorAll('.tabs a')),parts=[].slice.call(document.querySelectorAll('.part'));
  function onScroll(){{var y=window.scrollY;up.classList.toggle('show',y>600);
    var cur=parts[0];for(var i=0;i<parts.length;i++)if(parts[i].getBoundingClientRect().top<160)cur=parts[i];
    tabs.forEach(function(a){{var on=a.dataset.p===cur.dataset.p;if(on&&!a.classList.contains('on')){{var n=a.parentNode;n.scrollTo({{left:a.offsetLeft-(n.clientWidth-a.offsetWidth)/2,behavior:'smooth'}})}}a.classList.toggle('on',on)}});
    st.y=y;clearTimeout(onScroll.s);onScroll.s=setTimeout(save,300)}}
  window.addEventListener('scroll',onScroll,{{passive:true}});
  if(!location.hash&&st.y)setTimeout(function(){{R.style.scrollBehavior='auto';window.scrollTo(0,st.y);R.style.scrollBehavior='';onScroll()}},60);
  onScroll();
}})();
</script>
</body>
</html>
"""
(HERE / 'index.html').write_text(page, encoding='utf-8')
print(total, 'clips;', round(len(page) / 1024), 'KB')
