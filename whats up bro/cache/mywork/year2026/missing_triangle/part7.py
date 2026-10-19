from manim import *
import numpy as np


# ============================================================
# PART 7
# FROM SLOPE DIFFERENCE TO AREA
#
# Core idea:
#
#       2/5 != 3/8
#
#       2/5 - 3/8 = 1/40
#
# A tiny difference in slope produces a growing vertical gap.
#
# The gap eventually becomes a visible triangular region.
#
# Visual sequence:
#
#       slope
#          ↓
#       angle
#          ↓
#       separation
#          ↓
#       triangle
#          ↓
#       area
#
# This part should feel like the puzzle is finally becoming
# measurable.
# ============================================================


class MissingTrianglePart7(MovingCameraScene):

    def construct(self):

        self.camera.background_color = "#F8F5E9"

        self.setup_geometry()

        self.create_reference_lines()

        self.create_labels()

        self.introduction()

        self.show_two_slopes()

        self.show_common_start()

        self.show_vertical_separation()

        self.show_gap_growth()

        self.show_scaled_gap()

        self.construct_triangle()

        self.label_triangle()

        self_introduce_area()

        self.calculate_area()

        self.connect_slope_difference()

        self.show_one_over_forty()

        self.animate_area_growth()

        self.compare_real_and_exaggerated()

        self.return_to_original_scale()

        self.show_final_relationship()

        self.end_part()


    # ========================================================
    # GEOMETRY SETUP
    # ========================================================

    def setup_geometry(self):

        self.origin = np.array([
            -4.5,
            -2.0,
            0,
        ])


        self.horizontal_length = 8.0

        self.scale = 0.42


        # First slope:
        #
        #       2
        #       -
        #       5

        self.m1 = 2 / 5


        # Second slope:
        #
        #       3
        #       -
        #       8

        self.m2 = 3 / 8


        self.slope_difference = (
            self.m1 - self.m2
        )


        # ----------------------------------------------------
        # Two rays starting from exactly the same point.
        # ----------------------------------------------------

        self.line_one_end = (
            self.origin
            +
            RIGHT
            * self.horizontal_length
            * self.scale
            +
            UP
            * self.m1
            * self.horizontal_length
            * self.scale
        )


        self.line_two_end = (
            self.origin
            +
            RIGHT
            * self.horizontal_length
            * self.scale
            +
            UP
            * self.m2
            * self.horizontal_length
            * self.scale
        )


        # ----------------------------------------------------
        # Vertical separation at the far end.
        # ----------------------------------------------------

        self.final_gap = (
            self.line_one_end[1]
            -
            self.line_two_end[1]
        )


        # ----------------------------------------------------
        # Intermediate points.
        # ----------------------------------------------------

        self.mid_x = (
            self.origin[0]
            +
            self.horizontal_length
            * self.scale
            * 0.5
        )


        self.mid_y_one = (
            self.origin[1]
            +
            self.m1
            *
            (
                self.mid_x
                -
                self.origin[0]
            )
        )


        self.mid_y_two = (
            self.origin[1]
            +
            self.m2
            *
            (
                self.mid_x
                -
                self.origin[0]
            )
        )


    # ========================================================
    # REFERENCE LINES
    # ========================================================

    def create_reference_lines(self):

        self.line_one = Line(
            self.origin,
            self.line_one_end,
            stroke_color=BLACK,
            stroke_width=5,
        )


        self.line_two = Line(
            self.origin,
            self.line_two_end,
            stroke_color=BLACK,
            stroke_width=5,
        )


        # ----------------------------------------------------
        # Dashed vertical line at the end.
        # ----------------------------------------------------

        self.final_vertical = DashedLine(
            self.line_two_end,
            self.line_one_end,
            dash_length=0.08,
            stroke_color=BLACK,
            stroke_width=3,
        )


        # ----------------------------------------------------
        # Horizontal base.
        # ----------------------------------------------------

        self.base_line = Line(
            self.origin,
            np.array([
                self.line_one_end[0],
                self.origin[1],
                0,
            ]),
            stroke_color=BLACK,
            stroke_width=2,
        )


        # ----------------------------------------------------
        # Vertical construction at midpoint.
        # ----------------------------------------------------

        self.mid_vertical = DashedLine(
            np.array([
                self.mid_x,
                self.mid_y_two,
                0,
            ]),
            np.array([
                self.mid_x,
                self.mid_y_one,
                0,
            ]),
            dash_length=0.06,
            stroke_color=BLACK,
            stroke_width=2,
        )


    # ========================================================
    # LABELS
    # ========================================================

    def create_labels(self):

        self.m1_label = MathTex(
            r"m_1=\frac25",
            color=BLACK,
        ).scale(0.72)


        self.m2_label = MathTex(
            r"m_2=\frac38",
            color=BLACK,
        ).scale(0.72)


        self.m1_label.next_to(
            self.line_one,
            UP,
            buff=0.15,
        )


        self.m2_label.next_to(
            self.line_two,
            DOWN,
            buff=0.15,
        )


        self.gap_label = MathTex(
            r"\Delta y",
            color=BLACK,
        ).scale(0.65)


        self.gap_label.next_to(
            self.final_vertical,
            RIGHT,
            buff=0.15,
        )


        self.base_label = MathTex(
            r"x",
            color=BLACK,
        ).scale(0.65)


    # ========================================================
    # INTRODUCTION
    # ========================================================

    def introduction(self):

        self.title = Text(
            "The tiny slope difference starts to matter.",
            font_size=31,
            color=BLACK,
        )


        self.title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            FadeIn(
                self.title,
                shift=DOWN * 0.15,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        intro_equation = MathTex(
            r"\frac25-\frac38=\frac1{40}",
            color=BLACK,
        ).scale(0.9)


        intro_equation.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                intro_equation,
            ),
            run_time=1,
        )


        self.wait(1)


        self.play(
            FadeOut(
                intro_equation,
            ),
            run_time=0.5,
        )


    # ========================================================
    # SHOW TWO SLOPES
    # ========================================================

    def show_two_slopes(self):

        self.play(
            Create(
                self.line_one,
            ),
            run_time=1,
        )


        self.play(
            Create(
                self.line_two,
            ),
            run_time=1,
        )


        self.wait(0.7)


        self.play(
            Write(
                self.m1_label,
            ),
            run_time=0.7,
        )


        self.play(
            Write(
                self.m2_label,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                self.m1_label,
            ),
            Indicate(
                self.m2_label,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


    # ========================================================
    # COMMON START
    # ========================================================

    def show_common_start(self):

        common_title = Text(
            "Both lines start from exactly the same point.",
            font_size=28,
            color=BLACK,
        )


        common_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                common_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.origin_dot = Dot(
            self.origin,
            radius=0.08,
            color=BLACK,
        )


        self.play(
            FadeIn(
                self.origin_dot,
            ),
            run_time=0.4,
        )


        self.play(
            Indicate(
                self.origin_dot,
                scale_factor=1.5,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        common_label = Text(
            "same starting point",
            font_size=22,
            color=BLACK,
        )


        common_label.next_to(
            self.origin_dot,
            DOWN,
            buff=0.2,
        )


        self.play(
            FadeIn(
                common_label,
            ),
            run_time=0.6,
        )


        self.wait(0.8)


        self.common_label = common_label


    # ========================================================
    # VERTICAL SEPARATION
    # ========================================================

    def show_vertical_separation(self):

        self.play(
            FadeOut(
                self.common_label,
            ),
            run_time=0.4,
        )


        separation_title = Text(
            "But they slowly separate.",
            font_size=30,
            color=BLACK,
        )


        separation_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                separation_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            Create(
                self.final_vertical,
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        self.play(
            Write(
                self.gap_label,
            ),
            run_time=0.7,
        )


        self.wait(0.7)


        separation_equation = MathTex(
            r"\Delta y"
            r"="
            r"y_1-y_2",
            color=BLACK,
        ).scale(0.78)


        separation_equation.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            Write(
                separation_equation,
            ),
            run_time=0.8,
        )


        self.wait(0.9)


        self.separation_equation = separation_equation


    # ========================================================
    # GAP GROWTH
    # ========================================================

    def show_gap_growth(self):

        growth_title = Text(
            "The farther we travel, the larger the gap becomes.",
            font_size=27,
            color=BLACK,
        )


        growth_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                growth_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.separation_equation,
                self.gap_label,
            ),
            run_time=0.4,
        )


        # ----------------------------------------------------
        # Moving vertical measuring line.
        # ----------------------------------------------------

        tracker = ValueTracker(0.05)


        def upper_point():

            x = (
                self.origin[0]
                +
                self.horizontal_length
                *
                self.scale
                *
                tracker.get_value()
            )


            y = (
                self.origin[1]
                +
                self.m1
                *
                (
                    x
                    -
                    self.origin[0]
                )
            )


            return np.array([
                x,
                y,
                0,
            ])


        def lower_point():

            x = (
                self.origin[0]
                +
                self.horizontal_length
                *
                self.scale
                *
                tracker.get_value()
            )


            y = (
                self.origin[1]
                +
                self.m2
                *
                (
                    x
                    -
                    self.origin[0]
                )
            )


            return np.array([
                x,
                y,
                0,
            ])


        moving_gap = always_redraw(
            lambda: Line(
                lower_point(),
                upper_point(),
                stroke_color=BLACK,
                stroke_width=4,
            )
        )


        moving_dot_upper = always_redraw(
            lambda: Dot(
                upper_point(),
                radius=0.055,
                color=BLACK,
            )
        )


        moving_dot_lower = always_redraw(
            lambda: Dot(
                lower_point(),
                radius=0.055,
                color=BLACK,
            )
        )


        self.add(
            moving_gap,
            moving_dot_upper,
            moving_dot_lower,
        )


        self.play(
            tracker.animate.set_value(0.95),
            run_time=2.5,
            rate_func=linear,
        )


        self.wait(0.8)


        self.remove(
            moving_gap,
            moving_dot_upper,
            moving_dot_lower,
        )


    # ========================================================
    # SCALED GAP
    # ========================================================

    def show_scaled_gap(self):

        scaled_title = Text(
            "Let's make the tiny difference easier to see.",
            font_size=28,
            color=BLACK,
        )


        scaled_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                scaled_title,
            ),
            run_time=0.7,
        )


        self.wait(0.6)


        self.play(
            self.camera.frame.animate
            .scale(0.72)
            .move_to(
                (
                    self.line_one_end
                    +
                    self.line_two_end
                )
                / 2
            ),
            run_time=1.2,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                self.final_vertical,
                scale_factor=1.15,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


    # ========================================================
    # CONSTRUCT TRIANGLE
    # ========================================================

    def construct_triangle(self):

        triangle_title = Text(
            "Now the gap forms a triangle.",
            font_size=30,
            color=BLACK,
        )


        triangle_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                triangle_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            Create(
                self.base_line,
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        # ----------------------------------------------------
        # Triangle boundary.
        # ----------------------------------------------------

        self.gap_triangle = Polygon(
            self.origin,
            self.line_one_end,
            self.line_two_end,
            stroke_color=BLACK,
            stroke_width=3,
            fill_opacity=0,
        )


        self.play(
            Create(
                self.gap_triangle,
            ),
            run_time=1.2,
        )


        self.wait(0.8)


        self.corner_one = Dot(
            self.line_one_end,
            radius=0.07,
            color=BLACK,
        )


        self.corner_two = Dot(
            self.line_two_end,
            radius=0.07,
            color=BLACK,
        )


        self.play(
            FadeIn(
                self.corner_one,
                self.corner_two,
            ),
            run_time=0.5,
        )


        self.wait(0.7)


    # ========================================================
    # LABEL TRIANGLE
    # ========================================================

    def label_triangle(self):

        label_title = Text(
            "Every side has a meaning.",
            font_size=30,
            color=BLACK,
        )


        label_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                label_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        base_label = MathTex(
            r"x",
            color=BLACK,
        ).scale(0.75)


        base_label.move_to(
            (
                self.origin
                +
                np.array([
                    self.horizontal_length
                    * self.scale
                    / 2,
                    -0.3,
                    0,
                ])
            )
        )


        self.play(
            Write(
                base_label,
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        height_label = MathTex(
            r"\Delta y",
            color=BLACK,
        ).scale(0.7)


        height_label.next_to(
            self.final_vertical,
            RIGHT,
            buff=0.18,
        )


        self.play(
            Write(
                height_label,
            ),
            run_time=0.6,
        )


        self.wait(0.6)


        slope_label = MathTex(
            r"\Delta m",
            color=BLACK,
        ).scale(0.7)


        slope_label.move_to(
            (
                self.line_one_end
                +
                self.line_two_end
            )
            /
            2
            +
            RIGHT
            * 0.55,
        )


        self.play(
            Write(
                slope_label,
            ),
            run_time=0.6,
        )


        self.wait(0.8)


        self.base_label_object = base_label

        self.height_label_object = height_label

        self.slope_label_object = slope_label


    # ========================================================
    # AREA INTRODUCTION
    # ========================================================

    def_introduce_area = None

    def self_introduce_area(self):

        area_title = Text(
            "And this triangular gap has an area.",
            font_size=29,
            color=BLACK,
        )


        area_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                area_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        area_formula = MathTex(
            r"A"
            "="
            r"\frac12"
            r"\times"
            r"\text{base}"
            r"\times"
            r"\text{height}",
            color=BLACK,
        ).scale(0.75)


        area_formula.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            Write(
                area_formula,
            ),
            run_time=0.9,
        )


        self.wait(0.8)


        self.area_formula = area_formula


    # ========================================================
    # AREA CALCULATION
    # ========================================================

    def calculate_area(self):

        calculation_title = Text(
            "Let's calculate it.",
            font_size=30,
            color=BLACK,
        )


        calculation_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                calculation_title,
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.area_formula,
            ),
            run_time=0.4,
        )


        step_one = MathTex(
            r"A"
            "="
            r"\frac12"
            r"x"
            r"\Delta y",
            color=BLACK,
        ).scale(0.9)


        step_one.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                step_one,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        step_two = MathTex(
            r"\Delta y"
            "="
            r"x"
            r"\Delta m",
            color=BLACK,
        ).scale(0.82)


        step_two.next_to(
            step_one,
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                step_two,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        step_three = MathTex(
            r"A"
            "="
            r"\frac12"
            r"x^2"
            r"\Delta m",
            color=BLACK,
        ).scale(0.9)


        step_three.next_to(
            step_two,
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                step_three,
            ),
            run_time=0.9,
        )


        self.wait(1)


        self.calculation_group = VGroup(
            step_one,
            step_two,
            step_three,
        )


    # ========================================================
    # CONNECT SLOPE DIFFERENCE
    # ========================================================

    def connect_slope_difference(self):

        connect_title = Text(
            "But what exactly is Δm?",
            font_size=30,
            color=BLACK,
        )


        connect_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                connect_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.calculation_group,
            ),
            run_time=0.5,
        )


        slope_difference = MathTex(
            r"\Delta m"
            "="
            r"m_1-m_2",
            color=BLACK,
        ).scale(0.9)


        slope_difference.move_to(
            UP * 0.8,
        )


        self.play(
            Write(
                slope_difference,
            ),
            run_time=0.8,
        )


        self.wait(0.6)


        slope_difference_2 = MathTex(
            r"\Delta m"
            "="
            r"\frac25-\frac38",
            color=BLACK,
        ).scale(0.85)


        slope_difference_2.next_to(
            slope_difference,
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                slope_difference_2,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        slope_difference_3 = MathTex(
            r"\Delta m"
            "="
            r"\frac1{40}",
            color=BLACK,
        ).scale(0.95)


        slope_difference_3.next_to(
            slope_difference_2,
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                slope_difference_3,
            ),
            run_time=0.9,
        )


        self.wait(1)


        self.slope_difference_group = VGroup(
            slope_difference,
            slope_difference_2,
            slope_difference_3,
        )


    # ========================================================
    # SHOW ONE OVER FORTY
    # ========================================================

    def show_one_over_forty(self):

        one_title = Text(
            "So the gap grows according to one-fortieth.",
            font_size=28,
            color=BLACK,
        )


        one_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                one_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.slope_difference_group,
            ),
            run_time=0.5,
        )


        main_relation = MathTex(
            r"\Delta y"
            "="
            r"x"
            r"\left(\frac1{40}\right)",
            color=BLACK,
        ).scale(0.95)


        main_relation.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                main_relation,
            ),
            run_time=0.9,
        )


        self.wait(0.9)


        self.play(
            Indicate(
                main_relation,
                scale_factor=1.1,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        self.main_relation = main_relation


    # ========================================================
    # ANIMATE AREA GROWTH
    # ========================================================

    def animate_area_growth(self):

        growth_title = Text(
            "The separation grows linearly with x.",
            font_size=29,
            color=BLACK,
        )


        growth_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                growth_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.main_relation,
            ),
            run_time=0.4,
        )


        tracker = ValueTracker(0.15)


        def current_x():

            return (
                self.origin[0]
                +
                self.horizontal_length
                *
                self.scale
                *
                tracker.get_value()
            )


        def current_upper():

            x = current_x()


            y = (
                self.origin[1]
                +
                self.m1
                *
                (
                    x
                    -
                    self.origin[0]
                )
            )


            return np.array([
                x,
                y,
                0,
            ])


        def current_lower():

            x = current_x()


            y = (
                self.origin[1]
                +
                self.m2
                *
                (
                    x
                    -
                    self.origin[0]
                )
            )


            return np.array([
                x,
                y,
                0,
            ])


        dynamic_gap = always_redraw(
            lambda: Line(
                current_lower(),
                current_upper(),
                stroke_color=BLACK,
                stroke_width=4,
            )
        )


        dynamic_base = always_redraw(
            lambda: Line(
                self.origin,
                np.array([
                    current_x(),
                    self.origin[1],
                    0,
                ]),
                stroke_color=BLACK,
                stroke_width=2,
            )
        )


        dynamic_triangle = always_redraw(
            lambda: Polygon(
                self.origin,
                current_upper(),
                current_lower(),
                stroke_color=BLACK,
                stroke_width=2,
                fill_opacity=0,
            )
        )


        self.add(
            dynamic_gap,
            dynamic_base,
            dynamic_triangle,
        )


        self.play(
            tracker.animate.set_value(0.95),
            run_time=3,
            rate_func=linear,
        )


        self.wait(0.8)


        self.remove(
            dynamic_gap,
            dynamic_base,
            dynamic_triangle,
        )


    # ========================================================
    # REAL VS EXAGGERATED
    # ========================================================

    def compare_real_and_exaggerated(self):

        compare_title = Text(
            "The real gap is tiny.",
            font_size=30,
            color=BLACK,
        )


        compare_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                compare_title,
            ),
            run_time=0.7,
        )


        self.wait(0.6)


        # ----------------------------------------------------
        # Show original geometry again.
        # ----------------------------------------------------

        self.play(
            FadeIn(
                self.final_vertical,
            ),
            run_time=0.5,
        )


        self.wait(0.6)


        # ----------------------------------------------------
        # Make an enlarged duplicate of the gap.
        # ----------------------------------------------------

        enlarged_gap = self.final_vertical.copy()


        enlarged_gap.move_to(
            RIGHT * 2.8
            +
            UP * 1.8
        )


        enlarged_gap.scale(
            4
        )


        enlarged_label = MathTex(
            r"\frac1{40}",
            color=BLACK,
        ).scale(0.85)


        enlarged_label.next_to(
            enlarged_gap,
            RIGHT,
            buff=0.2,
        )


        enlarged_text = Text(
            "same ratio, easier to see",
            font_size=21,
            color=BLACK,
        )


        enlarged_text.next_to(
            enlarged_gap,
            DOWN,
            buff=0.25,
        )


        self.play(
            TransformFromCopy(
                self.final_vertical,
                enlarged_gap,
            ),
            run_time=1,
        )


        self.play(
            Write(
                enlarged_label,
            ),
            FadeIn(
                enlarged_text,
            ),
            run_time=0.7,
        )


        self.wait(1)


        self.enlarged_group = VGroup(
            enlarged_gap,
            enlarged_label,
            enlarged_text,
        )


    # ========================================================
    # RETURN TO ORIGINAL SCALE
    # ========================================================

    def return_to_original_scale(self):

        return_title = Text(
            "Now put the scale back.",
            font_size=30,
            color=BLACK,
        )


        return_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                return_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.enlarged_group,
            ),
            run_time=0.6,
        )


        self.play(
            self.camera.frame.animate
            .scale(1 / 0.72)
            .move_to(ORIGIN),
            run_time=1.2,
        )


        self.wait(0.8)


        self.play(
            FadeOut(
                self.final_vertical,
            ),
            run_time=0.4,
        )


    # ========================================================
    # FINAL RELATIONSHIP
    # ========================================================

    def show_final_relationship(self):

        final_title = Text(
            "The whole puzzle is now connected.",
            font_size=30,
            color=BLACK,
        )


        final_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                final_title,
            ),
            run_time=0.7,
        )


        self.wait(0.6)


        relation_one = MathTex(
            r"\Delta m"
            "="
            r"\frac1{40}",
            color=BLACK,
        ).scale(0.85)


        relation_one.move_to(
            UP * 1.1,
        )


        self.play(
            Write(
                relation_one,
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        relation_two = MathTex(
            r"\Delta y"
            "="
            r"x\Delta m",
            color=BLACK,
        ).scale(0.85)


        relation_two.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                relation_two,
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        relation_three = MathTex(
            r"A"
            "="
            r"\frac12x^2\Delta m",
            color=BLACK,
        ).scale(0.9)


        relation_three.move_to(
            DOWN * 1.1,
        )


        self.play(
            Write(
                relation_three,
            ),
            run_time=0.9,
        )


        self.wait(1)


        self.play(
            Indicate(
                relation_one,
                scale_factor=1.08,
            ),
            run_time=0.6,
        )


        self.play(
            Indicate(
                relation_two,
                scale_factor=1.08,
            ),
            run_time=0.6,
        )


        self.play(
            Indicate(
                relation_three,
                scale_factor=1.08,
            ),
            run_time=0.6,
        )


        self.wait(1)


        self.final_relations = VGroup(
            relation_one,
            relation_two,
            relation_three,
        )


    # ========================================================
    # END
    # ========================================================

    def end_part(self):

        self.play(
            FadeOut(
                self.final_relations,
            ),
            run_time=0.6,
        )


        end_title = Text(
            "A tiny slope error creates a real area.",
            font_size=31,
            color=BLACK,
        )


        end_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                end_title,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        end_equation = MathTex(
            r"""\boxed{
                A=\frac12x^2
                \left(\frac1{40}\right)
            }""",
            color=BLACK,
        ).scale(0.82)


        end_equation.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                end_equation,
            ),
            run_time=1,
        )


        self.wait(1.2)


        self.play(
            Indicate(
                end_equation,
                scale_factor=1.08,
            ),
            run_time=0.8,
        )


        self.wait(1)


        self.play(
            FadeOut(
                end_equation,
            ),
            run_time=0.5,
        )


        hook = Text(
            "But is this the missing area we were looking for?",
            font_size=28,
            color=BLACK,
        )


        hook.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            FadeIn(
                hook,
                shift=UP * 0.1,
            ),
            run_time=0.8,
        )


        self.wait(2)


        self.play(
            FadeOut(
                self.title,
                hook,
                self.line_one,
                self.line_two,
                self.base_line,
                self.gap_triangle,
                self.origin_dot,
                self.corner_one,
                self.corner_two,
                run_time=1,
            ),
        )


        self.wait(0.8)


# ============================================================
# END OF PART 7
# ============================================================
