"""
window_viewport — মডুলার উইন্ডো এবং বাউন্ডারি ভিউপোর্ট টুলকিট (v1.0 | 2026-09-16)

মূল বৈশিষ্ট্য:
- ক্যাসকেডিং বাউন্ডারি হায়ারার্কি: Window ---> Axis ---> Shapes
- উইন্ডো ছাড়া সরাসরি দৃশ্যপটের অক্ষ: Axis ---> Shapes
- ডিফল্টভাবে অদৃশ্য অক্ষ (ক্লিন ড্যাশবোর্ড বা মনিটর লুক)
- হার্ডওয়্যার/ক্যামেরা লেভেল ক্লিপিং মাস্ক (জিরো ওভারল্যাপ গ্যারান্টি)

ব্যবহার:
    from manim import *
    from year2026.window_viewport.window import Window, BoundedPlane, ViewportScene

    class MyScene(ViewportScene):
        def construct(self):
            win = Window(width=5, height=4, x_range=[0, 100, 20], border_color=BLUE)
            circle = Circle(radius=1).move_to(win.c2p(50, 25))
            win.bind(circle)
            self.add(win, circle)
"""

from manim import *


class ClippedCamera(Camera):
    """
    ক্যামেরা লেভেলে স্টেনসিল মাস্ক প্রয়োগ করে।
    যেকোনো অবজেক্টের প্যারেন্ট Window বা BoundedPlane থাকলে, অবজেক্টটির ভিজ্যুয়াল
    শুধুমাত্র তার নির্দিষ্ট বাউন্ডিং বক্সের ভেতরেই সীমাবদ্ধ থাকবে।
    """
    def display_vectorized(self, vmobject: VMobject, ctx) -> Camera:
        owner = getattr(vmobject, "_bound_owner", None)
        if owner is not None and hasattr(owner, "get_bounding_box"):
            clip_box = owner.get_bounding_box()
            ctx.save()
            self.set_cairo_context_path(ctx, clip_box)
            ctx.clip()
            super().display_vectorized(vmobject, ctx)
            ctx.restore()
        else:
            super().display_vectorized(vmobject, ctx)
        return self


class BoundedPlane(NumberPlane):
    """
    স্বয়ংক্রিয় বাউন্ডারি সম্পন্ন কো-অর্ডিনেট প্লেন।
    - যদি কোনো Window-এর ভেতরে থাকে: Window-এর সীমানা উত্তরাধিকার সূত্রে গ্রহণ করে।
    - যদি সরাসরি সিনে থাকে: নিজের চারকোনা দৈর্ঘ্য-প্রস্থ অনুযায়ী সীমানা নির্ধারণ করে।
    """
    def __init__(self, **kwargs):
        kwargs.setdefault("x_range", [-10, 10, 1])
        kwargs.setdefault("y_range", [-10, 10, 1])
        kwargs.setdefault("x_length", 6)
        kwargs.setdefault("y_length", 6)
        super().__init__(**kwargs)
        self.window = None  # প্যারেন্ট Window-এর রেফারেন্স (যদি থাকে)

    def get_bounding_box(self) -> Rectangle:
        """লাইভ বাউন্ডিং বক্স রিটার্ন করে (মুভ বা ট্রান্সফর্ম হলেও সঠিক থাকে)।"""
        if self.window is not None:
            return self.window.get_bounding_box()
        box = Rectangle(
            width=self.x_length,
            height=self.y_length,
            stroke_width=0,
            fill_opacity=0
        )
        box.move_to(self.get_center())
        return box

    def bind(self, *mobjects):
        """মবজেক্টগুলোকে এই প্লেন বা এর প্যারেন্ট উইন্ডোর সাথে লক করে।"""
        target_owner = self.window if self.window is not None else self
        for mob in mobjects:
            for subm in mob.get_family():
                subm._bound_owner = target_owner
        return mobjects[0] if len(mobjects) == 1 else mobjects

    def plot(self, *args, **kwargs):
        """প্লট করা গ্রাফকে স্বয়ংক্রিয়ভাবে বাউন্ডারিতে লক করে।"""
        graph = super().plot(*args, **kwargs)
        self.bind(graph)
        return graph


