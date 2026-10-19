from manim import *
import numpy as np


# ============================================================
# PART 1
# THE IMPOSSIBLE TRIANGLE
#
# Goal:
# Introduce the geometric puzzle.
#
# IMPORTANT:
# This file is intentionally structured so that later parts
# can reuse the same geometry and the same visual objects.
#
# Part 1 does NOT reveal the mathematical trick.
# It only establishes:
#
#   1. The original arrangement
#   2. The four pieces
#   3. The rearrangement
#   4. The apparent missing region
#   5. The central question
#
# Part 2 will investigate the pieces.
# ============================================================


# ============================================================
# GLOBAL VISUAL CONSTANTS
# ============================================================

BACKGROUND_COLOR = "#F8F5E9"

PIECE_A_COLOR = "#4C78A8"
PIECE_B_COLOR = "#F58518"
PIECE_C_COLOR = "#54A24B"
PIECE_D_COLOR = "#B279A2"

OUTLINE_COLOR = BLACK

LABEL_COLOR = BLACK

QUESTION_COLOR = BLACK


# ============================================================
# BASIC GEOMETRY HELPERS
# ============================================================

def point(x, y):
    """
    Convert a mathematical 2D coordinate into a Manim point.

    We keep this helper extremely simple because the geometry
    will be reused in later parts.
    """

    return np.array([x, y, 0.0])


def polygon_from_points(*points):
    """
    Construct a Polygon from a sequence of 2D/3D points.

    The helper makes the geometry definitions easier to read.
    """

    return Polygon(
        *points,
        stroke_color=OUTLINE_COLOR,
        stroke_width=2,
        fill_opacity=1,
    )


# ============================================================
# MAIN SCENE
# ============================================================

