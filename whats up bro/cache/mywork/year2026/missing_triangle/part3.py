from manim import *
import numpy as np


# ============================================================
# PART 3
# THE LINE THAT ISN'T A LINE
# ============================================================


class MissingTrianglePart3(Scene):

    def construct(self):

        self.camera.background_color = "#F8F5E9"

        self.setup_geometry()
        self.create_pieces()
        self.create_main_objects()
        self.create_slope_objects()
        self.create_labels()

        self.opening()
        self.show_two_triangles()
        self.compare_slopes()
        self.show_slope_equations()
        self.overlay_hypotenuses()
        self.zoom_to_difference()
        self.show_intersection()
        self.show_apparent_line()
        self.question()


    # ========================================================
    # GEOMETRY
    # ========================================================

    def setup_geometry(self):

        self.scale = 0.52

        self.base_y = -2.1

        self.left_x = -4.8

        self.height_1 = 2 * self.scale
        self.width_1 = 5 * self.scale

        self.height_2 = 3 * self.scale
        self.width_2 = 8 * self.scale

        self.total_width = 13 * self.scale
        self.total_height = 5 * self.scale


        # ----------------------------------------------------
        # FIRST TRIANGLE
        # ----------------------------------------------------

        self.A1 = np.array([
            self.left_x,
            self.base_y,
            0,
        ])

        self.B1 = np.array([
            self.left_x + self.width_1,
            self.base_y,
            0,
        ])

        self.C1 = np.array([
            self.left_x + self.width_1,
            self.base_y + self.height_1,
            0,
        ])


        # ----------------------------------------------------
        # SECOND TRIANGLE
        # ----------------------------------------------------

        self.A2 = np.array([
            self.left_x + self.width_1,
            self.base_y,
            0,
        ])

        self.B2 = np.array([
            self.left_x + self.total_width,
            self.base_y,
            0,
        ])

        self.C2 = np.array([
            self.left_x + self.total_width,
            self.base_y + self.total_height,
            0,
        ])


        # ----------------------------------------------------
        # SLOPE POINTS
        # ----------------------------------------------------

        self.slope1_start = self.A1
        self.slope1_end = self.C1

        self.slope2_start = self.A2
        self.slope2_end = self.C2


        # ----------------------------------------------------
        # COMMON BASE
        # ----------------------------------------------------

        self.base_start = self.A1

        self.base_end = self.B2


    # ========================================================
    # PIECES
    # ========================================================

    def create_pieces(self):

        self.triangle_1 = Polygon(
            self.A1,
            self.B1,
            self.C1,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color="#4C78A8",
            fill_opacity=1,
        )


        self.triangle_2 = Polygon(
            self.A2,
            self.B2,
            self.C2,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color="#F58518",
            fill_opacity=1,
        )


        self.triangle_group = VGroup(
            self.triangle_1,
            self.triangle_2,
        )


    # ========================================================
    # MAIN OBJECTS
    # ========================================================

    def create_main_objects(self):

        self.base_line = Line(
            self.base_start,
            self.base_end,
            stroke_color=BLACK,
            stroke_width=3,
        )


        self.left_vertical = Line(
            self.A1,
            self.C1,
            stroke_color=BLACK,
            stroke_width=3,
        )


        self.right_vertical = Line(
            self.B2,
            self.C2,
            stroke_color=BLACK,
            stroke_width=3,
        )


        self.outer_triangle = VGroup(
            self.base_line,
            self.left_vertical,
            self.right_vertical,
        )


    # ========================================================
    # SLOPE OBJECTS
    # ========================================================

    def create_slope_objects(self):

        self.hypotenuse_1 = Line(
            self.A1,
            self.C1,
            stroke_color=BLACK,
            stroke_width=5,
        )


        self.hypotenuse_2 = Line(
            self.A2,
            self.C2,
            stroke_color=BLACK,
            stroke_width=5,
        )


        self.hypotenuse_1.set_z_index(5)

        self.hypotenuse_2.set_z_index(5)


    # ========================================================
    # LABELS
    # ========================================================

    def create_labels(self):

        self.label_5 = MathTex(
            "5",
            color=BLACK,
        ).scale(0.5)


        self.label_2 = MathTex(
            "2",
            color=BLACK,
        ).scale(0.5)


        self.label_8 = MathTex(
            "8",
            color=BLACK,
        ).scale(0.5)


        self.label_3 = MathTex(
            "3",
            color=BLACK,
        ).scale(0.5)


        self.label_5.next_to(
            self.base_line,
            DOWN,
            buff=0.15,
        )


        self.label_2.next_to(
            self.left_vertical,
            LEFT,
            buff=0.15,
        )


        self.label_8.move_to(
            (
                self.A2
                +
                self.B2
            )
            / 2
            +
            DOWN * 0.25
        )


        self.label_3.next_to(
            self.right_vertical,
            RIGHT,
            buff=0.15,
        )


        self.title = Text(
            "Look carefully at the slanted edges",
            font_size=32,
            color=BLACK,
        )


        self.title.to_edge(
            UP,
            buff=0.4,
        )


    # ========================================================
    # OPENING
    # ========================================================

    def opening(self):

        self.wait(1)

        self.play(
            FadeIn(
                self.title,
                shift=DOWN * 0.2,
            ),
            run_time=0.8,
        )

        self.wait(0.5)


    # ========================================================
    # SHOW TRIANGLES
    # ========================================================

    def show_two_triangles(self):

        self.play(
            FadeIn(
                self.triangle_1,
                shift=UP * 0.2,
            ),
            run_time=0.8,
        )


        self.play(
            FadeIn(
                self.triangle_2,
                shift=UP * 0.2,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        self.play(
            FadeIn(
                self.label_5
            ),
            FadeIn(
                self.label_2
            ),
            FadeIn(
                self.label_8
            ),
            FadeIn(
                self.label_3
            ),
            run_time=0.7,
        )


        self.wait(1)


    # ========================================================
    # COMPARE SLOPES
    # ========================================================

    def compare_slopes(self):

        first_highlight = SurroundingRectangle(
            self.triangle_1,
            buff=0.15,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.play(
            Create(
                first_highlight
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        self.play(
            Indicate(
                self.hypotenuse_1,
                scale_factor=1.02,
            ),
            run_time=0.8,
        )


        self.play(
            FadeOut(
                first_highlight
            ),
            run_time=0.3,
        )


        second_highlight = SurroundingRectangle(
            self.triangle_2,
            buff=0.15,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.play(
            Create(
                second_highlight
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        self.play(
            Indicate(
                self.hypotenuse_2,
                scale_factor=1.02,
            ),
            run_time=0.8,
        )


        self.play(
            FadeOut(
                second_highlight
            ),
            run_time=0.3,
        )


        self.wait(0.7)


    # ========================================================
    # SLOPE EQUATIONS
    # ========================================================

    def show_slope_equations(self):

        slope_title = Text(
            "Their slopes",
            font_size=28,
            color=BLACK,
        )


        slope_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                slope_title,
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        slope_1 = MathTex(
            "m_1",
            "=",
            r"\frac{\Delta y}{\Delta x}",
            "=",
            r"\frac{2}{5}",
            color=BLACK,
        ).scale(0.65)


        slope_1.to_edge(
            LEFT,
            buff=0.7,
        )


        slope_1.shift(
            UP * 1.0
        )


        slope_2 = MathTex(
            "m_2",
            "=",
            r"\frac{\Delta y}{\Delta x}",
            "=",
            r"\frac{3}{8}",
            color=BLACK,
        ).scale(0.65)


        slope_2.to_edge(
            LEFT,
            buff=0.7,
        )


        slope_2.shift(
            DOWN * 0.3
        )


        self.play(
            Write(
                slope_1
            ),
            run_time=1,
        )


        self.wait(0.7)


        self.play(
            Write(
                slope_2
            ),
            run_time=1,
        )


        self.wait(1)


        difference = MathTex(
            r"\frac{2}{5}"
            r"\neq"
            r"\frac{3}{8}",
            color=BLACK,
        ).scale(0.75)


        difference.to_edge(
            RIGHT,
            buff=0.8,
        )


        self.play(
            Write(
                difference
            ),
            run_time=0.9,
        )


        self.wait(1)


        self.play(
            Indicate(
                difference,
                scale_factor=1.08,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        self.slope_group = VGroup(
            slope_1,
            slope_2,
            difference,
        )


    # ========================================================
    # OVERLAY HYPOTENUSES
    # ========================================================

    def overlay_hypotenuses(self):

        self.play(
            FadeOut(
                self.slope_group
            ),
            FadeOut(
                self.label_5
            ),
            FadeOut(
                self.label_2
            ),
            FadeOut(
                self.label_8
            ),
            FadeOut(
                self.label_3
            ),
            run_time=0.6,
        )


        self.play(
            Create(
                self.hypotenuse_1
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        self.play(
            Create(
                self.hypotenuse_2
            ),
            run_time=0.8,
        )


        self.wait(1)


        # Add direction indicators.

        arrow_1 = Arrow(
            self.A1,
            self.C1,
            buff=0.1,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.12,
        )


        arrow_2 = Arrow(
            self.A2,
            self.C2,
            buff=0.1,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.12,
        )


        self.play(
            FadeIn(
                arrow_1
            ),
            FadeIn(
                arrow_2
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.play(
            FadeOut(
                arrow_1
            ),
            FadeOut(
                arrow_2
            ),
            run_time=0.4,
        )


    # ========================================================
    # ZOOM
    # ========================================================

    def zoom_to_difference(self):

        intersection_x = (
            self.left_x
            +
            self.width_1
        )

        intersection_y = (
            self.base_y
            +
            self.height_1
        )


        zoom_point = np.array([
            intersection_x,
            intersection_y,
            0,
        ])


        zoom_dot = Dot(
            zoom_point,
            radius=0.06,
            color=BLACK,
        )


        self.play(
            FadeIn(
                zoom_dot
            ),
            run_time=0.4,
        )


        self.wait(0.5)


        self.play(
            self.camera.frame.animate.scale(
                0.62
            ).move_to(
                zoom_point
            ),
            run_time=1.5,
        )


        self.wait(1)


    # ========================================================
    # INTERSECTION
    # ========================================================

    def show_intersection(self):

        intersection_dot = Dot(
            self.C1,
            radius=0.08,
            color=BLACK,
        )


        self.play(
            FadeIn(
                intersection_dot,
                scale=0.5,
            ),
            run_time=0.5,
        )


        self.wait(0.7)


        tangent_1 = Line(
            self.C1 + LEFT * 1.3,
            self.C1 + RIGHT * 1.3,
            stroke_color=BLACK,
            stroke_width=1,
        )


        tangent_1.set_opacity(
            0.15
        )


        self.play(
            Create(
                tangent_1
            ),
            run_time=0.5,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                tangent_1
            ),
            run_time=0.4,
        )


    # ========================================================
    # APPARENT STRAIGHT LINE
    # ========================================================

    def show_apparent_line(self):

        apparent_line = Line(
            self.A1,
            self.B2,
            stroke_color=BLACK,
            stroke_width=2,
        )


        apparent_line.set_opacity(
            0.18
        )


        self.play(
            Create(
                apparent_line
            ),
            run_time=1,
        )


        self.wait(0.7)


        false_line_text = Text(
            "It looks straight...",
            font_size=28,
            color=BLACK,
        )


        false_line_text.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                false_line_text,
            ),
            run_time=0.6,
        )


        self.wait(1)


        self.play(
            FadeOut(
                apparent_line
            ),
            run_time=0.5,
        )


    # ========================================================
    # QUESTION
    # ========================================================

    def question(self):

        self.play(
            self.camera.frame.animate.scale(
                1 / 0.62
            ).move_to(
                ORIGIN
            ),
            run_time=1.4,
        )


        self.wait(0.7)


        question_text = Text(
            "So why does the boundary look straight?",
            font_size=31,
            color=BLACK,
        )


        question_text.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                question_text,
            ),
            run_time=0.7,
        )


        self.wait(2)


        hint = MathTex(
            r"\frac{2}{5}"
            r"\neq"
            r"\frac{3}{8}",
            color=BLACK,
        ).scale(0.85)


        hint.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            FadeIn(
                hint,
                shift=UP * 0.15,
            ),
            run_time=0.7,
        )


        self.wait(2)


        self.play(
            FadeOut(
                hint
            ),
            FadeOut(
                self.title
            ),
            FadeOut(
                self.triangle_group
            ),
            FadeOut(
                self.hypotenuse_1
            ),
            FadeOut(
                self.hypotenuse_2
            ),
            FadeOut(
                self.outer_triangle
            ),
            FadeOut(
                self.base_line
            ),
            FadeOut(
                self.left_vertical
            ),
            FadeOut(
                self.right_vertical
            ),
            run_time=1,
        )


        self.wait(1)
