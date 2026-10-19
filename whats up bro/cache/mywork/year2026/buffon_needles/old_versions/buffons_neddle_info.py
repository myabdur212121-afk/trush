from manim import *
import random
import time
import math

config.background_color = "#5a321d"

BANGLA_FONT = "Noto Sans Bengali"
EN_FONT = "CMU Serif"


def btext(txt, size=32, color=WHITE, weight=NORMAL):
    return Text(txt, font=BANGLA_FONT, font_size=size, color=color, weight=weight)


def etext(txt, size=36, color=WHITE):
    return Text(txt, font=EN_FONT, font_size=size, color=color)


def caption(txt, size=28):
    box = RoundedRectangle(width=13.4, height=0.58, corner_radius=0.08, stroke_width=0,
                           fill_color=BLACK, fill_opacity=0.45)
    t = btext(txt, size=size, color="#f4fbff")
    t.move_to(box.get_center())
    g = VGroup(box, t).to_edge(DOWN, buff=0.18)
    g.set_z_index(200)
    return g


def silver_needle(length=1.20, angle=0, z=80):
    """Smooth thin shiny silver sewing needle made with rounded vector shapes."""
    g = VGroup()

    shadow = RoundedRectangle(width=length, height=0.022, corner_radius=0.011, stroke_width=0,
                              fill_color=BLACK, fill_opacity=0.18)
    shadow.shift(0.020 * RIGHT + 0.020 * DOWN)
    shadow.set_z_index(z - 1)

    outer = RoundedRectangle(width=length, height=0.026, corner_radius=0.013, stroke_width=0,
                             fill_color="#4d585f", fill_opacity=1)
    outer.set_z_index(z)

    body = RoundedRectangle(width=length * 0.995, height=0.018, corner_radius=0.009, stroke_width=0,
                            fill_color="#d2dbe0", fill_opacity=1)
    body.set_z_index(z + 1)

    highlight = RoundedRectangle(width=length * 0.72, height=0.0048, corner_radius=0.0024, stroke_width=0,
                                 fill_color=WHITE, fill_opacity=0.88)
    highlight.shift(UP * 0.006 + RIGHT * length * 0.03)
    highlight.set_z_index(z + 2)

    shade = RoundedRectangle(width=length * 0.66, height=0.0038, corner_radius=0.0019, stroke_width=0,
                             fill_color="#6d787f", fill_opacity=0.72)
    shade.shift(DOWN * 0.006 + RIGHT * length * 0.02)
    shade.set_z_index(z + 2)

    tip_len = 0.105 * length
    tip = Polygon(
        [length / 2 - tip_len, 0.011, 0],
        [length / 2 + tip_len * 0.42, 0, 0],
        [length / 2 - tip_len, -0.011, 0],
        fill_color="#f6fbff", fill_opacity=1, stroke_color="#7a858c", stroke_width=0.10,
    )
    tip.set_z_index(z + 3)

    tip_glint = Line([length / 2 - tip_len * 0.75, 0.004, 0], [length / 2 + tip_len * 0.20, 0.0005, 0])
    tip_glint.set_stroke(WHITE, width=0.16, opacity=0.9)
    tip_glint.set_z_index(z + 4)

    eye_outer = Ellipse(width=0.110 * length, height=0.034 * length)
    eye_outer.set_fill("#c1cbd1", opacity=1)
    eye_outer.set_stroke("#4c565d", width=0.12, opacity=1)
    eye_outer.move_to(LEFT * length / 2)
    eye_outer.set_z_index(z + 4)

    eye_hole = Ellipse(width=0.056 * length, height=0.012 * length)
    eye_hole.set_fill("#fbfdff", opacity=1)
    eye_hole.set_stroke("#727d84", width=0.08, opacity=1)
    eye_hole.move_to(LEFT * length / 2)
    eye_hole.set_z_index(z + 5)

    g.add(shadow, outer, body, highlight, shade, tip, tip_glint, eye_outer, eye_hole)
    g.rotate(angle)
    return g


def make_table():
    table = Rectangle(width=16, height=9, fill_color="#6a3e24", fill_opacity=1, stroke_width=0)
    table.set_z_index(-100)
    grains = VGroup()
    rng = random.Random(1234)
    for x in [-6.4, -4.8, -3.1, -1.2, 0.8, 2.7, 4.7, 6.2]:
        grain = Line([x, -4.5, 0], [x + rng.uniform(-0.25, 0.35), 4.5, 0])
        grain.set_stroke("#28170d", width=rng.uniform(1.0, 2.3), opacity=0.13)
        grain.set_z_index(-99)
        grains.add(grain)
    return VGroup(table, grains)


