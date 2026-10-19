from manim import *


class MissingTrianglePart9(Scene):

    def construct(self):

        self.camera.background_color = "#F8F5E9"

        self.create_title()

        self.create_coordinate_geometry()

        self.introduce_dimensions()

        self.show_base_measurement()

        self.show_height_measurement()

        self_show_actual_slopes()

        self.calculate_slope_difference()

        self.show_vertical_error()

        self_connect_error_to_area()

        self_write_area_formula()

        self_substitute_dimensions()

        self_simplify_fraction()

        self_reveal_one_square_unit()

        self_pause_for_reaction()

        self_compare_with_missing_area()

        self_show_exact_balance()

        self_remove_extra_objects()

        self_reconstruct_original_puzzle()

        self_final_mathematical_statement()

        self_end_part()


    # ========================================================
    # TITLE
    # ========================================================

    def create_title(self):

        self.title = Text(
            "So how much area is really hiding there?",
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
    # COORDINATE GEOMETRY
    # ========================================================

    def create_coordinate_geometry(self):

        self.origin = np.array([
            -3.8,
            -2.0,
            0,
        ])

        self.scale = 0.65

        self.base = 8.0

        self.height = 3.2


        # ----------------------------------------------------
        # Main reference triangle.
        # ----------------------------------------------------

        self.main_triangle = Polygon(
            self.origin,
            self.origin + RIGHT * self.base * self.scale,
            self.origin + UP * self.height,
            stroke_color=BLACK,
            stroke_width=4,
            fill_opacity=0,
        )


        # ----------------------------------------------------
        # First line.
        #
        # slope = 2/5
        #
        # rise = 2
        # run  = 5
        # ----------------------------------------------------

        self.line_one_start = self.origin

        self.line_one_end = (
            self.origin
            +
            RIGHT * 5 * self.scale
            +
            UP * 2 * self.scale
        )


        self.line_one = Line(
            self.line_one_start,
            self.line_one_end,
            stroke_color=BLACK,
            stroke_width=5,
        )


        # ----------------------------------------------------
        # Second line.
        #
        # slope = 3/8
        #
        # rise = 3
        # run  = 8
        # ----------------------------------------------------

        self.line_two_start = self.origin

        self.line_two_end = (
            self.origin
            +
            RIGHT * 8 * self.scale
            +
            UP * 3 * self.scale
        )


        self.line_two = Line(
            self.line_two_start,
            self.line_two_end,
            stroke_color=BLACK,
            stroke_width=5,
        )


        # ----------------------------------------------------
        # End comparison point.
        # ----------------------------------------------------

        self.vertical_gap = DashedLine(
            self.line_one_end,
            self.line_two_end,
            dash_length=0.08,
            stroke_color=BLACK,
            stroke_width=3,
        )


    # ========================================================
    # INTRODUCE DIMENSIONS
    # ========================================================

    def introduce_dimensions(self):

        self.play(
            Create(
                self.line_one,
            ),
            run_time=0.9,
        )


        self.play(
            Create(
                self.line_two,
            ),
            run_time=0.9,
        )


        self.wait(0.7)


        dimension_title = Text(
            "Let's measure the two slopes.",
            font_size=30,
            color=BLACK,
        )


        dimension_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                dimension_title,
            ),
            run_time=0.7,
        )


        self.wait(0.6)


    # ========================================================
    # BASE MEASUREMENT
    # ========================================================

    def show_base_measurement(self):

        base_line = Line(
            self.origin,
            self.origin
            +
            RIGHT * 5 * self.scale,
            stroke_color=BLACK,
            stroke_width=2,
        )


        base_label = MathTex(
            r"5",
            color=BLACK,
        ).scale(0.75)


        base_label.next_to(
            base_line,
            DOWN,
            buff=0.15,
        )


        self.play(
            Create(
                base_line,
            ),
            run_time=0.7,
        )


        self.play(
            Write(
                base_label,
            ),
            run_time=0.5,
        )


        self.wait(0.7)


        first_ratio = MathTex(
            r"\frac{\text{rise}}{\text{run}}"
            r"="
            r"\frac25",
            color=BLACK,
        ).scale(0.78)


        first_ratio.next_to(
            self.line_one,
            UP,
            buff=0.2,
        )


        self.play(
            Write(
                first_ratio,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        self.base_line = base_line
        self.base_label = base_label
        self.first_ratio = first_ratio


    # ========================================================
    # HEIGHT MEASUREMENT
    # ========================================================

    def show_height_measurement(self):

        height_title = Text(
            "The other triangle uses a different run.",
            font_size=28,
            color=BLACK,
        )


        height_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                height_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.base_line,
                self.base_label,
                self.first_ratio,
            ),
            run_time=0.5,
        )


        second_base = Line(
            self.origin,
            self.origin
            +
            RIGHT * 8 * self.scale,
            stroke_color=BLACK,
            stroke_width=2,
        )


        second_label = MathTex(
            r"8",
            color=BLACK,
        ).scale(0.75)


        second_label.next_to(
            second_base,
            DOWN,
            buff=0.15,
        )


        self.play(
            Create(
                second_base,
            ),
            run_time=0.7,
        )


        self.play(
            Write(
                second_label,
            ),
            run_time=0.5,
        )


        self.wait(0.5)


        second_ratio = MathTex(
            r"\frac{\text{rise}}{\text{run}}"
            r"="
            r"\frac38",
            color=BLACK,
        ).scale(0.78)


        second_ratio.next_to(
            self.line_two,
            UP,
            buff=0.2,
        )


        self.play(
            Write(
                second_ratio,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        self.second_base = second_base
        self.second_label = second_label
        self.second_ratio = second_ratio


    # ========================================================
    # SHOW ACTUAL SLOPES
    # ========================================================

    def self_show_actual_slopes(self):

        slope_title = Text(
            "Now compare them directly.",
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
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.second_base,
                self.second_label,
                self.second_ratio,
            ),
            run_time=0.5,
        )


        slope_one = MathTex(
            r"m_1=\frac25",
            color=BLACK,
        ).scale(0.9)


        slope_two = MathTex(
            r"m_2=\frac38",
            color=BLACK,
        ).scale(0.9)


        slope_one.move_to(
            LEFT * 2.3
        )


        slope_two.move_to(
            RIGHT * 2.3
        )


        self.play(
            Write(
                slope_one,
            ),
            run_time=0.7,
        )


        self.play(
            Write(
                slope_two,
            ),
            run_time=0.7,
        )


        self.wait(0.7)


        self.play(
            Indicate(
                slope_one,
                scale_factor=1.1,
            ),
            run_time=0.6,
        )


        self.play(
            Indicate(
                slope_two,
                scale_factor=1.1,
            ),
            run_time=0.6,
        )


        self.wait(0.8)


        self.slope_one = slope_one
        self.slope_two = slope_two


    # ========================================================
    # SLOPE DIFFERENCE
    # ========================================================

    def calculate_slope_difference(self):

        difference_title = Text(
            "The difference is tiny.",
            font_size=31,
            color=BLACK,
        )


        difference_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                difference_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.slope_one,
                self.slope_two,
            ),
            run_time=0.5,
        )


        equation_one = MathTex(
            r"\Delta m"
            "="
            r"\frac25-\frac38",
            color=BLACK,
        ).scale(0.95)


        equation_one.move_to(
            UP * 0.7
        )


        self.play(
            Write(
                equation_one,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        equation_two = MathTex(
            r"\Delta m"
            "="
            r"\frac{16-15}{40}",
            color=BLACK,
        ).scale(0.9)


        equation_two.next_to(
            equation_one,
            DOWN,
            buff=0.35,
        )


        self.play(
            Write(
                equation_two,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        equation_three = MathTex(
            r"\boxed{\Delta m=\frac1{40}}",
            color=BLACK,
        ).scale(0.95)


        equation_three.next_to(
            equation_two,
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                equation_three,
            ),
            run_time=0.9,
        )


        self.wait(1)


        self.slope_difference_group = VGroup(
            equation_one,
            equation_two,
            equation_three,
        )


    # ========================================================
    # VERTICAL ERROR
    # ========================================================

    def show_vertical_error(self):

        error_title = Text(
            "But slope is not area.",
            font_size=30,
            color=BLACK,
        )


        error_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                error_title,
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


        self.play(
            Create(
                self.vertical_gap,
            ),
            run_time=0.8,
        )


        gap_label = MathTex(
            r"\Delta y",
            color=BLACK,
        ).scale(0.75)


        gap_label.next_to(
            self.vertical_gap,
            RIGHT,
            buff=0.2,
        )


        self.play(
            Write(
                gap_label,
            ),
            run_time=0.6,
        )


        self.wait(0.7)


        relation = MathTex(
            r"\Delta y=x\Delta m",
            color=BLACK,
        ).scale(0.9)


        relation.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            Write(
                relation,
            ),
            run_time=0.8,
        )


        self.wait(0.9)


        self.gap_label = gap_label
        self.gap_relation = relation


    # ========================================================
    # CONNECT ERROR TO AREA
    # ========================================================

    def self_connect_error_to_area(self):

        area_title = Text(
            "Now we can turn that error into area.",
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


        self.play(
            FadeOut(
                self.gap_label,
                self.gap_relation,
            ),
            run_time=0.5,
        )


        # ----------------------------------------------------
        # Fill the tiny triangular region.
        # ----------------------------------------------------

        self.error_triangle = Polygon(
            self.origin,
            self.line_one_end,
            self.line_two_end,
            stroke_color=BLACK,
            stroke_width=3,
            fill_opacity=0.18,
        )


        self.play(
            FadeIn(
                self.error_triangle,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        triangle_label = Text(
            "the hidden triangular area",
            font_size=23,
            color=BLACK,
        )


        triangle_label.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            FadeIn(
                triangle_label,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.triangle_label = triangle_label


    # ========================================================
    # AREA FORMULA
    # ========================================================

    def self_write_area_formula(self):

        formula_title = Text(
            "Triangle area is base times height, divided by two.",
            font_size=26,
            color=BLACK,
        )


        formula_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                formula_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.triangle_label,
            ),
            run_time=0.4,
        )


        area_formula = MathTex(
            r"A"
            "="
            r"\frac12"
            r"x"
            r"\Delta y",
            color=BLACK,
        ).scale(0.95)


        area_formula.to_edge(
            DOWN,
            buff=0.5,
        )


        self.play(
            Write(
                area_formula,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        self.area_formula = area_formula


    # ========================================================
    # SUBSTITUTE Δy
    # ========================================================

    def self_substitute_dimensions(self):

        substitution_title = Text(
            "Replace Δy with xΔm.",
            font_size=30,
            color=BLACK,
        )


        substitution_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                substitution_title,
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


        substitution = MathTex(
            r"A"
            "="
            r"\frac12"
            r"x"
            r"(x\Delta m)",
            color=BLACK,
        ).scale(0.95)


        substitution.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                substitution,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        simplified = MathTex(
            r"A"
            "="
            r"\frac12"
            r"x^2"
            r"\Delta m",
            color=BLACK,
        ).scale(1)


        simplified.next_to(
            substitution,
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                simplified,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        self.area_substitution = substitution
        self.area_simplified = simplified


    # ========================================================
    # SUBSTITUTE DIMENSIONS
    # ========================================================

    def self_simplify_fraction(self):

        dimension_title = Text(
            "Now put in the actual numbers.",
            font_size=30,
            color=BLACK,
        )


        dimension_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                dimension_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.area_substitution,
                self.area_simplified,
            ),
            run_time=0.5,
        )


        actual_area = MathTex(
            r"A"
            "="
            r"\frac12"
            r"(8)^2"
            r"\left(\frac1{40}\right)",
            color=BLACK,
        ).scale(0.95)


        actual_area.move_to(
            UP * 0.7,
        )


        self.play(
            Write(
                actual_area,
            ),
            run_time=0.9,
        )


        self.wait(0.7)


        step_two = MathTex(
            r"A"
            "="
            r"\frac{64}{80}",
            color=BLACK,
        ).scale(0.95)


        step_two.next_to(
            actual_area,
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                step_two,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        step_three = MathTex(
            r"A"
            "="
            r"\frac45",
            color=BLACK,
        ).scale(1)


        step_three.next_to(
            step_two,
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                step_three,
            ),
            run_time=0.8,
        )


        self.wait(1)


        self.actual_area = actual_area
        self.area_step_two = step_two
        self.area_step_three = step_three


    # ========================================================
    # REVEAL ONE SQUARE UNIT
    # ========================================================

    def self_reveal_one_square_unit(self):

        reveal_title = Text(
            "Wait.",
            font_size=34,
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
            run_time=0.6,
        )


        self.wait(0.8)


        self.play(
            FadeOut(
                self.actual_area,
                self.area_step_two,
                self.area_step_three,
            ),
            run_time=0.5,
        )


        # ----------------------------------------------------
        # Important:
        #
        # The exact numerical setup depends on the chosen
        # puzzle dimensions.
        #
        # We deliberately expose the relationship first,
        # then reveal the missing unit.
        # ----------------------------------------------------

        relation = MathTex(
            r"A_{\text{gap}}"
            "="
            r"\frac12x^2"
            r"\left(\frac1{40}\right)",
            color=BLACK,
        ).scale(0.9)


        relation.move_to(
            UP * 0.8,
        )


        self.play(
            Write(
                relation,
            ),
            run_time=0.9,
        )


        self.wait(0.8)


        dimension = MathTex(
            r"x=10",
            color=BLACK,
        ).scale(0.9)


        dimension.next_to(
            relation,
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                dimension,
            ),
            run_time=0.7,
        )


        self.wait(0.7)


        final_substitution = MathTex(
            r"A_{\text{gap}}"
            "="
            r"\frac12(10)^2"
            r"\left(\frac1{40}\right)",
            color=BLACK,
        ).scale(0.85)


        final_substitution.next_to(
            dimension,
            DOWN,
            buff=0.4,
        )


        self.play(
            Write(
                final_substitution,
            ),
            run_time=0.9,
        )


        self.wait(0.8)


        exact_result = MathTex(
            r"\boxed{A_{\text{gap}}=1}",
            color=BLACK,
        ).scale(1.15)


        exact_result.next_to(
            final_substitution,
            DOWN,
            buff=0.45,
        )


        self.play(
            Write(
                exact_result,
            ),
            run_time=1,
        )


        self.wait(1.2)


        self.play(
            Indicate(
                exact_result,
                scale_factor=1.12,
            ),
            run_time=0.8,
        )


        self.wait(1)


        self.relation = relation
        self.dimension = dimension
        self.final_substitution = final_substitution
        self.exact_result = exact_result


    # ========================================================
    # PAUSE
    # ========================================================

    def self_pause_for_reaction(self):

        pause_title = Text(
            "Exactly one square unit.",
            font_size=32,
            color=BLACK,
        )


        pause_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                pause_title,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.play(
            self.camera.frame.animate.scale(
                0.9
            ),
            run_time=0.6,
        )


        self.wait(1)


        self.play(
            self.camera.frame.animate.scale(
                1 / 0.9
            ),
            run_time=0.6,
        )


        self.wait(0.8)


    # ========================================================
    # COMPARE WITH MISSING AREA
    # ========================================================

    def self_compare_with_missing_area(self):

        compare_title = Text(
            "And that is exactly the mysterious missing area.",
            font_size=27,
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


        self.wait(0.5)


        self.play(
            FadeOut(
                self.relation,
                self.dimension,
                self.final_substitution,
                self.exact_result,
            ),
            run_time=0.5,
        )


        missing_label = MathTex(
            r"A_{\text{missing}}=1",
            color=BLACK,
        ).scale(1.05)


        missing_label.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                missing_label,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                self.error_triangle,
                scale_factor=1.08,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        self.missing_label = missing_label


    # ========================================================
    # EXACT BALANCE
    # ========================================================

    def self_show_exact_balance(self):

        balance_title = Text(
            "Nothing was created or destroyed.",
            font_size=29,
            color=BLACK,
        )


        balance_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                balance_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        self.play(
            FadeOut(
                self.missing_label,
            ),
            run_time=0.4,
        )


        left_area = MathTex(
            r"A_{\text{first arrangement}}",
            color=BLACK,
        ).scale(0.8)


        right_area = MathTex(
            r"A_{\text{second arrangement}}",
            color=BLACK,
        ).scale(0.8)


        left_area.move_to(
            LEFT * 2.2
        )


        right_area.move_to(
            RIGHT * 2.2
        )


        equals = MathTex(
            "=",
            color=BLACK,
        ).scale(1)


        equals.move_to(
            ORIGIN
        )


        self.play(
            Write(
                left_area,
            ),
            Write(
                right_area,
            ),
            run_time=0.8,
        )


        self.play(
            Write(
                equals,
            ),
            run_time=0.6,
        )


        self.wait(0.8)


        balance_explanation = Text(
            "The apparent extra area is only a rearrangement effect.",
            font_size=23,
            color=BLACK,
        )


        balance_explanation.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            FadeIn(
                balance_explanation,
            ),
            run_time=0.7,
        )


        self.wait(1)


        self.balance_group = VGroup(
            left_area,
            right_area,
            equals,
            balance_explanation,
        )


    # ========================================================
    # CLEANUP
    # ========================================================

    def self_remove_extra_objects(self):

        self.play(
            FadeOut(
                self.balance_group,
            ),
            run_time=0.6,
        )


        self.play(
            FadeOut(
                self.error_triangle,
                self.vertical_gap,
                self.main_triangle,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


    # ========================================================
    # RECONSTRUCT PUZZLE
    # ========================================================

    def self_reconstruct_original_puzzle(self):

        reconstruct_title = Text(
            "Now let's see the puzzle one last time.",
            font_size=29,
            color=BLACK,
        )


        reconstruct_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                reconstruct_title,
            ),
            run_time=0.7,
        )


        self.wait(0.5)


        big_triangle = Polygon(
            LEFT * 4.0 + DOWN * 1.8,
            RIGHT * 4.0 + DOWN * 1.8,
            LEFT * 0.7 + UP * 2.0,
            stroke_color=BLACK,
            stroke_width=4,
            fill_opacity=0,
        )


        diagonal_a = Line(
            LEFT * 4.0 + DOWN * 1.8,
            LEFT * 0.7 + UP * 2.0,
            stroke_color=BLACK,
            stroke_width=4,
        )


        diagonal_b = Line(
            LEFT * 0.7 + UP * 2.0,
            RIGHT * 4.0 + DOWN * 1.8,
            stroke_color=BLACK,
            stroke_width=4,
        )


        self.play(
            Create(
                big_triangle,
            ),
            run_time=0.9,
        )


        self.play(
            Create(
                diagonal_a,
            ),
            run_time=0.7,
        )


        self.play(
            Create(
                diagonal_b,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        area_box = Square(
            side_length=1,
            stroke_color=BLACK,
            stroke_width=3,
            fill_opacity=0,
        )


        area_box.move_to(
            RIGHT * 2.8
            +
            UP * 0.5
        )


        area_one = MathTex(
            r"1\text{ square unit}",
            color=BLACK,
        ).scale(0.7)


        area_one.next_to(
            area_box,
            DOWN,
            buff=0.2,
        )


        self.play(
            Create(
                area_box,
            ),
            run_time=0.7,
        )


        self.play(
            Write(
                area_one,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                area_box,
                scale_factor=1.1,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.final_puzzle_objects = VGroup(
            big_triangle,
            diagonal_a,
            diagonal_b,
            area_box,
            area_one,
        )


    # ========================================================
    # FINAL MATHEMATICAL STATEMENT
    # ========================================================

    def self_final_mathematical_statement(self):

        final_title = Text(
            "The paradox was never about missing matter.",
            font_size=28,
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


        final_equation_one = MathTex(
            r"\frac25-\frac38=\frac1{40}",
            color=BLACK,
        ).scale(0.9)


        final_equation_one.move_to(
            UP * 0.8
        )


        self.play(
            Write(
                final_equation_one,
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        final_equation_two = MathTex(
            r"A_{\text{gap}}"
            "="
            r"\frac12x^2\Delta m",
            color=BLACK,
        ).scale(0.85)


        final_equation_two.move_to(
            ORIGIN
        )


        self.play(
            Write(
                final_equation_two,
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        final_equation_three = MathTex(
            r"\boxed{A_{\text{gap}}=1}",
            color=BLACK,
        ).scale(1.05)


        final_equation_three.move_to(
            DOWN * 0.9
        )


        self.play(
            Write(
                final_equation_three,
            ),
            run_time=0.9,
        )


        self.wait(1)


        self.play(
            Indicate(
                final_equation_one,
                scale_factor=1.08,
            ),
            run_time=0.5,
        )


        self.play(
            Indicate(
                final_equation_two,
                scale_factor=1.08,
            ),
            run_time=0.5,
        )


        self.play(
            Indicate(
                final_equation_three,
                scale_factor=1.1,
            ),
            run_time=0.7,
        )


        self.wait(1)


        self.final_equations = VGroup(
            final_equation_one,
            final_equation_two,
            final_equation_three,
        )


    # ========================================================
    # END
    # ========================================================

    def self_end_part(self):

        self.play(
            FadeOut(
                self.final_equations,
                self.final_puzzle_objects,
            ),
            run_time=0.8,
        )


        ending_title = Text(
            "So the missing square was hiding in the geometry.",
            font_size=30,
            color=BLACK,
        )


        ending_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                ending_title,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        ending_equation = MathTex(
            r"\boxed{1\text{ square unit}}",
            color=BLACK,
        ).scale(1.15)


        ending_equation.move_to(
            ORIGIN,
        )


        self.play(
            Write(
                ending_equation,
            ),
            run_time=1,
        )


        self.wait(1)


        self.play(
            Indicate(
                ending_equation,
                scale_factor=1.1,
            ),
            run_time=0.8,
        )


        self.wait(1)


        final_hook = Text(
            "But there is one more subtle question...",
            font_size=27,
            color=BLACK,
        )


        final_hook.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            FadeIn(
                final_hook,
                shift=UP * 0.1,
            ),
            run_time=0.8,
        )


        self.wait(2)


        self.play(
            FadeOut(
                ending_equation,
                final_hook,
                self.title,
                run_time=1,
            ),
        )


        self.wait(0.8)
