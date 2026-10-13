from manim import *

class FactrioalScene(Scene):
    def hook_s1(self):
        # Binomial Theorem: Isolate "2!"
        binom_title = Text(
            "Binomial Theorem",
            font="CMU Serif",
            font_size=38,
            color=WHITE
        )
        binom_equation = MathTex(
            r"(a+b)^n = a^n + na^{n-1}b + \frac{n(n-1)}{2!}a^{n-2}b^2 + \cdots",
            substrings_to_isolate=["2!"],
            font_size=45,
            color=WHITE
        )

        # Taylor Series: Isolate "2!" and "3!"
        taylor_title = Text(
            "Taylor Series",
            font="CMU Serif",
            font_size=38,
            color=WHITE
        )
        taylor_equation = MathTex(
            r"e^x = 1+x+\frac{x^2}{2!}+\frac{x^3}{3!}+\cdots",
            substrings_to_isolate=["2!", "3!"],
            font_size=45,
            color=WHITE
        )

        # Combinations: Isolate "n!", "r!", "(n-r)!"
        combination_title = Text(
            "Combinations",
            font="CMU Serif",
            font_size=38,
            color=WHITE
        )
        combination_equation = MathTex(
            r"\binom{n}{r}=\frac{n!}{r!(n-r)!}",
            substrings_to_isolate=["n!", "r!", "(n-r)!"],
            font_size=45,
            color=WHITE
        )

        # Group each title and equation together with a larger gap (buff=0.45)
        group1 = VGroup(binom_title, binom_equation).arrange(DOWN, buff=0.45)
        group2 = VGroup(taylor_title, taylor_equation).arrange(DOWN, buff=0.45)
        group3 = VGroup(combination_title, combination_equation).arrange(DOWN, buff=0.45)

        # Position the groups evenly
        self.all_elements = VGroup(group1, group2, group3).arrange(DOWN, buff=0.5)
        self.all_elements.move_to(ORIGIN)

        self.rects = VGroup(
            SurroundingRectangle(binom_equation.get_part_by_tex("2!"), buff=0.1),
            SurroundingRectangle(taylor_equation.get_part_by_tex("2!"), buff=0.1),
            SurroundingRectangle(taylor_equation.get_part_by_tex("3!"), buff=0.1),
            SurroundingRectangle(combination_equation.get_part_by_tex("n!"), buff=0.1),
            SurroundingRectangle(combination_equation.get_part_by_tex("r!"), buff=0.1),
            SurroundingRectangle(combination_equation.get_part_by_tex("(n-r)!"), buff=0)
        )

    def construct(self):
        self.camera.background_color = "#050A12"

        # Call the helper method to build and position the components
        self.hook_s1()

        # Add and animate elements
        self.wait(1)
        self.play(LaggedStart(*[FadeIn(i, shift=DOWN) for i in self.all_elements], lag_ratio=1))
        self.wait(1)
        self.play(LaggedStart(*[Create(rect) for rect in self.rects], lag_ratio=0.6))
        self.wait(2)

        # Clear the screen: fade out everything currently displayed simultaneously
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

%manim -v ERROR -qm FactrioalScene
