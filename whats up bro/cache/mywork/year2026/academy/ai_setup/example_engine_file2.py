# -*- coding: utf-8 -*-
"""পল্লিসাহিত্য — সাধারণ ইঞ্জিন মডিউল (সব পর্বে পুনর্ব্যবহৃত হবে)
- পাতার মূল টেক্সট (reading) = LaTeX (XeLaTeX+polyglossia bengali) flowing paragraph
- বোর্ড আলোচনা (explanation) = Manim Text()/bn() — vrow, redline, qbox, qpanel (MCQ/Short/CQ ব্যাজ)
- প্রতিটি অনুচ্ছেদ ২-৩ সেগমেন্টে ভেঙে read(lines)+discuss(board) চক্র; অন্য অংশ আবছা (opacity~0.4)
"""
import re
from manim import *

INK = "#24231f"; DESK = "#d7d0c3"; PAGE = "#faf6ec"; MUTED = "#6d685e"
ACCENT = "#274c3d"; ACCENT2 = "#9b6239"; LINEC = "#b8ad9a"; HL = "#f5e6b8"
RED = "#a33d2e"; GREEN = "#2e6b45"; BLUE = "#2b5f8a"; PURPLE = "#6a3d8f"
SERIF = "Noto Serif Bengali"


# ================================================================== বোর্ড টেক্সট ইঞ্জিন (Text())
def bn(s, size=24, color=INK, weight=NORMAL):
    return Text(s, font=SERIF, font_size=size, color=color, weight=weight)


def bn_wrap(s, size=16, color=INK, weight=NORMAL, max_w=6.1, line_buff=0.08):
    """লম্বা বাক্যকে শব্দ-ভিত্তিক wrap করে একাধিক লাইনের VGroup বানায়।"""
    words = s.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        test = bn(trial, size, color, weight)
        if test.width > max_w and cur:
            lines.append(bn(cur, size, color, weight))
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(bn(cur, size, color, weight))
    return VGroup(*lines).arrange(DOWN, buff=line_buff, aligned_edge=LEFT)


def vrow(a, b, size=21, max_w=6.0):
    left = bn_wrap(a, size, ACCENT2, MEDIUM, max_w=max_w * 0.42)
    arrow = bn("→", int(size * 0.85), MUTED)
    right = bn_wrap(b, size, GREEN, MEDIUM, max_w=max_w * 0.48)
    return VGroup(left, arrow, right).arrange(RIGHT, buff=0.18)


def redline(t, size=19, max_w=6.1):
    return bn_wrap(t, size, RED, MEDIUM, max_w=max_w)


def qbox(lines, w=6.15, title="প্রশ্ন-পয়েন্ট:"):
    title_m = bn(title, 18, ACCENT, BOLD)
    items = [bn_wrap(l, 15.5, INK, max_w=w - 0.5) for l in lines]
    g = VGroup(title_m, *items).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    bg = RoundedRectangle(corner_radius=0.08, width=w, height=g.height + 0.4,
                           fill_color=HL, fill_opacity=1, stroke_color=ACCENT2, stroke_width=1.4)
    g.move_to(bg).align_to(bg, LEFT).shift(RIGHT * 0.22)
    return VGroup(bg, g)


def board_title():
    t = bn("স্যারের বোর্ড", 23, ACCENT, BOLD)
    sep = Line(ORIGIN, RIGHT * 6.0, stroke_color=INK, stroke_width=1.5)
    g = VGroup(t, sep).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    g.to_edge(RIGHT, buff=0.45).align_to([0, 3.45, 0], UP)
    return g


# ------- প্রশ্ন-ধরন ব্যাজ (MCQ / Short / CQ) -------
TAG_COLORS = {"MCQ": BLUE, "SHORT": GREEN, "CQ": PURPLE}
TAG_LABELS = {"MCQ": "MCQ", "SHORT": "সংক্ষিপ্ত", "CQ": "সৃজনশীল (ক-খ-গ-ঘ)"}


def qtag(kind):
    color = TAG_COLORS.get(kind, MUTED)
    label = TAG_LABELS.get(kind, kind)
    t = bn(label, 14, WHITE, BOLD)
    bg = RoundedRectangle(corner_radius=0.06, width=t.width + 0.28, height=t.height + 0.16,
                           fill_color=color, fill_opacity=1, stroke_width=0)
    t.move_to(bg)
    return VGroup(bg, t)


def qline(tag_kind, text, size=15.5, w=5.5):
    tg = qtag(tag_kind)
    txt = bn_wrap(text, size, INK, max_w=w)
    row = VGroup(tg, txt).arrange(RIGHT, buff=0.15, aligned_edge=UP)
    return row


def qpanel(items, w=6.15, title="সম্ভাব্য প্রশ্ন:"):
    """items: list of (tag_kind, text)।"""
    title_m = bn(title, 18, ACCENT, BOLD)
    rows = [qline(k, t, w=w - 1.7) for k, t in items]
    g = VGroup(title_m, *rows).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    bg = RoundedRectangle(corner_radius=0.08, width=w, height=g.height + 0.4,
                           fill_color=HL, fill_opacity=1, stroke_color=ACCENT2, stroke_width=1.4)
    g.move_to(bg).align_to(bg, LEFT).shift(RIGHT * 0.22)
    return VGroup(bg, g)