class MissingTrianglePart1(Scene):

    # --------------------------------------------------------
    # CONSTRUCTOR
    # --------------------------------------------------------

    def construct(self):

        # ----------------------------------------------------
        # BACKGROUND
        # ----------------------------------------------------

        self.camera.background_color = BACKGROUND_COLOR


        # ----------------------------------------------------
        # CREATE THE PUZZLE GEOMETRY
        # ----------------------------------------------------

        self.create_geometry()


        # ----------------------------------------------------
        # CREATE VISUAL OBJECTS
        # ----------------------------------------------------

        self.create_pieces()

        self.create_labels()

        self.create_reference_outlines()

        self.create_question()


        # ----------------------------------------------------
        # RUN THE STORY
        # ----------------------------------------------------

        self.opening()

        self.build_original_triangle()

        self.reveal_pieces()

        self.separate_pieces()

        self.show_piece_identity()

        self.reconstruct_original()

        self.rearrange_pieces()

        self.show_missing_region()

        self.compare_arrangements()

        self.end_part()


    # ========================================================
    # GEOMETRY
    # ========================================================

    def create_geometry(self):

        """
        Define every important geometric point here.

        DO NOT create geometry randomly inside animations.

        This is intentional.

        Part 2 and later parts will inspect these exact points.
        """

        # ----------------------------------------------------
        # ORIGINAL TRIANGLE SCALE
        # ----------------------------------------------------

        self.scale_factor = 0.42


        # ----------------------------------------------------
        # MAIN TRIANGLE POINTS
        # ----------------------------------------------------

        #
        # These coordinates represent the visual triangle
        # used throughout Part 1.
        #
        # The actual mathematical discrepancy will be
        # investigated later.
        #

        self.A = point(-4.0, -1.7)

        self.B = point(4.0, -1.7)

        self.C = point(0.0, 2.1)


        # ----------------------------------------------------
        # INTERNAL CONSTRUCTION POINTS
        # ----------------------------------------------------

        self.D = point(-1.7, -1.7)

        self.E = point(1.7, -1.7)

        self.F = point(-1.8, 0.0)

        self.G = point(1.8, 0.0)


        # ----------------------------------------------------
        # PIECE GEOMETRY
        # ----------------------------------------------------

        #
        # Piece A
        #
        # Left triangular region.
        #

        self.A_points = [
            self.A,
            self.D,
            self.F,
        ]


        #
        # Piece B
        #
        # Right triangular region.
        #

        self.B_points = [
            self.E,
            self.B,
            self.G,
        ]


        #
        # Piece C
        #
        # Upper central region.
        #

        self.C_points = [
            self.F,
            self.C,
            self.G,
        ]


        #
        # Piece D
        #
        # Bottom central region.
        #

        self.D_points = [
            self.D,
            self.E,
            self.G,
            self.F,
        ]


        # ----------------------------------------------------
        # NOTE
        # ----------------------------------------------------

        #
        # The four regions are intentionally kept as separate
        # polygon objects.
        #
        # Later parts can replace these coordinates with the
        # exact Curry-puzzle geometry without changing the
        # animation architecture.
        #


    # ========================================================
    # CREATE PIECES
    # ========================================================

    def create_pieces(self):

        # ----------------------------------------------------
        # PIECE A
        # ----------------------------------------------------

        self.piece_a = polygon_from_points(
            *self.A_points
        )

        self.piece_a.set_fill(
            PIECE_A_COLOR,
            opacity=1
        )


        # ----------------------------------------------------
        # PIECE B
        # ----------------------------------------------------

        self.piece_b = polygon_from_points(
            *self.B_points
        )

        self.piece_b.set_fill(
            PIECE_B_COLOR,
            opacity=1
        )


        # ----------------------------------------------------
        # PIECE C
        # ----------------------------------------------------

        self.piece_c = polygon_from_points(
            *self.C_points
        )

        self.piece_c.set_fill(
            PIECE_C_COLOR,
            opacity=1
        )


        # ----------------------------------------------------
        # PIECE D
        # ----------------------------------------------------

        self.piece_d = polygon_from_points(
            *self.D_points
        )

        self.piece_d.set_fill(
            PIECE_D_COLOR,
            opacity=1
        )


        # ----------------------------------------------------
        # MASTER GROUP
        # ----------------------------------------------------

        self.pieces = VGroup(
            self.piece_a,
            self.piece_b,
            self.piece_c,
            self.piece_d,
        )


        # ----------------------------------------------------
        # PIECE IDENTITY
        # ----------------------------------------------------

        self.piece_names = {
            "A": self.piece_a,
            "B": self.piece_b,
            "C": self.piece_c,
            "D": self.piece_d,
        }


    # ========================================================
    # LABELS
    # ========================================================

    def create_labels(self):

        # ----------------------------------------------------
        # LABEL A
        # ----------------------------------------------------

        self.label_a = MathTex(
            "A",
            color=LABEL_COLOR,
        )

        self.label_a.scale(0.45)

        self.label_a.move_to(
            self.piece_a.get_center()
        )


        # ----------------------------------------------------
        # LABEL B
        # ----------------------------------------------------

        self.label_b = MathTex(
            "B",
            color=LABEL_COLOR,
        )

        self.label_b.scale(0.45)

        self.label_b.move_to(
            self.piece_b.get_center()
        )


        # ----------------------------------------------------
        # LABEL C
        # ----------------------------------------------------

        self.label_c = MathTex(
            "C",
            color=LABEL_COLOR,
        )

        self.label_c.scale(0.45)

        self.label_c.move_to(
            self.piece_c.get_center()
        )


        # ----------------------------------------------------
        # LABEL D
        # ----------------------------------------------------

        self.label_d = MathTex(
            "D",
            color=LABEL_COLOR,
        )

        self.label_d.scale(0.45)

        self.label_d.move_to(
            self.piece_d.get_center()
        )


        # ----------------------------------------------------
        # LABEL GROUP
        # ----------------------------------------------------

        self.labels = VGroup(
            self.label_a,
            self.label_b,
            self.label_c,
            self.label_d,
        )


    # ========================================================
    # REFERENCE OUTLINES
    # ========================================================

    def create_reference_outlines(self):

        # ----------------------------------------------------
        # ORIGINAL TRIANGLE OUTLINE
        # ----------------------------------------------------

        self.original_outline = Polygon(
            self.A,
            self.B,
            self.C,
            stroke_color=OUTLINE_COLOR,
            stroke_width=3,
            fill_opacity=0,
        )


        # ----------------------------------------------------
        # GHOST VERSION
        # ----------------------------------------------------

        self.original_ghost = self.original_outline.copy()

        self.original_ghost.set_stroke(
            color=OUTLINE_COLOR,
            width=2,
            opacity=0.18,
        )


        # ----------------------------------------------------
        # FULL TRIANGLE
        # ----------------------------------------------------

        self.full_triangle = Polygon(
            self.A,
            self.B,
            self.C,
            stroke_color=OUTLINE_COLOR,
            stroke_width=3,
            fill_opacity=0,
        )


    # ========================================================
    # QUESTION
    # ========================================================

    def create_question(self):

        self.question = Text(
            "Where did the missing area come from?",
            color=QUESTION_COLOR,
            font_size=32,
        )

        self.question.to_edge(
            UP,
            buff=0.45
        )

        self.question.set_opacity(0)


    # ========================================================
    # OPENING
    # ========================================================

    def opening(self):

        """
        Start from an empty screen.

        The goal is to make the geometry appear naturally.
        """

        self.wait(1)


    # ========================================================
    # BUILD ORIGINAL TRIANGLE
    # ========================================================

    def build_original_triangle(self):

        # ----------------------------------------------------
        # THREE VERTICES
        # ----------------------------------------------------

        vertex_a = Dot(
            self.A,
            radius=0.055,
            color=BLACK,
        )

        vertex_b = Dot(
            self.B,
            radius=0.055,
            color=BLACK,
        )

        vertex_c = Dot(
            self.C,
            radius=0.055,
            color=BLACK,
        )


        # ----------------------------------------------------
        # SHOW FIRST VERTEX
        # ----------------------------------------------------

        self.play(
            FadeIn(
                vertex_a,
                scale=0.7
            ),
            run_time=0.4,
        )

        self.wait(0.25)


        # ----------------------------------------------------
        # SECOND VERTEX
        # ----------------------------------------------------

        self.play(
            FadeIn(
                vertex_b,
                scale=0.7
            ),
            run_time=0.4,
        )

        self.wait(0.25)


        # ----------------------------------------------------
        # THIRD VERTEX
        # ----------------------------------------------------

        self.play(
            FadeIn(
                vertex_c,
                scale=0.7
            ),
            run_time=0.4,
        )

        self.wait(0.5)


        # ----------------------------------------------------
        # LOWER EDGE
        # ----------------------------------------------------

        lower_edge = Line(
            self.A,
            self.B,
            stroke_color=OUTLINE_COLOR,
            stroke_width=3,
        )

        self.play(
            Create(
                lower_edge
            ),
            run_time=0.7,
        )


        # ----------------------------------------------------
        # LEFT EDGE
        # ----------------------------------------------------

        left_edge = Line(
            self.A,
            self.C,
            stroke_color=OUTLINE_COLOR,
            stroke_width=3,
        )

        self.play(
            Create(
                left_edge
            ),
            run_time=0.7,
        )


        # ----------------------------------------------------
        # RIGHT EDGE
        # ----------------------------------------------------

        right_edge = Line(
            self.C,
            self.B,
            stroke_color=OUTLINE_COLOR,
            stroke_width=3,
        )

        self.play(
            Create(
                right_edge
            ),
            run_time=0.7,
        )


        # ----------------------------------------------------
        # REMOVE TEMPORARY VERTICES
        # ----------------------------------------------------

        self.play(
            FadeOut(
                vertex_a,
                vertex_b,
                vertex_c,
            ),
            run_time=0.4,
        )


        # ----------------------------------------------------
        # SHOW PIECES
        # ----------------------------------------------------

        self.play(
            FadeIn(
                self.pieces
            ),
            run_time=1.0,
        )

        self.wait(1)


    # ========================================================
    # REVEAL PIECES
    # ========================================================

    def reveal_pieces(self):

        # ----------------------------------------------------
        # A
        # ----------------------------------------------------

        self.play(
            Indicate(
                self.piece_a,
                scale_factor=1.03,
                color=PIECE_A_COLOR,
            ),
            run_time=0.8,
        )

        self.wait(0.25)


        # ----------------------------------------------------
        # B
        # ----------------------------------------------------

        self.play(
            Indicate(
                self.piece_b,
                scale_factor=1.03,
                color=PIECE_B_COLOR,
            ),
            run_time=0.8,
        )

        self.wait(0.25)


        # ----------------------------------------------------
        # C
        # ----------------------------------------------------

        self.play(
            Indicate(
                self.piece_c,
                scale_factor=1.03,
                color=PIECE_C_COLOR,
            ),
            run_time=0.8,
        )

        self.wait(0.25)


        # ----------------------------------------------------
        # D
        # ----------------------------------------------------

        self.play(
            Indicate(
                self.piece_d,
                scale_factor=1.03,
                color=PIECE_D_COLOR,
            ),
            run_time=0.8,
        )

        self.wait(0.7)


    # ========================================================
    # SEPARATE PIECES
    # ========================================================

    def separate_pieces(self):

        # ----------------------------------------------------
        # SAVE ORIGINAL POSITIONS
        # ----------------------------------------------------

        self.pieces.save_state()

        self.labels.save_state()


        # ----------------------------------------------------
        # PIECE A TARGET
        # ----------------------------------------------------

        target_a = self.piece_a.copy()

        target_a.shift(
            LEFT * 1.5
            +
            UP * 0.7
        )


        # ----------------------------------------------------
        # PIECE B TARGET
        # ----------------------------------------------------

        target_b = self.piece_b.copy()

        target_b.shift(
            LEFT * 1.2
            +
            DOWN * 0.8
        )


        # ----------------------------------------------------
        # PIECE C TARGET
        # ----------------------------------------------------

        target_c = self.piece_c.copy()

        target_c.shift(
            RIGHT * 1.2
            +
            UP * 0.8
        )


        # ----------------------------------------------------
        # PIECE D TARGET
        # ----------------------------------------------------

        target_d = self.piece_d.copy()

        target_d.shift(
            RIGHT * 1.5
            +
            DOWN * 0.7
        )


        # ----------------------------------------------------
        # MOVE PIECE A
        # ----------------------------------------------------

        self.play(
            self.piece_a.animate.shift(
                LEFT * 1.5
                +
                UP * 0.7
            ),
            self.label_a.animate.shift(
                LEFT * 1.5
                +
                UP * 0.7
            ),
            run_time=1.0,
        )

        self.wait(0.25)


        # ----------------------------------------------------
        # MOVE PIECE B
        # ----------------------------------------------------

        self.play(
            self.piece_b.animate.shift(
                LEFT * 1.2
                +
                DOWN * 0.8
            ),
            self.label_b.animate.shift(
                LEFT * 1.2
                +
                DOWN * 0.8
            ),
            run_time=1.0,
        )

        self.wait(0.25)


        # ----------------------------------------------------
        # MOVE PIECE C
        # ----------------------------------------------------

        self.play(
            self.piece_c.animate.shift(
                RIGHT * 1.2
                +
                UP * 0.8
            ),
            self.label_c.animate.shift(
                RIGHT * 1.2
                +
                UP * 0.8
            ),
            run_time=1.0,
        )

        self.wait(0.25)


        # ----------------------------------------------------
        # MOVE PIECE D
        # ----------------------------------------------------

        self.play(
            self.piece_d.animate.shift(
                RIGHT * 1.5
                +
                DOWN * 0.7
            ),
            self.label_d.animate.shift(
                RIGHT * 1.5
                +
                DOWN * 0.7
            ),
            run_time=1.0,
        )

        self.wait(1)


    # ========================================================
    # SHOW PIECE IDENTITY
    # ========================================================

    def show_piece_identity(self):

        # ----------------------------------------------------
        # LABEL A
        # ----------------------------------------------------

        self.play(
            FadeIn(
                self.label_a
            ),
            run_time=0.35,
        )

        self.wait(0.2)


        # ----------------------------------------------------
        # LABEL B
        # ----------------------------------------------------

        self.play(
            FadeIn(
                self.label_b
            ),
            run_time=0.35,
        )

        self.wait(0.2)


        # ----------------------------------------------------
        # LABEL C
        # ----------------------------------------------------

        self.play(
            FadeIn(
                self.label_c
            ),
            run_time=0.35,
        )

        self.wait(0.2)


        # ----------------------------------------------------
        # LABEL D
        # ----------------------------------------------------

        self.play(
            FadeIn(
                self.label_d
            ),
            run_time=0.35,
        )

        self.wait(0.5)


        # ----------------------------------------------------
        # GROUP THE FOUR PIECES
        # ----------------------------------------------------

        self.play(
            AnimationGroup(
                Indicate(
                    self.piece_a,
                    scale_factor=1.02,
                ),
                Indicate(
                    self.piece_b,
                    scale_factor=1.02,
                ),
                Indicate(
                    self.piece_c,
                    scale_factor=1.02,
                ),
                Indicate(
                    self.piece_d,
                    scale_factor=1.02,
                ),
                lag_ratio=0.1,
            ),
            run_time=2.0,
        )

        self.wait(0.7)


    # ========================================================
    # RECONSTRUCT ORIGINAL
    # ========================================================

    def reconstruct_original(self):

        # ----------------------------------------------------
        # REMOVE LABELS TEMPORARILY
        # ----------------------------------------------------

        self.play(
            FadeOut(
                self.labels
            ),
            run_time=0.4,
        )


        # ----------------------------------------------------
        # RESTORE PIECES
        # ----------------------------------------------------

        self.play(
            Restore(
                self.pieces
            ),
            run_time=2.0,
        )


        # ----------------------------------------------------
        # LABELS RETURN TO ORIGINAL POSITIONS
        # ----------------------------------------------------

        self.label_a.move_to(
            self.piece_a.get_center()
        )

        self.label_b.move_to(
            self.piece_b.get_center()
        )

        self.label_c.move_to(
            self.piece_c.get_center()
        )

        self.label_d.move_to(
            self.piece_d.get_center()
        )


        # ----------------------------------------------------
        # SHOW LABELS
        # ----------------------------------------------------

        self.play(
            FadeIn(
                self.labels
            ),
            run_time=0.5,
        )

        self.wait(0.8)


    # ========================================================
    # REARRANGE PIECES
    # ========================================================

    def rearrange_pieces(self):

        # ----------------------------------------------------
        # HIDE LABELS
        # ----------------------------------------------------

        self.play(
            FadeOut(
                self.labels
            ),
            run_time=0.35,
        )


        # ----------------------------------------------------
        # PIECE A
        # ----------------------------------------------------

        self.play(
            self.piece_a.animate.shift(
                LEFT * 1.3
                +
                UP * 0.35
            ),
            run_time=1.0,
        )


        # ----------------------------------------------------
        # PIECE B
        # ----------------------------------------------------

        self.play(
            self.piece_b.animate.shift(
                LEFT * 0.8
                +
                UP * 0.35
            ),
            run_time=1.0,
        )


        # ----------------------------------------------------
        # PIECE C
        # ----------------------------------------------------

        self.play(
            self.piece_c.animate.shift(
                RIGHT * 0.8
                +
                DOWN * 0.25
            ),
            run_time=1.0,
        )


        # ----------------------------------------------------
        # PIECE D
        # ----------------------------------------------------

        self.play(
            self.piece_d.animate.shift(
                RIGHT * 1.3
                +
                DOWN * 0.25
            ),
            run_time=1.0,
        )


        # ----------------------------------------------------
        # REPOSITION LABELS
        # ----------------------------------------------------

        self.label_a.move_to(
            self.piece_a.get_center()
        )

        self.label_b.move_to(
            self.piece_b.get_center()
        )

        self.label_c.move_to(
            self.piece_c.get_center()
        )

        self.label_d.move_to(
            self.piece_d.get_center()
        )


        # ----------------------------------------------------
        # SHOW LABELS
        # ----------------------------------------------------

        self.play(
            FadeIn(
                self.labels
            ),
            run_time=0.5,
        )

        self.wait(1)


    # ========================================================
    # MISSING REGION
    # ========================================================

    def show_missing_region(self):

        # ----------------------------------------------------
        # CREATE APPARENT GAP
        # ----------------------------------------------------

        #
        # This region is intentionally shown as an empty
        # geometric space.
        #
        # Part 3 will investigate whether this is genuinely
        # inside the same triangle.
        #

        gap_center = point(
            0.0,
            -0.1
        )


        self.apparent_gap = Rectangle(
            width=0.65,
            height=0.32,
            stroke_width=0,
            fill_opacity=0,
        )

        self.apparent_gap.move_to(
            gap_center
        )


        # ----------------------------------------------------
        # EMPHASIZE THE EMPTY SPACE
        # ----------------------------------------------------

        self.play(
            self.camera.frame.animate.scale(
                0.92
            ),
            run_time=1.2,
        )

        self.wait(0.5)


        # ----------------------------------------------------
        # SUBTLE GAP INDICATION
        # ----------------------------------------------------

        gap_marker = SurroundingRectangle(
            self.apparent_gap,
            buff=0.08,
            stroke_color=BLACK,
            stroke_width=2,
        )

        gap_marker.set_stroke(
            opacity=0
        )


        self.play(
            gap_marker.animate.set_stroke(
                opacity=0.35
            ),
            run_time=0.7,
        )

        self.wait(1)


        # ----------------------------------------------------
        # REMOVE MARKER
        # ----------------------------------------------------

        self.play(
            FadeOut(
                gap_marker
            ),
            run_time=0.4,
        )

        self.wait(0.5)


    # ========================================================
    # SIDE-BY-SIDE COMPARISON
    # ========================================================

    def compare_arrangements(self):

        # ----------------------------------------------------
        # THIS IS A VISUAL PREPARATION FOR PART 2
        # ----------------------------------------------------

        #
        # We return the camera to a neutral framing.
        #

        self.play(
            self.camera.frame.animate.scale(
                1 / 0.92
            ),
            run_time=1.0,
        )


        # ----------------------------------------------------
        # CREATE ORIGINAL REFERENCE
        # ----------------------------------------------------

        reference = VGroup(
            self.piece_a.copy(),
            self.piece_b.copy(),
            self.piece_c.copy(),
            self.piece_d.copy(),
        )

        reference.move_to(
            LEFT * 3.0
        )

        reference.scale(
            0.55
        )


        # ----------------------------------------------------
        # REFERENCE LABEL
        # ----------------------------------------------------

        reference_title = Text(
            "original",
            font_size=26,
            color=BLACK,
        )

        reference_title.next_to(
            reference,
            DOWN,
            buff=0.35,
        )


        # ----------------------------------------------------
        # CURRENT GROUP
        # ----------------------------------------------------

        current = VGroup(
            self.piece_a.copy(),
            self.piece_b.copy(),
            self.piece_c.copy(),
            self.piece_d.copy(),
        )

        current.move_to(
            RIGHT * 3.0
        )

        current.scale(
            0.55
        )


        # ----------------------------------------------------
        # CURRENT LABEL
        # ----------------------------------------------------

        current_title = Text(
            "rearranged",
            font_size=26,
            color=BLACK,
        )

        current_title.next_to(
            current,
            DOWN,
            buff=0.35,
        )


        # ----------------------------------------------------
        # SHOW REFERENCE
        # ----------------------------------------------------

        self.play(
            FadeIn(
                reference
            ),
            FadeIn(
                reference_title
            ),
            run_time=0.8,
        )


        # ----------------------------------------------------
        # SHOW CURRENT
        # ----------------------------------------------------

        self.play(
            FadeIn(
                current
            ),
            FadeIn(
                current_title
            ),
            run_time=0.8,
        )

        self.wait(1)


        # ----------------------------------------------------
        # COMPARISON LINE
        # ----------------------------------------------------

        comparison_line = Line(
            point(0, -2.4),
            point(0, 2.4),
            stroke_color=BLACK,
            stroke_width=1.5,
        )

        comparison_line.set_stroke(
            opacity=0.18
        )


        self.play(
            Create(
                comparison_line
            ),
            run_time=0.5,
        )

        self.wait(1)


        # ----------------------------------------------------
        # REMOVE COMPARISON OBJECTS
        # ----------------------------------------------------

        self.play(
            FadeOut(
                reference
            ),
            FadeOut(
                reference_title
            ),
            FadeOut(
                current
            ),
            FadeOut(
                current_title
            ),
            FadeOut(
                comparison_line
            ),
            run_time=0.8,
        )


    # ========================================================
    # END PART
    # ========================================================

    def end_part(self):

        # ----------------------------------------------------
        # RESTORE MAIN VIEW
        # ----------------------------------------------------

        self.wait(0.5)


        # ----------------------------------------------------
        # QUESTION
        # ----------------------------------------------------

        self.play(
            self.question.animate.set_opacity(
                1
            ),
            run_time=0.8,
        )

        self.wait(2)


        # ----------------------------------------------------
        # REMOVE QUESTION
        # ----------------------------------------------------

        self.play(
            self.question.animate.set_opacity(
                0
            ),
            run_time=0.8,
        )


        # ----------------------------------------------------
        # FINAL PAUSE
        # ----------------------------------------------------

        self.wait(1)


        # ----------------------------------------------------
        # FADE OUT
        # ----------------------------------------------------

        self.play(
            FadeOut(
                self.pieces
            ),
            FadeOut(
                self.labels
            ),
            FadeOut(
                self.full_triangle
            ),
            FadeOut(
                self.original_outline
            ),
            run_time=1.0,
        )

        self.wait(0.5)


# ============================================================
# END OF PART 1
# ============================================================
