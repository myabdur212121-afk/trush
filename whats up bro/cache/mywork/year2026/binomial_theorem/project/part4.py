"""Part 4 — Chapter 3 (Pascal's Triangle) + Summary."""
from common import *

DX, DY, TSIZE = 1.15, 0.9, 54


def num(v, size=TSIZE, color=WHITE):
    return MathTex(str(v), font_size=size, color=color)


def vee(a, b, c, col=SOFT, w=3):
    """two arrows: upper a, b -> lower c"""
    return VGroup(*[Arrow(m.get_bottom(), c.get_top(), buff=0.08, stroke_width=w, color=col,
                          max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=8)
                    for m in (a, b)])


def dot(col=SOFT, r=0.17):
    return Circle(r).set_stroke(col, 2).set_fill(col, 0.3)


class Part4(Narrated, MovingCameraScene):

    def clear_all(self, rt=0.6, keep=()):
        mobs = [m for m in self.mobjects if m not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=rt)

    def construct(self):
        for i in range(1, 20):
            name = f"s{i:02d}"
            if hasattr(self, name) and (AUDIO / f"p4_{i:02d}.mp3").exists():
                getattr(self, name)()
        self.wait(0.5)

    # ------------------------------------------------------------ helpers
    def tri_pos(self, n, k, center=ORIGIN, rows=5, dx=DX, dy=DY):
        top = (rows - 1) * dy / 2
        return np.array([(k - n / 2) * dx, top - n * dy, 0]) + center

    def reset_tri(self, rt=0.5):
        self.play(*[m.animate.set_color(WHITE).set_opacity(1) for row in self.tri for m in row], run_time=rt)

    # ============================================================ s01
    def s01(self):
        self.clip("p4_01")
        G = MathTex("(A+B)^{n}", "=", r"\sum_{r=0}^{n}", "C(n,r)", "A^{n-r}", "B^{r}").scale(1.2)
        G[3].set_color(K_COL); G[4].set_color(A_COL); G[5].set_color(B_COL)
        G.move_to(UP * 0.4)
        self.at(0.3, Write(G[0]), rt=1.2)
        self.at(3.6, Write(G[1:]), rt=2.2)
        cb = SurroundingRectangle(G[3], color=K_COL, buff=0.1)
        lab = en("Combination", 34).set_color(SOFT).next_to(cb, DOWN, buff=0.7)
        ar = Arrow(lab.get_top(), cb.get_bottom(), buff=0.1, color=SOFT, stroke_width=3)
        self.at(8.4, Create(cb), Indicate(G[3], color=K_COL), rt=1.0)
        self.at(11.6, FadeIn(lab, shift=UP * 0.2), GrowArrow(ar), rt=0.9)
        self.at(15.3, FadeOut(VGroup(G, cb, lab, ar)), rt=0.8)

        # the list of expansions, aligned at "="
        self.rows = []
        EQX = -3.55
        for n in range(5):
            tex, info = expansion_row(n, sym=("A", "B"))
            tex.scale(0.72)
            tex.shift(np.array([EQX - info["eq"].get_x(), 2.4 - 0.8 * n - tex.get_y(), 0]))
            self.rows.append((tex, info))
        times = [(20.2, 1.6), (23.3, 2.4), (27.2, 3.4), (32.5, 4.8), (39.9, 7.0)]
        for (tex, info), (t, d) in zip(self.rows, times):
            self.at(t, Write(info["lhs"]), FadeIn(info["eq"]), rt=0.8)
            self.play(Write(info["rhs"]), run_time=d)
        self.end_clip()

    # ============================================================ s02
    def s02(self):
        self.clip("p4_02")
        more = VGroup()
        for i, n in enumerate((5, 6)):
            t = MathTex(f"(A+B)^{{{n}}}", "=", r"\cdots").scale(0.72)
            t[0].set_color(SOFT)
            t.shift(np.array([self.rows[0][1]["eq"].get_x() - t[1].get_x(), 2.4 - 0.8 * (5 + i) - t.get_y(), 0]))
            more.add(t)
        vd = MathTex(r"\vdots").scale(0.72).move_to(more[1][0].get_center() + DOWN * 0.7)
        self.at(3.4, FadeIn(more[0], shift=UP * 0.2), rt=0.6)
        self.at(5.3, FadeIn(more[1], shift=UP * 0.2), rt=0.6)
        self.at(6.7, FadeIn(vd), rt=0.5)
        # dim letters, reveal the hidden 1s
        dim, ones = [], []
        self.src = []           # per row: list of source mobs for each coefficient
        for n, (tex, info) in enumerate(self.rows):
            dim.append(info["lhs"]); dim.append(info["eq"]); dim.append(info["plus"])
            row_src = []
            for term in info["terms"]:
                if term["coef"] is not None:
                    row_src.append(term["coef"])
                    if n > 0:
                        dim.append(term["body"])
                else:
                    o = MathTex("1", color=K_COL).scale(0.72).move_to(term["body"])
                    ones.append(o)
                    dim.append(term["body"])
                    row_src.append(o)
            self.src.append(row_src)
        self.at(8.8, FadeOut(VGroup(more, vd)), *[m.animate.set_opacity(0.12) for m in dim], rt=1.2)
        self.play(LaggedStart(*[FadeIn(o, scale=1.4) for o in ones], lag_ratio=0.1), run_time=1.6)
        # coefficient rows on the right, left aligned
        LX = 1.3
        self.crow = []
        for n in range(5):
            y = self.rows[n][0].get_y()
            self.crow.append([num(comb(n, k)).move_to(np.array([LX + 0.75 * k, y, 0])) for k in range(n + 1)])
        cues = [[16.55], [18.5, 19.3], [21.3, 22.1, 22.75], [24.75, 25.55, 26.3, 27.0],
                [29.0, 29.75, 30.45, 31.25, 31.95]]
        for n in range(5):
            for k, t in enumerate(cues[n]):
                self.at(t, TransformFromCopy(self.src[n][k], self.crow[n][k]), rt=0.4)
        self.end_clip()
        self.ones = ones

    # ============================================================ s03
    def s03(self):
        self.clip("p4_03")
        old = [m for m in self.mobjects if not any(m in r for r in self.crow)]
        self.at(0.4, *[FadeOut(m) for m in old], rt=0.8)
        tri = VGroup(*[VGroup(*r) for r in self.crow])
        self.remove(*[m for r in self.crow for m in r]); self.add(tri)
        self.tri = tri
        self.at(1.6, *[tri[n][k].animate.move_to(self.tri_pos(n, k)) for n in range(5) for k in range(n + 1)], rt=2.4)
        top = self.tri_pos(0, 0) + UP * 0.6
        bl = self.tri_pos(4, 0) + LEFT * 0.75 + DOWN * 0.45
        br = self.tri_pos(4, 4) + RIGHT * 0.75 + DOWN * 0.45
        outline = Polygon(top, bl, br).set_stroke(A_COL, 2.5, 0.7).set_fill(A_COL, 0.05)
        self.at(8.2, Create(outline), rt=1.6)
        self.at(11.0, LaggedStart(*[Indicate(m, color=HL, scale_factor=1.2) for r in tri for m in r], lag_ratio=0.06),
                rt=1.8)
        self.outline = outline
        self.upto(12.85)
        chapter_title(self, "Pascal's Triangle", "Chapter 3", clear_after=False)
        self.end_clip()

    # ============================================================ s04
    def s04(self):
        tri = self.tri
        self.clip("p4_04")
        labs = VGroup(*[MathTex(f"(A+B)^{{{n}}}", color=SOFT).scale(0.62)
                        .move_to(np.array([-4.4, tri[n][0].get_y(), 0])) for n in range(5)])
        self.at(0.3, FadeOut(self.outline), LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in labs], lag_ratio=0.15),
                rt=1.6)
        q = MathTex("?", color=K_COL).scale(2.2).move_to(np.array([3.6, 0.2, 0]))
        self.at(4.6, FadeIn(q, scale=0.5), rt=0.6)
        self.at(7.2, FadeOut(labs, shift=LEFT * 0.2), rt=0.7)
        self.play(LaggedStart(*[Indicate(m, color=HL, scale_factor=1.25) for r in tri for m in r], lag_ratio=0.08),
                  run_time=2.4)
        self.at(12.4, FadeOut(q), rt=0.6)
        self.end_clip()
        self.head = pattern_heading(self, "Pattern 1")

    # ============================================================ s05  Pattern 1
    def s05(self):
        tri = self.tri
        self.clip("p4_05")
        left = [tri[n][0] for n in range(5)]
        right = [tri[n][n] for n in range(1, 5)]
        self.at(0.4, LaggedStart(*[Indicate(r, color=WHITE, scale_factor=1.08) for r in tri], lag_ratio=0.15), rt=1.8)
        self.at(3.5, LaggedStart(*[m.animate.set_color(HL).scale(1.15) for m in left], lag_ratio=0.2), rt=1.6)
        self.at(6.6, LaggedStart(*[m.animate.set_color(HL).scale(1.15) for m in right], lag_ratio=0.2), rt=1.4)
        for n, t in enumerate((9.67, 10.77, 12.1, 13.81, 15.86)):
            self.at(t, Indicate(tri[n], color=WHITE, scale_factor=1.12), rt=0.7)
        # labels C(n,0), C(n,n)
        lc = MathTex("C(n,0)", "=", "1").scale(0.85); lc[0].set_color(K_COL); lc[2].set_color(HL)
        rc = MathTex("C(n,n)", "=", "1").scale(0.85); rc[0].set_color(K_COL); rc[2].set_color(HL)
        y = tri[2][0].get_y()
        lc.move_to(np.array([-4.3, y, 0])); rc.move_to(np.array([4.3, y, 0]))
        la = Arrow(lc.get_right(), tri[2][0].get_left(), buff=0.15, color=SOFT, stroke_width=3)
        ra = Arrow(rc.get_left(), tri[2][2].get_right(), buff=0.15, color=SOFT, stroke_width=3)
        self.at(21.4, Write(lc[0]), GrowArrow(la), rt=1.0)
        self.at(24.7, Write(rc[0]), GrowArrow(ra), rt=1.0)
        self.at(27.3, Write(lc[1:]), rt=0.8)
        self.at(29.4, Write(rc[1:]), rt=0.8)
        gl = Line(self.tri_pos(0, 0) + UP * 0.2, self.tri_pos(4, 0) + DOWN * 0.2 + LEFT * 0.1)
        gr = Line(self.tri_pos(0, 0) + UP * 0.2, self.tri_pos(4, 4) + DOWN * 0.2 + RIGHT * 0.1)
        glow = VGroup(*[l.copy().set_stroke(HL, w, o) for l in (gl, gr) for w, o in ((30, 0.10), (14, 0.14))])
        self.at(31.5, FadeIn(glow), Indicate(lc[2]), Indicate(rc[2]), rt=1.2)
        self.end_clip(pad=0.3)
        self.play(FadeOut(VGroup(lc, rc, la, ra, glow)),
                  *[m.animate.set_color(WHITE).scale(1 / 1.15) for m in left + right], run_time=0.8)
        self.play(FadeOut(self.head), run_time=0.4)
        self.head = pattern_heading(self, "Pattern 2")

    # ============================================================ s06  Pattern 2
    def s06(self):
        tri = self.tri
        self.clip("p4_06")
        self.at(0.3, tri[3].animate.set_opacity(0.15), tri[4].animate.set_opacity(0.15), rt=0.8)
        self.at(5.0, tri[1][0].animate.set_color(HL), Indicate(tri[1][0], color=HL), rt=0.6)
        self.at(6.4, tri[1][1].animate.set_color(HL), Indicate(tri[1][1], color=HL), rt=0.6)
        LX = 3.8

        def lab(s, n, x=LX):
            return MathTex(s).scale(0.8).move_to(np.array([x, tri[n][0].get_y(), 0]))

        v1 = vee(tri[1][0], tri[1][1], tri[2][1], col=HL)
        l1 = lab("1+1=2", 2)
        self.at(7.4, *[GrowArrow(a) for a in v1], rt=0.8)
        self.at(8.9, Write(l1), rt=1.2)
        self.play(tri[2][1].animate.set_color(K_COL), Indicate(tri[2][1], color=K_COL, scale_factor=1.4), run_time=0.7)
        self.at(11.6, FadeOut(v1), tri[3].animate.set_opacity(1), *[m.animate.set_color(WHITE) for m in (tri[1][0], tri[1][1])],
                tri[2][1].animate.set_color(WHITE), rt=0.8)
        v2 = vee(tri[2][0], tri[2][1], tri[3][1], col=HL)
        v3 = vee(tri[2][1], tri[2][2], tri[3][2], col=B_COL)
        l2 = lab("1+2=3", 3)
        l3 = lab("2+1=3", 3, x=LX + 1.95)
        self.at(14.4, *[GrowArrow(a) for a in v2], Write(l2), tri[3][1].animate.set_color(HL), rt=1.2)
        self.at(16.9, *[GrowArrow(a) for a in v3], Write(l3), tri[3][2].animate.set_color(B_COL), rt=1.2)
        self.at(19.8, FadeOut(VGroup(v2, v3)), rt=0.5)
        for k, t in enumerate((21.43, 22.2, 22.89, 23.56)):
            self.at(t, Indicate(tri[3][k], color=HL, scale_factor=1.35), rt=0.5)
        self.at(24.4, tri[4].animate.set_opacity(1), *[m.animate.set_color(WHITE) for m in tri[3]], rt=0.6)
        v4 = vee(tri[3][1], tri[3][2], tri[4][2], col=K_COL)
        l4 = lab("3+3=6", 4)
        self.at(26.2, *[GrowArrow(a) for a in v4], Write(l4), tri[4][2].animate.set_color(K_COL), rt=1.2)
        self.at(28.8, FadeOut(v4), rt=0.4)
        for k, t in enumerate((29.85, 30.45, 31.05, 31.65, 32.25)):
            self.at(t, Indicate(tri[4][k], color=HL, scale_factor=1.35), rt=0.5)
        self.at(33.5, FadeOut(VGroup(l1, l2, l3, l4)), tri[4][2].animate.set_color(WHITE), rt=0.6)
        allv = VGroup()
        for n in range(2, 5):
            for k in range(1, n):
                allv.add(vee(tri[n - 1][k - 1], tri[n - 1][k], tri[n][k], col=SOFT, w=2.5))
        inner = [tri[n][k] for n in range(2, 5) for k in range(1, n)]
        self.play(LaggedStart(*[AnimationGroup(*[GrowArrow(a) for a in v]) for v in allv], lag_ratio=0.35),
                  run_time=3.0)
        self.play(*[m.animate.set_color(K_COL) for m in inner], run_time=0.6)
        self.end_clip()
        self.allv, self.inner = allv, inner

    # ============================================================ s07  why?
    def s07(self):
        tri = self.tri
        self.clip("p4_07")
        q = MathTex("?", color=K_COL).scale(2.2).move_to(np.array([3.6, 0.2, 0]))
        self.at(1.9, FadeIn(q, scale=0.5), rt=0.5)
        self.at(3.0, FadeOut(self.allv), *[m.animate.set_color(WHITE) for m in self.inner], rt=0.7)
        self.play(tri.animate.scale(0.6).move_to(np.array([-5.3, 0.0, 0])), FadeOut(q), run_time=1.2)
        CX = 2.0
        top = MathTex("C(n,r)", color=K_COL).scale(1.0).move_to(np.array([CX, 3.2, 0]))
        self.at(8.6, Write(top), rt=1.0)
        dots = VGroup(*[dot() for _ in range(5)]).arrange(RIGHT, buff=0.35).move_to(np.array([CX, 2.35, 0]))
        br = Brace(dots, DOWN, buff=0.15, color=SOFT)
        bn_ = MathTex("n", color=SOFT).scale(0.8).next_to(br, DOWN, buff=0.08)
        self.at(13.5, LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.15), rt=1.2)
        self.at(15.1, GrowFromCenter(br), FadeIn(bn_), rt=0.7)
        sel = [1, 2, 4]
        self.at(16.8, LaggedStart(*[dots[i].animate.set_fill(HL, 0.9).set_stroke(HL) for i in sel], lag_ratio=0.3),
                rt=1.4)
        self.at(19.5, *[dots[i].animate.set_fill(SOFT, 0.3).set_stroke(SOFT) for i in sel], rt=0.5)
        self.at(20.2, LaggedStart(*[dots[i].animate.set_fill(HL, 0.9).set_stroke(HL) for i in sel], lag_ratio=0.3),
                rt=1.4)
        self.at(23.0, *[dots[i].animate.set_fill(SOFT, 0.3).set_stroke(SOFT) for i in sel], rt=0.4)
        la = MathTex("A", color=A_COL).scale(0.7).next_to(dots[0], UP, buff=0.1)
        self.at(24.3, dots[0].animate.set_fill(A_COL, 0.9).set_stroke(A_COL).scale(1.2), FadeIn(la, shift=DOWN * 0.1),
                rt=0.8)
        self.play(Indicate(VGroup(dots[0], la), color=A_COL), run_time=0.8)
        L, R = np.array([-0.2, -0.3, 0]), np.array([4.4, -0.3, 0])
        aL = Arrow(bn_.get_bottom() + LEFT * 0.3, L + UP * 0.8, buff=0.1, color=SOFT, stroke_width=3)
        aR = Arrow(bn_.get_bottom() + RIGHT * 0.3, R + UP * 0.8, buff=0.1, color=SOFT, stroke_width=3)
        self.at(28.0, GrowArrow(aL), GrowArrow(aR), rt=0.9)
        AL = dot(A_COL).set_fill(A_COL, 0.9).scale(1.2).move_to(L + LEFT * 1.35)
        AR = dot(A_COL).set_fill(A_COL, 0.9).scale(1.2).move_to(R + LEFT * 1.35)
        ring = Circle(0.32).set_stroke(HL, 3).move_to(AL)
        cross = VGroup(Line(UL, DR), Line(UR, DL)).scale(0.22).set_stroke(K_COL, 4).move_to(AR)
        self.at(32.1, TransformFromCopy(dots[0], AL), Create(ring), rt=0.9)
        self.at(34.0, TransformFromCopy(dots[0], AR), rt=0.6)
        self.play(Create(cross), AR.animate.set_opacity(0.35), run_time=0.5)
        self.end_clip()
        self.why = dict(top=top, dots=dots, br=br, bn=bn_, la=la, aL=aL, aR=aR, AL=AL, AR=AR, ring=ring,
                        cross=cross, L=L, R=R)

    # ============================================================ s08
    def s08(self):
        W = self.why
        L, R = W["L"], W["R"]
        self.clip("p4_08")

        def branch(c):
            ds = VGroup(*[dot() for _ in range(4)]).arrange(RIGHT, buff=0.3).move_to(c + RIGHT * 0.35)
            b = Brace(ds, DOWN, buff=0.12, color=SOFT)
            t = MathTex("n-1", color=SOFT).scale(0.7).next_to(b, DOWN, buff=0.06)
            return ds, b, t

        dl, bl, tl = branch(L)
        dr, brr, tr = branch(R)
        self.at(1.5, TransformFromCopy(W["dots"][1:], dl), rt=0.9)
        self.at(3.4, GrowFromCenter(bl), FadeIn(tl), rt=0.6)
        selL = [0, 2]
        rl = MathTex("r-1", color=HL).scale(0.65)
        self.at(5.0, *[dl[i].animate.set_fill(HL, 0.9).set_stroke(HL) for i in selL], rt=0.8)
        rl.next_to(VGroup(*[dl[i] for i in selL]), UP, buff=0.12)
        self.play(FadeIn(rl, shift=DOWN * 0.1), run_time=0.4)
        cL = MathTex("C(n-1,\\,r-1)", color=K_COL).scale(0.85).move_to(L + DOWN * 1.4)
        self.at(9.5, Write(cL), rt=1.2)
        self.at(14.4, TransformFromCopy(W["dots"][1:], dr), rt=0.9)
        self.at(16.0, GrowFromCenter(brr), FadeIn(tr), rt=0.6)
        selR = [0, 1, 3]
        rr = MathTex("r", color=HL).scale(0.7)
        self.at(17.4, *[dr[i].animate.set_fill(HL, 0.9).set_stroke(HL) for i in selR], rt=0.8)
        rr.next_to(VGroup(*[dr[i] for i in selR]), UP, buff=0.12)
        self.play(FadeIn(rr, shift=DOWN * 0.1), run_time=0.4)
        cR = MathTex("C(n-1,\\,r)", color=K_COL).scale(0.85).move_to(R + DOWN * 1.4)
        self.at(21.6, Write(cR), rt=1.2)
        eq = MathTex("C(n,r)", "=", "C(n-1,\\,r-1)", "+", "C(n-1,\\,r)").scale(0.95)
        eq[0].set_color(K_COL); eq[2].set_color(HL); eq[4].set_color(B_COL)
        eq.move_to(np.array([2.1, -2.95, 0]))
        self.at(26.5, TransformFromCopy(W["top"], eq[0]), FadeIn(eq[1]), rt=1.0)
        self.at(28.6, TransformFromCopy(cL, eq[2]), FadeIn(eq[3]), rt=1.0)
        self.at(31.1, TransformFromCopy(cR, eq[4]), rt=1.0)
        self.end_clip()
        self.eq = eq

    # ============================================================ s09
    def s09(self):
        tri, eq = self.tri, self.eq
        self.clip("p4_09")
        keep = [tri, eq, self.head]
        self.play(*[FadeOut(m) for m in self.mobjects if m not in keep], run_time=0.7)
        self.play(eq.animate.scale(1.0).move_to(np.array([0.9, 2.85, 0])),
                  tri.animate.scale(1 / 0.6).move_to(DOWN * 0.45), run_time=1.2)
        box = SurroundingRectangle(eq, color=HL, buff=0.15, corner_radius=0.08)
        self.at(2.2, Create(box), rt=0.8)
        a, b, c = tri[3][1], tri[3][2], tri[4][2]
        v = VGroup(Arrow(a.get_bottom(), c.get_top(), buff=0.08, color=HL, stroke_width=3),
                   Arrow(b.get_bottom(), c.get_top(), buff=0.08, color=B_COL, stroke_width=3))
        self.at(4.6, a.animate.set_color(HL), b.animate.set_color(B_COL), Indicate(eq[2]), Indicate(eq[4]), rt=0.9)
        self.play(*[GrowArrow(x) for x in v], run_time=0.6)
        self.play(c.animate.set_color(K_COL), Indicate(c, color=K_COL, scale_factor=1.4), Indicate(eq[0]), run_time=0.8)
        self.at(9.4, FadeOut(v), *[m.animate.set_color(WHITE) for m in (a, b, c)], rt=0.5)
        # build the next row by addition only
        row5 = VGroup(*[num(comb(5, k), color=K_COL if 0 < k < 5 else WHITE) for k in range(6)])
        for k, m in enumerate(row5):
            m.move_to(np.array([(k - 2.5) * DX, tri[4][0].get_y() - DY, 0]))
        t0 = 11.0
        for k in range(6):
            if k in (0, 5):
                self.at(t0, FadeIn(row5[k], shift=DOWN * 0.15), rt=0.5)
                t0 += 0.6
            else:
                vv = vee(tri[4][k - 1], tri[4][k], row5[k], col=K_COL, w=2.5)
                self.at(t0, *[GrowArrow(x) for x in vv], rt=0.45)
                self.play(FadeIn(row5[k], scale=1.3), FadeOut(vv), run_time=0.45)
                t0 += 1.05
        self.at(17.9, Indicate(VGroup(eq, box), color=HL, scale_factor=1.05), rt=1.2)
        self.end_clip(pad=0.2)
        self.play(FadeOut(VGroup(eq, box, row5)), FadeOut(self.head), run_time=0.8)
        self.head = pattern_heading(self, "Pattern 3")

    # ============================================================ s10  Pattern 3
    def s10(self):
        tri = self.tri
        self.clip("p4_10")
        self.at(0.3, tri.animate.move_to(LEFT * 2.4 + UP * 0.15), rt=1.0)

        def rbox(n, col=HL):
            return SurroundingRectangle(tri[n], color=col, buff=0.12, corner_radius=0.1)

        def sum_tex(n, total):
            parts = []
            for k in range(n + 1):
                if k:
                    parts.append("+")
                parts.append(str(comb(n, k)))
            parts += ["=", str(total)]
            t = MathTex(*parts).scale(0.9)
            t[-1].set_color(HL)
            t.next_to(tri[n], RIGHT, buff=1.0)
            t.set_y(tri[n].get_y())
            return t

        b3 = rbox(3)
        self.at(5.7, Create(b3), rt=0.7)
        self.play(LaggedStart(*[Indicate(m, scale_factor=1.3) for m in tri[3]], lag_ratio=0.25), run_time=1.6)
        s3 = sum_tex(3, 8)
        nums3 = [s3[2 * k] for k in range(4)]
        self.at(9.6, *[TransformFromCopy(tri[3][k], nums3[k]) for k in range(4)], rt=1.0)
        self.play(*[FadeIn(s3[2 * k + 1]) for k in range(3)], run_time=0.8)
        self.at(14.0, Write(s3[-2:]), rt=0.8)
        b4 = rbox(4)
        self.at(16.4, ReplacementTransform(b3, b4), rt=0.7)
        self.play(LaggedStart(*[Indicate(m, scale_factor=1.3) for m in tri[4]], lag_ratio=0.25), run_time=1.8)
        s4 = sum_tex(4, 16)
        nums4 = [s4[2 * k] for k in range(5)]
        self.at(21.1, *[TransformFromCopy(tri[4][k], nums4[k]) for k in range(5)], rt=1.0)
        self.play(*[FadeIn(s4[2 * k + 1]) for k in range(4)], run_time=0.8)
        self.at(25.4, Write(s4[-2:]), rt=0.8)
        self.at(28.0, FadeOut(b4), rt=0.5)
        # 1, 2, 4, 8, 16, ...
        seqv = [1, 2, 4, 8, 16]
        seq = VGroup(*[MathTex(str(v), color=HL).scale(1.0) for v in seqv])
        for i, m in enumerate(seq):
            m.move_to(np.array([-3.0 + 1.5 * i, -2.95, 0]))
        dots_ = MathTex(r"\cdots", color=HL).move_to(np.array([-3.0 + 1.5 * 5, -2.95, 0]))
        for i, t in enumerate((30.6, 31.3, 32.0, 32.7, 33.4)):
            src = [None, None, None, s3[-1], s4[-1]][i]
            if src is not None:
                self.at(t, TransformFromCopy(src, seq[i]), rt=0.5)
            else:
                self.at(t, FadeIn(seq[i], shift=UP * 0.2), rt=0.5)
        self.at(34.0, FadeIn(dots_), rt=0.4)
        arcs = VGroup()
        for i in range(4):
            a = CurvedArrow(seq[i].get_top() + UP * 0.08, seq[i + 1].get_top() + UP * 0.08, angle=-PI / 2.2,
                            color=K_COL, stroke_width=2.5, tip_length=0.15)
            t = MathTex(r"\times 2", color=K_COL).scale(0.75).next_to(a, UP, buff=0.04)
            arcs.add(VGroup(a, t))
        self.at(35.0, LaggedStart(*[AnimationGroup(Create(g[0]), FadeIn(g[1])) for g in arcs], lag_ratio=0.5), rt=3.5)
        self.at(41.2, Indicate(VGroup(seq, dots_), color=HL, scale_factor=1.1), rt=1.0)
        self.end_clip()
        self.p3 = dict(s3=s3, s4=s4, seq=seq, dots=dots_, arcs=arcs)

    # ============================================================ s11  sum of a row, general
    def s11(self):
        tri, P = self.tri, self.p3
        self.clip("p4_11")
        self.play(FadeOut(VGroup(P["s3"], P["s4"], P["seq"], P["dots"], P["arcs"])),
                  tri.animate.scale(0.7).move_to(np.array([-5.0, 0.2, 0])), run_time=1.0)
        CX = 2.0
        rowl = MathTex("C(n,0)", ",", "C(n,1)", ",", "C(n,2)", ",", r"\dots", ",", "C(n,n)").scale(0.85)
        for i in (0, 2, 4, 8):
            rowl[i].set_color(K_COL)
        rowl.move_to(np.array([CX, 2.2, 0]))
        rb = SurroundingRectangle(tri[4], color=HL, buff=0.1, corner_radius=0.08)
        self.at(1.2, Create(rb), rt=0.7)
        for idx, t in zip((0, 2, 4, 6, 8), (3.6, 5.1, 6.6, 8.0, 8.8)):
            anims = [FadeIn(rowl[idx], shift=UP * 0.15)]
            if idx:
                anims.append(FadeIn(rowl[idx - 1]))
            self.at(t, *anims, rt=0.5)
        sm = MathTex("C(n,0)", "+", "C(n,1)", "+", "C(n,2)", "+", r"\cdots", "+", "C(n,n)").scale(0.85)
        for i in (0, 2, 4, 8):
            sm[i].set_color(K_COL)
        sm.move_to(np.array([CX, 1.2, 0]))
        for idx, t in zip((0, 2, 4, 6, 8), (12.9, 14.4, 16.2, 18.0, 19.2)):
            anims = [TransformFromCopy(rowl[idx], sm[idx])]
            if idx:
                anims.append(FadeIn(sm[idx - 1]))
            self.at(t, *anims, rt=0.6)
        th = MathTex("(A+B)^{n}", "=", r"\sum_{r=0}^{n}", "C(n,r)", "A^{n-r}", "B^{r}").scale(0.9)
        th[3].set_color(K_COL); th[4].set_color(A_COL); th[5].set_color(B_COL)
        th.move_to(np.array([CX, -0.35, 0]))
        self.at(21.8, FadeOut(rb), Write(th), rt=1.8)
        sub = MathTex("A = 1", ",", r"\;B = 1").scale(0.85).next_to(th, DOWN, buff=0.45)
        sub[0].set_color(A_COL); sub[2].set_color(B_COL)
        self.at(26.0, Indicate(th[0]), rt=0.8)
        self.at(29.0, FadeIn(sub[0], shift=UP * 0.15), rt=0.5)
        self.at(30.4, FadeIn(sub[1:], shift=UP * 0.15), rt=0.5)
        lhs = MathTex("(1+1)^{n}", "=", "2^{n}").scale(0.95)
        lhs[2].set_color(HL)
        lhs.move_to(np.array([CX - 2.6, -2.75, 0]))
        self.at(33.9, TransformFromCopy(th[0], lhs[0]), rt=1.0)
        self.at(36.5, Write(lhs[1]), Write(lhs[2]), rt=0.8)
        self.end_clip()
        self.s11d = dict(rowl=rowl, sm=sm, th=th, sub=sub, lhs=lhs)

    # ============================================================ s12
    def s12(self):
        D = self.s11d
        th, sm, lhs = D["th"], D["sm"], D["lhs"]
        self.clip("p4_12")
        ones = MathTex("1^{n-r}", r"\,1^{r}").scale(0.9)
        ones.move_to(VGroup(th[4], th[5])).align_to(th[4], LEFT)
        self.at(2.0, Indicate(VGroup(th[4], th[5]), color=HL), rt=1.0)
        self.at(6.0, ReplacementTransform(th[4], ones[0]), ReplacementTransform(th[5], ones[1]), rt=1.0)
        one = MathTex("1").scale(0.9).move_to(ones)
        self.at(9.3, ReplacementTransform(ones, one), rt=0.8)
        self.play(FadeOut(one), run_time=0.5)
        rhs = MathTex("=", "C(n,0)", "+", "C(n,1)", "+", "C(n,2)", "+", r"\cdots", "+", "C(n,n)").scale(0.8)
        for i in (1, 3, 5, 9):
            rhs[i].set_color(K_COL)
        rhs.next_to(lhs, RIGHT, buff=0.2)
        if rhs.get_right()[0] > 6.8:
            VGroup(lhs, rhs).shift(LEFT * (rhs.get_right()[0] - 6.8))
        self.at(12.0, Indicate(sm, color=K_COL, scale_factor=1.05), rt=1.0)
        self.at(14.4, *[TransformFromCopy(sm[i], rhs[i + 1]) for i in range(9)], FadeIn(rhs[0]), rt=1.6)
        F = MathTex("C(n,0)", "+", "C(n,1)", "+", r"\cdots", "+", "C(n,n)", "=", "2^{n}").scale(0.92)
        for i in (0, 2, 6):
            F[i].set_color(K_COL)
        F[8].set_color(HL)
        F.move_to(np.array([1.7, -1.2, 0]))
        keep = [self.tri, self.head, D["rowl"]]
        self.at(20.6, *[FadeOut(m) for m in self.mobjects if m not in keep and m not in set(lhs) | set(rhs)],
                *[ReplacementTransform(x, y) for x, y in zip(list(rhs[1:5]) + list(rhs[7:]), F[0:7])],
                FadeOut(rhs[5:7]), FadeOut(rhs[0]), FadeOut(lhs[0:2]),
                ReplacementTransform(lhs[2], F[8]), FadeIn(F[7]), rt=1.6)
        box = SurroundingRectangle(F, color=HL, buff=0.2, corner_radius=0.1)
        self.at(24.5, Create(box), rt=0.9)
        rb = SurroundingRectangle(self.tri[4], color=HL, buff=0.1, corner_radius=0.08)
        ar = Arrow(rb.get_right(), box.get_left(), buff=0.15, color=HL, stroke_width=3)
        self.at(28.0, Create(rb), rt=0.6)
        self.play(GrowArrow(ar), run_time=0.6)
        self.at(31.8, Indicate(F[8], color=HL, scale_factor=1.4), rt=1.0)
        self.end_clip()
        self.s12d = dict(F=F, box=box, rb=rb, ar=ar)

    # ============================================================ s13  visual doubling
    def s13(self):
        tri = self.tri
        self.clip("p4_13")
        keep = [tri, self.head]
        self.play(*[FadeOut(m) for m in self.mobjects if m not in keep],
                  tri.animate.scale(1 / 0.7).move_to(LEFT * 3.0 + UP * 0.15), run_time=1.0)
        EX, TX = -0.1, 3.9
        exprs, tots = [], []
        for n in range(5):
            y = tri[n][0].get_y()
            parts = []
            for k in range(n + 1):
                if k:
                    parts.append("+")
                parts.append(str(comb(n, k)))
            e = MathTex(*parts).scale(0.85)
            e.move_to(np.array([EX, y, 0]), aligned_edge=LEFT)
            e.set_y(y)
            t = MathTex("=", str(2 ** n)).scale(0.9)
            t[1].set_color(HL)
            t.move_to(np.array([TX, y, 0]))
            exprs.append(e); tots.append(t)
        cues = [(3.7, 3.9), (4.9, 7.0), (8.7, 11.6), (13.5, 17.2), (19.1, 23.4)]
        for n, (t1, t2) in enumerate(cues):
            e = exprs[n]
            nums = [e[2 * k] for k in range(n + 1)]
            self.at(t1, Indicate(tri[n], color=HL, scale_factor=1.1),
                    *[TransformFromCopy(tri[n][k], nums[k]) for k in range(n + 1)],
                    *[FadeIn(e[2 * k + 1]) for k in range(n)], rt=max(0.5, min(1.2, t2 - t1 - 0.4)))
            self.at(t2, Write(tots[n]), rt=0.6)
        arcs = VGroup()
        for n in range(4):
            a = CurvedArrow(tots[n][1].get_right() + RIGHT * 0.12, tots[n + 1][1].get_right() + RIGHT * 0.12,
                            angle=-PI / 1.6, color=K_COL, stroke_width=2.5, tip_length=0.14)
            lab = MathTex(r"\times 2", color=K_COL).scale(0.65).next_to(a, RIGHT, buff=0.08)
            arcs.add(VGroup(a, lab))
        self.at(25.4, LaggedStart(*[Indicate(t[1], color=HL, scale_factor=1.35) for t in tots], lag_ratio=0.4),
                rt=2.8)
        self.at(30.3, LaggedStart(*[AnimationGroup(Create(g[0]), FadeIn(g[1])) for g in arcs], lag_ratio=0.4),
                rt=2.0)
        pw = [MathTex(f"2^{{{n}}}", color=HL).scale(0.9).move_to(tots[n][1]) for n in range(5)]
        self.at(33.1, *[TransformMatchingShapes(tots[n][1], pw[n]) for n in range(5)], rt=1.2)
        self.play(*[Indicate(p, color=HL, scale_factor=1.3) for p in pw], run_time=0.8)
        self.end_clip()

    # ============================================================ s14  what we saw
    def s14(self):
        tri = self.tri
        self.clip("p4_14")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not tri],
                  tri.animate.move_to(DOWN * 0.2), run_time=1.0)
        # numbers -> C(n,k)
        cf = VGroup(*[VGroup(*[MathTex(f"C({n},{k})", font_size=30, color=K_COL).move_to(tri[n][k])
                               for k in range(n + 1)]) for n in range(5)])
        self.at(1.4, *[ReplacementTransform(tri[n][k].copy(), cf[n][k]) for n in range(5) for k in range(n + 1)],
                *[tri[n][k].animate.set_opacity(0) for n in range(5) for k in range(n + 1)], rt=1.2)
        self.at(3.9, *[FadeOut(cf[n][k]) for n in range(5) for k in range(n + 1)],
                *[tri[n][k].animate.set_opacity(1) for n in range(5) for k in range(n + 1)], rt=0.9)
        allv = VGroup()
        for n in range(2, 5):
            for k in range(1, n):
                allv.add(vee(tri[n - 1][k - 1], tri[n - 1][k], tri[n][k], col=K_COL, w=2.5))
        self.at(5.6, LaggedStart(*[AnimationGroup(*[GrowArrow(a) for a in v]) for v in allv], lag_ratio=0.3), rt=2.0)
        self.at(8.6, FadeOut(allv), rt=0.5)
        pw = VGroup(*[MathTex(f"2^{{{n}}}", color=HL).scale(0.8)
                      .move_to(np.array([3.6, tri[n][0].get_y(), 0])) for n in range(5)])
        self.at(10.4, LaggedStart(*[FadeIn(p, shift=LEFT * 0.2) for p in pw], lag_ratio=0.2), rt=1.6)
        self.at(15.3, FadeOut(pw), rt=0.6)
        top = self.tri_pos(0, 0, center=DOWN * 0.2) + UP * 0.65
        bl = self.tri_pos(4, 0, center=DOWN * 0.2) + LEFT * 0.85 + DOWN * 0.5
        br = self.tri_pos(4, 4, center=DOWN * 0.2) + RIGHT * 0.85 + DOWN * 0.5
        outline = Polygon(top, bl, br).set_stroke(A_COL, 2.5, 0.8).set_fill(A_COL, 0.06)
        glow = VGroup(*[outline.copy().set_fill(opacity=0).set_stroke(A_COL, w, o) for w, o in ((12, 0.12), (24, 0.05))])
        cols = [A_COL, HL, B_COL, K_COL, A_COL]
        self.at(17.0, Create(outline), rt=1.6)
        self.at(20.0, LaggedStart(*[r.animate.set_color(c) for r, c in zip(tri, cols)], lag_ratio=0.3), FadeIn(glow),
                rt=2.2)
        name = en("Pascal's Triangle", 50).set_color(WHITE).next_to(outline, DOWN, buff=0.3)
        if name.get_bottom()[1] < -3.7:
            VGroup(tri, outline, glow).shift(UP * 0.45)
            name.next_to(outline, DOWN, buff=0.3)
        self.at(27.9, FadeIn(name, shift=UP * 0.2, scale=1.1), rt=1.0)
        self.end_clip(pad=0.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)

    # ============================================================ Summary
    def node(self, label, i):
        x = -5.1 + 3.4 * i
        if isinstance(label, str):
            t = en(label, 26)
        else:
            t = label
        if t.width > 2.6:
            t.scale_to_fit_width(2.6)
        box = RoundedRectangle(width=3.0, height=0.85, corner_radius=0.15).set_stroke(A_COL, 2).set_fill(A_COL, 0.08)
        g = VGroup(box, t.move_to(box)).move_to(np.array([x, 2.45, 0]))
        return g

    def s15(self):
        self.clip("p4_15")
        hdr = en("Summary", 30).set_color(SOFT).move_to(UP * 3.5)
        self.at(0.4, FadeIn(hdr, shift=DOWN * 0.2), rt=0.8)
        self.nodes = [self.node("Combination", 0), self.node("Binomial Theorem", 1),
                      self.node(MathTex("A_1A_2A_3,\\ B_1B_2B_3", font_size=30), 2),
                      self.node("Pascal's Triangle", 3)]
        self.nodes[2][1][0][0:6].set_color(A_COL); self.nodes[2][1][0][7:].set_color(B_COL)
        self.links = [Arrow(self.nodes[i].get_right(), self.nodes[i + 1].get_left(), buff=0.06, color=SOFT,
                            stroke_width=3, max_tip_length_to_length_ratio=0.35) for i in range(3)]
        self.at(4.7, Create(self.nodes[0][0]), Write(self.nodes[0][1]), rt=1.0)
        dots = VGroup(*[dot() for _ in range(7)]).arrange(RIGHT, buff=0.35).move_to(UP * 0.6)
        bN = Brace(dots, DOWN, buff=0.12, color=SOFT)
        tN = MathTex("N", color=SOFT).scale(0.8).next_to(bN, DOWN, buff=0.06)
        self.at(6.6, LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.1), GrowFromCenter(bN), FadeIn(tN),
                rt=1.2)
        sel = [0, 2, 3, 5]
        tM = MathTex("M", color=HL).scale(0.8)
        self.play(*[dots[i].animate.set_fill(HL, 0.9).set_stroke(HL) for i in sel], run_time=0.6)
        tM.next_to(dots, UP, buff=0.15)
        self.play(FadeIn(tM), run_time=0.3)
        f = MathTex(r"C(N,M)", "=", r"\frac{N(N-1)(N-2)\cdots(N-M+1)}{M!}").scale(0.95)
        f[0].set_color(K_COL)
        f.move_to(DOWN * 1.9)
        self.at(11.5, Write(f[0:2]), rt=0.8)
        self.play(Write(f[2]), run_time=3.2)
        self.at(16.4, Circumscribe(f[2], color=HL, fade_out=True), rt=1.4)
        self.at(21.5, GrowArrow(self.links[0]), Create(self.nodes[1][0]), Write(self.nodes[1][1]), rt=1.0)
        th = MathTex("(A+B)^{n}", "=", r"\sum_{r=0}^{n}", "C(n,r)", "A^{n-r}", "B^{r}").scale(0.9)
        th[3].set_color(K_COL); th[4].set_color(A_COL); th[5].set_color(B_COL)
        self.at(23.1, FadeOut(VGroup(dots, bN, tN, tM)), f.animate.scale(0.7).move_to(np.array([-3.3, 0.3, 0])), rt=0.9)
        th.move_to(np.array([3.1, -1.4, 0]))
        self.play(Write(th), run_time=1.4)
        cb = SurroundingRectangle(th[3], color=K_COL, buff=0.08)
        ar = CurvedArrow(f[0].get_bottom() + DOWN * 0.1, cb.get_left() + LEFT * 0.05, angle=PI / 3, color=K_COL,
                         stroke_width=3, tip_length=0.18)
        self.at(25.8, Create(cb), Create(ar), rt=1.0)
        self.end_clip()
        self.sd = dict(hdr=hdr, f=f, th=th, cb=cb, ar=ar)

    def s16(self):
        S = self.sd
        self.clip("p4_16")
        self.at(0.4, FadeOut(VGroup(S["f"], S["ar"], S["cb"], S["th"])), GrowArrow(self.links[1]),
                Create(self.nodes[2][0]), Write(self.nodes[2][1]), rt=1.0)
        fac = MathTex("(A_1+B_1)", "(A_2+B_2)", "(A_3+B_3)").scale(0.9).move_to(UP * 0.9)
        self.at(3.0, Write(fac), rt=1.4)
        terms = VGroup(*[MathTex(*[f"{c}_{{{i + 1}}}" for i, c in enumerate(s)]) for s in ("AAB", "ABA", "BAA")])
        for t, s in zip(terms, ("AAB", "ABA", "BAA")):
            for m, c in zip(t, s):
                m.set_color(A_COL if c == "A" else B_COL)
        terms.arrange(RIGHT, buff=0.6).scale(0.9).move_to(UP * 0.0)
        self.at(6.5, LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in terms], lag_ratio=0.3), rt=1.4)
        bt = Brace(terms, DOWN, buff=0.12, color=SOFT)
        ct = MathTex("3", "=", "C(3,1)").scale(0.85).next_to(bt, DOWN, buff=0.08)
        ct[2].set_color(K_COL); ct[0].set_color(HL)
        self.at(9.6, GrowFromCenter(bt), FadeIn(ct), rt=0.9)
        # positions: n slots, r of them B
        self.at(12.9, FadeOut(VGroup(fac, terms, bt, ct)), rt=0.6)
        slots = VGroup(*[Square(0.5).set_stroke(SOFT, 2) for _ in range(6)]).arrange(RIGHT, buff=0.12).move_to(UP * 0.4)
        bsel = [1, 4]
        for i in bsel:
            slots[i].set_fill(B_COL, 0.85).set_stroke(B_COL)
        bl = VGroup(*[MathTex("B", color=BG).scale(0.7).move_to(slots[i]) for i in bsel])
        bn_ = Brace(slots, DOWN, buff=0.12, color=SOFT)
        tn = MathTex("n", color=SOFT).scale(0.8).next_to(bn_, DOWN, buff=0.06)
        cnr = MathTex("C(n,r)", color=K_COL).scale(1.2).move_to(DOWN * 1.9)
        self.play(LaggedStart(*[Create(s) for s in slots], lag_ratio=0.1), GrowFromCenter(bn_), FadeIn(tn), run_time=1.2)
        self.at(15.0, Write(cnr), rt=0.9)
        rl = MathTex("r", color=B_COL).scale(0.8).next_to(slots, UP, buff=0.15)
        self.at(16.8, LaggedStart(*[FadeIn(b, scale=1.4) for b in bl], lag_ratio=0.4), FadeIn(rl), rt=1.0)
        self.at(19.0, Circumscribe(cnr, color=HL, fade_out=True), rt=1.2)
        self.at(21.3, FadeOut(VGroup(slots, bl, bn_, tn, rl, cnr)), GrowArrow(self.links[2]),
                Create(self.nodes[3][0]), Write(self.nodes[3][1]), rt=1.0)
        mini = VGroup(*[VGroup(*[num(comb(n, k), size=40) for k in range(n + 1)]) for n in range(5)])
        for n in range(5):
            for k in range(n + 1):
                mini[n][k].move_to(np.array([(k - n / 2) * 0.9, -n * 0.72, 0]))
        mini.move_to(DOWN * 0.9)
        self.at(23.2, LaggedStart(*[FadeIn(r, shift=DOWN * 0.15) for r in mini], lag_ratio=0.35), rt=2.2)
        self.at(26.0, Indicate(self.nodes[3], color=HL, scale_factor=1.05), rt=1.0)
        self.end_clip()
        self.mini = mini

    def s17(self):
        mini = self.mini
        self.clip("p4_17")
        self.at(0.5, mini.animate.scale(0.9).move_to(np.array([-4.2, -1.0, 0])), rt=1.0)
        c1 = MathTex("C(n,r)", "=", "C(n-1,\\,r-1)", "+", "C(n-1,\\,r)").scale(0.85)
        c1[0].set_color(K_COL); c1[2].set_color(HL); c1[4].set_color(B_COL)
        c2 = MathTex("C(n,0)", "+", "C(n,1)", "+", r"\cdots", "+", "C(n,n)", "=", "2^{n}").scale(0.85)
        for i in (0, 2, 6):
            c2[i].set_color(K_COL)
        c2[8].set_color(HL)
        c1.move_to(np.array([2.3, 0.0, 0])); c2.move_to(np.array([2.3, -2.0, 0]))
        k1 = SurroundingRectangle(c1, color=SOFT, buff=0.25, corner_radius=0.12)
        k2 = SurroundingRectangle(c2, color=SOFT, buff=0.25, corner_radius=0.12)
        n1 = en("1", 26).set_color(HL).next_to(k1, LEFT, buff=0.2)
        n2 = en("2", 26).set_color(HL).next_to(k2, LEFT, buff=0.2)
        v = vee(mini[3][1], mini[3][2], mini[4][2], col=K_COL, w=2.5)
        self.at(4.6, *[GrowArrow(a) for a in v], mini[4][2].animate.set_color(K_COL), rt=0.9)
        self.at(9.3, Create(k1), FadeIn(n1), rt=0.6)
        self.play(Write(c1), run_time=2.4)
        rb = SurroundingRectangle(mini[4], color=HL, buff=0.08, corner_radius=0.06)
        self.at(17.2, FadeOut(v), mini[4][2].animate.set_color(WHITE), Create(rb), rt=0.8)
        self.at(19.0, Create(k2), FadeIn(n2), rt=0.6)
        self.play(Write(c2[:8]), run_time=1.6)
        self.at(21.7, Write(c2[8]), rt=0.6)
        self.play(Indicate(c2[8], color=HL, scale_factor=1.4), run_time=0.8)
        self.end_clip(pad=0.4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)

    def s18(self):
        self.clip("p4_18")
        core = en("Binomial Theorem", 40)
        cbox = SurroundingRectangle(core, color=HL, buff=0.3, corner_radius=0.15)
        cg = VGroup(cbox, core).move_to(UP * 0.3)
        glow = VGroup(*[cbox.copy().set_stroke(HL, w, o) for w, o in ((10, 0.15), (22, 0.06))])
        self.at(0.4, Create(cbox), Write(core), rt=1.2)
        self.play(FadeIn(glow), run_time=0.6)
        sats = []
        for name, pos, t in (("Calculus", np.array([-4.3, 2.4, 0]), 5.4), ("Combination", np.array([4.3, 2.4, 0]), 6.7),
                             ("Statistics", np.array([0, -2.6, 0]), 8.0)):
            s = en(name, 32).set_color(SOFT).move_to(pos)
            ln = Line(cg.get_center(), pos).set_stroke(SOFT, 1.5, 0.6)
            ln.put_start_and_end_on(cbox.get_boundary_point(normalize(pos - cg.get_center())) if False else
                                    cg.get_center() + (pos - cg.get_center()) * 0.28,
                                    pos - (pos - cg.get_center()) * 0.18)
            self.at(t, Create(ln), FadeIn(s, scale=0.8), rt=0.7)
            sats.append(VGroup(ln, s))
        # Newton and pi
        self.at(10.2, FadeOut(VGroup(*sats)), VGroup(cg, glow).animate.scale(0.7).move_to(UP * 3.1), rt=1.0)
        newton = en("Isaac Newton", 34).set_color(B_COL).move_to(UP * 1.8)
        self.at(11.6, FadeIn(newton, shift=UP * 0.2), rt=0.8)
        series = MathTex(r"\pi", "=", r"\frac{3\sqrt{3}}{4}", "+", r"24\left(\frac{1}{12}-\frac{1}{5\cdot 2^{5}}"
                         r"-\frac{1}{28\cdot 2^{7}}-\frac{1}{72\cdot 2^{9}}-\cdots\right)").scale(0.85)
        series[0].set_color(HL)
        series.move_to(UP * 0.4)
        self.at(14.2, Write(series), rt=2.4)
        digits = MathTex(r"\pi \approx", r"3.", *list("14159265358979")).scale(0.95)
        digits[0].set_color(HL)
        digits.move_to(DOWN * 1.1)
        self.at(17.2, FadeIn(digits[0:2]), rt=0.4)
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.1) for d in digits[2:]], lag_ratio=0.12), run_time=1.8)
        bd = Brace(digits[1:], DOWN, buff=0.1, color=SOFT)
        bt = MathTex("15", color=SOFT).scale(0.7).next_to(bd, DOWN, buff=0.06)
        self.play(GrowFromCenter(bd), FadeIn(bt), run_time=0.6)
        bin_ = MathTex(r"(1-x)^{\frac{1}{2}}", "=", "1", r"-\frac{1}{2}x", r"-\frac{1}{8}x^{2}", r"-\frac{1}{16}x^{3}",
                       r"-\cdots").scale(0.8)
        bin_[0].set_color(A_COL)
        bin_.move_to(DOWN * 2.9)
        self.at(20.3, Write(bin_), rt=1.6)
        a1 = Arrow(cg.get_bottom() + LEFT * 2.6, bin_.get_left() + LEFT * 0.1, buff=0.1, color=HL, stroke_width=2.5,
                   path_arc=0.9) if False else None
        self.at(22.3, Indicate(VGroup(cg), color=HL, scale_factor=1.08), Circumscribe(bin_, color=HL, fade_out=True),
                rt=1.4)
        self.end_clip(pad=0.3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)

    def s19(self):
        self.clip("p4_19")
        chain = VGroup(en("Combination", 34), MathTex(r"\rightarrow", color=SOFT),
                       en("Binomial Theorem", 34), MathTex(r"\rightarrow", color=SOFT),
                       en("Pascal's Triangle", 34)).arrange(RIGHT, buff=0.35)
        chain[0].set_color(A_COL); chain[2].set_color(HL); chain[4].set_color(B_COL)
        chain.move_to(UP * 0.3)
        self.at(0.4, LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in chain], lag_ratio=0.35), rt=2.4)
        ul = Line(chain.get_left(), chain.get_right()).next_to(chain, DOWN, buff=0.3)
        ul.set_stroke(width=2).set_color([BG, A_COL, HL, A_COL, BG])
        self.at(5.2, GrowFromCenter(ul), rt=1.0)
        self.at(10.0, FadeOut(VGroup(chain, ul), shift=UP * 0.3), rt=0.8)
        bye = bn("আল্লাহ হাফেজ", 64)
        g = VGroup()
        self.at(11.3, FadeIn(bye, scale=1.15), FadeIn(g), rt=1.0)
        self.end_clip(pad=1.5)
        self.play(FadeOut(VGroup(bye, g)), run_time=1.0)
        self.outro()

    def channel_mark(self):
        if LOGO_FILE.exists():
            img = ImageMobject(str(LOGO_FILE)).set_height(2.2)
            name = en(CHANNEL_NAME, 40, color=SOFT).next_to(img, DOWN, buff=0.35)
            return Group(img, name).move_to(ORIGIN)
        ring = Circle(radius=1.0, stroke_color=A_COL, stroke_width=4)
        dots = VGroup()
        for n in range(4):
            for k in range(n + 1):
                dots.add(Dot(np.array([(k - n / 2) * 0.36, 0.5 - n * 0.33, 0]), radius=0.07,
                             color=[HL, A_COL, B_COL, K_COL][n]))
        name = en(CHANNEL_NAME, 40, color=SOFT).next_to(ring, DOWN, buff=0.35)
        return VGroup(ring, dots, name).move_to(ORIGIN)

    def outro(self):
        """channel name + 5 s music sting, then the video ends"""
        self.add_sound(str(AUDIO / "music_outro.wav"))
        mark = self.channel_mark()
        self.play(FadeIn(mark, scale=0.9), run_time=1.0)
        self.wait(2.6)
        self.play(FadeOut(mark), run_time=1.4)
