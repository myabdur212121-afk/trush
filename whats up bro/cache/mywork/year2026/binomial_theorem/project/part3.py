"""Part 3 — Chapter 2 body: labelled factors → C(n,r) → Binomial Theorem."""
from common import *


# ------------------------------------------------------------------ builders
def factors(n, scale=1.0):
    """(A_1+B_1)(A_2+B_2)... ; returns tex, dict k -> (A mob, B mob, whole factor group)"""
    parts = []
    for k in range(1, n + 1):
        parts += ["(", f"A_{{{k}}}", "+", f"B_{{{k}}}", ")"]
    t = MathTex(*parts).scale(scale)
    info = {}
    for k in range(1, n + 1):
        i = 5 * (k - 1)
        t[i + 1].set_color(A_COL)
        t[i + 3].set_color(B_COL)
        info[k] = (t[i + 1], t[i + 3], VGroup(*t[i:i + 5]))
    return t, info


def lab_term(seq, scale=1.0):
    t = MathTex(*[f"{c}_{{{k + 1}}}" for k, c in enumerate(seq)]).scale(scale)
    for m, c in zip(t, seq):
        m.set_color(A_COL if c == "A" else B_COL)
    return t


def indicator(seq, s=0.2):
    g = VGroup()
    for c in seq:
        sq = Square(s).set_stroke(A_COL if c == "A" else B_COL, 2)
        sq.set_fill(B_COL if c == "B" else BG, 0.9 if c == "B" else 0)
        g.add(sq)
    return g.arrange(RIGHT, buff=0.05)


def ab_tex(tex, scale=1.0):
    """colour A/B symbols inside a single MathTex string (e.g. '3A^{2}B')."""
    t = MathTex(tex).scale(scale)
    return t


def colored(parts, scale=1.0):
    """MathTex from parts; parts starting with A → A_COL, B → B_COL, 'C(' → K_COL."""
    t = MathTex(*parts).scale(scale)
    for m, p in zip(t, parts):
        if p.startswith("A"):
            m.set_color(A_COL)
        elif p.startswith("B"):
            m.set_color(B_COL)
        elif p.startswith("C(") or p.startswith(r"\binom") or p.startswith(r"\frac{n!}"):
            m.set_color(K_COL)
    return t


SEQ2 = ["AA", "AB", "BA", "BB"]
SEQ3 = ["AAA", "AAB", "ABA", "BAA", "ABB", "BAB", "BBA", "BBB"]