# ================================================================== পাতার মূল টেক্সট ইঞ্জিন (LaTeX)
BENGALI_PREAMBLE = r"""
\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{bengali}
\setmainfont{Noto Serif Bengali}[
  UprightFont = *-Regular,
  BoldFont = *-Bold,
]
\newfontfamily\latinfont{Noto Serif}
\usepackage{xcolor}
\usepackage{ragged2e}
\setlength{\parindent}{0pt}
\AtBeginDocument{%
  \righthyphenmin=62\lefthyphenmin=62
  \hyphenpenalty=10000\exhyphenpenalty=10000
  \tolerance=9999\emergencystretch=3em
}
"""


def latin(text):
    """ইংরেজি/লাতিন অংশকে সঠিক ফন্টে রেন্ডার করতে wrap করে (polyglossia bengali-তে glyph miss হয়)।"""
    return r"{\latinfont %s}" % text


bn_template = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv",
    documentclass="\\documentclass[preview]{standalone}",
    preamble=BENGALI_PREAMBLE,
)

MINIPAGE_IN = 6.2
UNITS_PER_IN = 3.6
TARGET_TEXT_W = 6.2
FIXED_SCALE = TARGET_TEXT_W / (MINIPAGE_IN * UNITS_PER_IN)


def tex_raw(latex_body, scale=FIXED_SCALE, color=INK):
    t = Tex(latex_body, tex_template=bn_template, color=color)
    t.scale(scale)
    return t


def latex_inline(text, size=15, color=INK, bold=False):
    inner = r"\textbf{%s}" % text if bold else text
    latex = r"\fontsize{%s}{%s}\selectfont %s" % (size, size * 1.3, inner)
    return tex_raw(latex, color=color)


def latex_paragraph(text, size=14, leading=21, color=INK, width_in=MINIPAGE_IN):
    """পুরো অনুচ্ছেদ একটাই flowing LaTeX ব্লক (স্বাভাবিক প্যারাগ্রাফ, বাক্য জোর করে ভাঙা হয় না)।"""
    latex = (r"\begin{minipage}{%sin}\fontsize{%s}{%s}\selectfont\justifying %s\end{minipage}"
              % (width_in, size, leading, text))
    mobj = tex_raw(latex, color=color)
    line_h_units = (leading / 72.27) * FIXED_SCALE
    return mobj, line_h_units


def cluster_into_lines(mobj, line_h_units):
    """glyph-গুলোকে তাদের y-অবস্থান অনুযায়ী প্রকৃত রেন্ডার-লাইনে ভাগ করে (চূড়ান্ত scale/position-এর পরে)।"""
    fam = mobj.family_members_with_points()
    if not fam:
        return [mobj]
    buckets = {}
    for m in fam:
        y = m.get_center()[1]
        key = round(y / line_h_units)
        buckets.setdefault(key, []).append(m)
    lines = []
    for k in sorted(buckets.keys(), reverse=True):
        lines.append(VGroup(*buckets[k]))
    return lines


# ================================================================== পাতার লেআউট
PAGE_W = 6.9; PAGE_H = 7.5; TEXT_W = 6.2


def book_page(head_title, sub_title, section, paragraphs, sizes, page_label):
    page = RoundedRectangle(corner_radius=0.05, width=PAGE_W, height=PAGE_H,
                             fill_color=PAGE, fill_opacity=1, stroke_color=LINEC, stroke_width=2)
    page.to_edge(LEFT, buff=0.25).set_y(0)

    head = latex_inline(head_title, size=24, color=ACCENT, bold=True)
    sub = latex_inline(sub_title, size=15, color=MUTED)
    headg = VGroup(head, sub).arrange(DOWN, buff=0.05)
    sec = latex_inline(section, size=18, color=ACCENT2, bold=True) if section else None

    para_mobjs = []
    line_heights = []
    parts = [headg]
    if sec:
        parts.append(sec)
    for text, size in zip(paragraphs, sizes):
        pg, lh = latex_paragraph(text, size=size, leading=size * 1.5)
        para_mobjs.append(pg)
        line_heights.append(lh)
        parts.append(pg)

    body = VGroup(*parts).arrange(DOWN, buff=0.24)
    for pg in para_mobjs:
        pg.align_to(body, LEFT)
    if sec:
        sec.align_to(body, LEFT)
    scale_factor_w = TEXT_W / body.width
    body.scale(scale_factor_w)
    max_h = PAGE_H - 1.0
    scale_factor_h = 1.0
    if body.height > max_h:
        scale_factor_h = max_h / body.height
        body.scale(scale_factor_h)
    total_scale = scale_factor_w * scale_factor_h
    body.move_to(page).align_to(page, UP).shift(DOWN * 0.25)

    para_data = []
    for pg, lh in zip(para_mobjs, line_heights):
        final_lh = lh * total_scale
        lines = cluster_into_lines(pg, final_lh)
        para_data.append((pg, lines))

    no = latex_inline(page_label, size=12, color=MUTED).move_to(page.get_bottom() + UP * 0.2)

    page_group = VGroup(page, body, no)
    return page_group, para_data


