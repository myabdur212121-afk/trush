from manim import *
import random, time, math
from pathlib import Path

# Helper functions/classes are imported from this file.
# Keep buffons_needle_intro.py in the same folder.
from buffons_needle_intro import btext, etext, caption, silver_needle, make_table, needle_drop_anims

config.background_color = "#5a321d"

# ============================================================
# ANIMATION ONLY VERSION
# ============================================================
# This file does NOT require any audio files.
# Wherever audio/caption was used, I kept commented lines with '#'.
# Later, if you want to use your own voice/captions:
#   1. Put your audio files in a folder, for example: audio/my_voice/seg_01.mp3
#   2. Uncomment the relevant self.add_sound(...) lines.
#   3. Uncomment caption(...) / self.play(FadeIn(cap)) / self.change_caption(...) lines if needed.
# ============================================================


def make_a4_paper(width=4.45, line_gap=0.82, line_count=8):
    height = width * 1.414
    shadow = RoundedRectangle(width=width, height=height, corner_radius=0.025, stroke_width=0,
                              fill_color=BLACK, fill_opacity=0.24)
    shadow.shift(0.13 * DOWN + 0.13 * RIGHT)
    shadow.set_z_index(5)

    paper = RoundedRectangle(width=width, height=height, corner_radius=0.025,
                             stroke_color="#d8dde0", stroke_width=1.6,
                             fill_color="#eef9ff", fill_opacity=1)
    paper.set_z_index(6)

    lines = VGroup()
    ys = []
    start_y = paper.get_top()[1] - 0.65
    for i in range(line_count):
        y = start_y - i * line_gap
        if y < paper.get_bottom()[1] + 0.42:
            continue
        line = Line([paper.get_left()[0] + 0.06, y, 0], [paper.get_right()[0] - 0.06, y, 0])
        line.set_stroke("#13242c", width=1.9, opacity=0.92)
        line.set_z_index(12)
        lines.add(line)
        ys.append(y)
    return VGroup(shadow, paper, lines), paper, lines, ys


def random_landings(rng, paper, count, min_dist=0.38, margin=0.62, length_range=(1.05, 1.30)):
    pts = []
    attempts = 0
    while len(pts) < count and attempts < 6000:
        attempts += 1
        length = rng.uniform(*length_range)
        angle = rng.uniform(-math.pi, math.pi)
        x = rng.uniform(paper.get_left()[0] + margin, paper.get_right()[0] - margin)
        y = rng.uniform(paper.get_bottom()[1] + margin, paper.get_top()[1] - margin)
        if all(math.hypot(x - px, y - py) > min_dist for px, py, _, _ in pts):
            pts.append((x, y, angle, length))
    return pts


