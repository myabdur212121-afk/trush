"""buffon_needles — scene/construct অংশ। lib অংশ: paper_lib.py"""
from manim import *
from year2026.buffon_needles.paper_lib import *


class BuffonNeedlesScene(Scene):
    def construct(self):
        paper = Paper()
        lines = paper.add_lines()
        grid = paper.add_grid()
        dots = grid.random_points(points=50, color=BLACK)
        self.add(paper, lines, grid, dots)
        self.wait(3)
