"""Build factorial_production.py from the repo scene.

Adds ONLY:
  * logo import + show_logo() (repo logo module, explode-assemble)
  * mid logo break + outro logo, exactly where the pasted version had them
  * mark(key): records scene time to $SCENE_MARKS_FILE (for audio placement)
  * pad(key): extra hold from $VOICE_PAD_FILE (so a voice clip fits its segment)
No animation/visual logic is otherwise changed.
"""
import pathlib
import sys

SRC = pathlib.Path("/home/user/1Fill2Blank/year2026/factorial/factorial_scene.py")
DST = pathlib.Path("/home/user/1Fill2Blank/year2026/factorial/factorial_production.py")
src = SRC.read_text(encoding="utf-8")


def sub(old: str, new: str) -> None:
    global src
    n = src.count(old)
    if n != 1:
        sys.exit(f"ANCHOR FAIL ({n}x): {old[:90]!r}...")
    src = src.replace(old, new, 1)


# 1) Imports + pads/marks config
sub(
    """try:
    from .grow_with_bouncing import GrowWithBouncing
except ImportError:
    from grow_with_bouncing import GrowWithBouncing
""",
    """try:
    from .grow_with_bouncing import GrowWithBouncing
except ImportError:
    from grow_with_bouncing import GrowWithBouncing

import json
import os

try:
    from year2026.logo.logo import Logo1Fill2Blank, logo_explode_assemble
except ImportError:  # pragma: no cover
    from my_1fill2blank import Logo1Fill2Blank, logo_explode_assemble

_PAD_FILE = os.environ.get("VOICE_PAD_FILE", "/home/user/production/pad.json")
_MARKS_FILE = os.environ.get("SCENE_MARKS_FILE", "/home/user/production/marks.json")


def _load_pads():
    try:
        with open(_PAD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


_VOICE_PADS = _load_pads()
""",
)

# 2) helper methods inside the class
sub(
    """    def camera_sync(self, alpha):""",
    '''    def _scene_time(self):
        try:
            vale = getattr(getattr(self, "renderer", None), "time", None)
            if vale is not None:
                return float(vale() if callable(vale) else vale)
        except Exception:
            pass
        try:
            vale = getattr(self, "time", None)
            return float(vale() if callable(vale) else vale)
        except Exception:
            return 0.0

    def mark(self, name):
        t = self._scene_time()
        data = {}
        if _MARKS_FILE and os.path.exists(_MARKS_FILE):
            try:
                with open(_MARKS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}
        data[name] = t
        try:
            folder = os.path.dirname(_MARKS_FILE)
            if folder:
                os.makedirs(folder, exist_ok=True)
            with open(_MARKS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
        print(f"[MARK] {name} @ {t:.3f}")
        try:
            self.next_section(name)
        except Exception:
            pass

    def pad(self, key):
        try:
            t = float(_VOICE_PADS.get(key, 0.0))
        except Exception:
            t = 0.0
        if t > 0.02:
            self.wait(t)

    def show_logo(self, wait_time=2):
        logo = Logo1Fill2Blank()
        logo.move_to(ORIGIN)
        logo_explode_assemble(self, logo, wait_time=wait_time)
        return logo

    def camera_sync(self, alpha):''',
)

# 3) construct start: clear old marks, mark S01
sub(
    """        self.hook_s7()""",
    """        self.hook_s7()
        if _MARKS_FILE and os.path.exists(_MARKS_FILE):
            try:
                os.remove(_MARKS_FILE)
            except Exception:
                pass
        self.mark("S01")""",
)

# S01 -> S02
sub(
    """        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])""",
    """        self.wait(2)
        self.pad("S01")
        self.mark("S02")
        self.play(*[FadeOut(mob) for mob in self.mobjects])""",
)

