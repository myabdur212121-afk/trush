from manim import *


class Logo(Scene):
    def construct(self):
        # Stage objects
        circle = Circle(radius=2).set_stroke(color=WHITE, width=2)
        dot = Dot(ORIGIN, radius=0.05, color=WHITE)

        line_angles = [PI/6, PI/6 + 2*PI/3, PI/6 + 4*PI/3]
        lines = VGroup(*[
            Line(ORIGIN, 2 * np.array([np.cos(a), np.sin(a), 0]))
            .set_stroke(color=WHITE, width=1.5)
            for a in line_angles
        ])

        sector_filled = Sector(
            radius=2, start_angle=PI/6, angle=2*PI/3,
        ).set_fill(color="#1D9E75", opacity=1).set_stroke(color=WHITE, width=2)

        sector_blank1 = Sector(
            radius=2, start_angle=PI/6 + 2*PI/3, angle=2*PI/3,
        ).set_fill(opacity=0).set_stroke(color=WHITE, width=2)

        sector_blank2 = Sector(
            radius=2, start_angle=PI/6 + 4*PI/3, angle=2*PI/3,
        ).set_fill(opacity=0).set_stroke(color=WHITE, width=2)

        logo = VGroup(sector_filled, sector_blank1, sector_blank2)

        name = Text("1Fill2Blank", font="CMU Serif", font_size=48)
        name.next_to(logo, DOWN, buff=0.6)

        # Stage 1 — dot + circle appears (2s)
        self.play(FadeIn(dot, scale=2), run_time=0.5)
        self.play(Create(circle, rate_func=smooth), run_time=1.5)

        # Stage 2 — lines divide the circle (2.5s)
        self.play(
            LaggedStart(
                *[Create(line, rate_func=smooth) for line in lines],
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.wait(0.5)

        # Stage 3 — swap to final logo (1.3s)
        self.play(
            FadeOut(circle),
            FadeOut(dot),
            FadeOut(lines),
            FadeIn(logo),
            run_time=0.8
        )
        self.wait(0.5)

        # Stage 5 — text appears (1.5s)
        self.play(
            Write(name),
            run_time=1.5
        )

        # Stage 6 — hold (3s)
        self.wait(3)