class BuffonsNeedleAnimationOnly(ThreeDScene):
    def construct(self):
        seed = time.time_ns()
        rng = random.Random(seed)
        print("Random seed:", seed)

        self.set_camera_orientation(phi=0, theta=-PI/2, zoom=1.0)
        table = make_table()
        self.add(table)

        # ============================================================
        # 1. Hook experiment
        # ============================================================
        # self.add_sound("audio/my_voice/seg_01.mp3")
        # cap = caption("গত সপ্তাহে আমি একটা ছোট্ট এক্সপেরিমেন্ট করেছিলাম।", 28)

        paper_group, paper, lines, line_ys = make_a4_paper(width=4.45, line_gap=0.86, line_count=8)
        paper_group.move_to(ORIGIN)
        self.play(FadeIn(paper_group, shift=0.18 * UP), run_time=0.65)
        # self.play(FadeIn(cap), run_time=0.25)

        hook_landings = random_landings(rng, paper, 15, min_dist=0.43, margin=0.68, length_range=(1.06, 1.30))
        hook_needles, hook_anims = needle_drop_anims(self, rng, hook_landings, z_base=100, bounce=0.075)
        self.play(AnimationGroup(*hook_anims, lag_ratio=0), run_time=1.15)
        self.wait(0.45)

        # ============================================================
        # 2. Pi reveal
        # ============================================================
        # self.add_sound("audio/my_voice/seg_02.mp3")
        # cap = self.change_caption(cap, "এই এক্সপেরিমেন্টে আমি π-এর মান বের করেছি।", 27)

        experiment_group = VGroup(paper_group, *hook_needles)
        self.play(experiment_group.animate.shift(LEFT * 2.35).scale(0.82), run_time=0.75)

        pi_symbol = MathTex(r"\pi", font_size=124, color="#ffe082")
        pi_value = MathTex(r"\pi \approx 3.14159", font_size=44, color="#f4fbff")
        pi_group = VGroup(pi_symbol, pi_value).arrange(DOWN, buff=0.20).shift(RIGHT * 3.10 + UP * 0.08)
        glow = Circle(radius=1.65, stroke_color="#ffe082", stroke_width=2.5, stroke_opacity=0.38).move_to(pi_group)
        self.play(FadeIn(glow, scale=1.10), DrawBorderThenFill(pi_symbol), Write(pi_value), run_time=1.2)
        self.wait(0.55)

        # ============================================================
        # 3. Randomness explanation
        # ============================================================
        # self.add_sound("audio/my_voice/seg_03.mp3")
        # cap = self.change_caption(cap, "পুরো পদ্ধতিটাই নির্ভর করে সম্পূর্ণ র্যান্ডম ঘটনার ওপর।", 25)

        self.play(FadeOut(pi_group), FadeOut(glow), run_time=0.45)
        rand_box = RoundedRectangle(width=3.7, height=1.35, corner_radius=0.08,
                                    stroke_color="#90caf9", stroke_opacity=0.55,
                                    fill_color=BLACK, fill_opacity=0.36).shift(RIGHT * 3.1 + UP * 0.45)
        rand1 = etext("Random positions", 28, "#a5d6ff")
        rand2 = etext("Random angles", 28, "#a5d6ff")
        rand_text = VGroup(rand1, rand2).arrange(DOWN, buff=0.18).move_to(rand_box)
        self.play(FadeIn(rand_box), Write(rand_text), run_time=0.75)
        self.wait(0.4)

        # ============================================================
        # 4. Circle relation
        # ============================================================
        # self.add_sound("audio/my_voice/seg_04.mp3")
        # cap = self.change_caption(cap, "π সাধারণত বৃত্তের সঙ্গে সম্পর্কিত।", 27)

        self.play(FadeOut(rand_box), FadeOut(rand_text), run_time=0.35)
        circle = Circle(radius=1.0, color="#f4fbff", stroke_width=5).shift(RIGHT * 3.1 + UP * 0.40)
        circ_formula = MathTex(r"C=2\pi r", font_size=40, color="#f4fbff").next_to(circle, DOWN, buff=0.25)
        self.play(Create(circle), Write(circ_formula), run_time=1.0)
        self.wait(0.35)

        # ============================================================
        # 5. No circle
        # ============================================================
        # self.add_sound("audio/my_voice/seg_05.mp3")
        # cap = self.change_caption(cap, "কিন্তু এই পরীক্ষায় নেই কোনো বৃত্ত, নেই কোনো পরিধি।", 25)

        cross = VGroup(
            Line(circle.get_corner(UL), circle.get_corner(DR), color=RED, stroke_width=7),
            Line(circle.get_corner(DL), circle.get_corner(UR), color=RED, stroke_width=7),
        )
        no_circle = etext("No circle", 34, "#ffccbc").next_to(circ_formula, DOWN, buff=0.18)
        self.play(Create(cross), Write(no_circle), run_time=0.75)
        self.wait(0.35)

        # ============================================================
        # 6. Question
        # ============================================================
        # self.add_sound("audio/my_voice/seg_06.mp3")
        # cap = self.change_caption(cap, "তাহলে সূচ ফেলেই π কীভাবে বেরিয়ে আসে?", 27)

        q = MathTex("?", font_size=92, color="#ffccbc").next_to(no_circle, DOWN, buff=0.04)
        self.play(Write(q), run_time=0.45)
        self.wait(0.45)
        self.play(FadeOut(VGroup(experiment_group, circle, circ_formula, cross, no_circle, q)), run_time=0.65)
        # self.play(FadeOut(cap), run_time=0.25)

        # ============================================================
        # 7. A4 paper setup
        # ============================================================
        # self.add_sound("audio/my_voice/seg_07.mp3")
        # cap = caption("ধরো, তোমার কাছে একটা A4 কাগজ আছে।", 27)

        setup_group, setup_paper, setup_lines, setup_ys = make_a4_paper(width=4.75, line_gap=0.82, line_count=8)
        setup_group.shift(LEFT * 1.45)
        setup_group[0].set_z_index(5)
        setup_group[1].set_z_index(6)
        for line in setup_lines:
            line.set_z_index(12)
        setup_ys = [line.get_center()[1] for line in setup_lines]
        self.add(setup_group[0], setup_group[1])
        self.play(FadeIn(setup_group[0]), FadeIn(setup_group[1]), run_time=0.8)
        # self.play(FadeIn(cap), run_time=0.25)

        a4_label = etext("A4 paper", 30, "#e3f2fd").next_to(setup_group[1], UP, buff=0.15)
        self.play(Write(a4_label), run_time=0.45)
        self.wait(0.35)

        # ============================================================
        # 8. Draw parallel lines — paper stays visible
        # ============================================================
        # self.add_sound("audio/my_voice/seg_08.mp3")
        # cap = self.change_caption(cap, "কাগজের ওপর কয়েকটি সমান্তরাল রেখা আঁকি।", 27)

        self.add(setup_group[0], setup_group[1])
        self.play(LaggedStart(*[Create(line) for line in setup_lines], lag_ratio=0.10), run_time=1.1)
        self.add(setup_group[0], setup_group[1], setup_lines)
        self.wait(0.35)

        # ============================================================
        # 9. Distance equals needle length
        # ============================================================
        # self.add_sound("audio/my_voice/seg_09.mp3")
        # cap = self.change_caption(cap, "প্রতিটি রেখার দূরত্ব একটি সূচের দৈর্ঘ্যের সমান।", 25)

        y1, y2 = setup_ys[1], setup_ys[2]
        xb = setup_paper.get_right()[0] + 0.14
        brace_line = Line([xb, y2, 0], [xb, y1, 0], color="#ffe082", stroke_width=3)
        brace_tips = VGroup(
            Line([xb - 0.12, y1, 0], [xb + 0.12, y1, 0], color="#ffe082", stroke_width=3),
            Line([xb - 0.12, y2, 0], [xb + 0.12, y2, 0], color="#ffe082", stroke_width=3),
        )
        d_label = MathTex("d", font_size=38, color="#ffe082").next_to(brace_line, RIGHT, buff=0.14)
        sample = silver_needle(length=0.82, angle=0, z=150).shift(RIGHT * 3.25 + UP * 0.70)
        lab = VGroup(etext("needle length", 24), MathTex("=d", font_size=34, color="#ffe082"))
        lab.arrange(RIGHT, buff=0.12).next_to(sample, DOWN, buff=0.22)
        self.play(Create(brace_line), Create(brace_tips), Write(d_label), FadeIn(sample), Write(lab), run_time=0.9)
        self.wait(0.45)

        # ============================================================
        # 10. Random drop actual experiment
        # ============================================================
        # self.add_sound("audio/my_voice/seg_10.mp3")
        # cap = self.change_caption(cap, "এবার অনেকগুলো সূচ সম্পূর্ণ র্যান্ডমভাবে ছুঁড়ে ফেলি।", 26)

        self.play(FadeOut(VGroup(brace_line, brace_tips, d_label, sample, lab, a4_label)), run_time=0.35)

        N = 46
        L = 0.82
        margin = 0.44

        def make_trial():
            pts = []
            attempts = 0
            while len(pts) < N and attempts < 9000:
                attempts += 1
                x = rng.uniform(setup_paper.get_left()[0] + margin, setup_paper.get_right()[0] - margin)
                y = rng.uniform(setup_paper.get_bottom()[1] + margin, setup_paper.get_top()[1] - margin)
                angle = rng.uniform(-math.pi, math.pi)
                if all(math.hypot(x - px, y - py) > 0.17 for px, py, _, _ in pts):
                    pts.append((x, y, angle, L))
            return pts

        def count_hits(pts):
            hits = []
            for i, (x, y, angle, length) in enumerate(pts):
                half = abs(math.sin(angle)) * length / 2
                if any(abs(y - ly) <= half for ly in setup_ys):
                    hits.append(i)
            return hits

        experiment_landings = None
        touching = []
        pi_est = 0
        for _ in range(500):
            pts = make_trial()
            hits = count_hits(pts)
            if hits:
                est = 2 * N / len(hits)
                if 3.05 <= est <= 3.25:
                    experiment_landings = pts
                    touching = hits
                    pi_est = est
                    break
        if experiment_landings is None:
            experiment_landings = make_trial()
            touching = count_hits(experiment_landings)
            pi_est = 2 * N / max(len(touching), 1)

        needles, anims = needle_drop_anims(self, rng, experiment_landings, z_base=160, bounce=0.055)
        self.play(AnimationGroup(*anims, lag_ratio=0), run_time=1.25)
        self.wait(0.45)

        # ============================================================
        # 11. Count total
        # ============================================================
        # self.add_sound("audio/my_voice/seg_11.mp3")
        # cap = self.change_caption(cap, "প্রথম সংখ্যা—মোট কতগুলো সূচ ফেলেছি।", 27)

        total_text = VGroup(btext("মোট সূচ", 25), MathTex(f"N={N}", font_size=40, color="#bbdefb"))
        total_text.arrange(RIGHT, buff=0.2)
        box1 = RoundedRectangle(width=3.45, height=0.70, corner_radius=0.08,
                                stroke_color="#90caf9", stroke_opacity=0.55,
                                fill_color=BLACK, fill_opacity=0.36)
        total_group = VGroup(box1, total_text).shift(RIGHT * 3.95 + UP * 1.62)
        self.play(FadeIn(box1), Write(total_text), run_time=0.75)
        self.wait(0.35)

        # ============================================================
        # 12. Count touching
        # ============================================================
        # self.add_sound("audio/my_voice/seg_12.mp3")
        # cap = self.change_caption(cap, "দ্বিতীয় সংখ্যা—কতগুলো সূচ কোনো রেখাকে স্পর্শ করেছে।", 24)

        H = len(touching)
        hit_text = VGroup(btext("রেখা স্পর্শ", 23), MathTex(f"H={H}", font_size=40, color="#fff176"))
        hit_text.arrange(RIGHT, buff=0.2)
        box2 = RoundedRectangle(width=3.45, height=0.70, corner_radius=0.08,
                                stroke_color="#fff176", stroke_opacity=0.55,
                                fill_color=BLACK, fill_opacity=0.36)
        hit_group = VGroup(box2, hit_text).next_to(total_group, DOWN, buff=0.12)

        highlights = VGroup()
        for i in touching:
            x, y, angle, length = experiment_landings[i]
            hline = Line(LEFT * length * 0.55, RIGHT * length * 0.55)
            hline.set_stroke("#fff176", width=5, opacity=0.55)
            hline.rotate(angle).move_to([x, y, 0])
            hline.set_z_index(155)
            highlights.add(hline)
        self.play(FadeIn(box2), Write(hit_text), FadeIn(highlights), run_time=0.85)
        self.wait(0.35)

        # ============================================================
        # 13. Formula
        # ============================================================
        # self.add_sound("audio/my_voice/seg_13.mp3")
        # cap = self.change_caption(cap, "হিসাব: মোট সূচ গুণ দুই, ভাগ রেখা স্পর্শ করা সূচ।", 24)

        formula = MathTex(r"\pi \approx {2N \over H}", font_size=52, color="#f4fbff")
        formula.shift(RIGHT * 3.85 + DOWN * 1.18)
        numeric = MathTex(f"\\pi \\approx \\frac{{2\\times {N}}}{{{H}}} = {pi_est:.3f}", font_size=36, color="#ffe082")
        numeric.next_to(formula, DOWN, buff=0.18)
        self.play(Write(formula), run_time=1.0)
        self.play(TransformFromCopy(formula, numeric), run_time=1.0)
        self.wait(0.45)

        # ============================================================
        # 14. Close to pi
        # ============================================================
        # self.add_sound("audio/my_voice/seg_14.mp3")
        # cap = self.change_caption(cap, "আমরা যে সংখ্যাটি পাই, সেটি π-এর খুব কাছাকাছি।", 26)

        actual = MathTex(r"\pi = 3.14159\ldots", font_size=36, color="#bbdefb")
        actual.next_to(numeric, DOWN, buff=0.18)
        self.play(Write(actual), run_time=0.8)
        self.wait(0.45)

        # ============================================================
        # 15. Final question — no extra π? text by default
        # ============================================================
        # self.add_sound("audio/my_voice/seg_15.mp3")
        # cap = self.change_caption(cap, "তাহলে কোনো বৃত্ত না থাকলেও π এলো কোথা থেকে?", 26)
        self.wait(0.45)

        # ============================================================
        # 16. Cinematic title
        # ============================================================
        # self.add_sound("audio/my_voice/seg_16.mp3")
        # cap = self.change_caption(cap, "আজ আমরা আলোচনা করব বুফোঁর নিডল মেথড নিয়ে।", 26)

        self.play(FadeOut(VGroup(table, setup_group, *needles, highlights, total_group, hit_group, formula, numeric, actual)), run_time=0.8)

        # Actual camera background color, not a rectangle.
        self.camera.background_color = "#020817"

        grid = VGroup()
        for x in [i * 0.5 for i in range(-12, 13)]:
            grid.add(Line([x, -3.5, 0], [x, 3.5, 0], color="#0b2a5a", stroke_width=1, stroke_opacity=0.34))
        for y in [i * 0.5 for i in range(-7, 8)]:
            grid.add(Line([-6, y, 0], [6, y, 0], color="#0b2a5a", stroke_width=1, stroke_opacity=0.34))
        grid.set_z_index(211)

        origin_dot = Dot(ORIGIN, radius=0.035, color="#64b5f6").set_z_index(212)
        title = VGroup(
            etext("Buffon's Needle", 58, "#f4fbff"),
            etext("Method", 58, "#ffe082"),
        ).arrange(DOWN, buff=0.10).move_to(ORIGIN)
        title.set_z_index(220)

        self.play(FadeIn(grid), FadeIn(origin_dot), run_time=0.45)
        self.move_camera(phi=1.22, theta=-PI / 2, frame_center=ORIGIN, zoom=0.82, run_time=0.07)
        self.move_camera(
            phi=0,
            theta=-PI / 2,
            frame_center=ORIGIN,
            zoom=1.05,
            run_time=3.35,
            rate_func=smooth,
            added_anims=[DrawBorderThenFill(title, run_time=3.15)],
        )
        self.wait(0.5)
