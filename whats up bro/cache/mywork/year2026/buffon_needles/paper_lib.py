"""
paper_lib — নোটবুক-পেপার স্টাইল chart toolkit
Updated v2.4 | 2026-09-07  (add_needles: layout param + random_layout — save/replay)

Logical inheritance map:
    manim.Rectangle   + PaperOps       -> Paper
    manim.Axes        + CoordinateOps  -> Axes
    manim.NumberPlane + CoordinateOps  -> NumberPlane

পুরনো নাম -> নতুন নাম:
    PublicOperation         -> PaperOps
    CordianteBasedOperation -> CoordinateOps
    "standart"              -> "standard"
"""

from typing import Literal

import numpy as np
from manim import *
from manim import Axes as _ManimAxes
from manim import NumberPlane as _ManimNumberPlane


class CoordinateOps:
    """Axes/NumberPlane-এর mixin: random point / angle / needle tools।"""

    def _sample_coords(self, n, x_range=None, y_range=None, buff=0.0):
        """n টা random (x, y) pair — object-এর coordinate space-এ (np.ndarray)।

        buff = border restriction (Munit): bbox থেকে চারদিকে buff ভিতরে।
        """
        if buff < 0:
            raise ValueError(f"buff must be >= 0, got {buff}")
        if buff > 0:
            x_min = self.p2c(self.get_left() + buff * RIGHT)[0]
            x_max = self.p2c(self.get_right() + buff * LEFT)[0]
            y_min = self.p2c(self.get_bottom() + buff * UP)[1]
            y_max = self.p2c(self.get_top() + buff * DOWN)[1]
        else:
            x_min, x_max = (x_range[0], x_range[1]) if x_range else (self.x_range[0], self.x_range[1])
            y_min, y_max = (y_range[0], y_range[1]) if y_range else (self.y_range[0], self.y_range[1])
        if not (x_min < x_max and y_min < y_max):
            raise ValueError(f"buff={buff} অনেক বড় — sampling area নেই। ছোট buff দিন।")
        xs = np.random.uniform(x_min, x_max, n)
        ys = np.random.uniform(y_min, y_max, n)
        return np.column_stack([xs, ys])

    def random_layout(self, n, x_range=None, y_range=None, buff=0.0, degrees=False):
        """[[[x, y], angle], ...] — save/replay করার মতো পুরো layout data।

        degrees=True হলে angle গুলো degree-এ (float), নাহলে radians-এ।
        পরে add_needles(layout=...) দিয়ে হুবহু same layout ফেরানো যায়।
        """
        pts = self._sample_coords(n, x_range, y_range, buff)
        angs = self.random_angles(n)
        if degrees:
            angs = np.degrees(angs)
        return [[p.tolist(), float(a)] for p, a in zip(pts, angs)]

    def _place_from_data(self, prototype, data, degrees, buff):
        """data = [[(x,y), angle], ...] থেকে needles বসায় → VGroup।"""
        group = VGroup()
        for pt, ang in data:
            a = np.radians(ang) if degrees else ang
            m = prototype.copy()
            m.move_to(self.c2p(*pt))
            m.rotate(a)
            group.add(m)
        self.needles = group
        self.angles = np.array([np.radians(a) if degrees else a for _, a in data])
        return group

    def random_point(self, x_range=None, y_range=None, buff=0.0, **kwargs):
        """একটা random Dot — default range = object-এর নিজের range।

        buff = border restriction (Munit): পুরো object-এর bbox থেকে চারদিক
        (উপর, নিচ, বাম, ডান) buff পরিমাণ ভিতরে ঢুকে অদৃশ্য ছোট area-তে
        point পড়ে। buff=0 (default) = আগের মতো পুরো area।
        """
        x, y = self._sample_coords(1, x_range, y_range, buff)[0]
        kwargs.setdefault("color", BLACK)
        return Dot(self.c2p(x, y), **kwargs)

    def random_points(self, points=10, **kwargs):
        """points সংখ্যক random Dot-এর VGroup; self.dots-এও save হয়।"""
        self.dots = VGroup(*(self.random_point(**kwargs) for _ in range(points)))
        return self.dots

    def random_angles(self, angles=10, min_angle=0.0, max_angle=TAU):
        """angles সংখ্যক random angle (radians) — np.ndarray (float)।"""
        if min_angle > max_angle:
            raise ValueError(f"min_angle ({min_angle}) > max_angle ({max_angle})")
        return np.random.uniform(min_angle, max_angle, angles)

    def add_needles(self, shape=None, needles=10, length=1.0, buff=None,
                    min_angle=0.0, max_angle=TAU, rotation=0.0,
                    color_by_gradient=None, layout=None, degrees=False, **kwargs):
        """Needles বসায় → VGroup। দুই mode:

        RANDOM mode (layout=None): random position + random rotation।
        CUSTOM mode (layout=[[ (x,y), angle ], ...]): হুবহু সেই data থেকে
        বসায় — random_layout() দিয়ে save করে পরের render-এ same layout।

        shape   = prototype Mobject (SVG / Image / VMobject / …);
                  None → ``length`` লম্বার classic Line needle।
        needles = কতটা needle (random mode)।
        buff    = border restriction; None → auto = shape-এর half-diagonal
                  (যেকোনো rotation-এ needle পুরো ভিতরে থাকবে)।
        rotation = base angle (radians): প্রতিটা needle-এর random angle-এর
                  সাথে যোগ হয় — সব needle ঘোরানো ভঙ্গিতে বসবে।
        color_by_gradient = color-এর list, যেমন [RED, BLUE] বা
                  ["#8f959c", "#f2f5f8"] → needles-এ gradient fill।
        layout  = custom [[(x, y), angle], ...] data (random-এর বদলে)।
        degrees = True হলে layout-এর angle গুলো degree-এ।
        **kwargs = prototype-এর style (color, stroke_width, …)।
        self.needles ও self.angles-এও save হয়।
        """
        prototype = shape.copy() if shape is not None else Line(ORIGIN, RIGHT * length)
        if color_by_gradient:
            prototype.set_fill(color=list(color_by_gradient))
            prototype.set_stroke(color=list(color_by_gradient))
        if kwargs:
            prototype.set(**kwargs)
        if buff is None:
            buff = np.hypot(prototype.width, prototype.height) / 2
        if layout is not None:
            return self._place_from_data(prototype, layout, degrees, buff)
        coords = self._sample_coords(needles, buff=buff)
        angles = self.random_angles(needles, min_angle, max_angle) + rotation
        group = VGroup()
        for (x, y), ang in zip(coords, angles):
            m = prototype.copy()
            m.move_to(self.c2p(x, y))
            m.rotate(ang)
            group.add(m)
        self.needles = group
        self.angles = angles
        return group