def segment_ranges(n_lines, n_segments):
    """n_lines-কে n_segments ভাগে (প্রায়) সমান ভাগ করে [(start,end), ...] রিটার্ন করে।"""
    n_segments = max(1, min(n_segments, n_lines))
    base = n_lines // n_segments
    rem = n_lines % n_segments
    ranges = []
    start = 0
    for i in range(n_segments):
        size = base + (1 if i < rem else 0)
        end = start + size
        ranges.append((start, end))
        start = end
    return ranges


def dim_except(lines, keep_start, keep_end, keep_opacity=1.0, dim_opacity=0.4):
    anims = []
    for i, ln in enumerate(lines):
        target = keep_opacity if keep_start <= i < keep_end else dim_opacity
        anims.append(ln.animate.set_opacity(target))
    return anims


# ================================================================== Scene বেস
class BaseScene(Scene):
    T = 30.0

    def construct(self):
        self.camera.background_color = DESK
        self.el = 0.0
        self.body()
        pad = self.T - self.el
        if pad > 0:
            self.wait(pad)

    def p(self, *a, rt=0.7):
        self.play(*a, run_time=rt)
        self.el += rt

    def w(self, t):
        if t > 0:
            self.wait(t)
            self.el += t

    def upto(self, t):
        self.w(t - self.el)

    def read_lines(self, blocks, t_start, t_end):
        weights = [max(len(b.family_members_with_points()), 1) for b in blocks]
        total = sum(weights) or 1
        span = t_end - t_start
        cur = blocks[0]
        hl = SurroundingRectangle(cur, fill_color=HL, fill_opacity=0.55, stroke_width=0, buff=0.04)
        bar = Rectangle(width=cur.width + 0.1, height=0.04, fill_color=ACCENT2, fill_opacity=1, stroke_width=0)
        bar.next_to(cur, DOWN, buff=0.02)
        self.upto(t_start)
        self.p(FadeIn(hl), FadeIn(bar), rt=0.3)
        self.bring_to_back(hl)
        t = t_start
        for i, b in enumerate(blocks):
            dur = span * weights[i] / total
            t += dur
            if i < len(blocks) - 1:
                nxt = blocks[i + 1]
                nhl = SurroundingRectangle(nxt, fill_color=HL, fill_opacity=0.55, stroke_width=0, buff=0.04)
                nbar = Rectangle(width=nxt.width + 0.1, height=0.04, fill_color=ACCENT2, fill_opacity=1, stroke_width=0)
                nbar.next_to(nxt, DOWN, buff=0.02)
                self.upto(t - 0.2)
                self.p(Transform(hl, nhl), Transform(bar, nbar), rt=0.2)
                self.bring_to_back(hl)
        self.upto(t_end)
        self.p(FadeOut(hl), FadeOut(bar), rt=0.4)


def segment_scene_factory(page_kwargs_fn, n_segments, seg_index, read_dur, discuss_dur,
                           discuss_builder):
    """একটি generic segment scene ক্লাস তৈরি করে।
    page_kwargs_fn: () -> dict (book_page আর্গুমেন্ট) — প্রতিবার নতুন mobject বানাতে function হিসেবে
    discuss_builder: () -> VGroup (বোর্ডের কন্টেন্ট, নিজেই arrange করা)
    """
    total_t = read_dur + discuss_dur + 1.6

    class _Seg(BaseScene):
        T = total_t

        def body(self):
            page_group, para_data = book_page(**page_kwargs_fn())
            _, lines = para_data[0]
            ranges = segment_ranges(len(lines), n_segments)
            s0, s1 = ranges[seg_index]
            bt = board_title()
            self.p(FadeIn(page_group, shift=RIGHT * 0.2), FadeIn(bt), rt=0.8)
            if seg_index > 0:
                for i, ln in enumerate(lines):
                    if i < s0:
                        ln.set_opacity(0.4)
            self.upto(1.0)
            self.read_lines(lines[s0:s1], 1.0, 1.0 + read_dur)
            self.p(*dim_except(lines, s0, s1), rt=0.5)

            board_content = discuss_builder()
            board_content.next_to(bt, DOWN, buff=0.32).align_to(bt, LEFT)
            for m in board_content:
                if hasattr(m, "width") and m.width > 6.25:
                    m.scale_to_fit_width(6.25)

            t0 = self.el
            n_items = len(board_content)
            remain = self.T - 0.5 - t0
            per = max(remain / max(n_items, 1), 0.3)
            t = t0
            for m in board_content:
                self.upto(t)
                self.p(FadeIn(m, shift=UP * 0.1), rt=min(0.6, per * 0.6))
                t += per
            self.upto(self.T - 0.4)

    return _Seg
  