class Part3(Narrated, MovingCameraScene):

    def clear_all(self, rt=0.6, keep=()):
        mobs = [m for m in self.mobjects if m not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=rt)

    def pick(self, finfo, seq, term, rt=0.9):
        """highlight the chosen letter in each factor and fly copies into `term`."""
        chosen = [finfo[k + 1][0 if c == "A" else 1] for k, c in enumerate(seq)]
        boxes = VGroup(*[SurroundingRectangle(m, buff=0.05, color=(A_COL if c == "A" else B_COL),
                                              stroke_width=2.5) for m, c in zip(chosen, seq)])
        self.play(Create(boxes), run_time=0.25)
        self.play(*[TransformFromCopy(m, term[i]) for i, m in enumerate(chosen)], run_time=rt)
        self.play(FadeOut(boxes), run_time=0.2)

    def construct(self):
        self.wait(0.4)
        for i in range(1, 18):
            getattr(self, f"s{i:02d}")()
        self.wait(1.0)

    # ============================================================ (A+B)(A+B) with labels
    def s01(self):
        self.clip("p3_01")
        pr = MathTex("(", "A", "+", "B", ")", "(", "A", "+", "B", ")").scale(1.4)
        for i in (1, 6):
            pr[i].set_color(A_COL)
        for i in (3, 8):
            pr[i].set_color(B_COL)
        self.at(4.7, Write(pr[:5]), rt=1.2)
        self.at(6.4, Write(pr[5:]), rt=1.2)
        sq = MathTex("=", "(A+B)^2").scale(1.4)
        grp = VGroup(pr.copy(), sq).arrange(RIGHT, buff=0.3)
        self.at(8.5, pr.animate.move_to(grp[0]), rt=0.6)
        sq.move_to(grp[1])
        self.play(Write(sq), run_time=1.0)
        direct = MathTex("=", "A^2+2AB+B^2", color=GREY_B).scale(1.2).next_to(grp, DOWN, buff=0.6)
        self.at(11.3, FadeIn(direct, shift=DOWN * 0.2), rt=1.0)
        self.at(15.8, FadeOut(direct, shift=DOWN * 0.3), FadeOut(sq), rt=1.0)
        self.at(18.4, pr.animate.move_to(UP * 1.2), rt=1.0)
        fac, fi = factors(2, 1.4)
        fac.move_to(UP * 1.2)
        self.at(23.5, *[ReplacementTransform(pr[i], fac[i]) for i in range(5)], rt=1.2)
        self.at(27.3, *[ReplacementTransform(pr[i], fac[i]) for i in range(5, 10)], rt=1.2)
        self.at(29.8, Indicate(fac[:5], color=WHITE, scale_factor=1.1), rt=1.2)
        self.at(32.0, Indicate(fac[5:], color=WHITE, scale_factor=1.1), rt=1.2)
        self.end_clip()
        self.fac2, self.fi2 = fac, fi

    def s02(self):
        fac, fi = self.fac2, self.fi2
        self.clip("p3_02")
        A = MathTex("A", color=A_COL).scale(1.5).move_to(DOWN * 1.4 + LEFT * 2.5)
        a1, a2 = fi[1][0], fi[2][0]
        arr = VGroup(*[Arrow(m.get_bottom(), A.get_top(), buff=0.15, color=A_COL, stroke_width=3,
                             max_tip_length_to_length_ratio=0.1) for m in (a1, a2)])
        self.at(0.5, Indicate(a1, scale_factor=1.5), rt=0.8)
        self.at(1.6, Indicate(a2, scale_factor=1.5), rt=0.8)
        self.at(3.0, GrowArrow(arr[0]), GrowArrow(arr[1]), FadeIn(A, scale=0.6), rt=1.2)
        b1 = Brace(fi[1][2], DOWN, color=SOFT)
        b2 = Brace(fi[2][2], DOWN, color=SOFT)
        n1 = MathTex("1", color=SOFT).scale(0.8).next_to(b1, DOWN, buff=0.1)
        n2 = MathTex("2", color=SOFT).scale(0.8).next_to(b2, DOWN, buff=0.1)
        self.at(6.0, FadeOut(arr), A.animate.set_opacity(0.4), rt=0.6)
        self.at(8.3, GrowFromCenter(b1), FadeIn(n1), Indicate(a1), rt=1.0)
        self.at(11.0, GrowFromCenter(b2), FadeIn(n2), Indicate(a2), rt=1.0)
        B = MathTex("B", color=B_COL).scale(1.5).move_to(DOWN * 1.4 + RIGHT * 2.5)
        bb1, bb2 = fi[1][1], fi[2][1]
        arrB = VGroup(*[Arrow(m.get_bottom(), B.get_top(), buff=0.15, color=B_COL, stroke_width=3,
                              max_tip_length_to_length_ratio=0.1) for m in (bb1, bb2)])
        self.at(13.2, FadeOut(VGroup(b1, b2, n1, n2)), rt=0.5)
        self.at(15.4, Indicate(bb1, scale_factor=1.5), Indicate(bb2, scale_factor=1.5), rt=0.9)
        self.play(GrowArrow(arrB[0]), GrowArrow(arrB[1]), FadeIn(B, scale=0.6), run_time=1.1)
        self.end_clip()
        self.play(FadeOut(VGroup(A, B, arrB)), fac.animate.scale(0.8).move_to(UP * 2.6), run_time=0.8)

    # ============================================================ expand the product of 2
    def s03(self):
        fac, fi = self.fac2, self.fi2
        self.clip("p3_03")
        terms = [lab_term(s, 1.2) for s in SEQ2]
        row = VGroup(MathTex("=").scale(1.2), terms[0], MathTex("+").scale(1.2), terms[1],
                     MathTex("+").scale(1.2), terms[2], MathTex("+").scale(1.2), terms[3]).arrange(RIGHT, buff=0.3)
        row.move_to(UP * 1.1)
        self.at(7.3, FadeIn(row[0]), rt=0.3)
        for i, t in enumerate((7.8, 9.35, 11.3, 13.3)):
            self.upto(t)
            if i:
                self.add(row[2 * i])
            self.pick(fi, SEQ2[i], terms[i], rt=0.8)
        # A1A2: no B chosen
        box = SurroundingRectangle(terms[0], color=A_COL, buff=0.12)
        self.at(18.9, Create(box), rt=0.6)
        self.at(20.9, fi[1][1].animate.set_opacity(0.25), fi[2][1].animate.set_opacity(0.25), rt=0.6)
        self.at(23.3, Indicate(fi[1][0], scale_factor=1.5), Indicate(fi[2][0], scale_factor=1.5),
                Indicate(terms[0], color=A_COL), rt=1.2)
        self.at(27.4, Transform(box, SurroundingRectangle(terms[3], color=B_COL, buff=0.12)),
                fi[1][1].animate.set_opacity(1), fi[2][1].animate.set_opacity(1), rt=0.8)
        self.at(30.0, fi[1][0].animate.set_opacity(0.25), fi[2][0].animate.set_opacity(0.25), rt=0.5)
        self.play(Indicate(fi[1][1], scale_factor=1.5), Indicate(fi[2][1], scale_factor=1.5),
                  Indicate(terms[3], color=B_COL), run_time=1.2)
        self.end_clip()
        self.play(FadeOut(box), fi[1][0].animate.set_opacity(1), fi[2][0].animate.set_opacity(1), run_time=0.5)
        self.row2, self.terms2 = row, terms

    def s04(self):
        fac, fi = self.fac2, self.fi2
        row, terms = self.row2, self.terms2
        self.clip("p3_04")
        mid = VGroup(terms[1], terms[2])
        self.at(0.2, terms[0].animate.set_opacity(0.3), terms[3].animate.set_opacity(0.3), rt=0.6)
        b1 = SurroundingRectangle(terms[1], color=HL, buff=0.12)
        b2 = SurroundingRectangle(terms[2], color=HL, buff=0.12)
        self.at(2.6, Create(b1), rt=0.6)
        self.at(5.0, Create(b2), rt=0.6)
        q = MathTex("?", color=K_COL).scale(1.3).next_to(mid, DOWN, buff=0.4)
        self.at(7.4, FadeIn(q, shift=UP * 0.2), rt=0.5)
        self.at(8.6, FadeOut(q), Indicate(terms[1][1], color=B_COL, scale_factor=1.5),
                Indicate(terms[2][0], color=B_COL, scale_factor=1.5), rt=1.2)
        self.at(12.0, Wiggle(terms[1][1]), Wiggle(terms[2][0]), rt=1.3)
        # where did B come from?
        a_1 = CurvedArrow(fi[2][1].get_bottom() + DOWN * 0.05, terms[1][1].get_top() + UP * 0.05,
                          angle=-PI / 4, color=B_COL, stroke_width=3, tip_length=0.18)
        self.at(16.0, Create(a_1), Indicate(fi[2][1], scale_factor=1.5), rt=1.2)
        a_2 = CurvedArrow(fi[1][1].get_bottom() + DOWN * 0.05, terms[2][0].get_top() + UP * 0.05,
                          angle=PI / 4, color=B_COL, stroke_width=3, tip_length=0.18)
        self.at(20.0, Create(a_2), Indicate(fi[1][1], scale_factor=1.5), rt=1.2)
        br = Brace(mid, DOWN, color=HL)
        two = MathTex("2", color=HL).scale(1.2).next_to(br, DOWN, buff=0.1)
        self.at(24.6, GrowFromCenter(br), FadeIn(two, scale=1.4), rt=0.9)
        self.end_clip()
        self.play(FadeOut(VGroup(a_1, a_2, b1, b2)), run_time=0.4)
        self.br2 = VGroup(br, two)

    def s05(self):
        fac, fi = self.fac2, self.fi2
        row, terms = self.row2, self.terms2
        self.clip("p3_05")
        r1 = VGroup(lab_term("AB"), MathTex("+"), lab_term("BA")).arrange(RIGHT, buff=0.25)
        e1 = MathTex("=", "A", "B", "+", "A", "B")
        e2 = MathTex("=", "2", "A", "B")
        for e in (e1, e2):
            for m, tx in zip(e, e.tex_strings):
                if tx == "A":
                    m.set_color(A_COL)
                if tx == "B":
                    m.set_color(B_COL)
        e2[1].set_color(K_COL)
        line = VGroup(r1, e1, e2).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.9)
        self.at(4.3, FadeOut(self.br2), TransformFromCopy(VGroup(terms[1], terms[2]), VGroup(r1[0], r1[2])),
                FadeIn(r1[1]), rt=1.2)
        self.at(7.3, Write(e1), rt=1.4)
        self.at(9.9, Write(e2), rt=0.9)
        self.at(11.6, terms[0].animate.set_opacity(1), terms[3].animate.set_opacity(1), rt=0.5)
        self.at(15.0, LaggedStart(*[Indicate(t, scale_factor=1.15) for t in terms], lag_ratio=0.5), rt=5.5)
        fin = MathTex("=", "A^2", "+", "2", "AB", "+", "B^2").scale(1.2)
        fin[1].set_color(A_COL); fin[3].set_color(K_COL); fin[4].set_color(WHITE); fin[6].set_color(B_COL)
        fin.move_to(DOWN * 0.3)
        self.at(21.9, FadeOut(line, shift=DOWN * 0.3), rt=0.4)
        self.play(TransformFromCopy(terms[0], fin[1]), TransformFromCopy(VGroup(terms[1], terms[2]), VGroup(fin[3], fin[4])),
                  TransformFromCopy(terms[3], fin[6]), FadeIn(fin[0]), FadeIn(fin[2]), FadeIn(fin[5]), run_time=1.6)
        ring = Circle(radius=0.36, color=HL).move_to(fin[3])
        self.at(26.0, Create(ring), rt=0.7)
        self.play(Indicate(fi[1][1], scale_factor=1.5), run_time=0.9)
        self.play(Indicate(fi[2][1], scale_factor=1.5), run_time=0.9)
        self.end_clip()
        self.clear_all(0.7)

    # ============================================================ three factors
    def s06(self):
        self.clip("p3_06")
        cube = MathTex("(A+B)^3").scale(1.4)
        self.at(2.4, Write(cube), rt=1.0)
        fac, fi = factors(3, 1.15)
        fac.move_to(UP * 2.8)
        self.at(5.2, cube.animate.scale(0.7).move_to(UP * 2.8 + LEFT * 5.2).set_opacity(0.5), rt=0.8)
        self.at(6.2, Write(fac[0:5]), rt=0.9)
        self.at(7.6, Write(fac[5:10]), rt=0.8)
        self.at(8.8, Write(fac[10:15]), rt=0.8)
        terms = [lab_term(s, 1.0) for s in SEQ3]
        plus = [MathTex("+") for _ in range(8)]
        rows = [VGroup(MathTex("="), terms[0], plus[1], terms[1], plus[2], terms[2], plus[3], terms[3]),
                VGroup(plus[4], terms[4], plus[5], terms[5], plus[6], terms[6]),
                VGroup(plus[7], terms[7])]
        for r in rows:
            r.arrange(RIGHT, buff=0.25)
        for r, y in zip(rows, (1.3, 0.2, -0.9)):
            r.move_to(np.array([0, y, 0]))
            r.shift(RIGHT * (-4.6 - r.get_left()[0]))
        rows[1].shift(RIGHT * 0.6)
        rows[2].shift(RIGHT * 0.6)
        times = (15.0, 16.4, 18.1, 20.0, 21.9, 23.7, 25.4, 27.0)
        self.upto(14.9)
        self.add(rows[0][0])
        for i, t in enumerate(times):
            self.upto(t)
            if i:
                self.add(plus[i])
            self.pick(fi, SEQ3[i], terms[i], rt=0.6)
        self.at(29.0, *[Indicate(t, scale_factor=1.1) for t in terms], rt=1.0)
        self.end_clip()
        self.fac3, self.fi3, self.terms3, self.plus3, self.eq3 = fac, fi, terms, plus, rows[0][0]
        self.cube = cube

    # ============================================================ group by number of B's
    COLX = (-4.9, -1.65, 1.65, 4.9)
    COLY = (1.2, 0.35, -0.5)

    def col_pos(self, seq):
        nb = seq.count("B")
        same = [s for s in SEQ3 if s.count("B") == nb]
        return np.array([self.COLX[nb], self.COLY[same.index(seq)], 0])

    def s07(self):
        terms, fi = self.terms3, self.fi3
        self.clip("p3_07")
        self.at(0.2, FadeOut(VGroup(*self.plus3[1:], self.eq3)), rt=0.6)
        self.play(VGroup(*terms).animate.scale(0.8).move_to(DOWN * 2.4), run_time=0.8)

        def move(i):
            return terms[i].animate(path_arc=-0.4).scale(1 / 0.8).move_to(self.col_pos(SEQ3[i]))
        self.at(1.6, move(0), rt=1.0)
        self.at(4.4, *[fi[k][1].animate.set_opacity(0.25) for k in (1, 2, 3)], rt=0.6)
        self.at(6.5, Indicate(terms[0], color=A_COL), rt=1.0)
        self.at(8.6, *[fi[k][1].animate.set_opacity(1) for k in (1, 2, 3)], rt=0.5)
        for i, t in zip((1, 2, 3), (11.0, 13.6, 16.2)):
            self.at(t, move(i), rt=1.0)
        self.at(19.1, *[Indicate(terms[i][SEQ3[i].index("B")], color=B_COL, scale_factor=1.3) for i in (1, 2, 3)], rt=1.2)
        for i, t in zip((4, 5, 6), (24.9, 27.6, 30.3)):
            self.at(t, move(i), rt=1.0)
        self.at(33.3, *[Indicate(m, color=B_COL, scale_factor=1.3)
                        for i in (4, 5, 6) for m, c in zip(terms[i], SEQ3[i]) if c == "B"], rt=1.2)
        self.at(37.5, move(7), rt=1.0)
        self.at(40.2, Indicate(terms[7], color=B_COL, scale_factor=1.3), rt=1.0)
        self.end_clip()

    def headers(self):
        hs = VGroup()
        for k, x in enumerate(self.COLX):
            h = MathTex(str(k), "B").scale(1.0)
            h[1].set_color(B_COL)
            hs.add(h.move_to(np.array([x, 2.0, 0])))
        return hs

    def focus(self, k, rt=0.6):
        """dim all columns except k"""
        anims = []
        for i, s in enumerate(SEQ3):
            anims.append(self.terms3[i].animate.set_opacity(1 if s.count("B") == k else 0.3))
        for j, h in enumerate(self.hdr):
            anims.append(h.animate.set_opacity(1 if j == k else 0.3))
        self.play(*anims, run_time=rt)

    def s08(self):
        terms, fi = self.terms3, self.fi3
        self.clip("p3_08")
        self.hdr = self.headers()
        for k, t in enumerate((3.4, 4.6, 5.5, 6.4)):
            self.at(t, FadeIn(self.hdr[k], shift=DOWN * 0.2), rt=0.5)
        seps = VGroup(*[DashedLine(np.array([x, 2.3, 0]), np.array([x, -2.9, 0]), dash_length=0.08)
                        .set_stroke(SOFT, 1.5, 0.45) for x in (-3.3, 0, 3.3)])
        self.at(7.8, LaggedStart(*[Create(s) for s in seps], lag_ratio=0.2), rt=1.5)
        self.upto(12.8)
        self.focus(0)
        self.at(14.9, Indicate(terms[0], color=A_COL, scale_factor=1.25), rt=1.0)
        ind = indicator("AAA").next_to(terms[0], DOWN, buff=0.25)
        self.at(17.2, FadeIn(ind, shift=DOWN * 0.1), *[Indicate(fi[k][0]) for k in (1, 2, 3)], rt=1.2)
        self.at(21.5, LaggedStart(*[Indicate(sq, color=WHITE, scale_factor=1.6) for sq in ind], lag_ratio=0.3), rt=2.0)
        c = colored(["C(3,0)", "=", "1"], 0.95).move_to(np.array([self.COLX[0], -1.5, 0]))
        c[2].set_color(HL)
        self.at(27.3, Write(c), rt=1.4)
        res = colored(["A^{3}"], 1.1).move_to(np.array([self.COLX[0], -2.45, 0]))
        self.at(31.4, TransformFromCopy(terms[0], res), Indicate(c[2]), rt=1.0)
        self.end_clip()
        self.seps = seps
        self.inds = {0: ind}
        self.cvals = {0: c}
        self.res = {0: res}

    def column_story(self, k, t_terms, t_glow, t_choices, t_ways, t_c, t_res, res_tex):
        terms = self.terms3
        idx = [i for i, s in enumerate(SEQ3) if s.count("B") == k]
        self.upto(0.2)
        self.focus(k)
        for i, t in zip(idx, t_terms):
            self.at(t, Indicate(terms[i], scale_factor=1.2), rt=0.7)
        self.at(t_glow, *[Indicate(m, color=B_COL, scale_factor=1.6)
                          for i in idx for m, c in zip(terms[i], SEQ3[i]) if c == "B"], rt=1.1)
        inds = VGroup(*[indicator(SEQ3[i]).next_to(terms[i], RIGHT, buff=0.18) for i in idx])
        order = [idx.index(i) for i in sorted(idx, key=lambda i: SEQ3[i][::-1])]  # position order
        for j, t in zip(order, t_choices):
            self.at(t, FadeIn(inds[j], shift=LEFT * 0.1), Indicate(terms[idx[j]], color=HL, scale_factor=1.15), rt=0.8)
        br = Brace(VGroup(*[terms[i] for i in idx]), LEFT, color=HL, buff=0.12)
        three = MathTex("3", color=HL).next_to(br, LEFT, buff=0.1)
        self.at(t_ways, GrowFromCenter(br), FadeIn(three), rt=0.8)
        c = colored([f"C(3,{k})", "=", "3" if k in (1, 2) else "1"], 0.95).move_to(np.array([self.COLX[k], -1.5, 0]))
        c[2].set_color(HL)
        self.at(t_c, Write(c), rt=1.3)
        res = MathTex(res_tex).scale(1.1).move_to(np.array([self.COLX[k], -2.45, 0]))
        self.at(t_res, TransformFromCopy(VGroup(*[terms[i] for i in idx]), res), FadeOut(VGroup(br, three)), rt=1.2)
        self.inds[k], self.cvals[k], self.res[k] = inds, c, res

    def s09(self):
        self.clip("p3_09")
        self.column_story(1, (3.2, 4.9, 6.9), 9.3, (20.7, 22.9, 25.0), 27.3, 29.9, 34.2, r"3A^{2}B")
        self.end_clip()

    def s10(self):
        self.clip("p3_10")
        self.column_story(2, (2.8, 3.7, 5.3), 7.5, (18.3, 19.8, 21.4), 23.8, 26.3, 29.6, r"3AB^{2}")
        self.end_clip()

    def s11(self):
        terms = self.terms3
        self.clip("p3_11")
        self.upto(0.2)
        self.focus(3)
        self.at(1.9, Indicate(terms[7], scale_factor=1.2), rt=0.8)
        ind = indicator("BBB").next_to(terms[7], DOWN, buff=0.25)
        self.at(4.9, FadeIn(ind, shift=DOWN * 0.1), *[Indicate(self.fi3[k][1]) for k in (1, 2, 3)], rt=1.2)
        self.at(9.1, LaggedStart(*[Indicate(sq, color=WHITE, scale_factor=1.6) for sq in ind], lag_ratio=0.3), rt=1.8)
        c = colored(["C(3,3)", "=", "1"], 0.95).move_to(np.array([self.COLX[3], -1.5, 0]))
        c[2].set_color(HL)
        self.at(12.5, Write(c), rt=1.3)
        res = MathTex("B^{3}").scale(1.1).move_to(np.array([self.COLX[3], -2.45, 0]))
        self.at(16.0, TransformFromCopy(terms[7], res), rt=1.0)
        self.inds[3], self.cvals[3], self.res[3] = ind, c, res
        # the whole expansion
        full = MathTex("A^{3}", "+", r"3A^{2}B", "+", r"3AB^{2}", "+", "B^{3}").scale(1.2).move_to(UP * 0.9)
        keep = [self.res[k] for k in range(4)] + [self.cvals[k] for k in range(4)]
        self.at(18.4, *[FadeOut(m) for m in self.mobjects if m not in keep],
                *[self.cvals[k].animate.set_opacity(0.5) for k in range(4)], rt=1.0)
        self.upto(20.9)
        self.play(*[ReplacementTransform(self.res[k], full[2 * k]) for k in range(4)],
                  *[FadeIn(full[2 * k + 1]) for k in range(3)], run_time=1.6)
        crow = MathTex("C(3,0)", "A^{3}", "+", "C(3,1)", r"A^{2}B", "+", "C(3,2)", r"AB^{2}", "+", "C(3,3)", "B^{3}").scale(1.1)
        for i in (0, 3, 6, 9):
            crow[i].set_color(K_COL)
        crow.move_to(DOWN * 0.8)
        groups = [(0, 1), (2, 3, 4), (5, 6, 7), (8, 9, 10)]
        for k, t in enumerate((28.1, 31.4, 34.8, 37.9)):
            self.at(t, TransformFromCopy(self.cvals[k][0], crow[groups[k][-2]]),
                    FadeOut(self.cvals[k]), *[FadeIn(crow[j]) for j in groups[k] if j != groups[k][-2]], rt=1.0)
        self.end_clip()
        self.full3, self.crow3 = full, crow

    # ============================================================ the powers
    def s12(self):
        full, crow = self.full3, self.crow3
        self.clip("p3_12")
        self.at(0.4, FadeOut(crow), full.animate.move_to(UP * 2.2), rt=1.0)
        centers = [full[2 * k].get_center() for k in range(4)]
        lx = centers[0][0] - 1.6
        la = MathTex("A", color=A_COL).move_to(np.array([lx, 0.6, 0]))
        lb = MathTex("B", color=B_COL).move_to(np.array([lx, -0.4, 0]))
        ea = [MathTex(str(3 - k), color=A_COL).move_to(np.array([centers[k][0], 0.6, 0])) for k in range(4)]
        eb = [MathTex(str(k), color=B_COL).move_to(np.array([centers[k][0], -0.4, 0])) for k in range(4)]
        self.at(2.0, FadeIn(la), FadeIn(lb), rt=0.6)
        tb = [(6.2, 8.1), (9.9, 11.2), (13.3, 14.7), (16.8, 18.3)]
        for k, (t1, t2) in enumerate(tb):
            self.at(t1, FadeIn(eb[k], shift=DOWN * 0.2), Indicate(full[2 * k], scale_factor=1.15), rt=0.6)
            self.at(t2, FadeIn(ea[k], shift=UP * 0.2), rt=0.6)
        up = Arrow(eb[0].get_center() + DOWN * 0.45, eb[3].get_center() + DOWN * 0.45, buff=0.1, color=B_COL, stroke_width=3)
        dn = Arrow(ea[0].get_center() + UP * 0.45, ea[3].get_center() + UP * 0.45, buff=0.1, color=A_COL, stroke_width=3)
        pl = MathTex("+1", color=B_COL).scale(0.7).next_to(up, DOWN, buff=0.1)
        mi = MathTex("-1", color=A_COL).scale(0.7).next_to(dn, UP, buff=0.1)
        self.at(20.4, GrowArrow(up), FadeIn(pl), rt=1.0)
        self.at(23.4, GrowArrow(dn), FadeIn(mi), rt=1.0)
        f3 = MathTex("(A+B)", "(A+B)", "(A+B)").scale(0.9).move_to(DOWN * 2.8 + LEFT * 0.3)
        b3 = Brace(f3, DOWN, color=SOFT, buff=0.08)
        n3 = MathTex("3", color=HL).next_to(b3, RIGHT, buff=0.15).shift(UP * 0.1)
        self.at(26.0, FadeOut(VGroup(up, dn, pl, mi)), FadeIn(f3, shift=UP * 0.2), GrowFromCenter(b3), FadeIn(n3), rt=1.0)
        sums = [MathTex("=", "3").scale(0.9).move_to(np.array([centers[k][0], -1.35, 0])) for k in range(4)]
        lines = [Line(LEFT * 0.35, RIGHT * 0.35).set_stroke(SOFT, 2).move_to(np.array([centers[k][0], -0.85, 0])) for k in range(4)]
        for s in sums:
            s[1].set_color(HL)
        self.upto(29.0)
        for k in range(4):
            self.play(Indicate(full[2 * k], scale_factor=1.15), run_time=0.5)
        self.at(32.0, LaggedStart(*[AnimationGroup(Create(lines[k]), FadeIn(sums[k], shift=DOWN * 0.1)) for k in range(4)],
                                  lag_ratio=0.4), rt=2.4)
        self.at(35.5, *[Indicate(s[1], scale_factor=1.4) for s in sums], Indicate(n3, scale_factor=1.4), rt=1.0)
        self.end_clip()
        self.clear_all(0.7)

    # ============================================================ general n
    def s13(self):
        self.clip("p3_13")
        facs = VGroup(*[MathTex("(", "A", "+", "B", ")").scale(1.0) for _ in range(5)])
        for f in facs:
            f[1].set_color(A_COL); f[3].set_color(B_COL)
        dots = MathTex(r"\cdots").scale(1.2)
        row = VGroup(*facs[:4], dots, facs[4]).arrange(RIGHT, buff=0.25).move_to(UP * 2.0)
        br = Brace(row, DOWN, color=SOFT)
        bn_ = MathTex("n", color=SOFT).next_to(br, DOWN, buff=0.1)
        self.at(0.8, LaggedStart(*[FadeIn(m, shift=DOWN * 0.2) for m in row], lag_ratio=0.15), rt=1.8)
        self.at(3.6, GrowFromCenter(br), FadeIn(bn_), rt=0.8)
        chosenB = [1, 3, 4]      # factors where B is picked (r of them)
        chosenA = [0, 2]
        bbox = VGroup(*[SurroundingRectangle(facs[i][3], color=B_COL, buff=0.06) for i in chosenB])
        abox = VGroup(*[SurroundingRectangle(facs[i][1], color=A_COL, buff=0.06) for i in chosenA])
        self.at(7.0, LaggedStart(*[Create(b) for b in bbox], lag_ratio=0.35), *[facs[i][1].animate.set_opacity(0.3) for i in chosenB], rt=1.8)
        rB = MathTex("r", color=B_COL).scale(0.9).next_to(bbox, UP, buff=0.35)
        self.play(FadeIn(rB), run_time=0.4)
        cnr = MathTex("C(n, r)", color=K_COL).scale(1.3).move_to(DOWN * 0.6)
        self.at(12.2, TransformFromCopy(bbox, cnr), rt=1.1)
        self.at(14.2, LaggedStart(*[Create(b) for b in abox], lag_ratio=0.35), *[facs[i][3].animate.set_opacity(0.3) for i in chosenA], rt=1.4)
        nr = MathTex("n-r", color=A_COL).scale(0.9).next_to(abox, UP, buff=0.35).set_y(rB.get_y())
        self.play(FadeIn(nr), run_time=0.4)
        term = MathTex("A^{n-r}", "B^{r}").scale(1.3)
        term[0].set_color(A_COL); term[1].set_color(B_COL)
        term.next_to(cnr, RIGHT, buff=0.25)
        self.at(21.2, TransformFromCopy(abox, term[0]), TransformFromCopy(bbox, term[1]), rt=1.3)
        gen = VGroup(cnr, term)
        self.at(25.9, gen.animate.move_to(DOWN * 1.2).scale(1.15), rt=0.8)
        box = SurroundingRectangle(gen, color=HL, buff=0.2, corner_radius=0.1)
        self.play(Create(box), run_time=0.8)
        self.end_clip()
        keep = [cnr, term, box]
        self.play(*[FadeOut(m) for m in self.mobjects if m not in keep], run_time=0.6)
        self.gen = VGroup(cnr, term, box)

    def s14(self):
        self.clip("p3_14")
        F = MathTex("(A+B)^{n}", "=", r"\sum_{r=0}^{n}", "C(n, r)", "A^{n-r}", "B^{r}").scale(1.35)
        F[3].set_color(K_COL); F[4].set_color(A_COL); F[5].set_color(B_COL)
        F.move_to(UP * 0.3)
        self.at(1.0, FadeOut(self.gen[2]), rt=0.5)
        self.at(3.5, Write(F[0]), rt=1.2)
        self.at(5.9, Write(F[1]), rt=0.4)
        self.at(6.8, Write(F[2]), rt=1.6)
        self.at(9.8, ReplacementTransform(self.gen[0], F[3]), ReplacementTransform(self.gen[1][0], F[4]),
                ReplacementTransform(self.gen[1][1], F[5]), rt=1.6)
        glow = VGroup(*[F.copy().set_fill(opacity=0).set_stroke(HL, w, o) for w, o in ((8, 0.18), (18, 0.06))])
        self.at(15.8, FadeIn(glow), rt=1.0)
        self.play(FadeOut(glow), run_time=1.0)
        cb = SurroundingRectangle(F[3], color=K_COL, buff=0.12)
        self.at(19.1, Create(cb), rt=0.8)
        self.end_clip()
        self.play(FadeOut(cb), run_time=0.3)
        self.F = F

    def s15(self):
        F = self.F
        self.clip("p3_15")
        self.at(0.5, F.animate.scale(0.75).to_edge(UP, buff=0.5), rt=1.0)
        F2 = MathTex("(A+B)^{2}", "=", r"\sum_{r=0}^{2}", "C(2, r)", "A^{2-r}", "B^{r}").scale(1.15)
        F2[3].set_color(K_COL); F2[4].set_color(A_COL); F2[5].set_color(B_COL)
        F2.move_to(UP * 1.1)
        self.at(5.7, TransformFromCopy(F[0], F2[0]), rt=1.0)
        self.at(7.6, TransformFromCopy(F[1:3], F2[1:3]), rt=1.2)
        self.at(11.0, TransformFromCopy(F[3], F2[3]), rt=0.9)
        self.at(12.5, TransformFromCopy(F[4], F2[4]), rt=0.9)
        self.at(14.6, TransformFromCopy(F[5], F2[5]), rt=0.9)
        T = MathTex("=", "C(2,0)", "A^{2}", "+", "C(2,1)", "AB", "+", "C(2,2)", "B^{2}").scale(1.1)
        for i in (1, 4, 7):
            T[i].set_color(K_COL)
        T[2].set_color(A_COL); T[8].set_color(B_COL)
        T.next_to(F2, DOWN, buff=0.5)
        T.set_x(0)
        if T.width > 12.8:
            T.scale_to_fit_width(12.8)
        self.at(18.3, FadeIn(T[0]), Write(T[1:3]), rt=1.2)
        self.at(20.4, Write(T[3:6]), rt=1.2)
        self.at(22.3, Write(T[6:]), rt=1.2)
        vals = VGroup(*[MathTex(s, color=K_COL).scale(0.9) for s in ("C(2,0)=1", "C(2,1)=2", "C(2,2)=1")]).arrange(RIGHT, buff=0.8)
        vals.next_to(T, DOWN, buff=0.55)
        for v, t in zip(vals, (25.0, 27.4, 29.2)):
            self.at(t, FadeIn(v, shift=UP * 0.2), rt=0.6)
        R = MathTex("(A+B)^{2}", "=", "A^{2}", "+", "2", "AB", "+", "B^{2}").scale(1.2)
        R[2].set_color(A_COL); R[4].set_color(K_COL); R[7].set_color(B_COL)
        R.next_to(vals, DOWN, buff=0.6)
        self.at(31.3, Write(R), rt=2.0)
        box = SurroundingRectangle(R, color=HL, buff=0.15)
        self.at(37.0, Create(box), rt=0.8)
        self.play(Flash(box.get_corner(UR), color=HL), run_time=0.7)
        self.end_clip()
        self.play(*[FadeOut(m) for m in self.mobjects if m is not F],
                  F.animate.scale(1 / 0.75).move_to(UP * 0.8), run_time=0.9)

    def s16(self):
        F = self.F
        self.clip("p3_16")
        self.at(2.9, Indicate(F, color=WHITE, scale_factor=1.05), rt=1.5)
        cb = SurroundingRectangle(F[3], color=K_COL, buff=0.12)
        self.at(13.8, Create(cb), rt=0.8)
        comb_note = MathTex("C(n, r)", "=", r"\frac{n!}{r!\,(n-r)!}").scale(1.1)
        comb_note[0].set_color(K_COL)
        comb_note.move_to(DOWN * 1.6)
        self.at(19.8, TransformFromCopy(F[3], comb_note[0]), FadeIn(comb_note[1:]), rt=1.3)
        G = MathTex("(A+B)^{n}", "=", r"\sum_{r=0}^{n}", r"\frac{n!}{r!\,(n-r)!}", "A^{n-r}", "B^{r}").scale(1.35)
        G[3].set_color(K_COL); G[4].set_color(A_COL); G[5].set_color(B_COL)
        G.move_to(UP * 0.8)
        self.at(29.3, FadeOut(cb), ReplacementTransform(F[0:3], G[0:3]), ReplacementTransform(F[4:], G[4:]),
                FadeOut(F[3]), TransformFromCopy(comb_note[2], G[3]), rt=1.8)
        self.at(31.8, FadeOut(comb_note, shift=DOWN * 0.3), rt=0.8)
        box = SurroundingRectangle(G, color=HL, buff=0.2, corner_radius=0.1)
        self.at(34.0, Create(box), rt=1.0)
        self.end_clip()
        self.clear_all(0.7)

    def s17(self):
        self.clip("p3_17")
        # labels disappear: A1 A2 A3 → A A A → A^3
        lab = lab_term("AAA", 1.4).move_to(UP * 1.4 + LEFT * 2.8)
        labB = lab_term("BBB", 1.4).move_to(UP * 1.4 + RIGHT * 2.8)
        self.at(0.5, FadeIn(lab, shift=UP * 0.2), FadeIn(labB, shift=UP * 0.2), rt=0.8)
        plainA = MathTex("A", "A", "A", color=A_COL).scale(1.4).move_to(lab)
        plainB = MathTex("B", "B", "B", color=B_COL).scale(1.4).move_to(labB)
        self.at(4.0, TransformMatchingShapes(lab, plainA), TransformMatchingShapes(labB, plainB), rt=1.5)
        a3 = MathTex("A^{3}", color=A_COL).scale(1.4).move_to(plainA)
        b3 = MathTex("B^{3}", color=B_COL).scale(1.4).move_to(plainB)
        self.at(8.3, TransformMatchingShapes(plainA, a3), TransformMatchingShapes(plainB, b3), rt=1.3)
        ak = MathTex(r"\underbrace{A\cdot A\cdots A}_{k}", "=", "A^{k}").scale(1.2)
        ak[0].set_color(A_COL); ak[2].set_color(A_COL)
        ak.move_to(DOWN * 1.0)
        self.at(12.0, FadeIn(ak[0], shift=UP * 0.2), rt=1.0)
        self.at(16.3, Write(ak[1:]), rt=1.0)
        self.at(19.3, FadeOut(VGroup(a3, b3, ak)), rt=0.8)
        T = MathTex("(A+B)^{n}", "=", "C(n,0)", "A^{n}", "+", "C(n,1)", "A^{n-1}", "B", "+",
                    "C(n,2)", "A^{n-2}", "B^{2}", "+", r"\cdots", "+", "C(n,n)", "B^{n}").scale(0.95)
        for i in (2, 5, 9, 15):
            T[i].set_color(K_COL)
        for i in (3, 6, 10):
            T[i].set_color(A_COL)
        for i in (7, 11, 16):
            T[i].set_color(B_COL)
        T.scale_to_fit_width(12.6).move_to(ORIGIN)
        self.at(23.5, Write(T[0:2]), rt=1.2)
        self.at(25.0, Write(T[2:4]), rt=1.2)
        self.at(27.6, Write(T[4:8]), rt=1.6)
        self.at(30.6, Write(T[8:12]), rt=1.6)
        self.at(33.4, Write(T[12:15]), rt=1.2)
        self.at(37.7, Write(T[15:]), rt=1.4)
        box = SurroundingRectangle(T, color=HL, buff=0.25, corner_radius=0.12)
        glow = VGroup(*[box.copy().set_stroke(HL, w, o) for w, o in ((10, 0.18), (22, 0.07))])
        self.at(39.6, Create(box), FadeIn(glow), rt=1.4)
        self.end_clip(pad=1.0)          # [wait(1)]
        self.play(FadeOut(VGroup(T, box, glow)), run_time=1.0)