# S02 -> LOGO_MID
sub(
    """        self.play(LaggedStart(*[FadeIn(q, scale=0.5, run_time=0.5) for q in self.questions], lag_ratio=0.18))
        self.wait(1)
        self.play(LaggedStart(*[FadeOut(q, run_time=0.4) for q in self.questions], lag_ratio=0.06))""",
    """        self.play(LaggedStart(*[FadeIn(q, scale=0.5, run_time=0.5) for q in self.questions], lag_ratio=0.18))
        self.wait(1)
        self.pad("S02")
        self.mark("LOGO_MID")
        self.play(LaggedStart(*[FadeOut(q, run_time=0.4) for q in self.questions], lag_ratio=0.06))""",
)

# mid logo + S03 start
sub(
    """        self.play(FadeOut(self.n_text), FadeOut(self.n_box))
        self.wait(0.5)
        self.play(LaggedStart(*[FadeIn(player, scale=0.5) for player in self.players], lag_ratio=0.3))""",
    """        self.play(FadeOut(self.n_text), FadeOut(self.n_box))
        self.wait(0.5)
        logo_front = self.show_logo(wait_time=2)
        self.play(FadeOut(logo_front))
        self.mark("S03")
        self.play(LaggedStart(*[FadeIn(player, scale=0.5) for player in self.players], lag_ratio=0.3))""",
)

# S03 -> S04
sub(
    """        self.play(Create(self.bar_outline), FadeIn(self.bar_fill))""",
    """        self.play(Create(self.bar_outline), FadeIn(self.bar_fill))
        self.pad("S03")
        self.mark("S04")""",
)

# S04 -> S05
sub(
    """        self.play(Write(self.question_text))
        self.wait(1)
        self.play(Unwrite(self.question_text))""",
    """        self.play(Write(self.question_text))
        self.wait(1)
        self.pad("S04")
        self.mark("S05")
        self.play(Unwrite(self.question_text))""",
)

# S05 -> S06
sub(
    """        self.play(self.players[2].animate.move_to(self.blocks[2][0].get_center()), run_time=1)
        self.wait(1)
        self.play(FadeOut(self.players), FadeOut(self.blocks), *[FadeOut(n) for n in self.numbers])""",
    """        self.play(self.players[2].animate.move_to(self.blocks[2][0].get_center()), run_time=1)
        self.wait(1)
        self.pad("S05")
        self.mark("S06")
        self.play(FadeOut(self.players), FadeOut(self.blocks), *[FadeOut(n) for n in self.numbers])""",
)

# S06 -> S07
sub(
    """        self.play(Write(self.tree_equal))""",
    """        self.play(Write(self.tree_equal))
        self.pad("S06")
        self.mark("S07")""",
)

# S07 hold over the complete tree + 6 arrangements, BEFORE the equation
# assembles (narration is still describing the branches/six ways there)
sub(
    """        self.play(Write(self.tree_result))
        self.wait(0.5)""",
    """        self.play(Write(self.tree_result))
        self.wait(0.5)
        self.pad("S07")""",
)

# S07 -> S08
sub(
    """        self.play(LaggedStart(*[Indicate(row, scale_factor=1.15) for row in self.arrangements], lag_ratio=0.3))
        self.wait(0.5)""",
    """        self.play(LaggedStart(*[Indicate(row, scale_factor=1.15) for row in self.arrangements], lag_ratio=0.3))
        self.wait(0.5)
        self.mark("S08")""",
)

# S08 hold, S09 hold, outro logo
sub(
    """        self.play(ShowPassingFlash(self.final_frame, time_width=0.15), run_time=1.4)
        self.wait(1)""",
    """        self.play(ShowPassingFlash(self.final_frame, time_width=0.15), run_time=1.4)
        self.wait(1)
        self.pad("S08")
        self.mark("S09")
        self.pad("S09")
        self.mark("OUTRO")
        self.play(FadeOut(self.final_eq))
        self.show_logo(wait_time=3)
        self.mark("END")""",
)

DST.write_text(src, encoding="utf-8")
print("WROTE", DST, len(src.splitlines()), "lines")