class PaperOps:
    """Rectangle/Paper-এর mixin: axes, grid, ruled lines, vertex labels।"""

    @staticmethod
    def _plot_center(coord):
        """Plot-area-র center — c2p anchor (bbox নয়, তাই shift-গ্লিচ নেই)।"""
        xm = (coord.x_range[0] + coord.x_range[1]) / 2
        ym = (coord.y_range[0] + coord.y_range[1]) / 2
        return coord.c2p(xm, ym)

    def add_axes(self, **kwargs):
        base = dict(
            x_range=[-5, 5, 1],
            y_range=[-10, 10, 1],
            x_length=self.width,
            y_length=self.height,
            axis_config={"color": BLACK, "include_tip": False},
        )
        base.update(kwargs)
        ax = Axes(**base)
        ax.shift(self.get_center() - self._plot_center(ax))
        return ax

    def add_grid(self, **kwargs):
        base = dict(
            x_range=[-5, 5, 1],
            y_range=[-10, 10, 1],
            x_length=self.width,
            y_length=self.height,
            axis_config={"color": BLACK, "include_tip": False},
        )
        base.update(kwargs)
        grid = NumberPlane(**base)
        grid.shift(self.get_center() - self._plot_center(grid))
        return grid

    def add_lines(self, lines=10, visual_lines=True, buff=0.2, **kwargs):
        """অনুভূমিক ruled lines; buff = কাগজের ধার থেকে ভিতরের দিকে ফাঁকা।"""
        kwargs.setdefault("color", BLACK)
        kwargs.setdefault("stroke_width", 1)
        left_x = self.get_left()[0] + buff
        right_x = self.get_right()[0] - buff
        ys = np.linspace(self.get_top()[1], self.get_bottom()[1], lines)
        group = VGroup(*(Line([left_x, y, 0], [right_x, y, 0], **kwargs) for y in ys))
        if visual_lines and len(group) > 2:
            group.remove(group[0], group[-1])  # প্রথম-শেষ line কাগজের edge-এর সাথে মিলে যেতো
        return group

    def show_vertices(self, vertex_index=None, position_scale_factor=1.2, **kwargs):
        """Vertex গুলো label করে; int / list / None তিনটাই চলে; যেকোনো অবস্থানে কাজ করে।"""
        verts = self.get_vertices()
        if vertex_index is None:
            chosen = list(range(len(verts)))
        elif isinstance(vertex_index, (int, np.integer)):
            chosen = [int(vertex_index)]
        else:
            chosen = [int(i) for i in vertex_index]
        center = self.get_center()
        labels = VGroup()
        for vi in chosen:
            target = center + (verts[vi] - center) * position_scale_factor
            try:
                label = MathTex(str(vi), **kwargs)
            except Exception:
                label = Text(str(vi), **kwargs)
            labels.add(label.move_to(target))
        self.add(labels)
        return labels


class Axes(_ManimAxes, CoordinateOps):
    """manim Axes + random point tools।"""


class NumberPlane(_ManimNumberPlane, CoordinateOps):
    """manim NumberPlane + random point tools।"""


class Paper(Rectangle, PaperOps):
    """নোটবুক-পেপার: cream fill + সঠিক aspect ratio (width = height × 9/11)।"""

    def __init__(self, mode: Literal["standard"] | None = "standard", **kwargs):
        self.mode = mode
        if mode == "standard":
            height = kwargs.get("height", 6)
            kwargs.setdefault("height", height)
            if "width" not in kwargs:
                kwargs["width"] = height * (9 / 11)
            kwargs.setdefault("fill_color", "#F8F5E9")
            kwargs.setdefault("fill_opacity", 1)
            kwargs.setdefault("stroke_color", "#3B3B3B")
        super().__init__(**kwargs)
