from manim import *

config.background_color = "#050A12"
BRAND_GOLD = "#FFD23F"


class BrandMark(Scene):
    def build_mark(self):
        self.badge = Circle(radius=1.55, color=WHITE, stroke_width=6, fill_color="#0B1626", fill_opacity=1)
        apex, base_l, base_r = UP * 0.88, LEFT * 0.78 + DOWN * 0.44, RIGHT * 0.78 + DOWN * 0.44
        cut_l, cut_r = LEFT * 0.52, RIGHT * 0.52
        self.third_fill = Polygon(base_l, base_r, cut_r, cut_l, color=BRAND_GOLD, fill_color=BRAND_GOLD, fill_opacity=1, stroke_width=0)
        self.cone = Polygon(apex, base_r, base_l, color=WHITE, stroke_width=7, fill_opacity=0)
        self.fraction = MathTex(r"\frac{1}{3}", font_size=30, color=BRAND_GOLD)
        self.fraction.next_to(self.cone, DOWN, buff=0.08)


class LogoScene(BrandMark):
    def construct(self):
        self.build_mark()
        logo = VGroup(self.badge, self.third_fill, self.cone, self.fraction)
        name = Text("WhyOneThird", font="CMU Serif", font_size=44, color=WHITE, weight=BOLD)
        name.next_to(logo, DOWN, buff=0.25)
        self.add(VGroup(logo, name).scale(1.25))


class BrandIntroScene(BrandMark):
    def construct(self):
        self.build_mark()
        name = Text("WhyOneThird", font="CMU Serif", font_size=54, color=WHITE, weight=BOLD)
        tagline = Text("Ask why. See why.", font="CMU Serif", font_size=26, color=BRAND_GOLD)
        mark = VGroup(self.badge, self.third_fill, self.cone, self.fraction)
        name.next_to(mark, DOWN, buff=0.3)
        tagline.next_to(name, DOWN, buff=0.18)
        self.play(Create(self.badge), run_time=0.8)
        self.play(Create(self.cone), run_time=0.7)
        self.play(FadeIn(self.third_fill, shift=UP * 0.2), run_time=0.5)
        self.play(Write(self.fraction), run_time=0.5)
        self.play(Write(name))
        self.play(FadeIn(tagline, shift=UP * 0.15), run_time=0.5)
        self.wait(0.6)
