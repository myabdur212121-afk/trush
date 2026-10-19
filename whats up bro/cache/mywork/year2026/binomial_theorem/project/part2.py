"""Part 2 — Chapter 1 (factorial → combination) + opening of Chapter 2,
ending on the 'Binomial Theorem / Chapter 2' title."""
from common import *

PCOL = {"A": A_COL, "B": B_COL, "C": K_COL, "D": HL, "E": "#C39BFF"}


# ------------------------------------------------------------------ small builders
def person(L, scale=1.0, col=None):
    col = col or PCOL.get(L, SOFT)
    head = Circle(radius=0.32, color=col, stroke_width=3).set_fill(col, 0.15)
    body = Arc(radius=0.5, start_angle=0, angle=PI, color=col, stroke_width=3)
    body.next_to(head, DOWN, buff=0.06)
    lab = MathTex(L, color=col).scale(0.8).move_to(head)
    return VGroup(body, head, lab).scale(scale)


def dot_person(col=SOFT, r=0.16):
    return Dot(radius=r, color=col)


def slot(w=1.15, h=1.55):
    return RoundedRectangle(corner_radius=0.14, width=w, height=h).set_stroke(SOFT, 2, 0.7)


def tile(word, s=0.62):
    g = VGroup()
    for ch in word:
        sq = Square(s).set_stroke(PCOL[ch], 2.5).set_fill(PCOL[ch], 0.12)
        g.add(VGroup(sq, MathTex(ch, color=PCOL[ch]).scale(0.75).move_to(sq)))
    return g.arrange(RIGHT, buff=0.08)


def set_tex(letters, scale=1.0):
    parts = [r"\{"]
    for i, L in enumerate(letters):
        if i:
            parts.append(",")
        parts.append(L)
    parts.append(r"\}")
    t = MathTex(*parts).scale(scale)
    for m, p in zip(t, parts):
        if p in PCOL:
            m.set_color(PCOL[p])
    return t


def word_tex(word, scale=1.0):
    t = MathTex(*list(word)).scale(scale)
    for m, ch in zip(t, word):
        m.set_color(PCOL[ch])
    return t


def node(L, r=0.27):
    c = Circle(radius=r, color=PCOL[L], stroke_width=3).set_fill(BG, 1)
    return VGroup(c, MathTex(L, color=PCOL[L]).scale(0.7).move_to(c))


def edge(a, b, col=SOFT):
    return Line(a.get_center(), b.get_center(), buff=0.3).set_stroke(col, 2.5, 0.8)


def lbl(tex, col=K_COL, scale=1.0):
    return MathTex(tex, color=col).scale(scale)


