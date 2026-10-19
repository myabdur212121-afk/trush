"""Part 1 — Opening + Intro, ending on the 'Combination / Chapter 1' title."""
from common import *


class Part1(Narrated, MovingCameraScene):
    Y0 = 1.8             # y of row 1
    DY = 1.2
    SC = 1.12            # equation scale

    def setup(self):
        super().setup()
        # line the '=' signs up so that the longest (row 4) is centred horizontally
        tex, info = expansion_row(4)
        tex.scale(self.SC).move_to(ORIGIN)
        self.X_EQ = info["eq"].get_center()[0]

    # --------------------------------------------------------------- helpers
    def row(self, n, scale=None):
        scale = scale or self.SC
        tex, info = expansion_row(n)
        tex.scale(scale)
        tex.shift(np.array([self.X_EQ - info["eq"].get_center()[0],
                            self.Y0 - (n - 1) * self.DY - info["eq"].get_center()[1], 0]))
        return tex, info

    def logo(self):
        if LOGO_FILE.exists():
            return ImageMobject(str(LOGO_FILE)).set_height(2.2)
        # placeholder mark: a tiny Pascal triangle of dots inside a ring
        ring = Circle(radius=1.0, stroke_color=A_COL, stroke_width=4)
        dots = VGroup()
        for n in range(4):
            for k in range(n + 1):
                dots.add(Dot(np.array([(k - n / 2) * 0.36, 0.5 - n * 0.33, 0]), radius=0.07,
                             color=[HL, A_COL, B_COL, K_COL][n]))
        name = en(CHANNEL_NAME, 34, color=SOFT).next_to(ring, DOWN, buff=0.35)
        return VGroup(ring, dots, name).move_to(ORIGIN)

    # --------------------------------------------------------------- scenes
    def construct(self):
        frame = self.camera.frame
        self.opening()

        # ============ s1a : a, b  → (a+b)^1, (a+b)^2 ============
        self.clip("p1_s1a")
        a = MathTex("a", color=A_COL).scale(2.2).shift(LEFT * 1.6)
        b = MathTex("b", color=B_COL).scale(2.2).shift(RIGHT * 1.6)
        self.at(2.75, FadeIn(a, scale=0.4), rt=0.5)
        self.at(3.4, FadeIn(b, scale=0.4), rt=0.5)

        gen = MathTex("(", "a", "+", "b", ")", "^{n}").scale(1.9)
        gen[1].set_color(A_COL); gen[3].set_color(B_COL)
        self.upto(4.6)
        self.playto(6.6, ReplacementTransform(a, gen[1]), ReplacementTransform(b, gen[3]),
                    FadeIn(gen[2], scale=0.5), FadeIn(gen[0], shift=RIGHT * 0.3),
                    FadeIn(gen[4], shift=LEFT * 0.3), FadeIn(gen[5], shift=DOWN * 0.3))
        self.play(Indicate(gen[5], color=HL, scale_factor=1.4), run_time=0.8)

        r1, i1 = self.row(1)
        one = MathTex("^{1}").scale(1.9).move_to(gen[5])
        self.upto(8.9)
        self.playto(9.8, Transform(gen[5], one))
        # move generic (a+b)^1 into row-1 LHS slot
        self.playto(11.9, *[ReplacementTransform(g, l) for g, l in zip(gen, i1["lhs"])])
        self.playto(13.3, Write(i1["eq"]), Write(i1["rhs"]))
        self.at(13.9, Circumscribe(i1["rhs"], color=HL, fade_out=True, stroke_width=2), rt=0.9)

        r2, i2 = self.row(2)
        self.at(16.4, TransformFromCopy(i1["lhs"], i2["lhs"]), rt=1.2)
        self.upto(18.5)
        self.playto(21.2, Write(i2["eq"]), Write(i2["rhs"]))
        self.end_clip()

        # ============ s1b : (a+b)^3, (a+b)^4 ============
        self.clip("p1_s1b")
        r3, i3 = self.row(3)
        self.at(1.9, TransformFromCopy(i2["lhs"], i3["lhs"]), rt=1.2)
        self.upto(4.2)
        self.playto(8.6, Write(i3["eq"]), Write(i3["rhs"]))
        r4, i4 = self.row(4)
        self.at(11.9, TransformFromCopy(i3["lhs"], i4["lhs"]), rt=1.3)
        self.upto(14.0)
        self.playto(27.2, Write(i4["eq"]), Write(i4["rhs"]), rate_func=linear)
        self.at(29.6, Wiggle(i4["rhs"], scale_value=1.04, rotation_angle=0.01 * TAU), rt=1.4)
        self.end_clip(pad=1.0)                       # [wait(1)]

        rows = [(r1, i1), (r2, i2), (r3, i3), (r4, i4)]

        # ============ s2 : powers keep growing ============
        self.clip("p1_s2")
        extra = []
        starts = {5: 4.1, 6: 6.7, 7: 9.2}
        for n in (5, 6, 7):
            rn, iN = self.row(n)
            prev = rows[-1][1] if not extra else extra[-1][1]
            box = VGroup(*[r for r, _ in rows], *[r for r, _ in extra], rn)
            w = max(box.width + 2.0, (box.height + 1.6) * 16 / 9, config.frame_width)
            c = box.get_center()
            self.upto(starts[n])
            self.play(TransformFromCopy(prev["lhs"], iN["lhs"]),
                      frame.animate.set(width=w).move_to(c), run_time=0.8)
            self.play(Write(iN["eq"]), Write(iN["rhs"]), run_time=1.6)
            extra.append((rn, iN))

        # outline of the growing right edge
        allrows = rows + extra
        ends = [r.get_right() + RIGHT * 0.25 for r, _ in allrows]
        edge = VMobject().set_points_smoothly(ends).set_stroke(HL, width=4, opacity=0.9)
        self.at(12.5, Create(edge), rt=2.2)
        self.at(16.0, *[r.animate.set_opacity(0.45) for r, _ in extra], FadeOut(edge), rt=1.2)
        self.upto(21.0)
        self.playto(22.8, *[FadeOut(r) for r, _ in extra],
                    frame.animate.set(width=config.frame_width).move_to(ORIGIN))
        self.end_clip()

        # ============ s3 : the coefficients → triangle ============
        self.clip("p1_s3")
        r0, i0 = expansion_row(0)
        col = VGroup(r0, *[r for r, _ in rows])
        # shrink the equations into a left column
        target_scale = 0.7
        eqs = VGroup(*[r for r, _ in rows])
        self.upto(0.4)
        self.playto(2.6, eqs.animate.scale(target_scale).to_edge(LEFT, buff=0.4).shift(DOWN * 0.35))
        r0.scale(self.SC * target_scale)
        r0.shift(i1["eq"].get_center() + UP * self.DY * target_scale - i0["eq"].get_center())
        coefs = [t["coef"] for _, info in rows for t in info["terms"] if t["coef"] is not None]
        self.playto(6.9, LaggedStart(*[Indicate(c, color=K_COL, scale_factor=1.5) for c in coefs],
                                     lag_ratio=0.25))

        # triangle rows sit on the same lines as the equations they come from
        tri = pascal_rows(5, dx=0.95, dy=self.DY * target_scale, size=46)
        tri.set_x(4.3)
        tri.shift(UP * (i1["eq"].get_y() - tri[1][0].get_y()))
        self.at(7.6, FadeIn(r0, shift=DOWN * 0.2), rt=0.5)
        self.play(TransformFromCopy(i0["terms"][0]["all"], tri[0][0]), run_time=0.7)
        row_times = {1: 10.4, 2: 12.8, 3: 15.7, 4: 19.7}
        for n in range(1, 5):
            info = rows[n - 1][1]
            self.upto(row_times[n])
            rt = 1.0 if n < 4 else 2.2
            self.play(LaggedStart(*[TransformFromCopy(t["coef"] if t["coef"] is not None else t["body"],
                                                      tri[n][k])
                                    for k, t in enumerate(info["terms"])], lag_ratio=0.3),
                      run_time=rt)

        # coincidence?  -> triangle to centre
        self.upto(23.2)
        self.playto(24.9, FadeOut(VGroup(r0, eqs), shift=LEFT * 0.5),
                    tri.animate.scale(1.15).move_to(ORIGIN))
        outline = Polygon(tri[0][0].get_top() + UP * 0.35,
                          tri[4][0].get_corner(DL) + LEFT * 0.45 + DOWN * 0.3,
                          tri[4][-1].get_corner(DR) + RIGHT * 0.45 + DOWN * 0.3)
        outline.set_stroke(A_COL, width=2.5, opacity=0.7)
        self.at(25.6, Create(DashedVMobject(outline, num_dashes=45)), rt=1.8)
        dashed = self.mobjects[-1]
        self.at(28.9, LaggedStart(*[Indicate(m, color=WHITE, scale_factor=1.25)
                                    for row in tri for m in row], lag_ratio=0.08), rt=3.4)
        six = tri[4][2]
        others = VGroup(*[m for row in tri for m in row if m is not six])
        ring = Circle(radius=0.42, color=K_COL, stroke_width=4).move_to(six)
        self.at(34.0, others.animate.set_opacity(0.35), six.animate.set_color(K_COL).scale(1.35),
                Create(ring), rt=1.1)
        q = MathTex("?", color=K_COL).scale(1.3).next_to(ring, UR, buff=0.05)
        self.at(36.2, FadeIn(q, shift=UP * 0.2, scale=0.5), rt=0.6)
        fours = VGroup(tri[4][1], tri[4][3])
        self.at(37.6, fours.animate.set_opacity(1).set_color(B_COL), rt=0.5)
        self.play(fours.animate.set_opacity(0.35).set_color(WHITE), run_time=0.5)
        self.end_clip()

        # ============ s4 : another viewpoint → Combination ============
        self.clip("p1_s4")
        self.at(0.5, FadeOut(q), FadeOut(ring), others.animate.set_opacity(1),
                six.animate.set_color(WHITE).scale(1 / 1.35), rt=0.9)
        # "another point of view": flip the triangle like a card
        self.at(2.0, Rotate(VGroup(tri, dashed), angle=TAU, axis=UP), rt=3.2,
                rate_func=smooth)
        self.at(6.7, VGroup(tri, dashed).animate.scale(0.92), rt=2.5, rate_func=there_and_back)
        self.upto(11.55)
        chapter_title(self, "Combination", "Chapter 1", clear_after=True)
        self.wait(0.5)

    # --------------------------------------------------------------- opening
    def opening(self):
        self.add_sound(str(AUDIO / "music_intro.wav"))
        self.wait(0.8)
        lg = self.logo()
        if isinstance(lg, ImageMobject):
            self.play(FadeIn(lg, scale=0.8), run_time=1.5)
        else:
            ring, dots, name = lg
            self.play(Create(ring), run_time=1.0)
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.1),
                      FadeIn(name, shift=UP * 0.2), run_time=1.2)
        self.wait(1.4)
        self.play(FadeOut(lg, scale=1.1), run_time=0.8)

        title = en("Binomial Theorem", 72)
        sub = bn("সংখ্যাগুলো আসলে কোথা থেকে আসে?", 38, color=SOFT)
        line = Line(LEFT, RIGHT).set_width(title.width * 0.9).set_stroke(width=2)
        line.set_color([BG, A_COL, HL, A_COL, BG])
        grp = VGroup(title, line, sub).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3, scale=1.3) for c in title], lag_ratio=0.06),
                  GrowFromCenter(line), run_time=1.6)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(grp, shift=UP * 0.3), run_time=1.0)
        self.wait(0.8)
