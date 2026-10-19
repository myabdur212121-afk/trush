from manim import *


class FixedArrow(VGroup):
    def __init__(self, start, end, color=YELLOW, tip_size=0.14, stroke_width=4):
        direction = (end - start) / np.linalg.norm(end - start)
        shaft = Line(start, end - direction * tip_size * 0.6, color=color, stroke_width=stroke_width)
        tip = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0)
        tip.scale(tip_size).rotate(np.arctan2(direction[1], direction[0]) - PI / 2)
        tip.move_to(end - direction * tip_size * 0.6)
        super().__init__(shaft, tip)
        self.shaft = shaft

    def get_start(self):
        return self.shaft.get_start()

    def scale(self, scale_factor, scale_tips=False, **kwargs):
        return super().scale(scale_factor, **kwargs)


class GeneralizationScene(Scene):
    def make_man(self, letter, radius=0.3):
        circle = Circle(radius=radius, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=2)
        name = Text(letter, font="CMU Serif", font_size=28, color=BLACK, weight=BOLD)
        name.move_to(circle.get_center())
        return VGroup(circle, name)

    def construct(self):
        self.camera.background_color = "#050A12"

        equation = VGroup(*[MathTex(part, font_size=52, color=WHITE)
                            for part in [r"3!", "=", "1", r"\times", "2", r"\times", "3", "=", "6"]])
        equation.arrange(RIGHT, buff=0.18)
        equation.move_to([-1.6, 0, 0])
        arrangements = VGroup()
        for row, word in enumerate(["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]):
            group = VGroup(*[self.make_man(letter, radius=0.26) for letter in word])
            group.arrange(RIGHT, buff=0.1)
            group.move_to([4.35, 2.0 - row * 0.78, 0])
            arrangements.add(group)

        men = VGroup(*[self.make_man(letter) for letter in ["A", "B", "C"]],
                     Text("⋯", font="CMU Serif", font_size=36, color=WHITE),
                     *[self.make_man(letter) for letter in ["L", "M", "N"]])
        men.arrange(RIGHT, buff=0.42)
        men.move_to([0, 1.95, 0])
        man_of = {"A": men[0], "B": men[1], "C": men[2],
                  "L": men[4], "M": men[5], "N": men[6]}

        block_x = [-3.54 + 1.18 * k for k in range(7)]
        blocks = VGroup()
        for x in block_x:
            square = Square(side_length=0.78, color=WHITE, stroke_width=4)
            square.move_to([x, 0.2, 0])
            blocks.add(square)
        choice_texts = ["n", "(n-1)", "(n-2)", r"\cdots", "3", "2", "1"]
        choices = VGroup()
        for k, x in enumerate(block_x):
            choice = MathTex(choice_texts[k], font_size=30, color=YELLOW)
            choice.move_to([x, -0.75, 0])
            choices.add(choice)
        crosses = VGroup(*[Text("×", font="CMU Serif", font_size=26, color=YELLOW) for _ in range(6)])
        n_bang = MathTex(r"n!", font_size=52, color=WHITE)
        n_bang.move_to([0, 3.2, 0])

        self.add(equation, arrangements)
        self.wait(0.5)
        self.play(LaggedStart(*[FadeOut(row) for row in arrangements], lag_ratio=0.15),
                  equation.animate.move_to(ORIGIN), run_time=1.2)
        self.wait(0.3)
        self.play(Transform(equation[0], n_bang), *[FadeOut(token) for token in equation[1:]], run_time=1)
        n_bang = equation[0]
        self.play(LaggedStart(*[FadeIn(man, scale=0.5) for man in men], lag_ratio=0.1))
        self.wait(0.3)
        self.play(LaggedStart(*[Create(block) for block in blocks], lag_ratio=0.15))
        self.wait(0.3)

        remaining = [man_of[letter] for letter in ["A", "B", "C", "L", "M", "N"]]
        for stage in range(3):
            top = blocks[stage].get_top() + UP * 0.1
            arrows = VGroup(*[FixedArrow(man.get_bottom() + DOWN * 0.08, top) for man in remaining])
            self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.1), run_time=1)
            self.play(FadeOut(arrows), run_time=0.4)
            self.play(Write(choices[stage]), run_time=0.5)
            placer = remaining.pop(0)
            self.play(placer.animate.move_to(blocks[stage].get_center()), run_time=0.8)
            self.wait(0.2)

        self.play(Write(choices[3]), run_time=0.5)
        self.wait(0.2)
        remaining_final = [man_of[letter] for letter in ["L", "M", "N"]]
        for stage in [4, 5, 6]:
            top = blocks[stage].get_top() + UP * 0.1
            arrows = VGroup(*[FixedArrow(man.get_bottom() + DOWN * 0.08, top) for man in remaining_final])
            self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.12), run_time=1)
            self.play(FadeOut(arrows), run_time=0.4)
            self.play(Write(choices[stage]), run_time=0.5)
            placer = remaining_final.pop(0)
            self.play(placer.animate.move_to(blocks[stage].get_center()), run_time=0.8)
            self.wait(0.2)
        for k, cross in enumerate(crosses):
            gap_x = (choices[k].get_right()[0] + choices[k + 1].get_left()[0]) / 2
            cross.move_to([gap_x, -0.75, 0])
        self.play(LaggedStart(*[FadeIn(cross, scale=0.5) for cross in crosses], lag_ratio=0.12))
        self.wait(0.5)

        final_eq = MathTex(r"n! = n \times (n-1) \times (n-2) \times \cdots \times 3 \times 2 \times 1",
                           font_size=40, color=WHITE,
                           substrings_to_isolate=["n!", "=", "n", "(n-1)", "(n-2)",
                                                  r"\cdots", "3", "2", "1", r"\times"])
        final_eq.set_color(YELLOW)
        final_eq.get_part_by_tex("=").set_color(WHITE)
        final_eq.get_part_by_tex("n!").set_color(WHITE)
        final_eq.move_to([0, -0.2, 0])
        final_eq.set_opacity(0)
        self.add(final_eq)

        choice_targets = [final_eq.get_part_by_tex(tex).get_center()
                          for tex in ["n", "(n-1)", "(n-2)", r"\cdots", "3", "2", "1"]]
        cross_parts = [final_eq.id_to_vgroup_dict[mid] for tex, mid in final_eq.matched_strings_and_ids if tex == r"\times"]
        cross_targets = [cross_parts[k].get_center() for k in range(6)]
        bang_target = final_eq.get_part_by_tex("n!").get_center()
        bang_scale = final_eq.get_part_by_tex("n!").height / n_bang.height
        self.play(FadeOut(blocks), FadeOut(men),
                  *[choice.animate.move_to(choice_targets[k]) for k, choice in enumerate(choices)],
                  *[cross.animate.move_to(cross_targets[k]) for k, cross in enumerate(crosses)],
                  n_bang.animate.move_to(bang_target).scale(bang_scale), run_time=1.3)
        self.play(final_eq.animate.set_opacity(1), FadeOut(choices), FadeOut(crosses), FadeOut(n_bang), run_time=0.5)
        frame = Rectangle(width=final_eq.width + 0.35, height=final_eq.height + 0.3, color=WHITE, stroke_width=4)
        frame.move_to(final_eq.get_center())
        self.play(ShowPassingFlash(frame, time_width=0.15), run_time=1.4)
        self.wait(1)
