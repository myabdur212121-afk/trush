from manim import *


class MissingTrianglePart8(Scene):

    def construct(self):

        self.camera.background_color = "#F8F5E9"

        self.create_main_title()

        self.create_original_puzzle()

        self.introduce_two_configurations()

        self.show_configuration_a()

        self.show_configuration_b()

        self.compare_configurations()

        self.highlight_diagonal()

        self.zoom_into_diagonal()

        self.reveal_slope_one()

        self.reveal_slope_two()

        self.compare_slopes()

        self.show_non_collinearity()

        self.create_tiny_gap()

        self.expand_gap()

        self.connect_to_previous_part()

        self.show_area_difference()

        self.hide_large_construction()

        self.return_to_full_puzzle()

        self_end_hook()


    # ========================================================
    # TITLE
    # ========================================================

    def create_main_title(self):

        self.title = Text(
            "Look at the diagonal.",
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
                shift=DOWN * 0.15,
            ),
            run_time=0.8,
        )

        self.wait(0.8)


    # ========================================================
    # MAIN PUZZLE
    # ========================================================

    def create_original_puzzle(self):

        self.origin = np.array([
            -3.8,
            -1.8,
            0,
        ])

        self.scale = 0.55

        self.base_length = 7.0

        self.height = 3.0


        self.big_triangle = Polygon(
            self.origin,
            self.origin + RIGHT * self.base_length,
            self.origin + RIGHT * 2.5 + UP * self.height,
            stroke_color=BLACK,
            stroke_width=4,
            fill_opacity=0,
        )


        self.left_triangle = Polygon(
            self.origin,
            self.origin + RIGHT * 2.5 + UP * self.height,
            self.origin + UP * 0.2,
            stroke_color=BLACK,
            stroke_width=3,
            fill_opacity=0,
        )


        self.right_triangle = Polygon(
            self.origin + RIGHT * 2.5 + UP * self.height,
            self.origin + RIGHT * self.base_length,
            self.origin + RIGHT * 4.8 + UP * 0.5,
            stroke_color=BLACK,
            stroke_width=3,
            fill_opacity=0,
        )


        self.internal_line = Line(
            self.origin,
            self.origin + RIGHT * 2.5 + UP * self.height,
            stroke_color=BLACK,
            stroke_width=3,
        )


    # ========================================================
    # INTRODUCE TWO CONFIGURATIONS
    # ========================================================

    def introduce_two_configurations(self):

        new_title = Text(
            "We can arrange the same pieces in two ways.",
            font_size=30,
            color=BLACK,
        )

        new_title.to_edge(
            UP,
            buff=0.4,
        )

        self.play(
            Transform(
                self.title,
                new_title,
            ),
            run_time=0.7,
        )

        self.wait(0.7)


        self.configuration_a_label = Text(
            "Configuration A",
            font_size=25,
            color=BLACK,
        )

        self.configuration_b_label = Text(
            "Configuration B",
            font_size=25,
            color=BLACK,
        )


        self.configuration_a_label.move_to(
            LEFT * 3.1 + DOWN * 2.8
        )

        self.configuration_b_label.move_to(
            RIGHT * 3.1 + DOWN * 2.8
        )


    # ========================================================
    # CONFIGURATION A
    # ========================================================

    def show_configuration_a(self):

        self.a_left = Polygon(
            LEFT * 4.8 + DOWN * 2.0,
            LEFT * 1.2 + DOWN * 2.0,
            LEFT * 4.8 + UP * 0.5,
            stroke_color=BLACK,
            stroke_width=3,
            fill_opacity=0,
        )


        self.a_right = Polygon(
            LEFT * 1.2 + DOWN * 2.0,
            LEFT * 0.3 + UP * 0.5,
            LEFT * 4.8 + UP * 0.5,
            stroke_color=BLACK,
            stroke_width=3,
            fill_opacity=0,
        )


        self.a_rectangle = Polygon(
            LEFT * 4.8 + UP * 0.5,
            LEFT * 0.3 + UP * 0.5,
            LEFT * 0.3 + DOWN * 2.0,
            LEFT * 4.8 + DOWN * 2.0,
            stroke_color=BLACK,
            stroke_width=3,
            fill_opacity=0,
        )


        self.play(
            Create(
                self.a_left,
            ),
            run_time=0.7,
        )

        self.play(
            Create(
                self.a_right,
            ),
            run_time=0.7,
        )

        self.play(
            Create(
                self.a_rectangle,
            ),
            run_time=0.7,
        )


        self.play(
            FadeIn(
                self.configuration_a_label,
            ),
            run_time=0.5,
        )


        self.wait(0.8)


        a_diagonal = Line(
            LEFT * 4.8 + DOWN * 2.0,
            LEFT * 0.3 + UP * 0.5,
            stroke_color=BLACK,
            stroke_width=5,
        )


        self.play(
            Create(
                a_diagonal,
            ),
            run_time=0.9,
        )


        self.a_diagonal = a_diagonal


        self.wait(0.8)


    # ========================================================
    # CONFIGURATION B
    # ========================================================

    def show_configuration_b(self):

        self.b_left = Polygon(
            RIGHT * 1.0 + DOWN * 2.0,
            RIGHT * 4.6 + DOWN * 2.0,
            RIGHT * 1.0 + UP * 0.5,
            stroke_color=BLACK,
            stroke_width=3,
            fill_opacity=0,
        )


        self.b_right = Polygon(
            RIGHT * 4.6 + DOWN * 2.0,
            RIGHT * 5.5 + UP * 0.5,
            RIGHT * 1.0 + UP * 0.5,
            stroke_color=BLACK,
            stroke_width=3,
            fill_opacity=0,
        )


        self.b_rectangle = Polygon(
            RIGHT * 1.0 + UP * 0.5,
            RIGHT * 5.5 + UP * 0.5,
            RIGHT * 5.5 + DOWN * 2.0,
            RIGHT * 1.0 + DOWN * 2.0,
            stroke_color=BLACK,
            stroke_width=3,
            fill_opacity=0,
        )


        self.play(
            Create(
                self.b_left,
            ),
            run_time=0.7,
        )

        self.play(
            Create(
                self.b_right,
            ),
            run_time=0.7,
        )

        self.play(
            Create(
                self.b_rectangle,
            ),
            run_time=0.7,
        )


        self.play(
            FadeIn(
                self.configuration_b_label,
            ),
            run_time=0.5,
        )


        self.wait(0.8)


        b_diagonal = Line(
            RIGHT * 1.0 + DOWN * 2.0,
            RIGHT * 5.5 + UP * 0.5,
            stroke_color=BLACK,
            stroke_width=5,
        )


        self.play(
            Create(
                b_diagonal,
            ),
            run_time=0.9,
        )


        self.b_diagonal = b_diagonal


        self.wait(1)


    # ========================================================
    # COMPARE
    # ========================================================

    def compare_configurations(self):

        compare_title = Text(
            "They look almost identical.",
            font_size=31,
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

        self.wait(0.8)


        self.play(
            Indicate(
                self.a_diagonal,
                scale_factor=1.05,
            ),
            run_time=0.7,
        )

        self.play(
            Indicate(
                self.b_diagonal,
                scale_factor=1.05,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        question = MathTex(
            r"\text{Are these really straight lines?}",
            color=BLACK,
        ).scale(0.8)


        question.to_edge(
            DOWN,
            buff=0.5,
        )


        self.play(
            Write(
                question,
            ),
            run_time=0.8,
        )


        self.wait(1)


        self.question = question


    # ========================================================
    # HIGHLIGHT DIAGONAL
    # ========================================================

    def highlight_diagonal(self):

        highlight_title = Text(
            "Forget everything else.",
            font_size=31,
            color=BLACK,
        )

        highlight_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                highlight_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.question,
            ),
            run_time=0.4,
        )


        self.play(
            FadeOut(
                self.a_left,
                self.a_right,
                self.a_rectangle,
                self.b_left,
                self.b_right,
                self.b_rectangle,
                self.configuration_a_label,
                self.configuration_b_label,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            self.a_diagonal.animate.move_to(
                LEFT * 2.2
            ),
            self.b_diagonal.animate.move_to(
                RIGHT * 2.2
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        left_label = Text(
            "first diagonal",
            font_size=23,
            color=BLACK,
        )


        right_label = Text(
            "second diagonal",
            font_size=23,
            color=BLACK,
        )


        left_label.next_to(
            self.a_diagonal,
            DOWN,
            buff=0.25,
        )


        right_label.next_to(
            self.b_diagonal,
            DOWN,
            buff=0.25,
        )


        self.play(
            FadeIn(
                left_label,
            ),
            FadeIn(
                right_label,
            ),
            run_time=0.6,
        )


        self.wait(0.8)


        self.left_label = left_label
        self.right_label = right_label


    # ========================================================
    # ZOOM
    # ========================================================

    def zoom_into_diagonal(self):

        zoom_title = Text(
            "Let's zoom in.",
            font_size=32,
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
            FadeOut(
                self.left_label,
                self.right_label,
            ),
            run_time=0.4,
        )


        self.play(
            self.camera.frame.animate.scale(
                0.48
            ).move_to(
                self.a_diagonal.get_center()
            ),
            run_time=1.5,
        )


        self.wait(1)


        zoom_question = Text(
            "Something is hiding here.",
            font_size=28,
            color=BLACK,
        )


        zoom_question.to_edge(
            DOWN,
            buff=0.4,
        )


        self.play(
            FadeIn(
                zoom_question,
            ),
            run_time=0.7,
        )


        self.wait(1)


        self.zoom_question = zoom_question


    # ========================================================
    # FIRST SLOPE
    # ========================================================

    def reveal_slope_one(self):

        self.play(
            FadeOut(
                self.zoom_question,
            ),
            run_time=0.4,
        )


        slope_title = Text(
            "Measure the first slope.",
            font_size=30,
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


        horizontal_one = Line(
            self.a_diagonal.get_start(),
            np.array([
                self.a_diagonal.get_end()[0],
                self.a_diagonal.get_start()[1],
                0,
            ]),
            stroke_color=BLACK,
            stroke_width=2,
        )


        vertical_one = Line(
            np.array([
                self.a_diagonal.get_end()[0],
                self.a_diagonal.get_start()[1],
                0,
            ]),
            self.a_diagonal.get_end(),
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.play(
            Create(
                horizontal_one,
            ),
            run_time=0.6,
        )


        self.play(
            Create(
                vertical_one,
            ),
            run_time=0.6,
        )


        slope_one_equation = MathTex(
            r"m_1"
            "="
            r"\frac{\text{rise}}{\text{run}}"
            "="
            r"\frac25",
            color=BLACK,
        ).scale(0.9)


        slope_one_equation.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            Write(
                slope_one_equation,
            ),
            run_time=0.9,
        )


        self.wait(1)


        self.horizontal_one = horizontal_one
        self.vertical_one = vertical_one
        self.slope_one_equation = slope_one_equation


    # ========================================================
    # SECOND SLOPE
    # ========================================================

    def reveal_slope_two(self):

        second_title = Text(
            "Now measure the second slope.",
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


        self.play(
            FadeOut(
                self.horizontal_one,
                self.vertical_one,
                self.slope_one_equation,
            ),
            run_time=0.5,
        )


        # ----------------------------------------------------
        # Move focus toward the second line.
        # ----------------------------------------------------

        self.play(
            self.a_diagonal.animate.shift(
                LEFT * 1.8
            ),
            self.b_diagonal.animate.shift(
                RIGHT * 1.8
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        horizontal_two = Line(
            self.b_diagonal.get_start(),
            np.array([
                self.b_diagonal.get_end()[0],
                self.b_diagonal.get_start()[1],
                0,
            ]),
            stroke_color=BLACK,
            stroke_width=2,
        )


        vertical_two = Line(
            np.array([
                self.b_diagonal.get_end()[0],
                self.b_diagonal.get_start()[1],
                0,
            ]),
            self.b_diagonal.get_end(),
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.play(
            Create(
                horizontal_two,
            ),
            run_time=0.6,
        )


        self.play(
            Create(
                vertical_two,
            ),
            run_time=0.6,
        )


        slope_two_equation = MathTex(
            r"m_2"
            "="
            r"\frac{\text{rise}}{\text{run}}"
            "="
            r"\frac38",
            color=BLACK,
        ).scale(0.9)


        slope_two_equation.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            Write(
                slope_two_equation,
            ),
            run_time=0.9,
        )


        self.wait(1)


        self.horizontal_two = horizontal_two
        self.vertical_two = vertical_two
        self.slope_two_equation = slope_two_equation


    # ========================================================
    # COMPARE SLOPES
    # ========================================================

    def compare_slopes(self):

        compare_title = Text(
            "And now we see the problem.",
            font_size=31,
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


        self.play(
            FadeOut(
                self.horizontal_two,
                self.vertical_two,
                self.slope_two_equation,
            ),
            run_time=0.5,
        )


        comparison = MathTex(
            r"\frac25"
            r"\neq"
            r"\frac38",
            color=BLACK,
        ).scale(1.2)


        comparison.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                comparison,
            ),
            run_time=0.9,
        )


        self.wait(1)


        self.play(
            Indicate(
                comparison,
                scale_factor=1.15,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.comparison = comparison


    # ========================================================
    # NON COLLINEARITY
    # ========================================================

    def show_non_collinearity(self):

        non_title = Text(
            "Two different slopes cannot form one straight line.",
            font_size=27,
            color=BLACK,
        )


        non_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                non_title,
            ),
            run_time=0.7,
        )


        self.wait(0.6)


        self.play(
            FadeOut(
                self.comparison,
            ),
            run_time=0.4,
        )


        # ----------------------------------------------------
        # Bring both diagonals close.
        # ----------------------------------------------------

        self.play(
            self.a_diagonal.animate.move_to(
                LEFT * 1.5
            ),
            self.b_diagonal.animate.move_to(
                RIGHT * 1.5
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        non_collinear = Text(
            "not exactly collinear",
            font_size=24,
            color=BLACK,
        )


        non_collinear.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            FadeIn(
                non_collinear,
            ),
            run_time=0.6,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                self.a_diagonal,
                scale_factor=1.05,
            ),
            run_time=0.6,
        )


        self.play(
            Indicate(
                self.b_diagonal,
                scale_factor=1.05,
            ),
            run_time=0.6,
        )


        self.wait(0.8)


        self.non_collinear = non_collinear


    # ========================================================
    # CREATE TINY GAP
    # ========================================================

    def create_tiny_gap(self):

        gap_title = Text(
            "That tiny mismatch creates a gap.",
            font_size=30,
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
                self.non_collinear,
            ),
            run_time=0.4,
        )


        # ----------------------------------------------------
        # Put the two lines into a near-common configuration.
        # ----------------------------------------------------

        self.play(
            self.a_diagonal.animate.move_to(
                ORIGIN
                +
                DOWN * 0.3
            ),
            self.b_diagonal.animate.move_to(
                ORIGIN
                +
                DOWN * 0.3
                +
                RIGHT * 0.03
            ),
            run_time=1,
        )


        self.wait(0.6)


        tiny_gap = Line(
            self.a_diagonal.get_end(),
            self.b_diagonal.get_end(),
            stroke_color=BLACK,
            stroke_width=5,
        )


        self.play(
            Create(
                tiny_gap,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        gap_label = MathTex(
            r"\text{tiny gap}",
            color=BLACK,
        ).scale(0.7)


        gap_label.next_to(
            tiny_gap,
            RIGHT,
            buff=0.2,
        )


        self.play(
            Write(
                gap_label,
            ),
            run_time=0.6,
        )


        self.wait(0.8)


        self.tiny_gap = tiny_gap
        self.gap_label = gap_label


    # ========================================================
    # EXPAND GAP
    # ========================================================

    def expand_gap(self):

        expand_title = Text(
            "Let's exaggerate it.",
            font_size=31,
            color=BLACK,
        )


        expand_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                expand_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.gap_label,
            ),
            run_time=0.4,
        )


        # ----------------------------------------------------
        # Replace tiny gap with a clearly visible gap.
        # ----------------------------------------------------

        enlarged_gap = Line(
            self.a_diagonal.get_end(),
            self.b_diagonal.get_end(),
            stroke_color=BLACK,
            stroke_width=10,
        )


        self.play(
            Transform(
                self.tiny_gap,
                enlarged_gap,
            ),
            run_time=1,
        )


        self.wait(0.8)


        exaggerated = Text(
            "exaggerated × 20",
            font_size=23,
            color=BLACK,
        )


        exaggerated.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            FadeIn(
                exaggerated,
            ),
            run_time=0.6,
        )


        self.wait(0.8)


        self.exaggerated = exaggerated


    # ========================================================
    # CONNECT PREVIOUS PART
    # ========================================================

    def connect_to_previous_part(self):

        connection_title = Text(
            "This is exactly what Δm = 1/40 predicts.",
            font_size=28,
            color=BLACK,
        )


        connection_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                connection_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.exaggerated,
            ),
            run_time=0.4,
        )


        relation = MathTex(
            r"\Delta m"
            "="
            r"\frac25-\frac38"
            "="
            r"\frac1{40}",
            color=BLACK,
        ).scale(0.85)


        relation.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                relation,
            ),
            run_time=0.9,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                self.tiny_gap,
                scale_factor=1.4,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        self.play(
            Indicate(
                relation,
                scale_factor=1.08,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.relation = relation


    # ========================================================
    # AREA DIFFERENCE
    # ========================================================

    def show_area_difference(self):

        area_title = Text(
            "A gap means an area.",
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
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.relation,
            ),
            run_time=0.4,
        )


        area_equation = MathTex(
            r"A"
            "="
            r"\frac12x^2"
            r"\Delta m",
            color=BLACK,
        ).scale(1)


        area_equation.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                area_equation,
            ),
            run_time=0.9,
        )


        self.wait(0.8)


        area_substitution = MathTex(
            r"A"
            "="
            r"\frac12x^2"
            r"\left(\frac1{40}\right)",
            color=BLACK,
        ).scale(0.9)


        area_substitution.next_to(
            area_equation,
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                area_substitution,
            ),
            run_time=0.8,
        )


        self.wait(1)


        self.play(
            Indicate(
                area_substitution,
                scale_factor=1.08,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.area_equation = area_equation
        self.area_substitution = area_substitution


    # ========================================================
    # HIDE CONSTRUCTION
    # ========================================================

    def hide_large_construction(self):

        clean_title = Text(
            "But don't let the exaggeration fool you.",
            font_size=29,
            color=BLACK,
        )


        clean_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                clean_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.area_equation,
                self.area_substitution,
            ),
            run_time=0.5,
        )


        self.play(
            FadeOut(
                self.tiny_gap,
            ),
            run_time=0.5,
        )


        self.wait(0.5)


        # ----------------------------------------------------
        # Return to the original camera.
        # ----------------------------------------------------

        self.play(
            self.camera.frame.animate.scale(
                1 / 0.48
            ).move_to(
                ORIGIN
            ),
            run_time=1.4,
        )


        self.wait(0.8)


    # ========================================================
    # RETURN TO FULL PUZZLE
    # ========================================================

    def return_to_full_puzzle(self):

        full_title = Text(
            "Now return to the original puzzle.",
            font_size=29,
            color=BLACK,
        )


        full_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                full_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        # ----------------------------------------------------
        # Recreate a simplified puzzle.
        # ----------------------------------------------------

        triangle = Polygon(
            LEFT * 4.2 + DOWN * 1.8,
            RIGHT * 4.2 + DOWN * 1.8,
            LEFT * 0.8 + UP * 2.0,
            stroke_color=BLACK,
            stroke_width=4,
            fill_opacity=0,
        )


        diagonal = Line(
            LEFT * 4.2 + DOWN * 1.8,
            LEFT * 0.8 + UP * 2.0,
            stroke_color=BLACK,
            stroke_width=4,
        )


        second_diagonal = Line(
            LEFT * 0.8 + UP * 2.0,
            RIGHT * 4.2 + DOWN * 1.8,
            stroke_color=BLACK,
            stroke_width=4,
        )


        self.play(
            Create(
                triangle,
            ),
            run_time=1,
        )


        self.play(
            Create(
                diagonal,
            ),
            run_time=0.8,
        )


        self.play(
            Create(
                second_diagonal,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        warning = Text(
            "The apparent straight edge is the trick.",
            font_size=28,
            color=BLACK,
        )


        warning.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            FadeIn(
                warning,
            ),
            run_time=0.7,
        )


        self.wait(1)


        self.play(
            Indicate(
                diagonal,
                scale_factor=1.05,
            ),
            run_time=0.7,
        )


        self.play(
            Indicate(
                second_diagonal,
                scale_factor=1.05,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.warning = warning


    # ========================================================
    # END HOOK
    # ========================================================

    def self_end_hook(self):

        hook_title = Text(
            "So where did the missing area come from?",
            font_size=31,
            color=BLACK,
        )


        hook_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                hook_title,
            ),
            run_time=0.7,
        )


        self.wait(0.7)


        self.play(
            FadeOut(
                self.warning,
            ),
            run_time=0.5,
        )


        hook_equation = MathTex(
            r"""\boxed{
                \frac25-\frac38=\frac1{40}
            }""",
            color=BLACK,
        ).scale(0.95)


        hook_equation.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                hook_equation,
            ),
            run_time=0.9,
        )


        self.wait(1)


        self.play(
            Indicate(
                hook_equation,
                scale_factor=1.1,
            ),
            run_time=0.7,
        )


        self.wait(1)


        final_question = Text(
            "But how does that tiny error create exactly ONE square unit?",
            font_size=25,
            color=BLACK,
        )


        final_question.to_edge(
            DOWN,
            buff=0.4,
        )


        self.play(
            FadeIn(
                final_question,
                shift=UP * 0.1,
            ),
            run_time=0.8,
        )


        self.wait(2)


        self.play(
            FadeOut(
                triangle,
                diagonal,
                second_diagonal,
                hook_equation,
                final_question,
                self.title,
                run_time=1,
            ),
        )


        self.wait(0.8)