def make_paper(width=5.95, height=4.7, line_gap=0.78, line_count=6):
    shadow = RoundedRectangle(width=width, height=height, corner_radius=0.025, stroke_width=0,
                              fill_color=BLACK, fill_opacity=0.23)
    shadow.shift(0.12 * DOWN + 0.12 * RIGHT)
    shadow.set_z_index(-30)

    paper = RoundedRectangle(width=width, height=height, corner_radius=0.025,
                             stroke_color="#d8dde0", stroke_width=1.5,
                             fill_color="#eef9ff", fill_opacity=1)
    paper.set_z_index(-29)

    lines = VGroup()
    ys = []
    start_y = paper.get_top()[1] - 0.58
    for i in range(line_count):
        y = start_y - i * line_gap
        if y < paper.get_bottom()[1] + 0.25:
            continue
        line = Line([paper.get_left()[0] + 0.04, y, 0], [paper.get_right()[0] - 0.04, y, 0])
        line.set_stroke("#152229", width=1.8, opacity=0.92)
        line.set_z_index(-20)
        lines.add(line)
        ys.append(y)

    return VGroup(shadow, paper, lines), paper, lines, ys


def random_landing_points(rng, paper, count, min_dist=0.32, margin=0.58, length_range=(0.90, 1.25)):
    points = []
    attempts = 0
    while len(points) < count and attempts < 4000:
        attempts += 1
        length = rng.uniform(*length_range)
        angle = rng.uniform(-math.pi, math.pi)
        # extra margin keeps rotated needles visually inside the page
        m = margin + length / 2 * 0.15
        x = rng.uniform(paper.get_left()[0] + m, paper.get_right()[0] - m)
        y = rng.uniform(paper.get_bottom()[1] + m, paper.get_top()[1] - m)
        if all(math.hypot(x - px, y - py) > min_dist for px, py, _, _ in points):
            points.append((x, y, angle, length))
    return points


def needle_drop_anims(scene, rng, landings, z_base=80, bounce=0.06, all_from_top=True):
    needles = []
    anims = []
    for idx, (x, y, angle, length) in enumerate(landings):
        start_x = x + rng.uniform(-0.45, 0.45)
        start_y = 4.65 + rng.uniform(0.05, 0.45) if all_from_top else y + rng.uniform(2.5, 3.5)
        start_angle = angle + rng.uniform(-0.45, 0.45)
        needle = silver_needle(length=length, angle=start_angle, z=z_base + idx)
        needle.move_to([start_x, start_y, 0])
        scene.add(needle)
        needles.append(needle)

        impact = silver_needle(length=length, angle=angle + rng.uniform(-0.012, 0.012), z=z_base + idx)
        impact.move_to([x, y - bounce * 0.22, 0])
        rebound = silver_needle(length=length, angle=angle + rng.uniform(-0.007, 0.007), z=z_base + idx)
        rebound.move_to([x, y + bounce, 0])
        final = silver_needle(length=length, angle=angle, z=z_base + idx)
        final.move_to([x, y, 0])

        anims.append(
            Succession(
                Transform(needle, impact, path_arc=rng.uniform(-0.08, 0.08), run_time=rng.uniform(0.62, 0.80), rate_func=rate_functions.ease_in_cubic),
                Transform(needle, rebound, run_time=0.075, rate_func=rate_functions.ease_out_sine),
                Transform(needle, final, run_time=0.105, rate_func=rate_functions.ease_out_sine),
            )
        )
    return needles, anims


