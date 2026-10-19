"""Shared style + helpers for the Binomial Theorem video."""
from manim import *
import subprocess
import pathlib
from math import comb

ROOT = pathlib.Path(__file__).parent
AUDIO = ROOT / "audio"
LOGO_FILE = ROOT / "assets" / "logo.png"   # drop the channel logo here (png/svg)
CHANNEL_NAME = "Channel Name"              # placeholder until the user provides it

# ---------------------------------------------------------------- style
BG = "#0B1736"          # deep navy blue
config.background_color = BG
BN_FONT = "Noto Serif Bengali"
EN_FONT = "CMU Serif"

A_COL = "#6FC3FF"       # colour for A / a
B_COL = "#FFC857"       # colour for B / b
K_COL = "#FF7A9A"       # coefficients
HL = "#7CFFB2"          # highlight / accents
SOFT = "#9FB3D9"        # secondary text


def bn(s, size=36, **kw):
    return Text(s, font=BN_FONT, font_size=size, **kw)


def en(s, size=36, **kw):
    return Text(s, font=EN_FONT, font_size=size, **kw)


def audio_len(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout
    return float(out.strip())


# ---------------------------------------------------------------- narration sync
class Narrated:
    """Mixin: place a narration clip on the timeline, then schedule animations
    against clip-relative timestamps (seconds)."""

    def clip(self, name):
        path = AUDIO / f"{name}.mp3"
        self.add_sound(str(path))
        self._t0 = self.renderer.time
        self._dur = audio_len(path)

    def now(self):
        return self.renderer.time - self._t0

    def upto(self, t):
        d = t - self.now()
        if d > 1 / 60:
            self.wait(d)

    def playto(self, t, *anims, min_rt=0.25, **kw):
        rt = max(min_rt, t - self.now())
        self.play(*anims, run_time=rt, **kw)

    def at(self, t, *anims, rt=1.0, **kw):
        """wait until t, then play anims for rt seconds."""
        self.upto(t)
        self.play(*anims, run_time=rt, **kw)

    def end_clip(self, pad=0.0):
        self.upto(self._dur + pad)


# ---------------------------------------------------------------- titles
def _frame(scene):
    cam = scene.camera
    if hasattr(cam, "frame"):
        return cam.frame.get_center(), cam.frame.width, cam.frame.height
    return ORIGIN, config.frame_width, config.frame_height


def title_group(title, sub=None, size=76):
    t = en(title, size)
    parts = [t]
    line = Line(LEFT, RIGHT).set_width(max(t.width * 0.9, 3))
    line.set_stroke(width=2).set_color([BG, A_COL, HL, A_COL, BG])
    if sub:
        s = en(sub, 30, color=SOFT)
        grp = VGroup(s, line, t).arrange(DOWN, buff=0.28)
    else:
        grp = VGroup(line, t).arrange(DOWN, buff=0.28)
    return grp, t, line


def chapter_title(scene, title, sub=None, clear_after=True, hold=2.4, dim=0.58):
    """Dim everything already on screen (~0.4 visible), bring the title in at
    the centre with a soft music sting, then either clear the screen
    (clear_after=True) or restore the dimmed objects."""
    center, fw, fh = _frame(scene)
    old = [m for m in scene.mobjects]
    overlay = Rectangle(width=fw + 2, height=fh + 2).move_to(center)
    overlay.set_fill(BG, opacity=dim).set_stroke(width=0)

    grp, t, line = title_group(title, sub)
    grp.move_to(center)
    glow = VGroup(*[t.copy().set_fill(opacity=0).set_stroke(A_COL, width=w, opacity=o)
                    for w, o in ((10, 0.18), (22, 0.08), (36, 0.04))])

    scene.add_sound(str(AUDIO / "music_title.wav"))
    scene.play(FadeIn(overlay), run_time=0.7)
    anims = [
        LaggedStart(*[FadeIn(ch, shift=UP * 0.35, scale=1.4) for ch in t],
                    lag_ratio=0.07, run_time=1.5),
        GrowFromCenter(line, run_time=1.2),
    ]
    if sub:
        anims.append(FadeIn(grp[0], shift=DOWN * 0.25, run_time=1.2))
    scene.play(*anims)
    scene.play(FadeIn(glow), t.animate.set_color(WHITE), run_time=0.8)
    scene.wait(hold)
    scene.play(FadeOut(grp, shift=UP * 0.3), FadeOut(glow, shift=UP * 0.3), run_time=1.0)
    if clear_after:
        scene.play(*[FadeOut(m) for m in old], FadeOut(overlay), run_time=0.8)
    else:
        scene.play(FadeOut(overlay), run_time=0.8)


def pattern_heading(scene, text, size=48):
    """'# Pattern k': appears in the middle (larger), then settles in the UL corner
    at scale 1."""
    h = en(text, size).set_color(HL)
    h_final = h.copy().to_corner(UL, buff=0.45)
    h.scale(1.6).move_to(ORIGIN)
    scene.play(FadeIn(h, scale=0.7), run_time=0.8)
    scene.wait(0.4)
    scene.play(Transform(h, h_final), run_time=1.0)
    return h


# ---------------------------------------------------------------- algebra helpers
def _pw(sym, p):
    if p == 0:
        return None
    return sym if p == 1 else f"{sym}^{{{p}}}"


def expansion_row(n, sym=("a", "b"), coef_col=K_COL, lhs=True):
    """MathTex for (a+b)^n = sum ...  Returns (tex, info) where info holds
    submobject handles: lhs group, eq sign, and per-term dicts
    {'coef': mob|None, 'body': VGroup, 'all': VGroup, 'k': k}."""
    A, B = sym
    parts, roles = [], []
    if lhs:
        parts += ["(", A, "+", B, ")", f"^{{{n}}}", "="]
        roles += ["L", "LA", "L", "LB", "L", "L", "EQ"]
    for k in range(n + 1):
        if k:
            parts.append("+"); roles.append("PLUS")
        c = comb(n, k)
        if c != 1:
            parts.append(str(c)); roles.append(("C", k))
        a = _pw(A, n - k)
        b = _pw(B, k)
        if a:
            parts.append(a); roles.append(("A", k))
        if b:
            parts.append(b); roles.append(("B", k))
        if n == 0:
            parts.append("1"); roles.append(("C", 0))
    tex = MathTex(*parts)
    info = {"lhs": VGroup(), "eq": None, "terms": [], "plus": VGroup()}
    terms = {k: {"coef": None, "body": VGroup(), "all": VGroup(), "k": k} for k in range(n + 1)}
    for mob, r in zip(tex, roles):
        if r in ("L", "LA", "LB"):
            info["lhs"].add(mob)
            if r == "LA": mob.set_color(A_COL)
            if r == "LB": mob.set_color(B_COL)
        elif r == "EQ":
            info["eq"] = mob
        elif r == "PLUS":
            info["plus"].add(mob)
        else:
            kind, k = r
            terms[k]["all"].add(mob)
            if kind == "C":
                terms[k]["coef"] = mob
                mob.set_color(coef_col if n else WHITE)
            else:
                terms[k]["body"].add(mob)
                mob.set_color(A_COL if kind == "A" else B_COL)
    info["terms"] = [terms[k] for k in range(n + 1)]
    info["rhs"] = VGroup(*[m for m in tex if m not in info["lhs"] and m is not info["eq"]])
    return tex, info


def pascal_rows(nrows, dx=0.85, dy=0.8, size=44, color=WHITE):
    rows = VGroup()
    for n in range(nrows):
        row = VGroup(*[MathTex(str(comb(n, k)), font_size=size, color=color) for k in range(n + 1)])
        for k, m in enumerate(row):
            m.move_to(np.array([(k - n / 2) * dx, -n * dy, 0]))
        rows.add(row)
    rows.move_to(ORIGIN)
    return rows
