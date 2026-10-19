from manim import *

from animations import GrowWithBouncing


class GrowBouncyTest(Scene):
    def construct(self):
        self.camera.background_color = "#050A12"

        factorial = MathTex(r"n!", font_size=120, color=WHITE)
        rect = SurroundingRectangle(factorial, color=YELLOW, buff=0.18)
        label = Text(
            "Spring Bounce",
            font="CMU Serif",
            font_size=42,
            color=WHITE,
        )
        group = VGroup(VGroup(factorial, rect), label).arrange(DOWN, buff=0.6)

        # Create বা Write-এর বদলে GrowWithBouncing ব্যবহার
        # প্রথম বস্তু: ৩ বার দোলন, দ্বিতীয় বস্তু: ৪ বার দোলন
        self.play(GrowWithBouncing(group[0], number_of_bounces=3))
        self.wait(0.3)
        self.play(GrowWithBouncing(group[1], number_of_bounces=4, run_time=1.6))
        self.wait(0.8)
