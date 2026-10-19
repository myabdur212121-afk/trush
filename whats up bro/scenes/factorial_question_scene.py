from manim import *


class FixedArrow(VGroup):
    def __init__(self, start, end, color=YELLOW, tip_size=0.16, stroke_width=5):
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


class FactorialQuestionScene(Scene):
    def make_player(self, letter):
        circle = Circle(radius=0.38, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=3)
        name = Text(letter, font="CMU Serif", font_size=36, color=BLACK, weight=BOLD)
        name.move_to(circle.get_center())
        return VGroup(circle, name)

    def make_field(self):
        field = VGroup()
        ground = Rectangle(width=11.4, height=4.8, color=WHITE, stroke_width=3,
                           fill_color="#17573A", fill_opacity=0.9)
        ground.move_to([0, -0.95, 0])
        middle_line = Line(ground.get_top(), ground.get_bottom(), color=WHITE, stroke_width=3)
        center_circle = Circle(radius=0.75, color=WHITE, stroke_width=3).move_to(ground.get_center())
        center_dot = Dot(point=ground.get_center(), radius=0.05, color=WHITE)
        left_box = Rectangle(width=1.6, height=2.4, color=WHITE, stroke_width=3)
        left_box.move_to([ground.get_left()[0] + 0.8, -0.95, 0])
        right_box = Rectangle(width=1.6, height=2.4, color=WHITE, stroke_width=3)
        right_box.move_to([ground.get_right()[0] - 0.8, -0.95, 0])
        field.add(ground, middle_line, center_circle, center_dot, left_box, right_box)
        self.spots = {"GK": np.array([-4.65, -0.95, 0]), "DF": np.array([0, -0.95, 0]),
                      "ST": np.array([4.65, -0.95, 0])}
        for label, spot in self.spots.items():
            text = Text(label, font="CMU Serif", font_size=26, color=WHITE)
            text.move_to(spot + DOWN * 0.95)
            field.add(text)
        return field

    def make_status_bar(self):
        outline = Rectangle(width=6, height=0.3, color=WHITE, stroke_width=3)
        outline.move_to([0, 3.55, 0])
        self.bar_left = outline.get_left()[0] + 0.08
        fill = Rectangle(width=5.84, height=0.18, stroke_width=0,
                         fill_color=WHITE, fill_opacity=1)
        fill.move_to([self.bar_left + 5.84 / 2, 3.55, 0])
        return outline, fill, self.make_bar_target(0.45)

    def make_bar_target(self, level):
        target = Rectangle(width=5.84 * level, height=0.18, stroke_width=0,
                           fill_color="#F6A15C", fill_opacity=1)
        target.move_to([self.bar_left + target.width / 2, 3.55, 0])
        return target

    def swap(self, player1, player2):
        path1 = ArcBetweenPoints(player1.get_center(), player2.get_center(), angle=PI / 3)
        path2 = ArcBetweenPoints(player2.get_center(), player1.get_center(), angle=PI / 3)
        self.play(MoveAlongPath(player1, path1), MoveAlongPath(player2, path2), run_time=1.2)

    def make_blocks(self):
        blocks = VGroup()
        for number in ["1", "2", "3"]:
            square = Square(side_length=1.0, color=WHITE, stroke_width=4)
            label = Text(number, font="CMU Serif", font_size=32, color=WHITE)
            label.next_to(square, DOWN, buff=0.2)
            blocks.add(VGroup(square, label))
        blocks.arrange(RIGHT, buff=0.36)
        blocks.move_to(ORIGIN)
        return blocks

    def construct(self):
        self.camera.background_color = "#050A12"
        players = VGroup(self.make_player("A"), self.make_player("B"), self.make_player("C"))
        players.arrange(RIGHT, buff=0.6).set_z_index(5)
        home = [player.get_center().copy() for player in players]
        field = self.make_field()
        bar_outline, bar_fill, bar_less = self.make_status_bar()
        question_text = Text("তাহলে তিনজনকে মোট কতভাবে সাজানো যায়?",
                             font="Noto Serif Bengali", font_size=42, color=WHITE)
        question_text.move_to([0, -1.3, 0])
        blocks = self.make_blocks()

        self.play(LaggedStart(*[FadeIn(player, scale=0.5) for player in players], lag_ratio=0.3))
        self.wait(0.5)
        self.play(players.animate.to_edge(UP, buff=0.7))
        self.play(DrawBorderThenFill(field), run_time=2)
        self.wait(0.3)
        self.play(players[0].animate.move_to(self.spots["GK"]),
                  players[2].animate.move_to(self.spots["DF"]),
                  players[1].animate.move_to(self.spots["ST"]), run_time=1.2)
        self.play(Create(bar_outline), FadeIn(bar_fill))
        path_a = ArcBetweenPoints(players[0].get_center(), players[1].get_center(), angle=PI / 3)
        path_b = ArcBetweenPoints(players[1].get_center(), players[0].get_center(), angle=PI / 3)
        self.play(MoveAlongPath(players[0], path_a), MoveAlongPath(players[1], path_b), run_time=1.2)
        self.wait(1)
        self.play(Transform(bar_fill, bar_less), run_time=0.8)
        for first, second, level in [(1, 2, 0.30), (1, 0, 0.48), (2, 1, 0.36), (1, 0, 0.55)]:
            self.swap(players[first], players[second])
            self.play(Transform(bar_fill, self.make_bar_target(level)), run_time=0.5)
            self.wait(0.3)
        self.play(FadeOut(field), FadeOut(bar_outline), FadeOut(bar_fill))
        self.play(*[player.animate.move_to(home[i]) for i, player in enumerate(players)], run_time=1.2)
        self.wait(0.3)
        self.play(Write(question_text))
        self.wait(1)
        self.play(Unwrite(question_text))
        self.play(players.animate.move_to(UP * config.frame_height / 3), run_time=1)
        self.play(LaggedStart(*[Create(block[0]) for block in blocks], lag_ratio=0.3))
        self.play(LaggedStart(*[Write(block[1]) for block in blocks], lag_ratio=0.3))
        def choice_arrows(who, block_number):
            top = blocks[block_number][0].get_top() + UP * 0.12
            return VGroup(*[FixedArrow(players[i].get_bottom() + DOWN * 0.12, top) for i in who])

        def choice_number(block_number, digit):
            number = Text(digit, font="CMU Serif", font_size=40, color=YELLOW)
            number.move_to(blocks[block_number][0].get_center())
            return number

        arrows1 = choice_arrows([0, 1, 2], 0)
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows1], lag_ratio=0.25))
        self.wait(0.3)
        self.play(FadeOut(arrows1))
        num_three = choice_number(0, "3")
        self.play(Write(num_three))
        self.wait(0.3)
        self.play(players[0].animate.move_to(blocks[0][0].get_center()), run_time=1)

        arrows2 = choice_arrows([1, 2], 1)
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows2], lag_ratio=0.25))
        self.wait(0.3)
        self.play(FadeOut(arrows2))
        num_two = choice_number(1, "2")
        self.play(Write(num_two))
        self.wait(0.3)
        self.play(players[1].animate.move_to(blocks[1][0].get_center()), run_time=1)

        arrows3 = choice_arrows([2], 2)
        self.play(GrowArrow(arrows3[0]))
        self.wait(0.3)
        self.play(FadeOut(arrows3))
        num_one = choice_number(2, "1")
        self.play(Write(num_one))
        self.wait(0.3)
        self.play(players[2].animate.move_to(blocks[2][0].get_center()), run_time=1)
        self.wait(1)
        self.play(FadeOut(players), FadeOut(blocks),
                  FadeOut(num_three), FadeOut(num_two), FadeOut(num_one))
        self.wait(0.5)