class Part2(Narrated, MovingCameraScene):

    def clear_all(self, rt=0.6, keep=()):
        mobs = [m for m in self.mobjects if m not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=rt)

    def construct(self):
        self.wait(0.4)
        for i in range(1, 18):
            getattr(self, f"s{i:02d}")()
        self.wait(0.5)

    # ============================================================ p2_01  factorial
    def s01(self):
        self.clip("p2_01")
        nf = MathTex("n!").scale(2.6)
        self.at(7.2, FadeIn(nf, scale=0.5), rt=0.8)
        eq = MathTex("n!", "=", "1", r"\times", "2", r"\times", "3", r"\times", "4",
                     r"\times", r"\cdots", r"\times", "n").scale(1.35)
        self.at(8.3, ReplacementTransform(nf, eq[0]), rt=0.8)
        self.play(Write(eq[1]), run_time=0.4)
        self.playto(14.6, LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in eq[2:]], lag_ratio=0.3))
        q = MathTex("?", color=K_COL).scale(1.6).next_to(eq[0], UP, buff=0.3)
        self.at(16.9, eq[1:].animate.set_opacity(0.3), eq[0].animate.set_color(HL),
                FadeIn(q, shift=UP * 0.2), rt=0.9)
        self.at(20.7, FadeOut(eq[1:], shift=RIGHT * 0.4), FadeOut(q), rt=0.9)
        self.at(24.3, eq[0].animate.scale(1.25).move_to(UP * 2.3), rt=1.0)
        self.play(Flash(eq[0], color=HL, line_length=0.3, flash_radius=0.9), run_time=0.8)

        # n distinct objects being re-arranged
        cols = [A_COL, B_COL, K_COL, HL, "#C39BFF"]
        xs = [(-2 + i) * 1.2 for i in range(5)]
        dots = VGroup(*[Dot(np.array([x, -0.2, 0]), radius=0.26, color=c) for x, c in zip(xs, cols)])
        br = Brace(dots, DOWN, color=SOFT)
        bl = MathTex("n", color=SOFT).next_to(br, DOWN)
        self.at(28.6, LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.15), rt=1.2)
        self.play(GrowFromCenter(br), FadeIn(bl), run_time=0.6)
        for perm in ([2, 0, 4, 1, 3], [4, 3, 0, 2, 1], [0, 1, 2, 3, 4]):
            self.play(*[d.animate.move_to(np.array([xs[perm[i]], -0.2, 0])) for i, d in enumerate(dots)],
                      path_arc=PI / 2, run_time=1.3)
        self.end_clip()
        self.clear_all(0.6)

    # ============================================================ p2_02  A B C
    def s02(self):
        self.clip("p2_02")
        P = VGroup(*[person(L) for L in "ABC"]).arrange(RIGHT, buff=0.9).move_to(UP * 1.2)
        self.at(3.6, LaggedStart(*[FadeIn(p, shift=UP * 0.3) for p in P], lag_ratio=0.35), rt=1.4)
        self.at(5.9, LaggedStart(*[Indicate(p[2], scale_factor=1.5) for p in P], lag_ratio=0.45), rt=1.5)
        slots = VGroup(*[slot() for _ in range(3)]).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.6)
        self.at(8.3, LaggedStart(*[Create(s) for s in slots], lag_ratio=0.2), rt=1.4)
        # same three people
        box = SurroundingRectangle(P, color=HL, buff=0.25, corner_radius=0.2)
        self.at(11.3, Create(box), rt=1.0)
        self.play(FadeOut(box), run_time=0.6)
        # nobody leaves, nobody new comes in
        ghost = person("D", col=GREY_B).set_opacity(0.4).next_to(P, RIGHT, buff=1.1)
        self.at(14.5, FadeIn(ghost, shift=LEFT * 0.4), rt=0.8)
        self.play(FadeOut(ghost, shift=RIGHT * 0.6), run_time=0.8)
        # place them in slots, then swap to show positions changing
        self.at(17.7, *[P[i].animate.scale(0.9).move_to(slots[i]) for i in range(3)], rt=1.3)
        self.play(P[0].animate.move_to(slots[2]), P[2].animate.move_to(slots[0]),
                  path_arc=PI / 2, run_time=1.2)
        self.play(P[1].animate.move_to(slots[0]), P[2].animate.move_to(slots[1]),
                  path_arc=-PI / 2, run_time=1.2)
        self.end_clip()
        self.clear_all(0.5)

    # ============================================================ p2_03  football
    def s03(self):
        self.clip("p2_03")
        pitch = VGroup(
            Rectangle(width=4.2, height=5.6),
            Line(LEFT * 2.1, RIGHT * 2.1),
            Circle(radius=0.6),
            Rectangle(width=2.0, height=0.9).shift(DOWN * 2.35),
            Rectangle(width=2.0, height=0.9).shift(UP * 2.35),
        ).set_stroke(SOFT, 2, 0.55).shift(LEFT * 1.2)
        self.at(0.2, Create(pitch), rt=1.8)
        pos = {"GK": pitch[0].get_bottom() + UP * 0.55, "DF": pitch.get_center() + DOWN * 1.3,
               "ST": pitch.get_center() + UP * 1.6}
        roles = VGroup(*[en(r, 22, color=SOFT).next_to(pos[r], LEFT, buff=0.45) for r in ("GK", "DF", "ST")])
        pl = {"GK": Dot(pos["GK"], radius=0.24, color=A_COL),
              "DF": Dot(pos["DF"], radius=0.24, color=B_COL),
              "ST": Dot(pos["ST"], radius=0.24, color=K_COL)}
        players = VGroup(*pl.values())
        self.at(2.4, LaggedStart(*[GrowFromCenter(p) for p in players], lag_ratio=0.3),
                FadeIn(roles), rt=1.4)
        # team-strength meter (no text): full at start
        frame_bar = RoundedRectangle(corner_radius=0.1, width=0.45, height=4.2).set_stroke(SOFT, 2)
        frame_bar.move_to(RIGHT * 3.4)
        fill = Rectangle(width=0.35, height=4.0).set_stroke(width=0).set_fill(HL, 0.85)
        fill.move_to(frame_bar.get_bottom() + UP * 0.1, aligned_edge=DOWN)
        self.at(4.9, FadeIn(frame_bar), GrowFromEdge(fill, DOWN), rt=1.0)
        # formation changes
        self.at(6.2, pl["DF"].animate.shift(RIGHT * 1.2), pl["ST"].animate.shift(LEFT * 1.0), rt=1.0)
        self.play(pl["DF"].animate.move_to(pos["DF"]), pl["ST"].animate.move_to(pos["ST"]), run_time=0.8)
        # keeper plays striker
        self.at(10.6, Indicate(pl["GK"], color=A_COL, scale_factor=1.5), rt=0.8)
        self.at(12.4, pl["GK"].animate.move_to(pos["ST"] + RIGHT * 0.8),
                pl["ST"].animate.move_to(pos["GK"]), path_arc=PI / 3, rt=1.6)

        def lower(h, col):
            t = Rectangle(width=0.35, height=h).set_stroke(width=0).set_fill(col, 0.85)
            t.move_to(frame_bar.get_bottom() + UP * 0.1, aligned_edge=DOWN)
            return Transform(fill, t)
        self.at(14.8, lower(2.3, B_COL), rt=1.2)
        # striker plays defence
        self.at(18.3, Indicate(pl["ST"], color=K_COL, scale_factor=1.5), rt=0.8)
        self.at(20.2, pl["ST"].animate.move_to(pos["DF"] + LEFT * 0.9),
                pl["DF"].animate.move_to(pos["GK"] + RIGHT * 0.9), path_arc=-PI / 3, rt=1.4)
        self.play(lower(1.1, K_COL), run_time=1.0)
        # back to A, B, C
        P = VGroup(*[person(L) for L in "ABC"]).arrange(RIGHT, buff=0.9).move_to(UP * 1.2)
        self.at(22.6, FadeOut(VGroup(pitch, roles, frame_bar, fill)), rt=0.8)
        self.at(23.7, *[ReplacementTransform(d, p) for d, p in zip([pl["GK"], pl["DF"], pl["ST"]], P)], rt=1.2)
        slots = VGroup(*[slot() for _ in range(3)]).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.6)
        self.at(26.4, FadeIn(slots), *[P[i].animate.scale(0.9).move_to(slots[i]) for i in range(3)], rt=1.2)
        self.play(P[0].animate.move_to(slots[1]), P[1].animate.move_to(slots[0]), path_arc=PI / 2, run_time=1.0)
        self.play(P[0].animate.move_to(slots[2]), P[2].animate.move_to(slots[1]), path_arc=PI / 2, run_time=1.0)
        q = MathTex("?", color=K_COL).scale(1.6).next_to(slots, UP, buff=0.5)
        self.at(30.6, FadeIn(q, scale=0.5), rt=0.6)
        self.end_clip()
        self.clear_all(0.5)

    # ============================================================ p2_04 / p2_05  counting positions
    def s04(self):
        self.clip("p2_04")
        P = VGroup(*[person(L, 0.9) for L in "ABC"]).arrange(RIGHT, buff=0.9).move_to(UP * 2.3)
        slots = VGroup(*[slot() for _ in range(3)]).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.6)
        nums = VGroup(*[MathTex(str(i + 1), color=SOFT).scale(0.7).next_to(s, UP, buff=0.12)
                        for i, s in enumerate(slots)])
        self.at(0.4, LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in P], lag_ratio=0.2), rt=1.2)
        self.at(3.4, LaggedStart(*[Create(s) for s in slots], lag_ratio=0.2), FadeIn(nums), rt=1.4)
        self.at(6.2, slots[0].animate.set_stroke(HL, 4, 1), rt=0.6)
        arrows = VGroup(*[Arrow(p.get_bottom(), slots[0].get_top(), buff=0.15, stroke_width=3,
                                color=PCOL[L], max_tip_length_to_length_ratio=0.12)
                          for p, L in zip(P, "ABC")])
        for i, t in enumerate((8.6, 9.6, 11.2)):
            self.at(t, GrowArrow(arrows[i]), Indicate(P[i], color=PCOL["ABC"[i]]), rt=0.7)
        self.c = VGroup()
        c1 = lbl("3", scale=1.3).next_to(slots[0], DOWN, buff=0.35)
        self.at(15.9, FadeIn(c1, scale=1.5), rt=0.6)
        self.at(17.5, FadeOut(arrows), P[0].animate.move_to(slots[0]),
                slots[0].animate.set_stroke(SOFT, 2, 0.7), rt=1.3)
        self.at(21.0, slots[1].animate.set_stroke(HL, 4, 1), rt=0.6)
        self.play(Wiggle(P[0], rotation_angle=0.03 * TAU), run_time=1.0)
        cross = Cross(P[0], stroke_color=K_COL, stroke_width=4).scale(0.6)
        self.play(Create(cross), run_time=0.5)
        self.play(FadeOut(cross), run_time=0.4)
        arr2 = VGroup(*[Arrow(P[i].get_bottom(), slots[1].get_top(), buff=0.15, stroke_width=3, color=PCOL[L],
                              max_tip_length_to_length_ratio=0.12) for i, L in ((1, "B"), (2, "C"))])
        self.at(27.0, GrowArrow(arr2[0]), Indicate(P[1], color=B_COL), rt=0.7)
        self.at(28.5, GrowArrow(arr2[1]), Indicate(P[2], color=K_COL), rt=0.7)
        c2 = lbl("2", scale=1.3).next_to(slots[1], DOWN, buff=0.35)
        self.at(31.9, FadeIn(c2, scale=1.5), rt=0.6)
        self.end_clip()
        self.st = dict(P=P, slots=slots, nums=nums, c=[c1, c2], arr2=arr2)

    def s05(self):
        st = self.st
        P, slots = st["P"], st["slots"]
        self.clip("p2_05")
        self.at(1.5, FadeOut(st["arr2"]), P[1].animate.move_to(slots[1]),
                slots[1].animate.set_stroke(SOFT, 2, 0.7), rt=1.3)
        self.at(4.2, slots[2].animate.set_stroke(HL, 4, 1), Indicate(P[2], color=K_COL), rt=0.9)
        self.at(5.6, P[2].animate.move_to(slots[2]), rt=1.2)
        self.play(slots[2].animate.set_stroke(SOFT, 2, 0.7), run_time=0.4)
        c3 = lbl("1", scale=1.3).next_to(slots[2], DOWN, buff=0.35)
        self.at(10.4, FadeIn(c3, scale=1.5), rt=0.6)
        c1, c2 = st["c"]
        x1 = MathTex(r"\times").scale(1.2).move_to((c1.get_center() + c2.get_center()) / 2)
        x2 = MathTex(r"\times").scale(1.2).move_to((c2.get_center() + c3.get_center()) / 2)
        self.at(14.2, FadeIn(x1, scale=0.5), rt=0.5)
        self.at(15.2, FadeIn(x2, scale=0.5), rt=0.5)
        res = MathTex("=", "6").scale(1.3).next_to(c3, RIGHT, buff=0.5)
        res[1].set_color(HL)
        self.at(17.8, FadeIn(res, shift=LEFT * 0.2), rt=0.6)
        self.play(Circumscribe(res[1], color=HL, shape=Circle), run_time=0.8)
        self.end_clip()
        self.clear_all(0.6)

    # ============================================================ p2_06  choice tree
    def s06(self):
        self.clip("p2_06")
        leaves = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]
        ys = [2.55 - i * 0.98 for i in range(6)]
        X0, X1, X2, X3, XL = -5.6, -3.4, -1.2, 1.0, 3.7
        root = Dot(np.array([X0, np.mean(ys), 0]), radius=0.12, color=WHITE)
        l1 = {}
        for j, L in enumerate("ABC"):
            l1[L] = node(L).move_to(np.array([X1, (ys[2 * j] + ys[2 * j + 1]) / 2, 0]))
        l2 = [node(w[1]).move_to(np.array([X2, ys[i], 0])) for i, w in enumerate(leaves)]
        l3 = [node(w[2]).move_to(np.array([X3, ys[i], 0])) for i, w in enumerate(leaves)]
        e1 = {L: edge(root, l1[L]) for L in "ABC"}
        e2 = [edge(l1[w[0]], l2[i]) for i, w in enumerate(leaves)]
        e3 = [edge(l2[i], l3[i]) for i in range(6)]

        self.at(3.2, GrowFromCenter(root), rt=0.6)
        groups = [("A", 5.9, 8.2), ("B", 11.8, 13.6), ("C", 16.6, 18.2)]
        for L, t1, t2 in groups:
            idx = [i for i, w in enumerate(leaves) if w[0] == L]
            self.at(t1, Create(e1[L]), FadeIn(l1[L], scale=0.6), rt=0.9)
            self.at(t2, *[Create(e2[i]) for i in idx], *[FadeIn(l2[i], scale=0.6) for i in idx], rt=1.1)
        # 3 ways, then 2 each, then 1 each
        self.at(20.8, *[e.animate.set_stroke(HL, 4, 1) for e in e1.values()], rt=0.8)
        self.at(23.8, *[e.animate.set_stroke(HL, 4, 1) for e in e2], rt=0.8)
        self.at(26.9, LaggedStart(*[AnimationGroup(Create(e3[i].set_stroke(HL, 4, 1)), FadeIn(l3[i], scale=0.6))
                                    for i in range(6)], lag_ratio=0.15), rt=1.6)
        # 3 × 2 × 1 = 6 under the three columns
        prod = VGroup(lbl("3").move_to(np.array([X1, -3.3, 0])), MathTex(r"\times").move_to(np.array([(X1 + X2) / 2, -3.3, 0])),
                      lbl("2").move_to(np.array([X2, -3.3, 0])), MathTex(r"\times").move_to(np.array([(X2 + X3) / 2, -3.3, 0])),
                      lbl("1").move_to(np.array([X3, -3.3, 0])), MathTex("=", "6").move_to(np.array([X3 + 1.3, -3.3, 0])))
        prod[-1][1].set_color(HL)
        self.at(29.6, LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in prod], lag_ratio=0.2), rt=2.0)
        # read off the six arrangements
        words = [word_tex(w).move_to(np.array([XL, ys[i], 0])) for i, w in enumerate(leaves)]
        times = [36.5, 37.5, 38.5, 39.5, 40.2, 40.8]
        for w, t, i in zip(words, times, range(6)):
            self.at(t, FadeIn(w, shift=LEFT * 0.3), Indicate(l3[i], scale_factor=1.3), rt=0.5)
        self.end_clip(pad=0.3)
        self.clear_all(0.6)

    # ============================================================ p2_07  N!
    def s07(self):
        self.clip("p2_07")
        pool = VGroup(*[dot_person(SOFT) for _ in range(9)]).arrange(RIGHT, buff=0.35).move_to(UP * 2.8)
        brace = Brace(pool, DOWN, color=SOFT, buff=0.12)
        bN = MathTex("N", color=SOFT).scale(0.9).next_to(brace, DOWN, buff=0.1)
        self.at(1.5, LaggedStart(*[GrowFromCenter(d) for d in pool], lag_ratio=0.08), rt=1.4)
        self.play(GrowFromCenter(brace), FadeIn(bN), run_time=0.6)
        xs = [-4.6, -2.8, -1.0, 0.8, 3.9]
        slots = VGroup(*[slot(1.0, 1.25).move_to(np.array([x, 0.1, 0])) for x in xs])
        dots_c = MathTex(r"\cdots").scale(1.4).move_to(np.array([2.35, 0.1, 0]))
        labels = [MathTex(s, color=K_COL).scale(0.95).next_to(sl, DOWN, buff=0.3)
                  for s, sl in zip(["N", "N-1", "N-2", "N-3", "1"], slots)]
        self.at(5.8, LaggedStart(*[Create(s) for s in slots], lag_ratio=0.1), FadeIn(dots_c), rt=1.0)
        self.play(FadeIn(labels[0], shift=UP * 0.2), pool[0].animate.move_to(slots[0]), run_time=0.8)
        self.at(11.5, FadeIn(labels[1], shift=UP * 0.2), pool[1].animate.move_to(slots[1]), rt=0.8)
        self.at(15.0, FadeIn(labels[2], shift=UP * 0.2), pool[2].animate.move_to(slots[2]), rt=0.8)
        self.at(16.9, FadeIn(labels[3], shift=UP * 0.2), pool[3].animate.move_to(slots[3]), rt=0.8)
        self.at(19.2, FadeIn(labels[4], shift=UP * 0.2), pool[8].animate.move_to(slots[4]),
                FadeOut(VGroup(*pool[4:8])), Indicate(dots_c), rt=1.2)
        full = MathTex("N", "(N-1)", "(N-2)", "(N-3)", r"\cdots", r"2 \cdot 1", "=", "N!").scale(1.1)
        full.move_to(DOWN * 2.6)
        full[-1].set_color(HL)
        srcs = labels[:4]
        self.upto(22.2)
        self.playto(29.8, LaggedStart(*[TransformFromCopy(s, full[i]) for i, s in enumerate(srcs)],
                                      FadeIn(full[4]), TransformFromCopy(labels[4], full[5]), lag_ratio=0.45))
        self.at(33.6, Write(full[6]), FadeIn(full[7], scale=1.6), rt=1.0)
        boxN = SurroundingRectangle(full[7], color=HL, buff=0.12)
        self.play(Create(boxN), run_time=0.6)
        # arrangement of N distinct things: dim others, shuffle the filled slots
        occupants = [pool[0], pool[1], pool[2], pool[3], pool[8]]
        for d, c in zip(occupants, [A_COL, B_COL, K_COL, HL, "#C39BFF"]):
            d.set_color(c)
        self.at(36.0, VGroup(*labels, brace, bN, full[:7]).animate.set_opacity(0.3), rt=0.6)
        for perm in ([1, 3, 0, 4, 2], [4, 0, 3, 2, 1]):
            self.play(*[d.animate.move_to(slots[perm[i]]) for i, d in enumerate(occupants)],
                      path_arc=PI / 2, run_time=1.3)
        self.end_clip()
        self.clear_all(0.6)

    # ============================================================ p2_08  5 people, pairs
    def row_people(self, letters, y=2.5, scale=0.8):
        return VGroup(*[person(L, scale) for L in letters]).arrange(RIGHT, buff=0.55).move_to(UP * y)

    def s08(self):
        self.clip("p2_08")
        q = MathTex("?", color=K_COL).scale(2.2)
        self.at(3.7, FadeIn(q, scale=0.5), rt=0.6)
        self.at(6.4, FadeOut(q, scale=1.5), rt=0.5)
        P = self.row_people("ABCDE")
        for i, t in enumerate((10.4, 10.9, 11.4, 11.9, 12.5)):
            self.at(t, FadeIn(P[i], shift=DOWN * 0.3), rt=0.45)
        slots = VGroup(slot(), slot()).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.8 + LEFT * 2.2)
        team = Brace(slots, DOWN, color=SOFT)
        self.at(14.3, LaggedStart(*[Create(s) for s in slots], lag_ratio=0.3), GrowFromCenter(team), rt=1.2)
        q2 = MathTex("?", color=K_COL).scale(1.2).next_to(team, DOWN)
        self.at(18.6, FadeIn(q2), rt=0.5)
        self.at(22.0, FadeOut(q2), slots[0].animate.set_stroke(HL, 4, 1), rt=0.6)
        arrs = VGroup(*[Arrow(p.get_bottom(), slots[0].get_top(), buff=0.12, stroke_width=2.5, color=PCOL[L],
                              max_tip_length_to_length_ratio=0.1) for p, L in zip(P, "ABCDE")])
        self.at(25.2, LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.2), rt=2.2)
        c1 = lbl("5", scale=1.2).next_to(slots[0], DOWN, buff=0.9)
        self.at(29.6, FadeIn(c1, scale=1.5), rt=0.5)
        self.at(31.8, FadeOut(arrs), P[0].animate.move_to(slots[0]), slots[0].animate.set_stroke(SOFT, 2, 0.7), rt=1.1)
        self.play(*[Indicate(p, scale_factor=1.12) for p in P[1:]], run_time=0.8)
        arrs2 = VGroup(*[Arrow(p.get_bottom(), slots[1].get_top(), buff=0.12, stroke_width=2.5, color=PCOL[L],
                               max_tip_length_to_length_ratio=0.1) for p, L in zip(P[1:], "BCDE")])
        self.at(34.5, slots[1].animate.set_stroke(HL, 4, 1), LaggedStart(*[GrowArrow(a) for a in arrs2], lag_ratio=0.15), rt=1.4)
        c2 = lbl("4", scale=1.2).next_to(slots[1], DOWN, buff=0.9)
        self.at(36.3, FadeIn(c2, scale=1.5), rt=0.5)
        res = MathTex("5", r"\times", "4", "=", "20").scale(1.2).move_to(RIGHT * 3.6 + DOWN * 0.8)
        res[0].set_color(K_COL); res[2].set_color(K_COL); res[4].set_color(HL)
        self.at(38.4, FadeOut(arrs2), slots[1].animate.set_stroke(SOFT, 2, 0.7),
                TransformFromCopy(c1, res[0]), TransformFromCopy(c2, res[2]), FadeIn(res[1]), rt=1.2)
        self.at(41.0, FadeIn(res[3:], shift=LEFT * 0.2), rt=0.6)
        self.end_clip()
        self.st = dict(P=P, slots=slots, team=team, c=[c1, c2], res=res)

    # ============================================================ p2_09  triples + pattern
    def s09(self):
        st = self.st
        P, slots, team = st["P"], st["slots"], st["team"]
        c1, c2 = st["c"]
        self.clip("p2_09")
        s3 = slot().next_to(slots, RIGHT, buff=0.5)
        new_team = Brace(VGroup(slots, s3), DOWN, color=SOFT)
        self.at(0.4, Create(s3), Transform(team, new_team),
                st["res"].animate.shift(RIGHT * 0.9).set_opacity(0.35), rt=1.2)
        self.at(3.6, Indicate(c1, scale_factor=1.4), rt=0.8)
        self.at(6.6, P[1].animate.move_to(slots[1]), Indicate(c2, scale_factor=1.4), rt=1.0)
        c3 = lbl("3", scale=1.2).next_to(s3, DOWN, buff=0.9)
        self.at(10.2, P[2].animate.move_to(s3), rt=1.0)
        self.play(FadeIn(c3, scale=1.5), run_time=0.5)
        res2 = MathTex("5", r"\times", "4", r"\times", "3", "=", "60").scale(1.1).move_to(RIGHT * 4.3 + DOWN * 1.9)
        for i in (0, 2, 4):
            res2[i].set_color(K_COL)
        res2[6].set_color(HL)
        self.at(14.0, TransformFromCopy(VGroup(c1, c2, c3), VGroup(res2[0], res2[2], res2[4])),
                FadeIn(res2[1]), FadeIn(res2[3]), rt=1.3)
        self.at(16.4, FadeIn(res2[5:], shift=LEFT * 0.2), rt=0.6)
        self.at(19.4, *[FadeOut(m) for m in self.mobjects], rt=0.8)

        # pattern table: (group of k dots) → 5×4×…
        rows = VGroup()
        for k, y in ((2, 1.4), (3, 0.0), (4, -1.4)):
            g = VGroup(*[Dot(radius=0.13, color=c) for c in [A_COL, B_COL, K_COL, HL][:k]]).arrange(RIGHT, buff=0.18)
            facs = [str(5 - i) for i in range(k)]
            parts = []
            for i, f in enumerate(facs):
                if i:
                    parts.append(r"\times")
                parts.append(f)
            prod = MathTex(*parts).scale(1.15)
            for m, p in zip(prod, parts):
                if p != r"\times":
                    m.set_color(K_COL)
            arrow = MathTex(r"\rightarrow", color=SOFT)
            row = VGroup(g, arrow, prod).arrange(RIGHT, buff=0.45)
            row.move_to(np.array([0, y, 0]))
            rows.add(row)
        # align the products on their left edge
        left_x = min(r[2].get_left()[0] for r in rows)
        for r in rows:
            r[2].shift(RIGHT * (left_x - r[2].get_left()[0]))
            r[1].next_to(r[2], LEFT, buff=0.45)
            r[0].next_to(r[1], LEFT, buff=0.45)
        rows.move_to(ORIGIN)
        for r, t in zip(rows, (22.4, 24.7, 27.7)):
            self.at(t, FadeIn(r[0], shift=RIGHT * 0.2), FadeIn(r[1]), Write(r[2]), rt=1.0)
        # each extra person → one fewer choice (−1 arcs on the last row)
        last = rows[2][2]
        facs = [last[0], last[2], last[4], last[6]]
        arcs = VGroup()
        for a, b in zip(facs[:-1], facs[1:]):
            ar = CurvedArrow(a.get_bottom() + DOWN * 0.1, b.get_bottom() + DOWN * 0.1, angle=PI / 2.2,
                             color=HL, stroke_width=3, tip_length=0.15)
            t = MathTex("-1", color=HL).scale(0.6).next_to(ar, DOWN, buff=0.05)
            arcs.add(VGroup(ar, t))
        self.at(32.0, LaggedStart(*[Create(a[0]) for a in arcs], lag_ratio=0.5),
                LaggedStart(*[FadeIn(a[1]) for a in arcs], lag_ratio=0.5), rt=3.0)
        self.end_clip()
        self.clear_all(0.6)

    # ============================================================ p2_10  N choose M ordered
    def s10(self):
        self.clip("p2_10")
        pool = VGroup(*[dot_person(SOFT) for _ in range(9)]).arrange(RIGHT, buff=0.35).move_to(UP * 2.9)
        brace = Brace(pool, DOWN, color=SOFT, buff=0.12)
        bN = MathTex("N", color=SOFT).scale(0.9).next_to(brace, DOWN, buff=0.1)
        self.at(0.8, LaggedStart(*[GrowFromCenter(d) for d in pool], lag_ratio=0.06), GrowFromCenter(brace),
                FadeIn(bN), rt=1.4)
        xs = [-4.6, -2.8, -1.0, 3.2]
        slots = VGroup(*[slot(1.0, 1.25).move_to(np.array([x, 0.35, 0])) for x in xs])
        dc = MathTex(r"\cdots").scale(1.4).move_to(np.array([1.1, 0.35, 0]))
        mb = Brace(slots, UP, color=SOFT, buff=0.15)
        mM = MathTex("M", color=SOFT).scale(0.9).next_to(mb, UP, buff=0.08)
        self.at(3.4, LaggedStart(*[Create(s) for s in slots], lag_ratio=0.1), FadeIn(dc), rt=1.0)
        self.play(GrowFromCenter(mb), FadeIn(mM), run_time=0.6)
        labs = [MathTex(s, color=K_COL).scale(0.95).next_to(sl, DOWN, buff=0.3)
                for s, sl in zip(["N", "N-1", "N-2"], slots[:3])]
        self.at(7.7, FadeIn(labs[0], shift=UP * 0.2), FadeOut(VGroup(mb, mM)), pool[0].animate.move_to(slots[0]), rt=0.8)
        self.at(10.8, FadeIn(labs[1], shift=UP * 0.2), pool[1].animate.move_to(slots[1]), rt=0.8)
        self.at(13.9, FadeIn(labs[2], shift=UP * 0.2), pool[2].animate.move_to(slots[2]), rt=0.8)
        self.at(16.0, slots[3].animate.set_stroke(HL, 4, 1), rt=0.6)
        before = Brace(VGroup(slots[:3], dc), UP, color=HL, buff=0.15)
        bM = MathTex("M-1", color=HL).scale(0.85).next_to(before, UP, buff=0.08)
        self.at(19.3, GrowFromCenter(before), FadeIn(bM), rt=0.8)
        lastlab = MathTex("N", "-", "(M-1)", color=K_COL).scale(0.95).next_to(slots[3], DOWN, buff=0.3)
        self.at(24.3, FadeIn(lastlab[:2], shift=UP * 0.2), rt=0.6)
        self.at(25.9, TransformFromCopy(bM, lastlab[2]), rt=0.9)
        lastlab2 = MathTex("N-M+1", color=K_COL).scale(0.95).next_to(slots[3], DOWN, buff=0.3)
        self.at(28.0, TransformMatchingShapes(lastlab, lastlab2), pool[3].animate.move_to(slots[3]),
                slots[3].animate.set_stroke(SOFT, 2, 0.7), rt=1.2)
        prod = MathTex("N", "(N-1)", "(N-2)", r"\cdots", "(N-M+1)").scale(1.15).move_to(DOWN * 2.5)
        self.at(31.8, FadeOut(VGroup(before, bM)), rt=0.5)
        self.upto(35.6)
        self.playto(42.8, LaggedStart(TransformFromCopy(labs[0], prod[0]), TransformFromCopy(labs[1], prod[1]),
                                      TransformFromCopy(labs[2], prod[2]), FadeIn(prod[3]),
                                      TransformFromCopy(lastlab2, prod[4]), lag_ratio=0.5))
        self.remove(*prod)
        self.add(prod)
        self.end_clip()
        keep = [prod]
        self.play(*[FadeOut(m) for m in self.mobjects if m not in keep],
                  prod.animate.scale(0.8).to_edge(UP, buff=0.4), run_time=0.8)
        self.prod = prod

    # ============================================================ p2_11  double counting
    def s11(self):
        prod = self.prod
        self.clip("p2_11")
        ul = Underline(prod, color=K_COL, buff=0.1)
        self.at(3.0, Create(ul), rt=0.8)
        tAB = tile("AB").move_to(LEFT * 2 + UP * 0.3)
        tBA = tile("BA").move_to(RIGHT * 2 + UP * 0.3)
        self.at(10.8, FadeIn(tAB, shift=UP * 0.3), rt=0.7)
        self.at(13.8, FadeIn(tBA, shift=UP * 0.3), rt=0.7)
        sAB = set_tex("AB").next_to(tAB, DOWN, buff=0.5)
        sBA = set_tex("AB").next_to(tBA, DOWN, buff=0.5)
        self.at(16.2, FadeIn(sAB, shift=DOWN * 0.2), FadeIn(sBA, shift=DOWN * 0.2), rt=0.9)
        # position swap
        self.at(20.9, Swap(tBA[0], tBA[1]), rt=1.2)
        self.play(Swap(tBA[0], tBA[1]), run_time=1.0)
        # same team: BA slides onto AB and they become one team
        self.at(27.6, tBA.animate.move_to(tAB), sBA.animate.move_to(sAB), rt=1.3)
        self.play(FadeOut(tBA), FadeOut(sBA), Flash(sAB, color=HL, flash_radius=0.8), run_time=0.8)
        cnt = MathTex(r"\times", "?", color=K_COL).scale(1.3).next_to(tAB, RIGHT, buff=0.4)
        self.at(31.8, FadeIn(cnt, shift=LEFT * 0.2), rt=0.7)
        self.end_clip()
        self.play(*[FadeOut(m) for m in self.mobjects if m is not prod], FadeOut(ul), run_time=0.6)

    # ============================================================ p2_12  two people
    def s12(self):
        prod = self.prod
        self.clip("p2_12")
        P = VGroup(person("A"), person("B")).arrange(RIGHT, buff=1.0).move_to(UP * 1.4)
        self.at(3.2, prod.animate.set_opacity(0.3), rt=0.5)
        self.at(5.5, FadeIn(P[0], shift=DOWN * 0.3), rt=0.5)
        self.at(6.3, FadeIn(P[1], shift=DOWN * 0.3), rt=0.5)
        tAB = tile("AB").move_to(LEFT * 2.2 + DOWN * 0.6)
        tBA = tile("BA").move_to(RIGHT * 2.2 + DOWN * 0.6)
        self.at(7.5, Circumscribe(P, color=HL, buff=0.2), rt=1.2)
        self.at(10.8, TransformFromCopy(P, tAB), rt=1.0)
        self.at(13.3, TransformFromCopy(VGroup(P[1], P[0]), tBA), rt=1.0)
        ne = MathTex(r"\neq", "?", color=SOFT).scale(1.4).move_to(DOWN * 0.6)
        self.at(16.0, FadeIn(ne), rt=0.6)
        eq = MathTex("=", color=HL).scale(1.6).move_to(DOWN * 0.6)
        self.at(19.5, ReplacementTransform(ne, eq), rt=0.5)
        s = set_tex("AB", 1.2).move_to(DOWN * 2.4)
        self.at(22.2, TransformFromCopy(tAB, s), TransformFromCopy(tBA, s.copy()), rt=1.3)
        self.at(26.6, Swap(tBA[0], tBA[1]), rt=1.1)
        self.play(Swap(tBA[0], tBA[1]), run_time=0.9)
        two = MathTex(r"\times 2", color=K_COL).scale(1.2).next_to(s, RIGHT, buff=0.4)
        self.at(30.2, FadeIn(two, shift=LEFT * 0.2), rt=0.6)
        fact = MathTex("2!", "=", "2", color=HL).scale(1.2).next_to(s, LEFT, buff=1.2)
        self.at(33.4, Write(fact), rt=1.0)
        self.at(35.6, Indicate(two, scale_factor=1.3), Indicate(fact[0], scale_factor=1.3), rt=1.0)
        self.end_clip()
        self.play(*[FadeOut(m) for m in self.mobjects if m is not prod], run_time=0.6)

    # ============================================================ p2_13  three people
    def s13(self):
        prod = self.prod
        self.clip("p2_13")
        P = self.row_people("ABC", y=2.2, scale=0.75)
        self.at(2.7, LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in P], lag_ratio=0.3), rt=1.2)
        words = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]
        tiles = VGroup(*[tile(w, 0.55) for w in words])
        grid = VGroup(VGroup(*tiles[:3]).arrange(RIGHT, buff=0.6), VGroup(*tiles[3:]).arrange(RIGHT, buff=0.6))
        grid.arrange(DOWN, buff=0.4).move_to(LEFT * 2.2 + DOWN * 0.5)
        for t, tm in zip(tiles, (9.9, 11.1, 12.2, 13.4, 14.7, 15.8)):
            self.at(tm, TransformFromCopy(P, t), rt=0.6)
        m321 = MathTex("3", r"\times", "2", r"\times", "1", "=", "6").scale(1.0).next_to(grid, DOWN, buff=0.55)
        self.at(18.0, Write(m321), rt=1.5)
        self.at(23.0, LaggedStart(*[Indicate(t, scale_factor=1.1) for t in tiles], lag_ratio=0.15), rt=2.0)
        s = set_tex("ABC", 1.2).move_to(RIGHT * 4.1 + DOWN * 0.5)
        self.at(28.3, FadeIn(s, shift=LEFT * 0.3), rt=0.8)
        self.at(31.3, *[Swap(t[0], t[-1]) for t in tiles], rt=1.0)
        self.play(*[Swap(t[0], t[-1]) for t in tiles], run_time=0.8)
        arrows = VGroup(*[Arrow(t.get_right(), s.get_left(), buff=0.15, stroke_width=2, color=SOFT,
                                max_tip_length_to_length_ratio=0.06) for t in tiles])
        x6 = MathTex(r"\times 6", color=K_COL).next_to(s, UP, buff=0.35)
        self.at(33.9, LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), FadeIn(x6), rt=1.6)
        f3 = MathTex("3!", "=", "6", color=HL).next_to(s, DOWN, buff=0.4)
        self.at(37.4, Write(f3), rt=1.0)
        div = MathTex(r"\frac{6}{3!}", "=", r"\frac{6}{6}", "=", "1").scale(1.1).move_to(DOWN * 3.0 + RIGHT * 1.8)
        div[-1].set_color(HL)
        self.at(40.0, FadeOut(arrows), m321.animate.set_opacity(0.4), rt=0.6)
        self.at(44.5, Write(div[0]), rt=0.8)
        self.at(45.2, Write(div[1:3]), rt=0.9)
        self.at(46.7, Write(div[3:]), rt=0.6)
        # the six arrangements collapse into one team
        self.at(49.5, *[t.animate.move_to(s).set_opacity(0) for t in tiles], Flash(s, color=HL, flash_radius=1.0),
                Circumscribe(div[-1], color=HL, shape=Circle), rt=1.3)
        self.end_clip()
        self.play(*[FadeOut(m) for m in self.mobjects if m is not prod], run_time=0.6)

    # ============================================================ p2_14  divide by M!
    def s14(self):
        prod = self.prod
        self.clip("p2_14")
        rows = VGroup()
        for k, f in ((2, "2!"), (3, "3!"), (None, "M!")):
            if k:
                g = VGroup(*[Dot(radius=0.14, color=c) for c in [A_COL, B_COL, K_COL][:k]]).arrange(RIGHT, buff=0.2)
            else:
                g = MathTex("M", color=SOFT)
            r = VGroup(g, MathTex(r"\rightarrow", color=SOFT), MathTex(f, color=HL).scale(1.2)).arrange(RIGHT, buff=0.5)
            rows.add(r)
        rows.arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(LEFT * 3.0 + DOWN * 0.3)
        self.at(0.6, FadeIn(rows[0], shift=RIGHT * 0.2), rt=0.9)
        self.at(5.6, FadeIn(rows[1], shift=RIGHT * 0.2), rt=0.9)
        self.at(8.6, FadeIn(rows[2][0:2], shift=RIGHT * 0.2), rt=0.8)
        self.at(15.0, FadeIn(rows[2][2], scale=1.4), rt=0.7)
        team = VGroup(*[Dot(radius=0.14, color=c) for c in (A_COL, B_COL, K_COL)]).arrange(RIGHT, buff=0.15)
        ring = SurroundingRectangle(team, buff=0.18, corner_radius=0.2, color=SOFT)
        tm = VGroup(team, ring)
        cnt = MathTex(r"\times", "M!", color=K_COL).scale(1.2)
        grp = VGroup(tm, cnt).arrange(RIGHT, buff=0.3).move_to(RIGHT * 3.0 + DOWN * 0.3)
        self.at(18.2, FadeIn(tm, scale=0.8), TransformFromCopy(rows[2][2], cnt[1]), FadeIn(cnt[0]), rt=1.2)
        pt = prod.copy().set_opacity(1).scale(1.25).move_to(UP * 0.4)
        self.at(24.3, FadeOut(VGroup(rows, grp)), Transform(prod, pt), rt=1.0)
        line = Line(LEFT, RIGHT).set_width(pt.width + 0.3).next_to(pt, DOWN, buff=0.2)
        den = MathTex("M!", color=HL).scale(1.2).next_to(line, DOWN, buff=0.2)
        self.at(28.5, GrowFromCenter(line), FadeIn(den, shift=UP * 0.3), rt=1.0)
        self.end_clip()
        self.frac = VGroup(prod, line, den)

    # ============================================================ p2_15  the combination formula
    def s15(self):
        self.clip("p2_15")
        frac = self.frac
        f1 = MathTex(r"\frac{N(N-1)(N-2)\cdots(N-M+1)}{M!}").scale(1.05)
        f1.move_to(UP * 2.0 + LEFT * 1.5)
        self.at(3.2, ReplacementTransform(frac, f1), rt=1.4)
        self.at(7.0, Circumscribe(f1, color=HL, fade_out=True), rt=1.2)
        eq2 = MathTex("=", r"\frac{N(N-1)(N-2)\cdots(N-M+1)\,(N-M)!}{M!\,(N-M)!}").scale(1.05)
        eq3 = MathTex("=", r"\frac{N!}{M!\,(N-M)!}").scale(1.05)
        eq2.next_to(f1, DOWN, buff=0.5, aligned_edge=LEFT).shift(LEFT * 0.0)
        eq2.shift(RIGHT * (f1.get_left()[0] - eq2[1].get_left()[0]))
        eq2[0].next_to(eq2[1], LEFT, buff=0.2)
        eq3.next_to(eq2, DOWN, buff=0.5)
        eq3.shift(RIGHT * (eq2[0].get_center()[0] - eq3[0].get_center()[0]))
        self.upto(14.3)
        self.playto(24.0, Write(eq2))
        self.at(26.6, Write(eq3), rt=1.6)
        box = SurroundingRectangle(eq3[1], color=HL, buff=0.15)
        self.at(29.6, Create(box), rt=0.8)
        final = VGroup(eq3[1].copy(), box.copy())
        self.at(31.8, FadeOut(VGroup(f1, eq2, eq3[0])), eq3[1].animate.move_to(ORIGIN + UP * 0.3).scale(1.2),
                box.animate.become(SurroundingRectangle(eq3[1].copy().move_to(ORIGIN + UP * 0.3).scale(1.2),
                                                         color=HL, buff=0.15)), rt=1.2)
        cnm = MathTex("C(N, M)", "=").scale(1.25)
        cnm[0].set_color(HL)
        self.at(39.0, VGroup(eq3[1], box).animate.shift(RIGHT * 1.6), rt=0.8)
        cnm.next_to(box, LEFT, buff=0.3)
        self.play(Write(cnm), run_time=1.0)
        glow = VGroup(*[cnm[0].copy().set_fill(opacity=0).set_stroke(HL, w, o) for w, o in ((8, 0.2), (16, 0.08))])
        self.at(42.6, FadeIn(glow), rt=1.0)
        self.end_clip()
        self.clear_all(0.7)

    # ============================================================ p2_16  back to (A+B)^n
    def exp_row(self, n, sc=1.0):
        tex, info = expansion_row(n, sym=("A", "B"))
        tex.scale(sc)
        return tex, info

    def s16(self):
        self.clip("p2_16")
        sc = 1.0
        rows = {}
        for n in (0, 1, 2, 3):
            rows[n] = self.exp_row(n, sc)
        # line up '=' signs; rows 1..3 visible first, row 0 slots in above later
        x_eq = -2.6
        for n, (t, i) in rows.items():
            t.shift(np.array([x_eq - i["eq"].get_center()[0], 1.6 - (n - 1) * 1.15 - i["eq"].get_center()[1], 0]))
        t1, i1 = rows[1]
        self.at(1.9, Write(i1["lhs"]), Write(i1["eq"]), rt=1.2)
        self.at(3.9, Write(i1["rhs"]), rt=1.0)
        t2, i2 = rows[2]
        self.at(6.2, TransformFromCopy(i1["lhs"], i2["lhs"]), FadeIn(i2["eq"]), rt=1.0)
        self.at(9.2, Write(i2["rhs"]), rt=2.4)
        t3, i3 = rows[3]
        self.at(13.0, TransformFromCopy(i2["lhs"], i3["lhs"]), FadeIn(i3["eq"]), rt=1.0)
        self.at(16.0, Write(i3["rhs"]), rt=3.8)
        # bigger and bigger ...
        dots = MathTex(r"\vdots").next_to(t3, DOWN, buff=0.3).set_x(i3["eq"].get_x())
        self.at(22.0, FadeIn(dots, shift=DOWN * 0.3), rt=0.8)
        coefs = [t["coef"] for n in (2, 3) for t in rows[n][1]["terms"] if t["coef"] is not None]
        self.at(29.3, LaggedStart(*[Indicate(c, color=K_COL, scale_factor=1.5) for c in coefs], lag_ratio=0.2), rt=2.8)
        # coefficient column on the right
        t0, i0 = rows[0]
        colx = 4.6
        crow = {}
        for n in range(4):
            y = rows[n][1]["eq"].get_y()
            g = VGroup(*[MathTex(str(comb(n, k)), color=K_COL) for k in range(n + 1)]).arrange(RIGHT, buff=0.35)
            crow[n] = g.move_to(np.array([colx, y, 0]))
        self.at(33.4, FadeIn(t0, shift=DOWN * 0.2), rt=0.5)
        self.play(TransformFromCopy(i0["terms"][0]["all"], crow[0][0]), run_time=0.5)
        for n, tm in ((1, 34.9), (2, 36.8), (3, 39.3)):
            info = rows[n][1]
            self.at(tm, LaggedStart(*[TransformFromCopy(t["coef"] if t["coef"] is not None else t["body"], crow[n][k])
                                      for k, t in enumerate(info["terms"])], lag_ratio=0.25), rt=1.4)
        box = SurroundingRectangle(VGroup(*crow.values()), color=K_COL, buff=0.25, corner_radius=0.15)
        tag = bn("সহগ", 30, color=K_COL).next_to(box, DOWN, buff=0.2)
        self.at(43.4, Create(box), FadeIn(tag, shift=UP * 0.2), rt=1.0)
        self.end_clip()
        self.rows16 = rows
        self.coefbox = VGroup(*crow.values(), box, tag)
        self.dots16 = dots

    # ============================================================ p2_17  why a pattern? → title
    def s17(self):
        rows = self.rows16
        self.clip("p2_17")
        q = MathTex("?", color=K_COL).scale(1.4).next_to(self.coefbox[4], UP, buff=0.2)
        self.at(0.5, FadeIn(q, shift=UP * 0.2), rt=0.6)
        # brute-force: every term times every term
        t3, i3 = rows[3]
        others = VGroup(rows[0][0], rows[1][0], rows[2][0], self.dots16)
        self.at(3.6, others.animate.set_opacity(0.25), rt=0.6)
        fac = MathTex("(", "A", "+", "B", ")", "(", "A", "+", "B", ")", "(", "A", "+", "B", ")").scale(1.1)
        for k in (1, 6, 11):
            fac[k].set_color(A_COL)
        for k in (3, 8, 13):
            fac[k].set_color(B_COL)
        fac.move_to(DOWN * 2.6 + LEFT * 1.6)
        self.play(TransformFromCopy(i3["lhs"], fac), run_time=1.0)
        picks = [(a, b, c) for a in (1, 3) for b in (6, 8) for c in (11, 13)]
        paths = VGroup()
        for a, b, c in picks:
            p = VMobject().set_points_smoothly([fac[a].get_top() + UP * 0.1,
                                                (fac[a].get_top() + fac[b].get_top()) / 2 + UP * 0.6,
                                                fac[b].get_top() + UP * 0.1,
                                                (fac[b].get_top() + fac[c].get_top()) / 2 + UP * 0.6,
                                                fac[c].get_top() + UP * 0.1])
            paths.add(p.set_stroke(color=[A_COL, K_COL, B_COL][len(paths) % 3], width=2, opacity=0.8))
        self.playto(11.5, LaggedStart(*[Create(p) for p in paths], lag_ratio=0.35))
        self.at(12.6, FadeOut(paths), FadeOut(fac), others.animate.set_opacity(1), rt=0.9)
        self.at(16.3, LaggedStart(*[Indicate(m, color=HL, scale_factor=1.25) for m in self.coefbox[:4]],
                                  lag_ratio=0.3), rt=2.2)
        self.at(19.9, FadeOut(q), rt=0.4)
        self.upto(24.3)
        chapter_title(self, "Binomial Theorem", "Chapter 2", clear_after=True)
        self.wait(0.4)