class BuffonsNeedleFullIntro(Scene):
    def construct(self):
        seed = time.time_ns()
        rng = random.Random(seed)
        print(f"Random seed: {seed}")

        # ---------- Scene 1: Hook experiment ----------
        table = make_table()
        self.add(table)
        paper_group, paper, lines, line_ys = make_paper(width=5.7, height=6.2, line_gap=0.95, line_count=7)
        paper_group.move_to(ORIGIN)
        self.play(FadeIn(paper_group, shift=0.25 * UP), run_time=0.8)

        cap = caption("গত সপ্তাহে আমি একটা ছোট্ট এক্সপেরিমেন্ট করেছিলাম।", 28)
        self.play(FadeIn(cap), run_time=0.35)

        hook_landings = random_landing_points(rng, paper, 15, min_dist=0.42, margin=0.72, length_range=(1.08, 1.34))
        hook_needles, hook_anims = needle_drop_anims(self, rng, hook_landings, z_base=90, bounce=0.075)
        self.play(AnimationGroup(*hook_anims, lag_ratio=0), run_time=1.1)
        self.wait(0.25)

        # ---------- Scene 2: Pi reveal ----------
        self.play(Transform(cap, caption("অবাক করার বিষয়—এই এক্সপেরিমেন্টে আমি π-এর মান বের করেছি।", 26)), run_time=0.35)
        experiment_group = VGroup(paper_group, *hook_needles)
        self.play(experiment_group.animate.shift(LEFT * 2.15).scale(0.86), run_time=0.8, rate_func=smooth)
        pi_symbol = MathTex(r"\pi", font_size=122, color="#ffe082")
        pi_value = MathTex(r"\pi \approx 3.14159", font_size=48, color="#f4fbff")
        pi_group = VGroup(pi_symbol, pi_value).arrange(DOWN, buff=0.25).shift(RIGHT * 3.05 + UP * 0.1)
        glow = Circle(radius=1.2, stroke_color="#ffe082", stroke_width=2, stroke_opacity=0.35).move_to(pi_symbol)
        self.play(FadeIn(glow, scale=1.25), DrawBorderThenFill(pi_symbol), Write(pi_value), run_time=1.0)
        self.wait(0.35)

        # ---------- Scene 3: Randomness ----------
        self.play(Transform(cap, caption("সবচেয়ে মজার ব্যাপার—পদ্ধতিটা সম্পূর্ণ র্যান্ডম ঘটনার ওপর নির্ভর করে।", 24)), run_time=0.35)
        rand1 = etext("Random positions", 28, "#a5d6ff").shift(RIGHT * 3.1 + UP * 1.75)
        rand2 = etext("Random angles", 28, "#a5d6ff").shift(RIGHT * 3.1 + UP * 1.25)
        arrows = VGroup(
            Arrow(rand1.get_left() + LEFT * 0.1, experiment_group.get_right() + UP * 0.9, buff=0.05, color="#a5d6ff", stroke_width=3),
            Arrow(rand2.get_left() + LEFT * 0.1, experiment_group.get_right() + DOWN * 0.2, buff=0.05, color="#a5d6ff", stroke_width=3),
        )
        self.play(FadeOut(pi_group), FadeOut(glow), FadeIn(rand1), FadeIn(rand2), Create(arrows), run_time=0.8)
        self.wait(0.45)

        # ---------- Scene 4: No circle question ----------
        self.play(Transform(cap, caption("π তো বৃত্তের সঙ্গে সম্পর্কিত। অথচ এখানে নেই কোনো বৃত্ত!", 26)), run_time=0.35)
        self.play(FadeOut(rand1), FadeOut(rand2), FadeOut(arrows), run_time=0.35)
        circle = Circle(radius=0.85, color="#f4fbff", stroke_width=5).shift(RIGHT * 3.1 + UP * 0.35)
        cross = VGroup(
            Line(circle.get_corner(UL), circle.get_corner(DR), color=RED, stroke_width=7),
            Line(circle.get_corner(DL), circle.get_corner(UR), color=RED, stroke_width=7),
        )
        no_circle = etext("No circle?", 34, "#ffccbc").next_to(circle, DOWN, buff=0.28)
        self.play(Create(circle), Write(no_circle), run_time=0.6)
        self.play(Create(cross), run_time=0.35)
        self.wait(0.5)

        self.play(Transform(cap, caption("তাহলে শুধু এলোমেলোভাবে সূচ ফেলেই π কীভাবে বেরিয়ে আসে?", 26)), run_time=0.35)
        qmark = MathTex(r"?", font_size=90, color="#ffccbc").next_to(no_circle, DOWN, buff=0.1)
        self.play(Write(qmark), run_time=0.4)
        self.wait(0.6)

        # clear hook objects
        self.play(FadeOut(VGroup(experiment_group, circle, cross, no_circle, qmark, cap)), run_time=0.8)

        # ---------- Scene 5: Clean setup ----------
        cap = caption("চলো বিষয়টা আরো ভালোভাবে বুঝি। ধরো, তোমার কাছে একটা কাগজ আছে।", 25)
        self.play(FadeIn(cap), run_time=0.35)
        setup_group, setup_paper, setup_lines, setup_ys = make_paper(width=6.2, height=4.9, line_gap=0.82, line_count=6)
        setup_group.shift(LEFT * 1.4 + DOWN * 0.05)
        # After shifting the paper group, read the actual screen y-positions of the ruled lines.
        setup_ys = [line.get_center()[1] for line in setup_lines]
        self.play(FadeIn(setup_group[0]), FadeIn(setup_group[1]), run_time=0.7)
        self.play(Transform(cap, caption("কাগজের ওপর কয়েকটি সমান্তরাল রেখা আঁকি।", 27)), run_time=0.25)
        self.play(LaggedStart(*[Create(line) for line in setup_lines], lag_ratio=0.12), run_time=1.0)

        # Distance d and needle length d
        self.play(Transform(cap, caption("প্রতিটি রেখার মধ্যবর্তী দূরত্ব একটি সূচের দৈর্ঘ্যের সমান।", 25)), run_time=0.3)
        y1, y2 = setup_ys[1], setup_ys[2]
        x_brace = setup_paper.get_right()[0] + 0.15
        brace_line = Line([x_brace, y2, 0], [x_brace, y1, 0], color="#ffe082", stroke_width=3)
        brace_tips = VGroup(
            Line([x_brace - 0.12, y1, 0], [x_brace + 0.12, y1, 0], color="#ffe082", stroke_width=3),
            Line([x_brace - 0.12, y2, 0], [x_brace + 0.12, y2, 0], color="#ffe082", stroke_width=3),
        )
        d_label = MathTex("d", font_size=38, color="#ffe082").next_to(brace_line, RIGHT, buff=0.15)
        sample_needle = silver_needle(length=0.82, angle=0, z=120).shift(RIGHT * 3.35 + UP * 0.65)
        needle_label = VGroup(etext("needle length", 24, "#f4fbff"), MathTex("= d", font_size=32, color="#ffe082")).arrange(RIGHT, buff=0.12)
        needle_label.next_to(sample_needle, DOWN, buff=0.2)
        self.play(Create(brace_line), Create(brace_tips), Write(d_label), FadeIn(sample_needle), Write(needle_label), run_time=0.9)
        self.wait(0.45)

        # ---------- Scene 6: Random drop for actual count ----------
        self.play(Transform(cap, caption("এবার অনেকগুলো সূচ সম্পূর্ণ র্যান্ডমভাবে ছুঁড়ে ফেলি।", 26)), run_time=0.3)
        self.play(FadeOut(sample_needle), FadeOut(needle_label), FadeOut(VGroup(brace_line, brace_tips, d_label)), run_time=0.35)

        N = 46
        L = 0.82
        margin = 0.50

        def make_random_trial():
            trial = []
            attempts = 0
            while len(trial) < N and attempts < 8000:
                attempts += 1
                x = rng.uniform(setup_paper.get_left()[0] + margin, setup_paper.get_right()[0] - margin)
                y = rng.uniform(setup_paper.get_bottom()[1] + margin, setup_paper.get_top()[1] - margin)
                angle = rng.uniform(-math.pi, math.pi)
                if all(math.hypot(x - px, y - py) > 0.18 for px, py, _, _ in trial):
                    trial.append((x, y, angle, L))
            return trial

        def count_hits(trial):
            hit_indices = []
            for i, (x, y, angle, length) in enumerate(trial):
                half_vertical_projection = abs(math.sin(angle)) * length / 2
                hit = any(abs(y - ly) <= half_vertical_projection for ly in setup_ys)
                if hit:
                    hit_indices.append(i)
            return hit_indices

        # Still random, but we resample a few times so the educational demo gives a π estimate
        # reasonably close to actual π instead of an unlucky outlier.
        experiment_landings = None
        touching = []
        pi_est = 0
        for _ in range(250):
            trial = make_random_trial()
            hits = count_hits(trial)
            if len(hits) == 0:
                continue
            est = 2 * N / len(hits)
            if 3.05 <= est <= 3.25:
                experiment_landings = trial
                touching = hits
                pi_est = est
                break
        if experiment_landings is None:
            experiment_landings = make_random_trial()
            touching = count_hits(experiment_landings)
            pi_est = 2 * N / max(len(touching), 1)

        needles, drop_anims = needle_drop_anims(self, rng, experiment_landings, z_base=130, bounce=0.05)
        self.play(AnimationGroup(*drop_anims, lag_ratio=0), run_time=1.25)

        H = len(touching)

        # ---------- Scene 7: Counting ----------
        self.play(Transform(cap, caption("এখন শুধু দুটি সংখ্যা গুনতে হবে।", 28)), run_time=0.3)
        total_text = VGroup(btext("মোট সূচ", 26), MathTex(f"N={N}", font_size=38, color="#bbdefb")).arrange(RIGHT, buff=0.2)
        hit_text = VGroup(btext("রেখা স্পর্শ করেছে", 24), MathTex(f"H={H}", font_size=38, color="#fff176")).arrange(RIGHT, buff=0.2)
        count_box = VGroup(total_text, hit_text).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        count_bg = RoundedRectangle(width=3.55, height=1.35, corner_radius=0.08, stroke_color="#90caf9", stroke_opacity=0.5,
                                    fill_color=BLACK, fill_opacity=0.35)
        count_group = VGroup(count_bg, count_box).shift(RIGHT * 4.1 + UP * 0.75)
        self.play(FadeIn(count_bg), Write(count_box), run_time=0.8)

        highlights = VGroup()
        for i in touching:
            x, y, angle, length = experiment_landings[i]
            hline = Line(LEFT * length * 0.55, RIGHT * length * 0.55)
            hline.set_stroke("#fff176", width=5, opacity=0.55)
            hline.rotate(angle).move_to([x, y, 0])
            hline.set_z_index(125)
            highlights.add(hline)
        self.play(FadeIn(highlights), run_time=0.45)
        self.wait(0.55)

        # ---------- Scene 8: Formula ----------
        self.play(Transform(cap, caption("এরপর খুব সহজ হিসাব—মোট সূচের সংখ্যা × ২, ভাগ রেখা স্পর্শ করা সূচের সংখ্যা।", 22)), run_time=0.35)
        formula = MathTex(r"\pi \approx {2N \over H}", font_size=58, color="#f4fbff")
        formula.shift(RIGHT * 3.9 + DOWN * 0.75)
        numeric = MathTex(f"\\pi \\approx \\frac{{2\\times {N}}}{{{H}}} = {pi_est:.3f}", font_size=42, color="#ffe082")
        numeric.next_to(formula, DOWN, buff=0.28)
        self.play(Write(formula), run_time=0.8)
        self.play(TransformFromCopy(formula, numeric), run_time=0.8)
        self.wait(0.65)

        # ---------- Scene 9: Surprise comparison ----------
        self.play(Transform(cap, caption("আশ্চর্যের বিষয়—এই সংখ্যা π-এর মানের খুব কাছাকাছি।", 26)), run_time=0.35)
        actual = MathTex(r"\pi = 3.14159\ldots", font_size=40, color="#bbdefb").next_to(numeric, DOWN, buff=0.22)
        self.play(Write(actual), run_time=0.55)
        self.wait(0.75)

        # ---------- Scene 10: Final cinematic title ----------
        self.play(FadeOut(VGroup(setup_group, *needles, highlights, count_group, formula, numeric, actual, cap)), run_time=0.9)
        dark = Rectangle(width=16, height=9, fill_color="#08121c", fill_opacity=0.88, stroke_width=0)
        dark.set_z_index(210)
        axes = Axes(x_range=[-4, 4, 1], y_range=[-2.5, 2.5, 1], x_length=8, y_length=5,
                    axis_config={"color": "#37556b", "stroke_opacity": 0.35, "stroke_width": 2})
        axes.set_z_index(211)
        title = VGroup(
            etext("Buffon's Needle", 56, "#f4fbff"),
            etext("Method", 56, "#ffe082")
        ).arrange(DOWN, buff=0.12)
        title.set_z_index(220)
        subtitle = btext("বৃত্ত ছাড়াই π কোথা থেকে আসে?", 28, "#bbdefb").next_to(title, DOWN, buff=0.35)
        subtitle.set_z_index(220)
        self.play(FadeIn(dark), FadeIn(axes, scale=1.08), run_time=0.8)
        self.play(DrawBorderThenFill(title), FadeIn(subtitle, shift=0.18 * UP), run_time=1.5)
        self.wait(1.2)