class Window(VGroup):
    """
    স্বতন্ত্র চারকোনা উইন্ডো (Modular Viewport)।
    ভেতরে নিজস্ব লোকাল কো-অর্ডিনেট অক্ষ থাকে, যা ডিফল্টভাবে সম্পূর্ণ অদৃশ্য (লুকানো)।
    """
    def __init__(
        self,
        width=4.5,
        height=3.5,
        x_range=[-10, 10, 1],
        y_range=[-10, 10, 1],
        show_border=True,
        show_axes=False,
        border_color=BLUE,
        border_width=3,
        background_color="#101827",
        background_opacity=0.7,
        title="",
        **kwargs
    ):
        super().__init__()
        self.win_width = width
        self.win_height = height

        # ১. বাইরের ফ্রেম ও ব্যাকগ্রাউন্ড
        self.border = Rectangle(
            width=width,
            height=height,
            stroke_color=border_color,
            stroke_width=border_width if show_border else 0,
            fill_color=background_color,
            fill_opacity=background_opacity
        )
        self.add(self.border)

        # টাইটেল লেবেল (ঐচ্ছিক)
        if title:
            self.title_mob = Text(title, font_size=18, color=border_color)
            self.title_mob.next_to(self.border, UP, buff=0.15)
            self.add(self.title_mob)

        # ২. ভেতরের লোকাল কো-অর্ডিনেট সিস্টেম (ডিফল্টভাবে অক্ষ লুকানো)
        axis_stroke = 2 if show_axes else 0
        bg_stroke = 0.5 if show_axes else 0

        self.axis = BoundedPlane(
            x_range=x_range,
            y_range=y_range,
            x_length=width,
            y_length=height,
            axis_config={
                "stroke_color": GREY_A,
                "stroke_width": axis_stroke,
                "include_tip": False
            },
            background_line_style={
                "stroke_color": GREY_C,
                "stroke_width": bg_stroke
            }
        )
        # Window ---> Axis সংযোগ স্থাপন
        self.axis.window = self

        # অক্ষের উপাদানগুলোকেও উইন্ডো বর্ডারে বেঁধে দেওয়া
        for subm in self.axis.get_family():
            subm._bound_owner = self

        self.add(self.axis)

    def get_bounding_box(self) -> Rectangle:
        """উইন্ডোর লাইভ সেন্টার অনুযায়ী বাউন্ডিং বক্স গণনা করে।"""
        box = Rectangle(
            width=self.win_width,
            height=self.win_height,
            stroke_width=0,
            fill_opacity=0
        )
        box.move_to(self.border.get_center())
        return box

    def c2p(self, *coords):
        """উইন্ডোর লোকাল কো-অর্ডিনেটকে স্ক্রিন পয়েন্টে রূপান্তর করে।"""
        return self.axis.c2p(*coords)

    def p2c(self, point):
        """স্ক্রিন পয়েন্টকে উইন্ডোর লোকাল কো-অর্ডিনেটে রূপান্তর করে।"""
        return self.axis.p2c(point)

    def plot(self, *args, **kwargs):
        """উইন্ডোর ভেতরের স্কেল অনুযায়ী গ্রাফ আঁকে এবং অটো-লক করে।"""
        graph = self.axis.plot(*args, **kwargs)
        self.bind(graph)
        return graph

    def bind(self, *mobjects):
        """যেকোনো মবজেক্টকে উইন্ডোর চারকোনা সীমানায় কঠোরভাবে লক করে।"""
        for mob in mobjects:
            for subm in mob.get_family():
                subm._bound_owner = self
        return mobjects[0] if len(mobjects) == 1 else mobjects


class ViewportScene(Scene):
    """
    ক্লিপিং সুবিধা সক্রিয় সংবলিত মূল সিন ক্লাস।
    Scene এর পরিবর্তে এই ক্লাসটি ইনহেরিট করুন।
    """
    def __init__(self, **kwargs):
        kwargs["camera_class"] = ClippedCamera
        super().__init__(**kwargs)
