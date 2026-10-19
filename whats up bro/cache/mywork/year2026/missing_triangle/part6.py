from manim import *
import numpy as np


# ============================================================
# PART 6
#
# THE HYPOTENUSE IS NOT REALLY STRAIGHT
#
# Main question:
#
#       "Is that long edge really one straight line?"
#
# We investigate two apparently matching line segments.
#
# Segment A:
#
#       rise = 2
#       run  = 5
#
# Segment B:
#
#       rise = 3
#       run  = 8
#
# Their slopes are:
#
#       2/5
#       3/8
#
# and
#
#       2/5 - 3/8 = 1/40
#
# That tiny difference is the entire secret.
#
# This part should feel like a mathematical detective story.
# ============================================================


class MissingTrianglePart6(MovingCameraScene):

    def construct(self):

        self.camera.background_color = "#F8F5E9"

        self.setup_scene()

        self.create_main_lines()

        self.create_slope_triangles()

        self.create_equations()

        self.create_gap_objects()

        self.opening()

        self.show_apparently_straight_line()

        self.break_line_into_two_parts()

        self.show_first_slope()

        self.show_second_slope()

        self.compare_slopes()

        self.show_cross_multiplication()

        self.reveal_one_over_forty()

        self.return_to_geometry()

        self.exaggerate_difference()

        self.show_endpoint_gap()

        self.show_true_shape()

        self.compare_straight_and_bent()

        self.zoom_into_corner()

        self.final_equation()

        self.final_question()

        self.end_part()


    # ========================================================
    # SCENE SETUP
    # ========================================================

    def setup_scene(self):

        self.scale_factor = 0.58

        self.left_x = -4.2

        self.base_y = -1.5


        self.start_point = np.array([
            self.left_x,
            self.base_y,
            0,
        ])


        self.first_run = 5

        self.first_rise = 2

        self.second_run = 8

        self.second_rise = 3


        self.first_end = (
            self.start_point
            + RIGHT
            * self.first_run
            * self.scale_factor
            + UP
            * self.first_rise
            * self.scale_factor
        )


        self.second_end = (
            self.first_end
            + RIGHT
            * self.second_run
            * self.scale_factor
            + UP
            * self.second_rise
            * self.scale_factor
        )


        self.total_run = (
            self.first_run
            +
            self.second_run
        )


        self.total_rise = (
            self.first_rise
            +
            self.second_rise
        )


        self.true_final_point = (
            self.start_point
            + RIGHT
            * self.total_run
            * self.scale_factor
            + UP
            * self.total_rise
            * self.scale_factor
        )


        # ----------------------------------------------------
        # A mathematically straight line connecting the same
        # starting and final points.
        # ----------------------------------------------------

        self.straight_line = Line(
            self.start_point,
            self.true_final_point,
            stroke_color=BLACK,
            stroke_width=5,
        )


        # ----------------------------------------------------
        # The two actual pieces.
        # ----------------------------------------------------

        self.segment_one = Line(
            self.start_point,
            self.first_end,
            stroke_color=BLACK,
            stroke_width=5,
        )


        self.segment_two = Line(
            self.first_end,
            self.second_end,
            stroke_color=BLACK,
            stroke_width=5,
        )


        self.bent_line = VGroup(
            self.segment_one,
            self.segment_two,
        )


    # ========================================================
    # SLOPE TRIANGLES
    # ========================================================

    def create_slope_triangles(self):

        # ----------------------------------------------------
        # Triangle for slope 2/5
        # ----------------------------------------------------

        first_horizontal_end = (
            self.start_point
            + RIGHT
            * self.first_run
            * self.scale_factor
        )


        self.first_slope_horizontal = Line(
            self.start_point,
            first_horizontal_end,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.first_slope_vertical = Line(
            first_horizontal_end,
            self.first_end,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.first_slope_triangle = VGroup(
            self.first_slope_horizontal,
            self.first_slope_vertical,
            self.segment_one.copy(),
        )


        # ----------------------------------------------------
        # Triangle for slope 3/8
        # ----------------------------------------------------

        second_horizontal_end = (
            self.first_end
            + RIGHT
            * self.second_run
            * self.scale_factor
        )


        self.second_slope_horizontal = Line(
            self.first_end,
            second_horizontal_end,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.second_slope_vertical = Line(
            second_horizontal_end,
            self.second_end,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.second_slope_triangle = VGroup(
            self.second_slope_horizontal,
            self.second_slope_vertical,
            self.segment_two.copy(),
        )


        self.first_slope_triangle.set_opacity(0)

        self.second_slope_triangle.set_opacity(0)


    # ========================================================
    # EQUATIONS
    # ========================================================

    def create_equations(self):

        self.first_slope_equation = MathTex(
            r"m_1"
            "="
            r"\frac{\text{rise}}{\text{run}}"
            "="
            r"\frac25",
            color=BLACK,
        ).scale(0.75)


        self.second_slope_equation = MathTex(
            r"m_2"
            "="
            r"\frac{\text{rise}}{\text{run}}"
            "="
            r"\frac38",
            color=BLACK,
        ).scale(0.75)


        self.slope_difference_equation = MathTex(
            r"m_1-m_2"
            "="
            r"\frac25-\frac38",
            color=BLACK,
        ).scale(0.75)


        self.cross_multiply_equation = MathTex(
            r"\frac25-\frac38"
            "="
            r"\frac{16}{40}-\frac{15}{40}",
            color=BLACK,
        ).scale(0.72)


        self.final_difference_equation = MathTex(
            r"\boxed{\frac25-\frac38=\frac1{40}}",
            color=BLACK,
        ).scale(0.85)


        self.not_equal_equation = MathTex(
            r"\frac25\neq\frac38",
            color=BLACK,
        ).scale(0.9)


    # ========================================================
    # GAP OBJECTS
    # ========================================================

    def create_gap_objects(self):

        # ----------------------------------------------------
        # The point where the bent line changes direction.
        # ----------------------------------------------------

        self.corner_dot = Dot(
            self.first_end,
            radius=0.07,
            color=BLACK,
        )


        self.start_dot = Dot(
            self.start_point,
            radius=0.07,
            color=BLACK,
        )


        self.final_dot = Dot(
            self.second_end,
            radius=0.07,
            color=BLACK,
        )


        # ----------------------------------------------------
        # Gap between the true bent endpoint and the straight
        # line at the same horizontal position.
        # ----------------------------------------------------

        x_position = self.second_end[0]


        straight_y_at_end = (
            self.start_point[1]
            +
            (
                self.true_final_point[1]
                -
                self.start_point[1]
            )
            *
            (
                (
                    x_position
                    -
                    self.start_point[0]
                )
                /
                (
                    self.true_final_point[0]
                    -
                    self.start_point[0]
                )
            )
        )


        self.straight_endpoint_at_bent_x = np.array([
            x_position,
            straight_y_at_end,
            0,
        ])


        self.endpoint_gap = Line(
            self.straight_endpoint_at_bent_x,
            self.second_end,
            stroke_color=BLACK,
            stroke_width=3,
        )


        self.gap_brace = Brace(
            self.endpoint_gap,
            direction=RIGHT,
        )


    # ========================================================
    # OPENING
    # ========================================================

    def opening(self):

        self.title = Text(
            "Look closely at the long edge.",
            font_size=32,
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


    # ========================================================
    # APPARENTLY STRAIGHT LINE
    # ========================================================

    def show_apparently_straight_line(self):

        self.play(
            Create(
                self.straight_line,
            ),
            run_time=1.5,
        )


        self.wait(0.7)


        straight_text = Text(
            "It looks perfectly straight.",
            font_size=28,
            color=BLACK,
        )


        straight_text.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            FadeIn(
                straight_text,
                shift=UP * 0.15,
            ),
            run_time=0.7,
        )


        self.wait(1)


        self.play(
            Indicate(
                self.straight_line,
                scale_factor=1.03,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        self.play(
            FadeOut(
                straight_text,
            ),
            run_time=0.4,
        )


    # ========================================================
    # BREAK INTO TWO PARTS
    # ========================================================

    def break_line_into_two_parts(self):

        break_title = Text(
            "But this edge is made from two pieces.",
            font_size=30,
            color=BLACK,
        )


        break_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                break_title,
            ),
            run_time=0.7,
        )


        self.wait(0.6)


        self.play(
            FadeOut(
                self.straight_line,
            ),
            run_time=0.5,
        )


        self.play(
            Create(
                self.segment_one,
            ),
            Create(
                self.segment_two,
            ),
            run_time=1.2,
        )


        self.wait(0.8)


        self.play(
            FadeIn(
                self.start_dot,
                self.corner_dot,
                self.final_dot,
            ),
            run_time=0.5,
        )


        self.wait(0.7)


        corner_label = Text(
            "corner",
            font_size=22,
            color=BLACK,
        )


        corner_label.next_to(
            self.corner_dot,
            DOWN,
            buff=0.15,
        )


        self.play(
            FadeIn(
                corner_label,
            ),
            run_time=0.5,
        )


        self.wait(0.8)


        self.corner_label = corner_label


    # ========================================================
    # FIRST SLOPE
    # ========================================================

    def show_first_slope(self):

        self.play(
            FadeOut(
                self.corner_label,
            ),
            run_time=0.4,
        )


        first_title = Text(
            "Measure the first piece.",
            font_size=30,
            color=BLACK,
        )


        first_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                first_title,
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        self.first_slope_triangle.set_opacity(1)


        self.play(
            Create(
                self.first_slope_horizontal,
            ),
            Create(
                self.first_slope_vertical,
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        rise_label = MathTex(
            r"2",
            color=BLACK,
        ).scale(0.65)


        rise_label.next_to(
            self.first_slope_vertical,
            RIGHT,
            buff=0.15,
        )


        run_label = MathTex(
            r"5",
            color=BLACK,
        ).scale(0.65)


        run_label.next_to(
            self.first_slope_horizontal,
            DOWN,
            buff=0.15,
        )


        self.play(
            Write(
                rise_label,
            ),
            Write(
                run_label,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.play(
            Write(
                self.first_slope_equation,
            ),
            run_time=0.9,
        )


        self.first_slope_equation.to_edge(
            DOWN,
            buff=0.45,
        )


        self.wait(1)


        self.first_rise_label = rise_label

        self.first_run_label = run_label


    # ========================================================
    # SECOND SLOPE
    # ========================================================

    def show_second_slope(self):

        second_title = Text(
            "Now measure the second piece.",
            font_size=30,
            color=BLACK,
        )


        second_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                second_title,
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        self.second_slope_triangle.set_opacity(1)


        self.play(
            Create(
                self.second_slope_horizontal,
            ),
            Create(
                self.second_slope_vertical,
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        rise_label_2 = MathTex(
            r"3",
            color=BLACK,
        ).scale(0.65)


        rise_label_2.next_to(
            self.second_slope_vertical,
            RIGHT,
            buff=0.15,
        )


        run_label_2 = MathTex(
            r"8",
            color=BLACK,
        ).scale(0.65)


        run_label_2.next_to(
            self.second_slope_horizontal,
            DOWN,
            buff=0.15,
        )


        self.play(
            Write(
                rise_label_2,
            ),
            Write(
                run_label_2,
            ),
            run_time=0.7,
        )


        self.wait(0.7)


        self.play(
            FadeOut(
                self.first_slope_equation,
            ),
            run_time=0.4,
        )


        self.second_slope_equation.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            Write(
                self.second_slope_equation,
            ),
            run_time=0.9,
        )


        self.wait(1)


        self.second_rise_label = rise_label_2

        self.second_run_label = run_label_2


    # ========================================================
    # COMPARE SLOPES
    # ========================================================

    def compare_slopes(self):

        compare_title = Text(
            "And now compare them.",
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
            run_time=0.6,
        )


        self.wait(0.6)


        self.play(
            FadeOut(
                self.second_slope_equation,
            ),
            run_time=0.4,
        )


        self.not_equal_equation.move_to(
            DOWN * 1.8,
        )


        self.play(
            Write(
                self.not_equal_equation,
            ),
            run_time=0.9,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                self.not_equal_equation,
                scale_factor=1.12,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        # ----------------------------------------------------
        # Put the two fractions vertically.
        # ----------------------------------------------------

        first_fraction = MathTex(
            r"\frac25",
            color=BLACK,
        ).scale(0.9)


        second_fraction = MathTex(
            r"\frac38",
            color=BLACK,
        ).scale(0.9)


        first_fraction.move_to(
            LEFT * 1.0
            +
            UP * 0.5,
        )


        second_fraction.move_to(
            LEFT * 1.0
            +
            DOWN * 0.5,
        )


        comparison_symbol = MathTex(
            r"\neq",
            color=BLACK,
        ).scale(0.8)


        comparison_symbol.move_to(
            RIGHT * 0.1,
        )


        self.play(
            FadeOut(
                self.not_equal_equation,
            ),
            FadeIn(
                first_fraction,
            ),
            FadeIn(
                comparison_symbol,
            ),
            FadeIn(
                second_fraction,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.fraction_group = VGroup(
            first_fraction,
            comparison_symbol,
            second_fraction,
        )


    # ========================================================
    # CROSS MULTIPLICATION
    # ========================================================

    def show_cross_multiplication(self):

        cross_title = Text(
            "Let's check it without decimals.",
            font_size=29,
            color=BLACK,
        )


        cross_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                cross_title,
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        cross_step = MathTex(
            r"\frac25"
            r"\quad\text{vs.}\quad"
            r"\frac38",
            color=BLACK,
        ).scale(0.8)


        cross_step.move_to(
            UP * 1.0,
        )


        self.play(
            ReplacementTransform(
                self.fraction_group,
                cross_step,
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        cross_numbers = MathTex(
            r"2\times8"
            r"\quad\text{vs.}\quad"
            r"3\times5",
            color=BLACK,
        ).scale(0.8)


        cross_numbers.next_to(
            cross_step,
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                cross_numbers,
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        cross_result = MathTex(
            r"16"
            r"\quad\text{vs.}\quad"
            r"15",
            color=BLACK,
        ).scale(0.85)


        cross_result.next_to(
            cross_numbers,
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                cross_result,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                cross_result,
                scale_factor=1.12,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        self.cross_group = VGroup(
            cross_step,
            cross_numbers,
            cross_result,
        )


    # ========================================================
    # ONE OVER FORTY
    # ========================================================

    def reveal_one_over_forty(self):

        reveal_title = Text(
            "The difference is exactly one part in forty.",
            font_size=28,
            color=BLACK,
        )


        reveal_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                reveal_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.cross_group,
            ),
            run_time=0.5,
        )


        self.final_difference_equation.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                self.final_difference_equation,
            ),
            run_time=1,
        )


        self.wait(0.9)


        self.play(
            Indicate(
                self.final_difference_equation,
                scale_factor=1.1,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        fraction_explanation = MathTex(
            r"\frac1{40}=0.025",
            color=BLACK,
        ).scale(0.75)


        fraction_explanation.next_to(
            self.final_difference_equation,
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                fraction_explanation,
            ),
            run_time=0.8,
        )


        self.wait(1)


        self.fraction_explanation = fraction_explanation


    # ========================================================
    # RETURN TO GEOMETRY
    # ========================================================

    def return_to_geometry(self):

        geometry_title = Text(
            "Now look back at the geometry.",
            font_size=30,
            color=BLACK,
        )


        geometry_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                geometry_title,
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.final_difference_equation,
                self.fraction_explanation,
                run_time=0.5,
            ),
        )


        self.play(
            FadeIn(
                self.segment_one,
                self.segment_two,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        # ----------------------------------------------------
        # Remove construction triangles temporarily.
        # ----------------------------------------------------

        self.play(
            FadeOut(
                self.first_slope_horizontal,
                self.first_slope_vertical,
                self.second_slope_horizontal,
                self.second_slope_vertical,
                self.first_rise_label,
                self.first_run_label,
                self.second_rise_label,
                self.second_run_label,
                run_time=0.5,
            ),
        )


        self.wait(0.6)


    # ========================================================
    # EXAGGERATE DIFFERENCE
    # ========================================================

    def exaggerate_difference(self):

        exaggeration_title = Text(
            "The difference is tiny...",
            font_size=30,
            color=BLACK,
        )


        exaggeration_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                exaggeration_title,
            ),
            run_time=0.6,
        )


        self.wait(0.6)


        self.play(
            self.camera.frame.animate
            .scale(0.55)
            .move_to(self.corner_dot),
            run_time=1.4,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                self.corner_dot,
                scale_factor=1.5,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        zoom_text = Text(
            "but not zero.",
            font_size=28,
            color=BLACK,
        )


        zoom_text.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            FadeIn(
                zoom_text,
                shift=UP * 0.1,
            ),
            run_time=0.7,
        )


        self.wait(1)


        self.zoom_text = zoom_text


    # ========================================================
    # ENDPOINT GAP
    # ========================================================

    def show_endpoint_gap(self):

        gap_title = Text(
            "Watch what happens farther away.",
            font_size=29,
            color=BLACK,
        )


        gap_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                gap_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.zoom_text,
            ),
            run_time=0.4,
        )


        # ----------------------------------------------------
        # Show the straight reference.
        # ----------------------------------------------------

        reference_line = DashedLine(
            self.start_point,
            self.true_final_point,
            dash_length=0.08,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.play(
            Create(
                reference_line,
            ),
            run_time=1,
        )


        self.wait(0.7)


        # ----------------------------------------------------
        # Show actual bent endpoint.
        # ----------------------------------------------------

        self.play(
            Create(
                self.endpoint_gap,
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        self.play(
            Create(
                self.gap_brace,
            ),
            run_time=0.5,
        )


        self.wait(0.6)


        gap_equation = MathTex(
            r"\text{gap}"
            r"\propto"
            r"\frac1{40}",
            color=BLACK,
        ).scale(0.7)


        gap_equation.to_edge(
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                gap_equation,
            ),
            run_time=0.8,
        )


        self.wait(1)


        self.gap_equation = gap_equation

        self.reference_line = reference_line


    # ========================================================
    # TRUE SHAPE
    # ========================================================

    def show_true_shape(self):

        true_title = Text(
            "The edge is actually two different slopes.",
            font_size=28,
            color=BLACK,
        )


        true_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                true_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.reference_line,
                self.gap_brace,
                self.gap_equation,
                run_time=0.5,
            ),
        )


        # ----------------------------------------------------
        # Recreate slope triangles.
        # ----------------------------------------------------

        self.first_slope_horizontal.set_opacity(1)

        self.first_slope_vertical.set_opacity(1)

        self.second_slope_horizontal.set_opacity(1)

        self.second_slope_vertical.set_opacity(1)


        self.play(
            Create(
                self.first_slope_horizontal,
            ),
            Create(
                self.first_slope_vertical,
            ),
            run_time=0.6,
        )


        self.play(
            Create(
                self.second_slope_horizontal,
            ),
            Create(
                self.second_slope_vertical,
            ),
            run_time=0.6,
        )


        self.wait(0.8)


        first_slope_small = MathTex(
            r"\frac25",
            color=BLACK,
        ).scale(0.7)


        first_slope_small.next_to(
            self.segment_one,
            UP,
            buff=0.15,
        )


        second_slope_small = MathTex(
            r"\frac38",
            color=BLACK,
        ).scale(0.7)


        second_slope_small.next_to(
            self.segment_two,
            UP,
            buff=0.15,
        )


        self.play(
            Write(
                first_slope_small,
            ),
            Write(
                second_slope_small,
            ),
            run_time=0.8,
        )


        self.wait(1)


        self.first_slope_small = first_slope_small

        self.second_slope_small = second_slope_small


    # ========================================================
    # STRAIGHT VS BENT
    # ========================================================

    def compare_straight_and_bent(self):

        compare_title = Text(
            "Straight line or bent line?",
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
            run_time=0.6,
        )


        self.wait(0.5)


        # ----------------------------------------------------
        # Clear construction marks.
        # ----------------------------------------------------

        self.play(
            FadeOut(
                self.first_slope_horizontal,
                self.first_slope_vertical,
                self.second_slope_horizontal,
                self.second_slope_vertical,
                self.first_slope_small,
                self.second_slope_small,
                run_time=0.5,
            ),
        )


        # ----------------------------------------------------
        # Straight reference.
        # ----------------------------------------------------

        straight_reference = Line(
            self.start_point,
            self.true_final_point,
            stroke_color=BLACK,
            stroke_width=3,
        )


        straight_reference.set_opacity(0.45)


        self.play(
            Create(
                straight_reference,
            ),
            run_time=0.9,
        )


        self.wait(0.6)


        # ----------------------------------------------------
        # Actual broken edge.
        # ----------------------------------------------------

        self.play(
            Indicate(
                self.segment_one,
                scale_factor=1.03,
            ),
            Indicate(
                self.segment_two,
                scale_factor=1.03,
            ),
            run_time=0.9,
        )


        self.wait(0.8)


        comparison_text = Text(
            "They are close — but not collinear.",
            font_size=27,
            color=BLACK,
        )


        comparison_text.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            FadeIn(
                comparison_text,
                shift=UP * 0.1,
            ),
            run_time=0.7,
        )


        self.wait(1)


        self.comparison_text = comparison_text

        self.straight_reference = straight_reference


    # ========================================================
    # ZOOM INTO CORNER
    # ========================================================

    def zoom_into_corner(self):

        self.play(
            FadeOut(
                self.comparison_text,
            ),
            run_time=0.4,
        )


        zoom_title = Text(
            "Let's zoom in on the corner.",
            font_size=29,
            color=BLACK,
        )


        zoom_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                zoom_title,
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        self.play(
            self.camera.frame.animate
            .scale(0.35)
            .move_to(self.corner_dot),
            run_time=1.5,
        )


        self.wait(1)


        corner_circle = Circle(
            radius=0.25,
            stroke_color=BLACK,
            stroke_width=2,
        )


        corner_circle.move_to(
            self.corner_dot,
        )


        self.play(
            Create(
                corner_circle,
            ),
            run_time=0.5,
        )


        self.wait(0.6)


        angle_1 = Angle(
            self.first_slope_horizontal,
            self.segment_one,
            radius=0.25,
        )


        angle_2 = Angle(
            self.segment_two,
            self.second_slope_horizontal,
            radius=0.32,
        )


        self.play(
            Create(
                angle_1,
            ),
            Create(
                angle_2,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        angle_text = Text(
            "The directions are slightly different.",
            font_size=25,
            color=BLACK,
        )


        angle_text.to_edge(
            DOWN,
            buff=0.4,
        )


        self.play(
            FadeIn(
                angle_text,
                shift=UP * 0.1,
            ),
            run_time=0.7,
        )


        self.wait(1)


        self.angle_text = angle_text

        self.corner_circle = corner_circle


    # ========================================================
    # FINAL EQUATION
    # ========================================================

    def final_equation(self):

        self.play(
            FadeOut(
                self.angle_text,
                self.corner_circle,
                angle_1,
                angle_2,
                run_time=0.5,
            ),
        )


        equation_title = Text(
            "And the entire difference is encoded here.",
            font_size=28,
            color=BLACK,
        )


        equation_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                equation_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        final_equation = MathTex(
            r"\frac25-\frac38"
            "="
            r"\frac1{40}",
            color=BLACK,
        ).scale(1.0)


        final_equation.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                final_equation,
            ),
            run_time=1,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                final_equation,
                scale_factor=1.1,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        self.final_equation_object = final_equation


    # ========================================================
    # FINAL QUESTION
    # ========================================================

    def final_question(self):

        self.play(
            FadeOut(
                self.final_equation_object,
            ),
            run_time=0.5,
        )


        question_title = Text(
            "So where does the missing area come from?",
            font_size=30,
            color=BLACK,
        )


        question_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                question_title,
            ),
            run_time=0.7,
        )


        self.wait(0.7)


        question_equation = MathTex(
            r"\frac1{40}"
            r"\quad\longrightarrow\quad"
            r"\text{a visible gap}",
            color=BLACK,
        ).scale(0.72)


        question_equation.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                question_equation,
            ),
            run_time=1,
        )


        self.wait(1)


        self.play(
            Indicate(
                question_equation,
                scale_factor=1.08,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        self.question_equation = question_equation


    # ========================================================
    # END
    # ========================================================

    def end_part(self):

        self.play(
            self.camera.frame.animate
            .scale(1 / 0.35)
            .move_to(ORIGIN),
            run_time=1.4,
        )


        self.wait(0.7)


        self.play(
            FadeOut(
                self.question_equation,
            ),
            run_time=0.5,
        )


        end_title = Text(
            "The missing square is not really missing.",
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
            run_time=0.8,
        )


        self.wait(0.8)


        end_statement = MathTex(
            r"\text{The ``straight'' edge was never straight.}",
            color=BLACK,
        ).scale(0.75)


        end_statement.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                end_statement,
            ),
            run_time=1,
        )


        self.wait(1.3)


        self.play(
            FadeOut(
                end_statement,
            ),
            run_time=0.5,
        )


        next_hook = Text(
            "But can we measure the exact area of that tiny gap?",
            font_size=28,
            color=BLACK,
        )


        next_hook.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            FadeIn(
                next_hook,
                shift=UP * 0.1,
            ),
            run_time=0.8,
        )


        self.wait(2)


        self.play(
            FadeOut(
                self.title,
                next_hook,
                self.segment_one,
                self.segment_two,
                self.start_dot,
                self.corner_dot,
                self.final_dot,
                run_time=1,
            ),
        )


        self.wait(0.8)


# ============================================================
# END OF PART 6
# ============================================================
