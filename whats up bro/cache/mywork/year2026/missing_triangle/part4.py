from manim import *
import numpy as np


# ============================================================
# PART 4
# TWO LINES THAT ALMOST AGREE
#
# Main idea:
#
#       2/5 != 3/8
#
# But the difference is very small.
#
# We will make that tiny difference visible.
# ============================================================


class MissingTrianglePart4(Scene):

    def construct(self):

        self.camera.background_color = "#F8F5E9"

        self.setup_scene()

        self.create_coordinate_geometry()

        self.create_lines()

        self.create_labels()

        self.create_equations()

        self.opening()

        self.introduce_first_line()

        self.introduce_second_line()

        self.compare_slopes()

        self.write_line_equations()

        self.show_same_starting_point()

        self.extend_lines()

        self.find_intersection()

        self.show_vertical_gap()

        self.zoom_into_gap()

        self.exaggerate_difference()

        self.return_to_normal()

        self.end_part()


    # ========================================================
    # SCENE SETUP
    # ========================================================

    def setup_scene(self):

        self.plane_center = np.array([
            0,
            -0.2,
            0,
        ])

        self.graph_width = 10

        self.graph_height = 6

        self.x_min = -5

        self.x_max = 5

        self.y_min = -3

        self.y_max = 3


    # ========================================================
    # COORDINATE GEOMETRY
    # ========================================================

    def create_coordinate_geometry(self):

        self.origin = np.array([
            -3.8,
            -1.7,
            0,
        ])


        self.horizontal_scale = 0.62

        self.vertical_scale = 0.62


        # ----------------------------------------------------
        # Mathematical dimensions
        # ----------------------------------------------------

        self.base_1 = 5

        self.height_1 = 2

        self.base_2 = 8

        self.height_2 = 3


        # ----------------------------------------------------
        # Slopes
        # ----------------------------------------------------

        self.m1 = self.height_1 / self.base_1

        self.m2 = self.height_2 / self.base_2


        # ----------------------------------------------------
        # Important points
        # ----------------------------------------------------

        self.start = self.origin.copy()


        self.line1_end = (
            self.start
            + RIGHT * self.base_1 * self.horizontal_scale
            + UP * self.height_1 * self.vertical_scale
        )


        self.line2_end = (
            self.start
            + RIGHT * self.base_2 * self.horizontal_scale
            + UP * self.height_2 * self.vertical_scale
        )


        # ----------------------------------------------------
        # Extend lines farther than the triangle
        # ----------------------------------------------------

        self.extension_length = 4


        self.line1_far = (
            self.start
            + RIGHT * self.extension_length
            + UP * self.extension_length * self.m1
        )


        self.line2_far = (
            self.start
            + RIGHT * self.extension_length
            + UP * self.extension_length * self.m2
        )


    # ========================================================
    # CREATE THE TWO LINES
    # ========================================================

    def create_lines(self):

        self.line_1 = Line(
            self.start,
            self.line1_far,
            stroke_color=BLACK,
            stroke_width=5,
        )


        self.line_2 = Line(
            self.start,
            self.line2_far,
            stroke_color=BLACK,
            stroke_width=5,
        )


        self.line_1.set_z_index(4)

        self.line_2.set_z_index(5)


        # ----------------------------------------------------
        # Endpoint markers
        # ----------------------------------------------------

        self.point_start = Dot(
            self.start,
            radius=0.065,
            color=BLACK,
        )


        self.point_1_end = Dot(
            self.line1_end,
            radius=0.055,
            color=BLACK,
        )


        self.point_2_end = Dot(
            self.line2_end,
            radius=0.055,
            color=BLACK,
        )


    # ========================================================
    # LABELS
    # ========================================================

    def create_labels(self):

        self.label_start = MathTex(
            "O",
            color=BLACK,
        ).scale(0.45)


        self.label_start.next_to(
            self.start,
            DOWN + LEFT,
            buff=0.12,
        )


        self.label_1 = MathTex(
            r"\frac{2}{5}",
            color=BLACK,
        ).scale(0.55)


        self.label_1.next_to(
            self.line_1_end,
            UP + LEFT,
            buff=0.15,
        )


        self.label_2 = MathTex(
            r"\frac{3}{8}",
            color=BLACK,
        ).scale(0.55)


        self.label_2.next_to(
            self.line_2_end,
            UP + RIGHT,
            buff=0.15,
        )


        self.line1_text = Text(
            "first edge",
            font_size=24,
            color=BLACK,
        )


        self.line2_text = Text(
            "second edge",
            font_size=24,
            color=BLACK,
        )


        self.line1_text.next_to(
            self.line_1_end,
            RIGHT,
            buff=0.2,
        )


        self.line2_text.next_to(
            self.line_2_end,
            RIGHT,
            buff=0.2,
        )


    # ========================================================
    # EQUATIONS
    # ========================================================

    def create_equations(self):

        self.eq1 = MathTex(
            r"y=\frac{2}{5}x",
            color=BLACK,
        ).scale(0.7)


        self.eq2 = MathTex(
            r"y=\frac{3}{8}x",
            color=BLACK,
        ).scale(0.7)


        self.eq1_box = SurroundingRectangle(
            self.eq1,
            buff=0.18,
            stroke_width=1.5,
        )


        self.eq2_box = SurroundingRectangle(
            self.eq2,
            buff=0.18,
            stroke_width=1.5,
        )


        self.equation_group = VGroup(
            self.eq1,
            self.eq2,
        )


    # ========================================================
    # OPENING
    # ========================================================

    def opening(self):

        self.title = Text(
            "Two almost identical lines",
            font_size=34,
            color=BLACK,
        )


        self.title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            FadeIn(
                self.title,
                shift=DOWN * 0.2,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


    # ========================================================
    # FIRST LINE
    # ========================================================

    def introduce_first_line(self):

        self.play(
            FadeIn(
                self.point_start,
            ),
            run_time=0.4,
        )


        self.play(
            Create(
                self.line_1,
            ),
            run_time=1.2,
        )


        self.play(
            FadeIn(
                self.label_start,
            ),
            run_time=0.4,
        )


        self.wait(0.5)


        self.play(
            FadeIn(
                self.point_1_end,
            ),
            FadeIn(
                self.label_1,
            ),
            run_time=0.5,
        )


        self.wait(0.7)


        first_triangle = VGroup(
            Line(
                self.start,
                self.line1_end,
                stroke_width=2,
            ),
            Line(
                self.line1_end,
                self.start + RIGHT * 5 * self.horizontal_scale,
                stroke_width=2,
            ),
            Line(
                self.start + RIGHT * 5 * self.horizontal_scale,
                self.start,
                stroke_width=2,
            ),
        )


        first_triangle.set_opacity(
            0.35
        )


        self.play(
            Create(
                first_triangle,
            ),
            run_time=0.7,
        )


        self.wait(0.6)


        self.play(
            FadeOut(
                first_triangle,
            ),
            run_time=0.4,
        )


    # ========================================================
    # SECOND LINE
    # ========================================================

    def introduce_second_line(self):

        self.play(
            Create(
                self.line_2,
            ),
            run_time=1.2,
        )


        self.wait(0.6)


        self.play(
            FadeIn(
                self.point_2_end,
            ),
            FadeIn(
                self.label_2,
            ),
            run_time=0.5,
        )


        self.wait(0.7)


        second_triangle = VGroup(
            Line(
                self.start,
                self.line2_end,
                stroke_width=2,
            ),
            Line(
                self.line2_end,
                self.start + RIGHT * 8 * self.horizontal_scale,
                stroke_width=2,
            ),
            Line(
                self.start + RIGHT * 8 * self.horizontal_scale,
                self.start,
                stroke_width=2,
            ),
        )


        second_triangle.set_opacity(
            0.35
        )


        self.play(
            Create(
                second_triangle,
            ),
            run_time=0.7,
        )


        self.wait(0.6)


        self.play(
            FadeOut(
                second_triangle,
            ),
            run_time=0.4,
        )


    # ========================================================
    # COMPARE SLOPES
    # ========================================================

    def compare_slopes(self):

        self.slope_title = Text(
            "The slopes are close...",
            font_size=28,
            color=BLACK,
        )


        self.slope_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                self.slope_title,
            ),
            run_time=0.6,
        )


        self.wait(0.4)


        slope_comparison = MathTex(
            r"\frac{2}{5}"
            r"\quad\text{and}\quad"
            r"\frac{3}{8}",
            color=BLACK,
        ).scale(0.8)


        slope_comparison.to_edge(
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                slope_comparison,
            ),
            run_time=0.9,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                slope_comparison,
                scale_factor=1.05,
            ),
            run_time=0.7,
        )


        self.wait(0.6)


        self.play(
            FadeOut(
                slope_comparison,
            ),
            run_time=0.4,
        )


    # ========================================================
    # LINE EQUATIONS
    # ========================================================

    def write_line_equations(self):

        equation_title = Text(
            "Let's write the equations.",
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
            run_time=0.6,
        )


        self.wait(0.5)


        self.eq1.to_edge(
            LEFT,
            buff=0.8,
        )


        self.eq1.shift(
            UP * 0.7,
        )


        self.eq2.to_edge(
            LEFT,
            buff=0.8,
        )


        self.eq2.shift(
            DOWN * 0.7,
        )


        self.play(
            Write(
                self.eq1,
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        self.play(
            Write(
                self.eq2,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        self.eq_difference = MathTex(
            r"\frac{2}{5}"
            r"\neq"
            r"\frac{3}{8}",
            color=BLACK,
        ).scale(0.75)


        self.eq_difference.to_edge(
            RIGHT,
            buff=0.8,
        )


        self.play(
            Write(
                self.eq_difference,
            ),
            run_time=0.8,
        )


        self.wait(1)


        self.equation_group_visible = VGroup(
            self.eq1,
            self.eq2,
            self.eq_difference,
        )


    # ========================================================
    # SAME STARTING POINT
    # ========================================================

    def show_same_starting_point(self):

        self.play(
            FadeOut(
                self.equation_group_visible,
            ),
            run_time=0.5,
        )


        self.same_point_text = Text(
            "But both lines start at exactly the same point.",
            font_size=27,
            color=BLACK,
        )


        self.same_point_text.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                self.same_point_text,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            Indicate(
                self.point_start,
                scale_factor=1.5,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        self.start_circle = Circle(
            radius=0.18,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.start_circle.move_to(
            self.start,
        )


        self.play(
            Create(
                self.start_circle,
            ),
            run_time=0.5,
        )


        self.wait(0.6)


        self.play(
            FadeOut(
                self.start_circle,
            ),
            run_time=0.4,
        )


    # ========================================================
    # EXTEND LINES
    # ========================================================

    def extend_lines(self):

        self.extension_title = Text(
            "So let's extend them.",
            font_size=29,
            color=BLACK,
        )


        self.extension_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                self.extension_title,
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        extra_line_1 = Line(
            self.line1_end,
            self.line1_far,
            stroke_color=BLACK,
            stroke_width=5,
        )


        extra_line_2 = Line(
            self.line2_end,
            self.line2_far,
            stroke_color=BLACK,
            stroke_width=5,
        )


        self.play(
            Create(
                extra_line_1,
            ),
            Create(
                extra_line_2,
            ),
            run_time=1.2,
        )


        self.wait(0.7)


        self.play(
            Indicate(
                self.line_1,
                scale_factor=1.01,
            ),
            Indicate(
                self.line_2,
                scale_factor=1.01,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


    # ========================================================
    # FIND INTERSECTION
    # ========================================================

    def find_intersection(self):

        # ----------------------------------------------------
        # Algebra
        #
        # 2/5 x = 3/8 x
        #
        # For these two lines through the same origin,
        # the only intersection is x = 0.
        #
        # This is precisely why the tiny difference becomes
        # visible only farther away from the origin.
        # ----------------------------------------------------

        intersection_title = Text(
            "Where do they meet?",
            font_size=29,
            color=BLACK,
        )


        intersection_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                intersection_title,
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        intersection_eq = MathTex(
            r"\frac{2}{5}x"
            "="
            r"\frac{3}{8}x",
            color=BLACK,
        ).scale(0.75)


        intersection_eq.move_to(
            UP * 1.0,
        )


        self.play(
            Write(
                intersection_eq,
            ),
            run_time=0.9,
        )


        self.wait(0.7)


        step_1 = MathTex(
            r"\left(\frac{2}{5}-\frac{3}{8}\right)x=0",
            color=BLACK,
        ).scale(0.7)


        step_1.next_to(
            intersection_eq,
            DOWN,
            buff=0.35,
        )


        self.play(
            Write(
                step_1,
            ),
            run_time=0.9,
        )


        self.wait(0.7)


        step_2 = MathTex(
            r"\frac{1}{40}x=0",
            color=BLACK,
        ).scale(0.7)


        step_2.next_to(
            step_1,
            DOWN,
            buff=0.35,
        )


        self.play(
            Write(
                step_2,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        step_3 = MathTex(
            r"x=0",
            color=BLACK,
        ).scale(0.8)


        step_3.next_to(
            step_2,
            DOWN,
            buff=0.35,
        )


        self.play(
            Write(
                step_3,
            ),
            run_time=0.7,
        )


        self.wait(1)


        self.intersection_math = VGroup(
            intersection_eq,
            step_1,
            step_2,
            step_3,
        )


        self.play(
            FadeOut(
                self.intersection_math,
            ),
            run_time=0.5,
        )


        self.wait(0.5)


    # ========================================================
    # VERTICAL GAP
    # ========================================================

    def show_vertical_gap(self):

        gap_title = Text(
            "They separate as we move away.",
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
            run_time=0.6,
        )


        self.wait(0.5)


        # Choose a point farther from origin.

        self.gap_x = 4.0


        self.gap_y1 = self.m1 * self.gap_x

        self.gap_y2 = self.m2 * self.gap_x


        self.gap_difference = (
            self.gap_y1
            -
            self.gap_y2
        )


        gap_start = (
            self.start
            +
            RIGHT
            * self.gap_x
            * self.horizontal_scale
            +
            UP
            * self.gap_y2
            * self.vertical_scale
        )


        gap_end = (
            self.start
            +
            RIGHT
            * self.gap_x
            * self.horizontal_scale
            +
            UP
            * self.gap_y1
            * self.vertical_scale
        )


        self.gap_line = Line(
            g
