"""Run with bin/manimgl; FontsOnly needs no LaTeX, FontsAndMath does."""
from manimlib import *


class FontsOnly(Scene):
    def construct(self):
        labels = VGroup(
            Text("Computer Modern Serif", font="CMU Serif", font_size=48),
            Text("বাংলা ফন্ট পরীক্ষা", font="Noto Serif Bengali", font_size=48),
        ).arrange(DOWN, buff=0.4).shift(UP * 0.6)
        circle = Circle(radius=0.45, color=BLUE).shift(DOWN * 1.6 + LEFT)
        glow = GlowDot(color=YELLOW, radius=0.12).shift(DOWN * 1.6 + RIGHT)
        self.play(FadeIn(labels), ShowCreation(circle), FadeIn(glow), run_time=0.5)
        self.wait(0.5)


class FontsAndMath(Scene):
    def construct(self):
        labels = VGroup(
            Text("CMU Serif + Noto Serif Bengali", font="CMU Serif", font_size=40),
            Text("গণিত ও বাংলা", font="Noto Serif Bengali", font_size=48),
            # The wrapper selects basic after latex_slim.sh, default after full.
            Tex(r"(a+b)^n=\sum_{k=0}^{n}\binom{n}{k}a^{n-k}b^k", font_size=44),
        ).arrange(DOWN, buff=0.5)
        self.play(FadeIn(labels), run_time=0.5)
        self.wait(0.5)
