from manim import *
import numpy as np


# ============================================================
# PART 5
# AREA CANNOT DISAPPEAR
#
# Main idea:
#
# The pieces have fixed areas.
#
# Rearranging them cannot magically create or destroy area.
#
# So if one arrangement appears to have one extra square,
# something about the large outer shape must be misleading.
#
# This part investigates the area before revealing the
# complete geometric trick.
# ============================================================


class MissingTrianglePart5(MovingCameraScene):

    def construct(self):

        self.camera.background_color = "#F8F5E9"

        self.setup_geometry()

        self.create_original_pieces()

        self.create_area_labels()

        self.create_first_arrangement()

        self.create_second_arrangement()

        self.create_area_equations()

        self.opening()

        self.show_all_pieces()

        self.introduce_area_idea()

        self.calculate_piece_areas()

        self.calculate_total_area()

        self.show_first_arrangement()

        self.show_second_arrangement()

        self.compare_arrangements()

        self.highlight_missing_region()

        self.calculate_missing_area()

        self.show_area_conservation()

        self.prepare_final_question()

        self.end_part()


    # ========================================================
    # GEOMETRY SETUP
    # ========================================================

    def setup_geometry(self):

        self.s = 0.5

        self.origin = np.array([
            -4.5,
            -2.0,
            0,
        ])


        # ----------------------------------------------------
        # Dimensions of the two small triangles
        # ----------------------------------------------------

        self.small_triangle_height = 2

        self.small_triangle_base = 5


        self.large_triangle_height = 3

        self.large_triangle_base = 8


        # ----------------------------------------------------
        # Dimensions of the full outer rectangle-like extent
        # ----------------------------------------------------

        self.total_base = 13

        self.total_height = 5


        # ----------------------------------------------------
        # Useful screen dimensions
        # ----------------------------------------------------

        self.base_screen_length = (
            self.total_base
            * self.s
        )


        self.height_screen_length = (
            self.total_height
            * self.s
        )


        # ----------------------------------------------------
        # First arrangement reference points
        # ----------------------------------------------------

        self.A = self.origin.copy()


        self.B = (
            self.A
            + RIGHT
            * self.small_triangle_base
            * self.s
        )


        self.C = (
            self.B
            + UP
            * self.small_triangle_height
            * self.s
        )


        self.D = (
            self.B
            + RIGHT
            * self.large_triangle_base
            * self.s
        )


        self.E = (
            self.D
            + UP
            * self.large_triangle_height
            * self.s
        )


        # ----------------------------------------------------
        # Outer top point
        # ----------------------------------------------------

        self.top_point = (
            self.A
            + RIGHT
            * self.total_base
            * self.s
            + UP
            * self.total_height
            * self.s
        )


        # ----------------------------------------------------
        # Shift used for separated pieces
        # ----------------------------------------------------

        self.piece_display_origin = np.array([
            -4.8,
            -1.2,
            0,
        ])


    # ========================================================
    # ORIGINAL PIECES
    # ========================================================

    def create_original_pieces(self):

        # ----------------------------------------------------
        # Triangle with base 5 and height 2
        # ----------------------------------------------------

        self.triangle_5_2 = Polygon(
            ORIGIN,
            RIGHT * 5 * self.s,
            RIGHT * 5 * self.s
            + UP * 2 * self.s,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color="#5B8FF9",
            fill_opacity=1,
        )


        self.triangle_5_2.move_to(
            self.piece_display_origin
            + LEFT * 1.0
        )


        # ----------------------------------------------------
        # Triangle with base 8 and height 3
        # ----------------------------------------------------

        self.triangle_8_3 = Polygon(
            ORIGIN,
            RIGHT * 8 * self.s,
            RIGHT * 8 * self.s
            + UP * 3 * self.s,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color="#F6BD16",
            fill_opacity=1,
        )


        self.triangle_8_3.move_to(
            self.piece_display_origin
            + RIGHT * 2.5
            + DOWN * 0.2
        )


        # ----------------------------------------------------
        # A small rectangular piece
        # ----------------------------------------------------

        self.rectangle_piece = Rectangle(
            width=3 * self.s,
            height=2 * self.s,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color="#61DDAA",
            fill_opacity=1,
        )


        self.rectangle_piece.move_to(
            self.piece_display_origin
            + LEFT * 2.0
            + DOWN * 1.7
        )


        # ----------------------------------------------------
        # A second rectangular piece
        # ----------------------------------------------------

        self.rectangle_piece_2 = Rectangle(
            width=5 * self.s,
            height=3 * self.s,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color="#65789B",
            fill_opacity=1,
        )


        self.rectangle_piece_2.move_to(
            self.piece_display_origin
            + RIGHT * 2.0
            + DOWN * 2.0
        )


        # ----------------------------------------------------
        # Group
        # ----------------------------------------------------

        self.all_pieces = VGroup(
            self.triangle_5_2,
            self.triangle_8_3,
            self.rectangle_piece,
            self.rectangle_piece_2,
        )


        self.all_pieces.set_z_index(2)


    # ========================================================
    # AREA LABELS
    # ========================================================

    def create_area_labels(self):

        self.area_triangle_5_2 = MathTex(
            r"A_1"
            r"="
            r"\frac12(5)(2)"
            r"="
            r"5",
            color=BLACK,
        ).scale(0.55)


        self.area_triangle_8_3 = MathTex(
            r"A_2"
            r"="
            r"\frac12(8)(3)"
            r"="
            r"12",
            color=BLACK,
        ).scale(0.55)


        self.area_rectangle_1 = MathTex(
            r"A_3"
            r"="
            r"(3)(2)"
            r"="
            r"6",
            color=BLACK,
        ).scale(0.55)


        self.area_rectangle_2 = MathTex(
            r"A_4"
            r"="
            r"(5)(3)"
            r"="
            r"15",
            color=BLACK,
        ).scale(0.55)


        self.area_triangle_5_2.next_to(
            self.triangle_5_2,
            DOWN,
            buff=0.2,
        )


        self.area_triangle_8_3.next_to(
            self.triangle_8_3,
            DOWN,
            buff=0.2,
        )


        self.area_rectangle_1.next_to(
            self.rectangle_piece,
            DOWN,
            buff=0.2,
        )


        self.area_rectangle_2.next_to(
            self.rectangle_piece_2,
            DOWN,
            buff=0.2,
        )


        self.area_labels = VGroup(
            self.area_triangle_5_2,
            self.area_triangle_8_3,
            self.area_rectangle_1,
            self.area_rectangle_2,
        )


    # ========================================================
    # FIRST ARRANGEMENT
    # ========================================================

    def create_first_arrangement(self):

        # ----------------------------------------------------
        # This arrangement is deliberately shown as a clean
        # composite figure.
        # ----------------------------------------------------

        self.first_base = Line(
            self.A,
            self.D,
            stroke_color=BLACK,
            stroke_width=3,
        )


        self.first_left = Line(
            self.A,
            self.A + UP * 5 * self.s,
            stroke_color=BLACK,
            stroke_width=3,
        )


        self.first_right = Line(
            self.D,
            self.D + UP * 5 * self.s,
            stroke_color=BLACK,
            stroke_width=3,
        )


        self.first_top = Line(
            self.A + UP * 5 * self.s,
            self.D + UP * 5 * self.s,
            stroke_color=BLACK,
            stroke_width=3,
        )


        self.first_outline = VGroup(
            self.first_base,
            self.first_left,
            self.first_right,
            self.first_top,
        )


        self.first_outline.set_opacity(0)


    # ========================================================
    # SECOND ARRANGEMENT
    # ========================================================

    def create_second_arrangement(self):

        self.second_shift = RIGHT * 0.5


        self.second_base = Line(
            self.A + self.second_shift,
            self.D + self.second_shift,
            stroke_color=BLACK,
            stroke_width=3,
        )


        self.second_left = Line(
            self.A + self.second_shift,
            self.A
            + self.second_shift
            + UP * 5 * self.s,
            stroke_color=BLACK,
            stroke_width=3,
        )


        self.second_right = Line(
            self.D + self.second_shift,
            self.D
            + self.second_shift
            + UP * 5 * self.s,
            stroke_color=BLACK,
            stroke_width=3,
        )


        self.second_top = Line(
            self.A
            + self.second_shift
            + UP * 5 * self.s,
            self.D
            + self.second_shift
            + UP * 5 * self.s,
            stroke_color=BLACK,
            stroke_width=3,
        )


        self.second_outline = VGroup(
            self.second_base,
            self.second_left,
            self.second_right,
            self.second_top,
        )


        self.second_outline.set_opacity(0)


    # ========================================================
    # AREA EQUATIONS
    # ========================================================

    def create_area_equations(self):

        self.total_area_equation = MathTex(
            r"A_{\mathrm{total}}"
            "="
            r"A_1+A_2+A_3+A_4",
            color=BLACK,
        ).scale(0.72)


        self.total_area_numbers = MathTex(
            r"="
            r"5+12+6+15",
            color=BLACK,
        ).scale(0.72)


        self.total_area_result = MathTex(
            r"="
            r"38",
            color=BLACK,
        ).scale(0.85)


        self.area_conservation = MathTex(
            r"A_{\mathrm{before}}"
            "="
            r"A_{\mathrm{after}}",
            color=BLACK,
        ).scale(0.85)


        self.area_difference = MathTex(
            r"\Delta A=1",
            color=BLACK,
        ).scale(0.9)


    # ========================================================
    # OPENING
    # ========================================================

    def opening(self):

        self.title = Text(
            "Before we chase the missing square...",
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
                shift=DOWN * 0.2,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        subtitle = Text(
            "let's count the area.",
            font_size=29,
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
                shift=UP * 0.1,
            ),
            run_time=0.6,
        )


        self.wait(1)


        self.subtitle = subtitle


    # ========================================================
    # SHOW ALL PIECES
    # ========================================================

    def show_all_pieces(self):

        self.play(
            FadeIn(
                self.triangle_5_2,
                shift=UP * 0.3,
            ),
            run_time=0.7,
        )


        self.play(
            FadeIn(
                self.triangle_8_3,
                shift=UP * 0.3,
            ),
            run_time=0.7,
        )


        self.play(
            FadeIn(
                self.rectangle_piece,
                shift=UP * 0.3,
            ),
            run_time=0.7,
        )


        self.play(
            FadeIn(
                self.rectangle_piece_2,
                shift=UP * 0.3,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.play(
            FadeOut(
                self.subtitle,
            ),
            run_time=0.4,
        )


    # ========================================================
    # AREA IDEA
    # ========================================================

    def introduce_area_idea(self):

        area_title = Text(
            "Every piece has a fixed area.",
            font_size=31,
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
            run_time=0.6,
        )


        self.wait(0.6)


        area_statement = MathTex(
            r"\text{Rearranging}"
            r"\quad\neq\quad"
            r"\text{changing area}",
            color=BLACK,
        ).scale(0.72)


        area_statement.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            Write(
                area_statement,
            ),
            run_time=1,
        )


        self.wait(1)


        self.area_statement = area_statement


    # ========================================================
    # CALCULATE PIECE AREAS
    # ========================================================

    def calculate_piece_areas(self):

        self.play(
            FadeOut(
                self.area_statement,
            ),
            run_time=0.4,
        )


        # ----------------------------------------------------
        # Triangle 1
        # ----------------------------------------------------

        self.play(
            Indicate(
                self.triangle_5_2,
                scale_factor=1.05,
            ),
            run_time=0.7,
        )


        self.area_triangle_5_2.next_to(
            self.triangle_5_2,
            DOWN,
            buff=0.2,
        )


        self.play(
            Write(
                self.area_triangle_5_2,
            ),
            run_time=1,
        )


        self.wait(0.5)


        # ----------------------------------------------------
        # Triangle 2
        # ----------------------------------------------------

        self.play(
            Indicate(
                self.triangle_8_3,
                scale_factor=1.05,
            ),
            run_time=0.7,
        )


        self.play(
            Write(
                self.area_triangle_8_3,
            ),
            run_time=1,
        )


        self.wait(0.5)


        # ----------------------------------------------------
        # Rectangle 1
        # ----------------------------------------------------

        self.play(
            Indicate(
                self.rectangle_piece,
                scale_factor=1.05,
            ),
            run_time=0.7,
        )


        self.play(
            Write(
                self.area_rectangle_1,
            ),
            run_time=1,
        )


        self.wait(0.5)


        # ----------------------------------------------------
        # Rectangle 2
        # ----------------------------------------------------

        self.play(
            Indicate(
                self.rectangle_piece_2,
                scale_factor=1.05,
            ),
            run_time=0.7,
        )


        self.play(
            Write(
                self.area_rectangle_2,
            ),
            run_time=1,
        )


        self.wait(1)


    # ========================================================
    # TOTAL AREA
    # ========================================================

    def calculate_total_area(self):

        self.play(
            FadeOut(
                self.area_labels,
            ),
            run_time=0.5,
        )


        total_title = Text(
            "Now add everything.",
            font_size=30,
            color=BLACK,
        )


        total_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                total_title,
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        self.total_area_equation.move_to(
            UP * 1.0,
        )


        self.play(
            Write(
                self.total_area_equation,
            ),
            run_time=1,
        )


        self.wait(0.5)


        self.total_area_numbers.next_to(
            self.total_area_equation,
            DOWN,
            buff=0.3,
        )


        self.play(
            Write(
                self.total_area_numbers,
            ),
            run_time=0.9,
        )


        self.wait(0.5)


        self.total_area_result.next_to(
            self.total_area_numbers,
            DOWN,
            buff=0.3,
        )


        self.play(
            Write(
                self.total_area_result,
            ),
            run_time=0.8,
        )


        self.wait(1)


        self.play(
            Indicate(
                self.total_area_result,
                scale_factor=1.12,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        self.total_area_group = VGroup(
            self.total_area_equation,
            self.total_area_numbers,
            self.total_area_result,
        )


    # ========================================================
    # FIRST ARRANGEMENT
    # ========================================================

    def show_first_arrangement(self):

        self.play(
            FadeOut(
                self.total_area_group,
            ),
            run_time=0.5,
        )


        first_title = Text(
            "Arrangement A",
            font_size=31,
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


        # ----------------------------------------------------
        # Move the pieces toward a common arrangement.
        # ----------------------------------------------------

        self.target_triangle_1 = Polygon(
            self.A,
            self.B,
            self.C,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color="#5B8FF9",
            fill_opacity=1,
        )


        self.target_triangle_2 = Polygon(
            self.B,
            self.D,
            self.E,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color="#F6BD16",
            fill_opacity=1,
        )


        self.target_rectangle_1 = Rectangle(
            width=3 * self.s,
            height=2 * self.s,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color="#61DDAA",
            fill_opacity=1,
        )


        self.target_rectangle_1.move_to(
            self.B
            + RIGHT * 1.5 * self.s
            + UP * 1.0 * self.s,
        )


        self.target_rectangle_2 = Rectangle(
            width=5 * self.s,
            height=3 * self.s,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color="#65789B",
            fill_opacity=1,
        )


        self.target_rectangle_2.move_to(
            self.B
            + RIGHT * 2.5 * self.s
            + UP * 3.5 * self.s,
        )


        # ----------------------------------------------------
        # We do not physically claim these are exact puzzle
        # pieces yet. They are visual area regions.
        # ----------------------------------------------------

        self.play(
            FadeOut(
                self.all_pieces,
            ),
            run_time=0.5,
        )


        self.play(
            FadeIn(
                self.target_triangle_1,
            ),
            FadeIn(
                self.target_triangle_2,
            ),
            FadeIn(
                self.target_rectangle_1,
            ),
            FadeIn(
                self.target_rectangle_2,
            ),
            run_time=1,
        )


        self.wait(1)


        self.first_arrangement_objects = VGroup(
            self.target_triangle_1,
            self.target_triangle_2,
            self.target_rectangle_1,
            self.target_rectangle_2,
        )


    # ========================================================
    # SECOND ARRANGEMENT
    # ========================================================

    def show_second_arrangement(self):

        second_title = Text(
            "Arrangement B",
            font_size=31,
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


        self.wait(0.6)


        # ----------------------------------------------------
        # Shift pieces.
        #
        # The important storytelling point:
        #
        # visually the outside boundary appears almost the
        # same, but the internal relationship changes.
        # ----------------------------------------------------

        self.second_triangle_1 = self.target_triangle_1.copy()

        self.second_triangle_2 = self.target_triangle_2.copy()

        self.second_rectangle_1 = self.target_rectangle_1.copy()

        self.second_rectangle_2 = self.target_rectangle_2.copy()


        self.second_triangle_1.shift(
            RIGHT * 0.45,
        )


        self.second_triangle_2.shift(
            LEFT * 0.30,
            UP * 0.15,
        )


        self.second_rectangle_1.shift(
            RIGHT * 0.15,
            DOWN * 0.12,
        )


        self.second_rectangle_2.shift(
            LEFT * 0.25,
            DOWN * 0.05,
        )


        self.second_arrangement_objects = VGroup(
            self.second_triangle_1,
            self.second_triangle_2,
            self.second_rectangle_1,
            self.second_rectangle_2,
        )


        self.play(
            ReplacementTransform(
                self.target_triangle_1,
                self.second_triangle_1,
            ),
            ReplacementTransform(
                self.target_triangle_2,
                self.second_triangle_2,
            ),
            ReplacementTransform(
                self.target_rectangle_1,
                self.second_rectangle_1,
            ),
            ReplacementTransform(
                self.target_rectangle_2,
                self.second_rectangle_2,
            ),
            run_time=1.5,
        )


        self.wait(1)


    # ========================================================
    # COMPARE ARRANGEMENTS
    # ========================================================

    def compare_arrangements(self):

        compare_title = Text(
            "Same pieces. Same total area.",
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


        self.wait(0.7)


        same_area = MathTex(
            r"A_A=A_B",
            color=BLACK,
        ).scale(0.9)


        same_area.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            Write(
                same_area,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        self.play(
            Indicate(
                same_area,
                scale_factor=1.1,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        self.same_area = same_area


    # ========================================================
    # HIGHLIGHT MISSING REGION
    # ========================================================

    def highlight_missing_region(self):

        self.play(
            FadeOut(
                self.same_area,
            ),
            run_time=0.4,
        )


        mystery_title = Text(
            "But the picture seems to have an extra square.",
            font_size=28,
            color=BLACK,
        )


        mystery_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                mystery_title,
            ),
            run_time=0.7,
        )


        self.wait(0.7)


        # ----------------------------------------------------
        # Create a deliberately highlighted unit-square region.
        # ----------------------------------------------------

        self.mystery_square = Square(
            side_length=0.5,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color="#F8F5E9",
            fill_opacity=1,
        )


        self.mystery_square.move_to(
            self.second_arrangement_objects.get_center()
            + RIGHT * 1.0
            + DOWN * 0.3,
        )


        self.mystery_square.set_z_index(20)


        self.play(
            Create(
                self.mystery_square,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.one_square = MathTex(
            r"1",
            color=BLACK,
        ).scale(0.6)


        self.one_square.move_to(
            self.mystery_square,
        )


        self.play(
            FadeIn(
                self.one_square,
                scale=0.5,
            ),
            run_time=0.5,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                self.mystery_square,
                scale_factor=1.15,
            ),
            run_time=0.8,
        )


        self.wait(1)


    # ========================================================
    # CALCULATE MISSING AREA
    # ========================================================

    def calculate_missing_area(self):

        calculation_title = Text(
            "How much area is apparently missing?",
            font_size=29,
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
            run_time=0.7,
        )


        self.wait(0.6)


        self.play(
            FadeOut(
                self.one_square,
            ),
            FadeOut(
                self.mystery_square,
            ),
            run_time=0.4,
        )


        # ----------------------------------------------------
        # Area difference calculation
        # ----------------------------------------------------

        difference_step_1 = MathTex(
            r"\Delta A"
            "="
            r"A_{\mathrm{large}}"
            "-"
            r"A_{\mathrm{pieces}}",
            color=BLACK,
        ).scale(0.68)


        difference_step_1.move_to(
            UP * 1.0,
        )


        self.play(
            Write(
                difference_step_1,
            ),
            run_time=0.9,
        )


        self.wait(0.6)


        difference_step_2 = MathTex(
            r"\Delta A"
            "="
            r"39"
            "-"
            r"38",
            color=BLACK,
        ).scale(0.75)


        difference_step_2.next_to(
            difference_step_1,
            DOWN,
            buff=0.35,
        )


        self.play(
            Write(
                difference_step_2,
            ),
            run_time=0.8,
        )


        self.wait(0.6)


        difference_result = MathTex(
            r"\boxed{\Delta A=1}",
            color=BLACK,
        ).scale(0.85)


        difference_result.next_to(
            difference_step_2,
            DOWN,
            buff=0.35,
        )


        self.play(
            Write(
                difference_result,
            ),
            run_time=0.9,
        )


        self.wait(1)


        self.play(
            Indicate(
                difference_result,
                scale_factor=1.12,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        self.difference_group = VGroup(
            difference_step_1,
            difference_step_2,
            difference_result,
        )


    # ========================================================
    # AREA CONSERVATION
    # ========================================================

    def show_area_conservation(self):

        self.play(
            FadeOut(
                self.difference_group,
            ),
            run_time=0.5,
        )


        conservation_title = Text(
            "But area cannot simply appear.",
            font_size=31,
            color=BLACK,
        )


        conservation_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                conservation_title,
            ),
            run_time=0.7,
        )


        self.wait(0.7)


        conservation_equation = MathTex(
            r"A_{\mathrm{before}}"
            "="
            r"A_{\mathrm{after}}",
            color=BLACK,
        ).scale(1.0)


        conservation_equation.move_to(
            ORIGIN
            +
            UP * 0.5,
        )


        self.play(
            Write(
                conservation_equation,
            ),
            run_time=1,
        )


        self.wait(0.8)


        conservation_text = Text(
            "Rearrangement preserves area.",
            font_size=28,
            color=BLACK,
        )


        conservation_text.next_to(
            conservation_equation,
            DOWN,
            buff=0.4,
        )


        self.play(
            FadeIn(
                conservation_text,
                shift=UP * 0.15,
            ),
            run_time=0.7,
        )


        self.wait(1)


        self.play(
            Indicate(
                conservation_equation,
                scale_factor=1.08,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        self.conservation_group = VGroup(
            conservation_equation,
            conservation_text,
        )


    # ========================================================
    # PREPARE FINAL QUESTION
    # ========================================================

    def prepare_final_question(self):

        self.play(
            FadeOut(
                self.conservation_group,
            ),
            run_time=0.5,
        )


        question_title = Text(
            "Then where did the extra 1 unit come from?",
            font_size=31,
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


        mystery_equation = MathTex(
            r"39-38=1",
            color=BLACK,
        ).scale(0.9)


        mystery_equation.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                mystery_equation,
            ),
            run_time=0.9,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                mystery_equation,
                scale_factor=1.1,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        # ----------------------------------------------------
        # Small visual pulse around the number 1.
        # ----------------------------------------------------

        one_circle = Circle(
            radius=0.35,
            stroke_color=BLACK,
            stroke_width=2,
        )


        one_circle.move_to(
            mystery_equation.get_right()
            + LEFT * 0.18,
        )


        self.play(
            Create(
                one_circle,
            ),
            run_time=0.5,
        )


        self.wait(0.6)


        self.play(
            FadeOut(
                one_circle,
            ),
            run_time=0.4,
        )


        self.mystery_equation = mystery_equation


    # ========================================================
    # END
    # ========================================================

    def end_part(self):

        self.play(
            FadeOut(
                self.mystery_equation,
            ),
            run_time=0.5,
        )


        final_question = Text(
            "The pieces did not change...",
            font_size=30,
            color=BLACK,
        )


        final_question.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                final_question,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        final_statement = MathTex(
            r"\text{So something about the ``large triangle'' must be wrong.}",
            color=BLACK,
        ).scale(0.65)


        final_statement.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                final_statement,
            ),
            run_time=1.1,
        )


        self.wait(1.2)


        self.play(
            FadeOut(
                final_statement,
            ),
            run_time=0.5,
        )


        hook = Text(
            "Is its hypotenuse really a straight line?",
            font_size=31,
            color=BLACK,
        )


        hook.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            FadeIn(
                hook,
                shift=UP * 0.15,
            ),
            run_time=0.8,
        )


        self.wait(2)


        # ----------------------------------------------------
        # Final cleanup
        # ----------------------------------------------------

        self.play(
            FadeOut(
                self.title,
                hook,
                self.second_arrangement_objects,
                run_time=1,
            ),
        )


        self.wait(1)


# ============================================================
# END OF PART 5
# ============================================================
