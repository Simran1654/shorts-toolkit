"""Smoke tests for shorts-toolkit. Run: python3 -m unittest discover -s tests -v"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import title  # noqa: E402
import hookscore  # noqa: E402


class TitleTests(unittest.TestCase):
    def test_short_specific_title_scores_well(self):
        r = title.check("5 Mistakes That Kill Your Tomato Plants")
        self.assertEqual(r["issues"], [])
        self.assertGreaterEqual(r["score"], 90)

    def test_over_40_chars_flags_mobile_cut(self):
        r = title.check("I Fixed a Leaky Tap With a $1 Rubber Band")
        kinds = {k for k, _ in r["issues"]}
        self.assertIn("mobile", kinds)

    def test_vague_overlong_title_is_flagged(self):
        r = title.check("Amazing Incredible Ultimate Guide to Everything You Need to Know "
                        "About All the Best and Most Powerful Secrets Ever Revealed")
        kinds = {k for k, _ in r["issues"]}
        self.assertIn("vague", kinds)
        self.assertIn("length", kinds)

    def test_thumbnail_repeating_title_is_flagged(self):
        r = title.check("How to Change a Bike Tire in 4 Minutes", thumb="BIKE TIRE CHANGE")
        kinds = {k for k, _ in r["issues"]}
        self.assertIn("duplicate", kinds)


class HookTests(unittest.TestCase):
    def test_specific_hook_beats_filler_hook(self):
        _, strong, _, _ = hookscore.score(
            "97% of people strip the screw in the first 10 seconds. "
            "Here is the $1 tool that stops it.")
        _, weak, _, _ = hookscore.score(
            "Hey guys, welcome back to the channel, today we are going to be "
            "talking about some really amazing stuff.")
        self.assertGreater(strong, weak)

    def test_verdict_band_labels(self):
        self.assertEqual(hookscore.band(80), "STRONG")
        self.assertEqual(hookscore.band(60), "WORKABLE")
        self.assertEqual(hookscore.band(30), "WEAK")


if __name__ == "__main__":
    unittest.main()
