from manim import * 
class NeedleWiggle(AnimationGroup):
    """প্রতিটা needle-কে angle_range-এর ভিতরে random angle-এ wiggle করায় —
    natural কাঁপুনি, কোনো mechanical ভাব নেই।

    n_wiggles   = প্রতি needle কতবার দুলবে
    angle_range = (min, max) — random wiggle angle-এর magnitude;
                  default radians, degrees=True হলে degree-এ
    run_time    = TOTAL সময়; প্রতি needle-এর wiggle সময় auto =
                  run_time / (1 + lag_ratio*(n-1)) — শেষ needle ঠিক সময়ে শেষ করে
    lag_ratio   = কতটা staggered (একটার পর একটা শুরু)
    scale_value = 1.0 = মাপ pulse বন্ধ; >1 দিলে Wiggle-এর দুলনির সাথে বড় হবে
    """

    def __init__(self, needles, n_wiggles=6, angle_range=(0.2, 0.6),
                 run_time=10, lag_ratio=0.1, scale_value=1.0,
                 degrees=False, **kwargs):
        if len(needles) == 0:
            raise ValueError("needles খালি — আগে add_needles() চালাও।")
        lo, hi = angle_range
        if degrees:
            lo, hi = np.radians(lo), np.radians(hi)
        if lo > hi:
            raise ValueError(f"angle_range-এর min ({lo}) > max ({hi})")
        n = len(needles)
        single = run_time / (1 + lag_ratio * max(n - 1, 1))
        anims = []
        for m in needles:
            mag = float(np.random.uniform(lo, hi)) * float(np.random.choice([1, -1]))
            anims.append(
                Wiggle(m, n_wiggles=n_wiggles, rotation_angle=mag,
                       scale_value=scale_value, run_time=single)
            )
        # group-এ আলাদা run_time দিই না — child-দের single সময় + manim-এর
        # নিজের lag rule (start_i = i*lag_ratio*single) মিলে total নিজে নিজেই
        # হুবহু run_time হয়; আলাদা দিলে হিসাব গড়বড় হয়
        super().__init__(*anims, lag_ratio=lag_ratio, **kwargs)
