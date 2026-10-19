"""
window_viewport ডেমো দৃশ্য (Scenes Showcase)

চালানোর নিয়ম:
    manim -qh year2026/window_viewport/demo.py WindowAPIShowcase -o output.mp4
"""

import numpy as np
from manim import *

# যদি প্যাকেজ হিসেবে ইমপোর্ট করেন:
try:
    from .window import Window, BoundedPlane, ViewportScene
except ImportError:
    from window import Window, BoundedPlane, ViewportScene


class WindowAPIShowcase(ViewportScene):
    """
    উইন্ডো এবং একক অক্ষের বাউন্ডারি টেস্ট দৃশ্য:
    ১. বামে: Window ---> Axis ---> Shapes (লুকানো অক্ষের চারকোনা মনিটর উইন্ডো)
    ২. ডানে: Standalone Axis ---> Shapes (সরাসরি সিনের দৃশ্যমান অক্ষ)
    """
    def construct(self):
        # ১. কেস ১: উইন্ডো তৈরি
        win1 = Window(
            width=5.0,
            height=4.0,
            x_range=[0, 100, 20],
            y_range=[0, 50, 10],
            show_border=True,
            show_axes=False,       # অক্ষ লুকানো থাকবে
            border_color=TEAL,
            title="Window (Window -> Axis -> Shapes)"
        ).move_to(LEFT * 3.5)

        # উইন্ডোর ভেতরে গ্রাফ ও শেপ
        graph1 = win1.plot(lambda x: 25 + 15 * np.sin(x / 5), color=YELLOW)
        circle1 = Circle(radius=1.2, color=RED).set_fill(PINK, opacity=0.6)
        circle1.move_to(win1.c2p(30, 25))
        win1.bind(circle1)

        # ২. কেস ২: উইন্ডো ছাড়া সরাসরি দৃশ্যমান অক্ষ
        ax2 = BoundedPlane(
            x_range=[-PI, PI, PI / 2],
            y_range=[-3, 3, 1],
            x_length=5.0,
            y_length=4.0,
            axis_config={"stroke_color": BLUE, "stroke_width": 3},
            background_line_style={"stroke_color": WHITE, "stroke_width": 0.5}
        ).move_to(RIGHT * 3.5)

        title2 = Text("Standalone Axis (Axis -> Shapes)", font_size=18, color=BLUE)
        title2.next_to(ax2, UP, buff=0.15)

        graph2 = ax2.plot(lambda x: 2 * np.cos(2 * x), color=GREEN)
        square2 = Square(side_length=2.0, color=GOLD).set_fill(ORANGE, opacity=0.6)
        square2.move_to(ax2.c2p(0, 0))
        ax2.bind(square2)

        # ৩. অ্যানিমেশন প্রদর্শন
        self.play(FadeIn(win1), FadeIn(ax2), FadeIn(title2))
        self.play(Create(graph1), Create(graph2), run_time=1.5)
        self.play(FadeIn(circle1), FadeIn(square2))
        self.wait(0.5)

        # মোশন টেস্ট: বৃত্ত ও বর্গক্ষেত্রকে বর্ডারের দিকে ধাক্কা দেওয়া হলো
        # উভয় শেপ নিজ নিজ বাউন্ডারির বাইরে এক পিক্সেলও বের হবে না!
        self.play(
            circle1.animate.shift(RIGHT * 3),
            square2.animate.shift(LEFT * 3),
            run_time=3
        )
        self.wait(1)

        # বৃত্তটিকে উইন্ডোর ওপরের বর্ডারের দিকে তুলে দেওয়া হলো (কোণায় কাটা পড়বে)
        self.play(
            circle1.animate.shift(UP * 2.5),
            run_time=2
        )
        self.wait(2)
