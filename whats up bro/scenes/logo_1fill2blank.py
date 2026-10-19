from manim import *

config.background_color = "#050A12"
BRAND_GOLD = "#FFD23F"
NAVY = "#0B1626"


class FillBlankMark(Scene):
    def build_mark(self):
        self.badge = Circle(radius=1.55, color=WHITE, stroke_width=6, fill_color=NAVY, fill_opacity=1)
        left, right, top, bottom = -0.96, 0.96, 0.62, -0.52
        step = (right - left) / 3
        self.filled = Rectangle(width=step, height=top - bottom, color=BRAND_GOLD, fill_color=BRAND_GOLD, fill_opacity=1, stroke_width=0)
        self.filled.move_to([(left + step / 2), (top + bottom) / 2, 0])
        apex = np.array([left + step / 2, top - 0.14, 0])
        base_y = bottom + 0.08
        self.pyramid = Polygon(apex, [left + 0.1, base_y, 0], [left + step - 0.1, base_y, 0], color=NAVY, fill_color=NAVY, fill_opacity=1, stroke_width=0)
        self.box = Rectangle(width=right - left, height=top - bottom, color=WHITE, stroke_width=5)
        self.box.move_to([0, (top + bottom) / 2, 0])
        self.dividers = VGroup(Line([left + step, bottom, 0], [left + step, top, 0], color=WHITE, stroke_width=5),
                               Line([left + 2 * step, bottom, 0], [left + 2 * step, top, 0], color=WHITE, stroke_width=5))
        self.mark = VGroup(self.badge, self.filled, self.pyramid, self.box, self.dividers)


class LogoScene(FillBlankMark):
    def construct(self):
        self.build_mark()
        name = Text("1Fill2Blank", font="CMU Serif", font_size=46, color=WHITE, weight=BOLD, t2c={"1": BRAND_GOLD, "2": BRAND_GOLD})
        name.next_to(self.mark, DOWN, buff=0.28)
        self.add(VGroup(self.mark, name).scale(1.5))


class LogoIconScene(FillBlankMark):
    def construct(self):
        self.build_mark()
        self.add(self.mark.scale(1.9))
