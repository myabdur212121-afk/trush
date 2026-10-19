"""GrowFromCenterBouncy-এর ধারাবাহিকতার পরীক্ষা।

চালানোর নিয়ম (সংগ্রহস্থলের চালানোর পরিবেশ দিয়ে):
    .venv দিয়ে: python -m unittest animations.test_grow_from_center_bouncy -v

যা যা যাচাই করা হয় (ভবিষ্যতে লেখা বদলালে ছেদ পড়লে এগুলো ব্যর্থ হবে):
  * শুরুতে আকার 0, শেষে ঠিক 1।
  * জোড়ার জায়গায় দুই পাশের মান সমান এবং গতি সমান (ছেদ নেই)।
  * বড় হওয়ার অংশে আকার শুধু বাড়ে, কখনো কমে না বা ঋণাত্মক হয় না।
  * দোলনের আকার নির্ধারিত সীমার বাইরে যায় না, শেষের গতি সামান্য।
"""

import math
import unittest

from animations.grow_from_center_bouncy import _growth_then_spring

CASES = [
    # (number_of_bounces, bounce_strength, resistance, grow_portion)
    (2, 0.12, 3.0, 0.4),
    (3, 0.12, 3.0, 0.4),
    (4, 0.12, 3.0, 0.4),
    (3, 0.08, 2.0, 0.3),
    (4, 0.20, 4.0, 0.5),
    (0, 0.12, 3.0, 0.4),
]


def rate(t, case):
    return _growth_then_spring(t, *case)


class TestContinuity(unittest.TestCase):
    def test_start_and_end(self):
        for case in CASES:
            with self.subTest(case=case):
                self.assertAlmostEqual(rate(0.0, case), 0.0, places=9)
                self.assertAlmostEqual(rate(1.0, case), 1.0, places=9)

    def test_join_value_and_velocity_match(self):
        eps = 1e-6
        for case in CASES:
            n, strength, _resistance, grow = case
            if n == 0:
                continue
            with self.subTest(case=case):
                left_value = rate(grow - eps, case)
                right_value = rate(grow + eps, case)
                self.assertAlmostEqual(left_value, right_value, delta=1e-4)
                left_velocity = (rate(grow, case) - rate(grow - 1e-4, case)) / 1e-4
                right_velocity = (rate(grow + 1e-4, case) - rate(grow, case)) / 1e-4
                self.assertAlmostEqual(left_velocity, right_velocity, delta=0.05)

    def test_growth_is_monotonic(self):
        for case in CASES:
            _n, _s, _r, grow = case
            with self.subTest(case=case):
                previous = 0.0
                for i in range(101):
                    value = rate(grow * i / 100, case)
                    self.assertGreaterEqual(value, previous - 1e-9)
                    self.assertGreaterEqual(value, 0.0)
                    self.assertLessEqual(value, 1.0 + 1e-9)
                    previous = value

    def test_spring_bounds_and_calm_end(self):
        for case in CASES:
            n, strength, _r, _g = case
            with self.subTest(case=case):
                values = [rate(i / 400, case) for i in range(401)]
                self.assertLessEqual(max(values), 1.0 + strength + 0.01)
                self.assertGreaterEqual(min(values), -0.01)
                end_velocity = abs(rate(1.0, case) - rate(0.999, case)) / 0.001
                self.assertLess(end_velocity, 0.6)


if __name__ == "__main__":
    unittest.main()
