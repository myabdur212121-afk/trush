from manim import *
import numpy as np


# ============================================================
# PART 2
# FOUR PIECES UNDER THE MICROSCOPE
# ============================================================

class MissingTrianglePart2(Scene):

    def construct(self):

        self.camera.background_color = "#F8F5E9"

        self.setup_geometry()
        self.create_pieces()
        self.create_labels()
        self.create_dimension_labels()
        self.create_titles()

        self.intro()
        self.show_four_pieces()
        self.show_dimensions()
        self.show_fibonacci_connection()
        self.move_pieces_apart()
        self.show_same_pieces()
        self.first_arrangement()
        self.second_arrangement()
        self.compare_arrangements()
        self.final_question()


    # ========================================================
    # GEOMETRY
    # ========================================================

    def setup_geometry(self):

        self.unit = 0.42

        # Main visual reference:
        #
        # width  = 13
        # height = 5
        #
        # Small triangles:
        # 5 x 2
        # 8 x 3

        self.origin = np.array([-5.0, -1.8, 0])

        self.P0 = self.origin

        self.P1 = self.origin + RIGHT * 5 * self.unit

        self.P2 = self.origin + RIGHT * 13 * self.unit

        self.P3 = self.origin + RIGHT * 13 * self.unit + UP * 5 * self.unit

        self.P4 = self.origin + RIGHT * 5 * self.unit + UP * 2 * self.unit


        # Second important point.

        self.Q = self.origin + RIGHT * 8 * self.unit + UP * 3 * self.unit


        # Dimensions for later parts.

        self.small_triangle_1_base = 5
        self.small_triangle_1_height = 2

        self.small_triangle_2_base = 8
        self.small_triangle_2_height = 3


        # ----------------------------------------------------
        # First right triangle
        # ----------------------------------------------------

        self.triangle_small_1_points = [
            self.P0,
            self.P1,
            self.P4,
        ]


        # ----------------------------------------------------
        # Second right triangle
        # ----------------------------------------------------

        self.triangle_small_2_points = [
            self.P4,
            self.P2,
            self.P3,
        ]


        # ----------------------------------------------------
        # Two middle pieces
        #
        # These are kept as rectilinear pieces.
        # Their exact role will be examined in later parts.
        # ----------------------------------------------------

        x5 = self.P1[0]
        x9 = self.origin[0] + 9 * self.unit
        x13 = self.P2[0]

        y0 = self.origin[1]
        y2 = self.origin[1] + 2 * self.unit
        y5 = self.origin[1] + 5 * self.unit

        self.middle_left_points = [
            np.array([x5, y0, 0]),
            np.array([x9, y0, 0]),
            np.array([x9, y2, 0]),
            np.array([x5, y2, 0]),
        ]

        self.middle_right_points = [
            np.array([x9, y0, 0]),
            np.array([x13, y0, 0]),
            np.array([x13, y2, 0]),
            np.array([x9, y2, 0]),
        ]


    # ========================================================
    # PIECES
    # ========================================================

    def create_pieces(self):

        self.piece_A = Polygon(
            *self.triangle_small_1_points,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color="#4C78A8",
            fill_opacity=1,
        )

        self.piece_B = Polygon(
            *self.triangle_small_2_points,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color="#F58518",
            fill_opacity=1,
        )

        self.piece_C = Polygon(
            *self.middle_left_points,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color="#54A24B",
            fill_opacity=1,
        )

        self.piece_D = Polygon(
            *self.middle_right_points,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color="#B279A2",
            fill_opacity=1,
        )

        self.pieces = VGroup(
            self.piece_A,
            self.piece_B,
            self.piece_C,
            self.piece_D,
        )


    # ========================================================
    # LABELS
    # ========================================================

    def create_labels(self):

        self.label_A = MathTex(
            "A",
            color=BLACK,
        ).scale(0.42)

        self.label_B = MathTex(
            "B",
            color=BLACK,
        ).scale(0.42)

        self.label_C = MathTex(
            "C",
            color=BLACK,
        ).scale(0.42)

        self.label_D = MathTex(
            "D",
            color=BLACK,
        ).scale(0.42)


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
    # DIMENSION LABELS
    # ========================================================

    def create_dimension_labels(self):

        self.dim_5 = MathTex(
            "5",
            color=BLACK,
        ).scale(0.4)

        self.dim_2 = MathTex(
            "2",
            color=BLACK,
        ).scale(0.4)

        self.dim_8 = MathTex(
            "8",
            color=BLACK,
        ).scale(0.4)

        self.dim_3 = MathTex(
            "3",
            color=BLACK,
        ).scale(0.4)


        # First triangle horizontal dimension.

        self.dim_5.next_to(
            Line(
                self.P0,
                self.P1,
            ),
            DOWN,
            buff=0.12,
        )


        # First triangle vertical dimension.

        vertical_2 = Line(
            self.P1,
            self.P4,
        )

        self.dim_2.next_to(
            vertical_2,
            RIGHT,
            buff=0.12,
        )


        # Second triangle horizontal dimension.

        horizontal_8 = Line(
            self.P4,
            self.P2,
        )

        self.dim_8.next_to(
            horizontal_8,
            DOWN,
            buff=0.12,
        )


        # Second triangle vertical dimension.

        vertical_3 = Line(
            self.P2,
            self.P3,
        )

        self.dim_3.next_to(
            vertical_3,
            RIGHT,
            buff=0.12,
        )


        self.dimension_labels = VGroup(
            self.dim_5,
            self.dim_2,
            self.dim_8,
            self.dim_3,
        )


    # ========================================================
    # TITLES
    # ========================================================

    def create_titles(self):

        self.title = Text(
            "Four pieces",
            font_size=34,
            color=BLACK,
        )

        self.title.to_edge(
            UP,
            buff=0.4,
        )


        self.subtitle = Text(
            "Nothing has changed except the arrangement.",
            font_size=24,
            color=BLACK,
        )

        self.subtitle.to_edge(
            DOWN,
            buff=0.35,
        )


        self.question = Text(
            "Are these really the same triangle?",
            font_size=30,
            color=BLACK,
        )

        self.question.to_edge(
            UP,
            buff=0.4,
        )


    # ========================================================
    # INTRO
    # ========================================================

    def intro(self):

        self.wait(0.8)

        self.play(
            FadeIn(
                self.title,
                shift=DOWN * 0.2,
            ),
            run_time=0.7,
        )

        self.wait(0.5)


    # ========================================================
    # SHOW FOUR PIECES
    # ========================================================

    def show_four_pieces(self):

        self.play(
            LaggedStart(
                FadeIn(
                    self.piece_A,
                    shift=UP * 0.2,
                ),
                FadeIn(
                    self.piece_B,
                    shift=UP * 0.2,
                ),
                FadeIn(
                    self.piece_C,
                    shift=UP * 0.2,
                ),
                FadeIn(
                    self.piece_D,
                    shift=UP * 0.2,
                ),
                lag_ratio=0.18,
            ),
            run_time=2,
        )

        self.wait(0.7)


        self.play(
            LaggedStart(
                FadeIn(self.label_A),
                FadeIn(self.label_B),
                FadeIn(self.label_C),
                FadeIn(self.label_D),
                lag_ratio=0.15,
            ),
            run_time=1.4,
        )

        self.wait(0.8)


    # ========================================================
    # DIMENSIONS
    # ========================================================

    def show_dimensions(self):

        self.play(
            LaggedStart(
                FadeIn(self.dim_5),
                FadeIn(self.dim_2),
                FadeIn(self.dim_8),
                FadeIn(self.dim_3),
                lag_ratio=0.18,
            ),
            run_time=1.4,
        )

        self.wait(1)


        # Highlight first triangle.

        self.play(
            Indicate(
                self.piece_A,
                color="#4C78A8",
                scale_factor=1.03,
            ),
            run_time=0.8,
        )

        self.wait(0.3)


        # Highlight second triangle.

        self.play(
            Indicate(
                self.piece_B,
                color="#F58518",
                scale_factor=1.03,
            ),
            run_time=0.8,
        )

        self.wait(0.7)


    # ========================================================
    # FIBONACCI CONNECTION
    # ========================================================

    def show_fibonacci_connection(self):

        fib_text = MathTex(
            "2,\\;3,\\;5,\\;8,\\;13",
            color=BLACK,
        ).scale(0.7)

        fib_text.to_edge(
            DOWN,
            buff=0.35,
        )


        self.play(
            FadeIn(
                fib_text,
                shift=UP * 0.2,
            ),
            run_time=0.8,
        )

        self.wait(0.8)


        fib_arrow_1 = Arrow(
            self.dim_2.get_bottom(),
            fib_text.get_top() + LEFT * 1.1,
            buff=0.1,
            stroke_width=2,
        )

        fib_arrow_2 = Arrow(
            self.dim_3.get_bottom(),
            fib_text.get_top() + RIGHT * 1.1,
            buff=0.1,
            stroke_width=2,
        )


        self.play(
            Create(fib_arrow_1),
            Create(fib_arrow_2),
            run_time=0.7,
        )

        self.wait(0.8)


        self.play(
            FadeOut(fib_arrow_1),
            FadeOut(fib_arrow_2),
            FadeOut(fib_text),
            run_time=0.5,
        )

        self.wait(0.5)


    # ========================================================
    # MOVE PIECES APART
    # ========================================================

    def move_pieces_apart(self):

        self.play(
            self.piece_A.animate.shift(
                LEFT * 2.4
                +
                UP * 0.6
            ),
            self.label_A.animate.shift(
                LEFT * 2.4
                +
                UP * 0.6
            ),
            run_time=1,
        )

        self.wait(0.2)


        self.play(
            self.piece_B.animate.shift(
                RIGHT * 2.4
                +
                UP * 0.6
            ),
            self.label_B.animate.shift(
                RIGHT * 2.4
                +
                UP * 0.6
            ),
            run_time=1,
        )

        self.wait(0.2)


        self.play(
            self.piece_C.animate.shift(
                LEFT * 2.2
                +
                DOWN * 1.0
            ),
            self.label_C.animate.shift(
                LEFT * 2.2
                +
                DOWN * 1.0
            ),
            run_time=1,
        )

        self.wait(0.2)


        self.play(
            self.piece_D.animate.shift(
                RIGHT * 2.2
                +
                DOWN * 1.0
            ),
            self.label_D.animate.shift(
                RIGHT * 2.2
                +
                DOWN * 1.0
            ),
            run_time=1,
        )

        self.wait(1)


    # ========================================================
    # SAME PIECES
    # ========================================================

    def show_same_pieces(self):

        pieces_copy = self.pieces.copy()

        self.play(
            LaggedStart(
                Indicate(
                    self.piece_A,
                    scale_factor=1.04,
                ),
                Indicate(
                    self.piece_B,
                    scale_factor=1.04,
                ),
                Indicate(
                    self.piece_C,
                    scale_factor=1.04,
                ),
                Indicate(
                    self.piece_D,
                    scale_factor=1.04,
                ),
                lag_ratio=0.2,
            ),
            run_time=2,
        )

        self.wait(0.5)


        same_text = Text(
            "same pieces",
            font_size=28,
            color=BLACK,
        )

        same_text.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                same_text,
            ),
            run_time=0.7,
        )

        self.wait(1)


    # ========================================================
    # FIRST ARRANGEMENT
    # ========================================================

    def first_arrangement(self):

        # Remove dimensions.

        self.play(
            FadeOut(
                self.dimension_labels
            ),
            run_time=0.5,
        )


        # Remove current labels.

        self.play(
            FadeOut(
                self.labels
            ),
            run_time=0.4,
        )


        # Current pieces are already separated.
        # Restore their original relative arrangement.

        self.play(
            self.piece_A.animate.shift(
                RIGHT * 2.4
                +
                DOWN * 0.6
            ),
            self.piece_B.animate.shift(
                LEFT * 2.4
                +
                DOWN * 0.6
            ),
            self.piece_C.animate.shift(
                RIGHT * 2.2
                +
                UP * 1.0
            ),
            self.piece_D.animate.shift(
                LEFT * 2.2
                +
                UP * 1.0
            ),
            run_time=1.8,
        )

        self.wait(0.8)


        # Recreate labels at their current centers.

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


        self.play(
            FadeIn(self.labels),
            run_time=0.5,
        )

        self.wait(0.8)


        # Show apparent boundary.

        self.apparent_outline_1 = VGroup(
            Line(
                self.P0,
                self.P1,
                stroke_width=3,
            ),
            Line(
                self.P1,
                self.P4,
                stroke_width=3,
            ),
            Line(
                self.P4,
                self.P3,
                stroke_width=3,
            ),
            Line(
                self.P3,
                self.P2,
                stroke_width=3,
            ),
            Line(
                self.P2,
                self.P0,
                stroke_width=3,
            ),
        )

        self.play(
            Create(
                self.apparent_outline_1
            ),
            run_time=1,
        )

        self.wait(1)


    # ========================================================
    # SECOND ARRANGEMENT
    # ========================================================

    def second_arrangement(self):

        self.play(
            FadeOut(
                self.apparent_outline_1
            ),
            run_time=0.4,
        )


        self.play(
            FadeOut(
                self.labels
            ),
            run_time=0.3,
        )


        # Move the two triangular pieces.

        self.play(
            self.piece_A.animate.shift(
                RIGHT * 2.0
                +
                UP * 0.1
            ),
            run_time=0.9,
        )

        self.play(
            self.piece_B.animate.shift(
                LEFT * 2.0
                +
                DOWN * 0.1
            ),
            run_time=0.9,
        )


        # Middle pieces exchange positions.

        self.play(
            self.piece_C.animate.shift(
                RIGHT * 1.4
            ),
            self.piece_D.animate.shift(
                LEFT * 1.4
            ),
            run_time=0.9,
        )


        self.wait(0.7)


        # New labels.

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


        self.play(
            FadeIn(
                self.labels
            ),
            run_time=0.5,
        )

        self.wait(0.8)


        # Apparent second boundary.

        self.apparent_outline_2 = VGroup(
            Line(
                self.P0 + RIGHT * 0.15,
                self.P1 + RIGHT * 0.15,
                stroke_width=3,
            ),
            Line(
                self.P1 + RIGHT * 0.15,
                self.P4 + RIGHT * 0.15,
                stroke_width=3,
            ),
            Line(
                self.P4 + RIGHT * 0.15,
                self.P3 + RIGHT * 0.15,
                stroke_width=3,
            ),
            Line(
                self.P3 + RIGHT * 0.15,
                self.P2 + RIGHT * 0.15,
                stroke_width=3,
            ),
            Line(
                self.P2 + RIGHT * 0.15,
                self.P0 + RIGHT * 0.15,
                stroke_width=3,
            ),
        )


        self.play(
            Create(
                self.apparent_outline_2
            ),
            run_time=1,
        )

        self.wait(1)


    # ========================================================
    # COMPARISON
    # ========================================================

    def compare_arrangements(self):

        self.play(
            FadeOut(
                self.labels
            ),
            run_time=0.3,
        )


        # Create two compact reference diagrams.

        left_group = VGroup(
            self.piece_A.copy(),
            self.piece_B.copy(),
            self.piece_C.copy(),
            self.piece_D.copy(),
        )

        right_group = VGroup(
            self.piece_A.copy(),
            self.piece_B.copy(),
            self.piece_C.copy(),
            self.piece_D.copy(),
        )


        left_group.scale(
            0.55
        )

        right_group.scale(
            0.55
        )


        left_group.move_to(
            LEFT * 3.0
        )

        right_group.move_to(
            RIGHT * 3.0
        )


        left_title = Text(
            "first arrangement",
            font_size=22,
            color=BLACK,
        )

        right_title = Text(
            "second arrangement",
            font_size=22,
            color=BLACK,
        )


        left_title.next_to(
            left_group,
            DOWN,
            buff=0.3,
        )

        right_title.next_to(
            right_group,
            DOWN,
            buff=0.3,
        )


        self.play(
            FadeIn(left_group),
            FadeIn(left_title),
            FadeIn(right_group),
            FadeIn(right_title),
            run_time=1,
        )

        self.wait(1)


        # Vertical separator.

        separator = DashedLine(
            UP * 2.5,
            DOWN * 2.5,
            stroke_width=1.5,
        )

        separator.set_opacity(
            0.25
        )


        self.play(
            Create(
                separator
            ),
            run_time=0.5,
        )

        self.wait(1)


        # Same-piece statement.

        same_statement = MathTex(
            "A+B+C+D",
            color=BLACK,
        ).scale(0.7)


        same_statement.next_to(
            separator,
            UP,
            buff=0.4,
        )


        self.play(
            FadeIn(
                same_statement
            ),
            run_time=0.6,
        )

        self.wait(1)


        # Equality idea.

        equality = MathTex(
            "=",
            color=BLACK,
        ).scale(0.8)


        equality.next_to(
            same_statement,
            DOWN,
            buff=0.25,
        )


        self.play(
            FadeIn(
                equality
            ),
            run_time=0.4,
        )

        self.wait(0.8)


        self.play(
            FadeOut(
                same_statement
            ),
            FadeOut(
                equality
            ),
            run_time=0.5,
        )


        self.wait(0.7)


        # Remove comparison.

        self.play(
            FadeOut(left_group),
            FadeOut(left_title),
            FadeOut(right_group),
            FadeOut(right_title),
            FadeOut(separator),
            run_time=0.8,
        )


    # ========================================================
    # FINAL QUESTION
    # ========================================================

    def final_question(self):

        self.play(
            FadeOut(
                self.apparent_outline_2
            ),
            run_time=0.5,
        )


        # Bring pieces into a calm central arrangement.

        self.play(
            self.piece_A.animate.shift(
                LEFT * 0.8
            ),
            self.piece_B.animate.shift(
                RIGHT * 0.8
            ),
            self.piece_C.animate.shift(
                LEFT * 0.4
            ),
            self.piece_D.animate.shift(
                RIGHT * 0.4
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.pieces
            ),
            run_time=0.6,
        )


        self.play(
            FadeIn(
                self.question,
                shift=DOWN * 0.15,
            ),
            run_time=0.8,
        )

        self.wait(2)


        self.play(
            FadeOut(
                self.question
            ),
            run_time=0.7,
        )

        self.wait(1)


# ============================================================
# END
# ============================================================
