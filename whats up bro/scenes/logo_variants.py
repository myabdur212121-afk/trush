from manim import *


class Logo1Fill2Blank(VGroup):
    def __init__(self, radius=2, font_size=48, color="#1D9E75", **kwargs):
        super().__init__(**kwargs)
        self.logo_radius = radius

        sector_filled = Sector(
            radius=radius, start_angle=PI/6, angle=2*PI/3,
        ).set_fill(color=color, opacity=1).set_stroke(color=WHITE, width=2)

        sector_blank1 = Sector(
            radius=radius, start_angle=PI/6 + 2*PI/3, angle=2*PI/3,
        ).set_fill(opacity=0).set_stroke(color=WHITE, width=2)

        sector_blank2 = Sector(
            radius=radius, start_angle=PI/6 + 4*PI/3, angle=2*PI/3,
        ).set_fill(opacity=0).set_stroke(color=WHITE, width=2)

        self.sectors = VGroup(sector_filled, sector_blank1, sector_blank2)
        self.label = Text("1Fill2Blank", font="CMU Serif", font_size=font_size)
        self.label.next_to(self.sectors, DOWN, buff=0.6)

        self.add(self.sectors, self.label)


# 1. Mathematical Construction
def logo_construction(scene, logo, wait_time=3):
    radius = logo.logo_radius
    circle = Circle(radius=radius).set_stroke(color=WHITE, width=2)
    angles = [PI/6, PI/6 + 2*PI/3, PI/6 + 4*PI/3]
    lines = VGroup(*[
        Line(ORIGIN, radius * np.array([np.cos(a), np.sin(a), 0]))
        .set_stroke(color=WHITE, width=1.5)
        for a in angles
    ])
    scene.play(Create(circle, rate_func=smooth), run_time=1.5)
    scene.play(
        LaggedStart(*[Create(l) for l in lines], lag_ratio=0.5),
        run_time=2
    )
    scene.wait(0.3)
    scene.play(FadeOut(circle), FadeOut(lines), FadeIn(logo.sectors), run_time=0.8)
    scene.wait(0.3)
    scene.play(Write(logo.label, rate_func=smooth), run_time=1.5)
    scene.wait(wait_time)


# 2. Unfold
def logo_unfold(scene, logo, wait_time=3):
    scene.play(
        LaggedStart(
            *[GrowFromCenter(s, rate_func=smooth) for s in logo.sectors],
            lag_ratio=0.6
        ),
        run_time=3
    )
    scene.play(Write(logo.label, rate_func=smooth), run_time=1.5)
    scene.wait(wait_time)


# 3. Spin Grow
def logo_spin_grow(scene, logo, wait_time=3):
    scene.play(GrowFromCenter(logo.sectors, rate_func=smooth), run_time=1.2)
    scene.play(Rotate(logo.sectors, angle=2 * PI, rate_func=smooth), run_time=1.3)
    scene.play(Write(logo.label, rate_func=smooth), run_time=1.5)
    scene.wait(wait_time)


# 4. From Fraction
def logo_from_fraction(scene, logo, wait_time=3):
    fraction = MathTex(r"\frac{1}{3}", font_size=120)
    scene.play(Write(fraction, rate_func=smooth), run_time=1.5)
    scene.wait(0.5)
    scene.play(
        ReplacementTransform(fraction, logo.sectors),
        run_time=1.5
    )
    scene.wait(0.3)
    scene.play(Write(logo.label, rate_func=smooth), run_time=1.5)
    scene.wait(wait_time)


# 5. Text First
def logo_text_first(scene, logo, wait_time=3):
    temp_label = logo.label.copy().move_to( ORIGIN)
    scene.play(Write(temp_label, rate_func=smooth), run_time=2)
    scene.wait(0.3)
    scene.play(
        ReplacementTransform(temp_label, logo.label),
        GrowFromCenter(logo.sectors, rate_func=smooth),
        run_time=2
    )
    scene.wait(wait_time)


# 6. Cascade Fade
def logo_cascade(scene, logo, wait_time=3):
    scene.play(
        LaggedStart(
            FadeIn(logo.sectors[1], shift=DOWN * 0.3),
            FadeIn(logo.sectors[2], shift=DOWN * 0.3),
            FadeIn(logo.sectors[0], shift=UP * 0.3),
            lag_ratio=0.5
        ),
        run_time=2.5
    )
    scene.play(Write(logo.label, rate_func=smooth), run_time=1.5)
    scene.wait(wait_time)


class LogoConstructionScene(Scene):
    def construct(self):
        logo_construction(self, Logo1Fill2Blank())


class LogoUnfoldScene(Scene):
    def construct(self):
        logo_unfold(self, Logo1Fill2Blank())


class LogoSpinGrowScene(Scene):
    def construct(self):
        logo_spin_grow(self, Logo1Fill2Blank())


class LogoFromFractionScene(Scene):
    def construct(self):
        logo_from_fraction(self, Logo1Fill2Blank())


class LogoTextFirstScene(Scene):
    def construct(self):
        logo_text_first(self, Logo1Fill2Blank())


class LogoCascadeScene(Scene):
    def construct(self):
        logo_cascade(self, Logo1Fill2Blank())
