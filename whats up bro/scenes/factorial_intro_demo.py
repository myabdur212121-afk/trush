from manim import *

from animations import GrowWithBouncing
from scenes.factorial_scene import FactrioalScene


# Demo: শুধু ভিডিওর শুরুর অংশ (হুক থেকে প্রথম লোগো পর্যন্ত),
# যাতে ট্রায়াল ভয়েসটা বসিয়ে শোনা যায়।
class FactrioalIntroDemo(FactrioalScene):
    def construct(self):
        self.camera.background_color = "#050A12"
        self.camera.frame.save_state()
        self.hook_s1()
        self.hook_s2()
        self.hook_s3()
        self.wait(2.1)
        self.play(FadeIn(self.all_elements[0], shift=DOWN), run_time=1.2)
        self.wait(0.96)
        self.play(FadeIn(self.all_elements[1], shift=DOWN), run_time=1.1)
        self.wait(0.34)
        self.play(FadeIn(self.all_elements[2], shift=DOWN), run_time=1.1)
        self.play(LaggedStart(*[Create(rect) for rect in self.rects], lag_ratio=0.6), run_time=3.9)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)
        self.wait(1.4)
        self.play(GrowWithBouncing(self.factorial_sign, number_of_bounces=3))
        self.wait(1.08)
        self.play(ShrinkToCenter(self.factorial_sign))
        self.wait(0.82)
        self.play(self.camera.frame.animate.set_width(self.start_w).set_height(self.start_h).move_to(self.start_center), run_time=0.8)
        self.play(LaggedStart(*[Write(line, run_time=1) for line in self.lines],
                              lag_ratio=self.lag_ratio, rate_func=linear, run_time=3.6),
                  self.camera.frame.animate(rate_func=self.camera_sync).set_width(self.target_w).set_height(self.target_h).move_to(self.target_center),
                  run_time=3.6)
        self.wait(0.7)
        self.play(Restore(self.camera.frame, run_time=0.8), FadeOut(self.lines, run_time=0.8))
        self.wait(1.08)
        self.play(Write(self.n_text), run_time=4.6)
        self.wait(0.58)
        self.play(ApplyWave(self.n_text, amplitude=0.25, run_time=1.0))
        self.add(self.n_box)
        self.play(LaggedStart(*[FadeIn(q, scale=0.5, run_time=0.5) for q in self.questions], lag_ratio=0.18), run_time=2.6)
        self.wait(3.08)
        self.play(LaggedStart(*[FadeOut(q, scale=0.3, run_time=0.6) for q in self.questions], lag_ratio=0.06))
        self.play(FadeOut(self.n_text), FadeOut(self.n_box))
        self.wait(0.9)
        logo_front = self.show_logo(wait_time=2)
        self.play(FadeOut(logo_front))
