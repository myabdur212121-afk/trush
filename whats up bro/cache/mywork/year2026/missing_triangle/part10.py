from manim import *
import numpy as np


# ============================================================
# PART 10
# THE MISSING SQUARE WAS NEVER MISSING
#
# Final chapter.
#
# We reconstruct the puzzle from the beginning and then
# replace the visual illusion with the exact geometry.
#
# Main conclusion:
#
#     2/5 != 3/8
#
# Therefore the apparent long diagonal is not one straight
# line.
#
# The tiny slope mismatch produces the apparent missing area.
# ============================================================


class MissingTrianglePart10(MovingCameraScene):

    def construct(self):

        self.camera.background_color = "#F8F5E9"

        self.setup_scene()

        self.create_piece_geometry()

        self.create_original_arrangement()

        self.create_rearranged_arrangement()

        self.create_measurement_objects()

        self.create_equations()

        self.opening()

        self.rebuild_puzzle()

        self_show_original()

        self_show_rearrangement()

        self_create_paradox()

        self_reveal_same_pieces()

        self_reveal_hidden_error()

        self_measure_first_slope()

        self_measure_second_slope()

        self_compare_slopes()

        self_show_tiny_gap()

        self_calculate_gap_area()

        self_show_exact_one()

        self_destroy_illusion()

        self_rebuild_true_geometry()

        self_final_proof()

        self_visual_summary()

        self_final_message()

        self_end_scene()


    # ========================================================
    # SCENE SETUP
    # ========================================================

    def setup_scene(self):

        self.center = ORIGIN

        self.main_scale = 0.55

        self.base = 10

        self.height = 4

        self.left = -4.8

        self.bottom = -2.0


        self.origin = np.array([
            self.left,
            self.bottom,
            0,
        ])


        self.right_point = np.array([
            self.left
            + self.base * self.main_scale,
            self.bottom,
            0,
        ])


        self.top_point = np.array([
            self.left
            + 5.0 * self.main_scale,
            self.bottom
            + self.height * self.main_scale,
            0,
        ])


        self.first_corner = np.array([
            self.left
            + 5.0 * self.main_scale,
            self.bottom
            + 2.0 * self.main_scale,
            0,
        ])


        self.second_corner = np.array([
            self.left
            + self.base * self.main_scale,
            self.bottom
            + 3.0 * self.main_scale,
            0,
        ])


    # ========================================================
    # PIECE GEOMETRY
    # ========================================================

    def create_piece_geometry(self):

        # ----------------------------------------------------
        # First triangular piece.
        # ----------------------------------------------------

        self.piece_A = Polygon(
            self.origin,
            self.origin
            + RIGHT * 5 * self.main_scale,
            self.first_corner,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color="#4C78A8",
            fill_opacity=1,
        )


        # ----------------------------------------------------
        # Second triangular piece.
        # ----------------------------------------------------

        self.piece_B = Polygon(
            self.first_corner,
            self.right_point,
            self.second_corner,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color="#F58518",
            fill_opacity=1,
        )


        # ----------------------------------------------------
        # Lower rectangular piece.
        # ----------------------------------------------------

        self.piece_C = Rectangle(
            width=3.0 * self.main_scale,
            height=2.0 * self.main_scale,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color="#54A24B",
            fill_opacity=1,
        )


        self.piece_C.move_to(
            np.array([
                -1.0,
                -1.45,
                0,
            ])
        )


        # ----------------------------------------------------
        # Upper rectangular piece.
        # ----------------------------------------------------

        self.piece_D = Rectangle(
            width=5.0 * self.main_scale,
            height=2.0 * self.main_scale,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color="#B279A2",
            fill_opacity=1,
        )


        self.piece_D.move_to(
            np.array([
                0.8,
                0.05,
                0,
            ])
        )


        self.pieces = VGroup(
            self.piece_A,
            self.piece_B,
            self.piece_C,
            self.piece_D,
        )


        # ----------------------------------------------------
        # Piece labels.
        # ----------------------------------------------------

        self.label_A = MathTex(
            "A",
            color=BLACK,
        ).scale(0.45)


        self.label_B = MathTex(
            "B",
            color=BLACK,
        ).scale(0.45)


        self.label_C = MathTex(
            "C",
            color=BLACK,
        ).scale(0.45)


        self.label_D = MathTex(
            "D",
            color=BLACK,
        ).scale(0.45)


        self.label_A.move_to(
            self.piece_A.get_center()
        )


        self.label_B.move_to(
            self.piece_B.get_center()
        )


        self.label_C.move_to(
            self.piece_C.get_center()
        )


        self.label_D.move_to(
            self.piece_D.get_center()
        )


        self.labels = VGroup(
            self.label_A,
            self.label_B,
            self.label_C,
            self.label_D,
        )


    # ========================================================
    # ORIGINAL ARRANGEMENT
    # ========================================================

    def create_original_arrangement(self):

        self.original_outline = Polygon(
            self.origin,
            self.right_point,
            self.second_corner,
            self.top_point,
            stroke_color=BLACK,
            stroke_width=4,
            fill_opacity=0,
        )


        self.original_base = Line(
            self.origin,
            self.right_point,
            stroke_color=BLACK,
            stroke_width=4,
        )


        self.original_left = Line(
            self.origin,
            self.top_point,
            stroke_color=BLACK,
            stroke_width=4,
        )


        self.original_right = Line(
            self.right_point,
            self.second_corner,
            stroke_color=BLACK,
            stroke_width=4,
        )


    # ========================================================
    # REARRANGED ARRANGEMENT
    # ========================================================

    def create_rearranged_arrangement(self):

        self.rearranged_A = self.piece_A.copy()

        self.rearranged_B = self.piece_B.copy()

        self.rearranged_C = self.piece_C.copy()

        self.rearranged_D = self.piece_D.copy()


        self.rearranged_A.shift(
            RIGHT * 0.35
        )


        self.rearranged_B.shift(
            LEFT * 0.25
        )


        self.rearranged_C.shift(
            RIGHT * 0.15
            +
            UP * 0.25
        )


        self.rearranged_D.shift(
            LEFT * 0.10
            -
            UP * 0.15
        )


        self.rearranged_pieces = VGroup(
            self.rearranged_A,
            self.rearranged_B,
            self.rearranged_C,
            self.rearranged_D,
        )


    # ========================================================
    # MEASUREMENT OBJECTS
    # ========================================================

    def create_measurement_objects(self):

        self.first_run_line = Line(
            self.origin,
            self.origin
            + RIGHT
            * 5
            * self.main_scale,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.first_rise_line = Line(
            self.origin
            + RIGHT
            * 5
            * self.main_scale,
            self.first_corner,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.second_run_line = Line(
            self.first_corner,
            self.right_point,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.second_rise_line = Line(
            self.right_point,
            self.second_corner,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.first_run_label = MathTex(
            "5",
            color=BLACK,
        ).scale(0.55)


        self.first_rise_label = MathTex(
            "2",
            color=BLACK,
        ).scale(0.55)


        self.second_run_label = MathTex(
            "8",
            color=BLACK,
        ).scale(0.55)


        self.second_rise_label = MathTex(
            "3",
            color=BLACK,
        ).scale(0.55)


        self.first_run_label.next_to(
            self.first_run_line,
            DOWN,
            buff=0.12,
        )


        self.first_rise_label.next_to(
            self.first_rise_line,
            LEFT,
            buff=0.12,
        )


        self.second_run_label.next_to(
            self.second_run_line,
            DOWN,
            buff=0.12,
        )


        self.second_rise_label.next_to(
            self.second_rise_line,
            RIGHT,
            buff=0.12,
        )


    # ========================================================
    # EQUATIONS
    # ========================================================

    def create_equations(self):

        self.slope_1 = MathTex(
            r"m_1=\frac25",
            color=BLACK,
        ).scale(0.9)


        self.slope_2 = MathTex(
            r"m_2=\frac38",
            color=BLACK,
        ).scale(0.9)


        self.slope_difference = MathTex(
            r"\Delta m"
            "="
            r"\frac25-\frac38"
            "="
            r"\frac1{40}",
            color=BLACK,
        ).scale(0.8)


        self.area_formula = MathTex(
            r"A"
            "="
            r"\frac12x^2\Delta m",
            color=BLACK,
        ).scale(0.9)


        self.final_area = MathTex(
            r"\boxed{A_{\text{gap}}=1}",
            color=BLACK,
        ).scale(1.15)


        self.final_truth = MathTex(
            r"""\boxed{
                \text{The ``straight'' edge was never straight.}
            }""",
            color=BLACK,
        ).scale(0.72)


    # ========================================================
    # OPENING
    # ========================================================

    def opening(self):

        self.title = Text(
            "Let's solve the puzzle.",
            font_size=35,
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


        subtitle = Text(
            "One last time. Slowly.",
            font_size=27,
            color=BLACK,
        )


        subtitle.next_to(
            self.title,
            DOWN,
            buff=0.2,
        )


        self.play(
            FadeIn(
                subtitle,
            ),
            run_time=0.6,
        )


        self.wait(1)


        self.subtitle = subtitle


    # ========================================================
    # REBUILD PUZZLE
    # ========================================================

    def rebuild_puzzle(self):

        self.play(
            FadeOut(
                self.subtitle,
            ),
            run_time=0.4,
        )


        self.play(
            Create(
                self.original_base,
            ),
            run_time=0.6,
        )


        self.play(
            Create(
                self.original_left,
            ),
            run_time=0.6,
        )


        self.play(
            Create(
                self.original_right,
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        self.play(
            FadeIn(
                self.pieces,
                lag_ratio=0.1,
            ),
            run_time=1,
        )


        self.wait(0.8)


        self.play(
            FadeIn(
                self.labels,
            ),
            run_time=0.6,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                self.pieces,
                scale_factor=1.02,
            ),
            run_time=0.9,
        )


        self.wait(0.7)


    # ========================================================
    # ORIGINAL VIEW
    # ========================================================

    def self_show_original(self):

        original_title = Text(
            "First arrangement.",
            font_size=31,
            color=BLACK,
        )


        original_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                original_title,
            ),
            run_time=0.6,
        )


        self.wait(0.7)


        self.play(
            Create(
                self.original_outline,
            ),
            run_time=0.9,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                self.original_outline,
                scale_factor=1.02,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


    # ========================================================
    # REARRANGEMENT
    # ========================================================

    def self_show_rearrangement(self):

        rearrange_title = Text(
            "Now rearrange the same pieces.",
            font_size=29,
            color=BLACK,
        )


        rearrange_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                rearrange_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.original_outline,
            ),
            run_time=0.4,
        )


        self.play(
            self.piece_A.animate.shift(
                RIGHT * 0.6
                +
                UP * 0.15,
            ),
            self.label_A.animate.shift(
                RIGHT * 0.6
                +
                UP * 0.15,
            ),
            run_time=0.7,
        )


        self.play(
            self.piece_B.animate.shift(
                LEFT * 0.4
                +
                UP * 0.20,
            ),
            self.label_B.animate.shift(
                LEFT * 0.4
                +
                UP * 0.20,
            ),
            run_time=0.7,
        )


        self.play(
            self.piece_C.animate.shift(
                RIGHT * 0.2
                +
                DOWN * 0.15,
            ),
            self.label_C.animate.shift(
                RIGHT * 0.2
                +
                DOWN * 0.15,
            ),
            run_time=0.7,
        )


        self.play(
            self.piece_D.animate.shift(
                LEFT * 0.25
                +
                DOWN * 0.10,
            ),
            self.label_D.animate.shift(
                LEFT * 0.25
                +
                DOWN * 0.10,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.rearranged_visible = VGroup(
            self.piece_A,
            self.piece_B,
            self.piece_C,
            self.piece_D,
        )


    # ========================================================
    # PARADOX
    # ========================================================

    def self_create_paradox(self):

        paradox_title = Text(
            "It still looks like the same triangle.",
            font_size=30,
            color=BLACK,
        )


        paradox_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                paradox_title,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        apparent_outer = Polygon(
            self.origin + RIGHT * 0.25,
            self.right_point + RIGHT * 0.25,
            self.top_point + RIGHT * 0.25,
            stroke_color=BLACK,
            stroke_width=4,
            fill_opacity=0,
        )


        self.play(
            Create(
                apparent_outer,
            ),
            run_time=0.9,
        )


        self.wait(0.7)


        self.apparent_outer = apparent_outer


        gap_region = Polygon(
            self.first_corner + RIGHT * 0.25,
            self.second_corner + RIGHT * 0.25,
            self.second_corner + RIGHT * 0.45,
            self.first_corner + RIGHT * 0.45,
            stroke_color=BLACK,
            stroke_width=2,
            fill_opacity=0,
        )


        self.play(
            FadeIn(
                gap_region,
            ),
            run_time=0.5,
        )


        self.wait(0.7)


        mystery = Text(
            "Where did this space come from?",
            font_size=27,
            color=BLACK,
        )


        mystery.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            FadeIn(
                mystery,
            ),
            run_time=0.7,
        )


        self.wait(1)


        self.mystery = mystery
        self.gap_region = gap_region


    # ========================================================
    # SAME PIECES
    # ========================================================

    def self_reveal_same_pieces(self):

        same_title = Text(
            "Notice something important.",
            font_size=30,
            color=BLACK,
        )


        same_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                same_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.mystery,
                self.gap_region,
            ),
            run_time=0.5,
        )


        self.play(
            LaggedStart(
                Indicate(
                    self.piece_A,
                    scale_factor=1.05,
                ),
                Indicate(
                    self.piece_B,
                    scale_factor=1.05,
                ),
                Indicate(
                    self.piece_C,
                    scale_factor=1.05,
                ),
                Indicate(
                    self.piece_D,
                    scale_factor=1.05,
                ),
                lag_ratio=0.15,
            ),
            run_time=2,
        )


        self.wait(0.7)


        same_text = MathTex(
            r"\text{same four pieces}",
            color=BLACK,
        ).scale(0.8)


        same_text.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            Write(
                same_text,
            ),
            run_time=0.7,
        )


        self.wait(1)


        self.same_text = same_text


    # ========================================================
    # HIDDEN ERROR
    # ========================================================

    def self_reveal_hidden_error(self):

        hidden_title = Text(
            "So the piec
