from manim import *
import numpy as np


class Logo(Scene):
    def construct(self):

        self.camera.background_color = "#050A12"

        GREEN = "#1D9E75"

        # ── 1. Your original logo ──

        sector_filled = Sector(
            radius=2,
            start_angle=PI / 6,
            angle=2 * PI / 3,
        ).set_fill(
            color=GREEN,
            opacity=1
        ).set_stroke(
            color=WHITE,
            width=2
        )

        sector_blank1 = Sector(
            radius=2,
            start_angle=PI / 6 + 2 * PI / 3,
            angle=2 * PI / 3,
        ).set_fill(
            opacity=0
        ).set_stroke(
            color=WHITE,
            width=2
        )

        sector_blank2 = Sector(
            radius=2,
            start_angle=PI / 6 + 4 * PI / 3,
            angle=2 * PI / 3,
        ).set_fill(
            opacity=0
        ).set_stroke(
            color=WHITE,
            width=2
        )

        logo = VGroup(
            sector_filled,
            sector_blank1,
            sector_blank2
        )

        # Keep the wordmark positioned beneath
        # the final, assembled logo.
        name = Text(
            "1fill2blank",
            font="Times New Roman",
            font_size=48,
            color=WHITE,
        )
        name.next_to(logo, DOWN, buff=0.6)

        # ── 2. Slightly separate the three pieces ──

        distance = 0.42

        offsets = [
            distance * UP,

            distance * np.array([
                np.cos(7 * PI / 6),
                np.sin(7 * PI / 6),
                0
            ]),

            distance * np.array([
                np.cos(11 * PI / 6),
                np.sin(11 * PI / 6),
                0
            ]),
        ]

        sectors = [
            sector_filled,
            sector_blank1,
            sector_blank2
        ]

        for sector, offset in zip(sectors, offsets):
            sector.shift(offset)

        # ── 4. Draw the three sectors ──

        self.play(
            LaggedStart(
                DrawBorderThenFill(sector_filled),
                Create(sector_blank1),
                Create(sector_blank2),
                lag_ratio=0.4,
                run_time=3.2,
            )
        )
        self.wait(0.2)

        # ── 5. Assemble the logo ──

        self.play(
            AnimationGroup(
                *[
                    sector.animate.shift(-offset)
                    for sector, offset
                    in zip(sectors, offsets)
                ],
                lag_ratio=0,
                rate_func=rate_functions.ease_out_back,
            ),
            run_time=1.5,
        )

        # ── 6. Give the finished symbol a pulse ──

        self.play(
            logo.animate.scale(1.025),
            rate_func=there_and_back,
            run_time=0.8,
        )

        # ── 7. Write the brand name ──

        self.play(
            Write(name, rate_func=smooth),
            run_time=1.6,
        )

        # ── 8. Draw a minimal green underline ──

        underline = Line(
            name.get_left() + RIGHT * 0.10 + DOWN * 0.13,
            name.get_right() + LEFT * 0.10 + DOWN * 0.13,
            color=GREEN,
            stroke_width=2.2,
        ).set_opacity(0.7)

        self.play(
            Create(underline),
            run_time=0.5,
        )

        # ── 10. Final brand settle ──

        brand = VGroup(logo, name, underline)

        self.play(
            brand.animate.scale(1.015),
            rate_func=there_and_back,
            run_time=0.7,
        )

        self.wait(0.5)
