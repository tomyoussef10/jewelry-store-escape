"""Unit tests for game.py. Run with: python -m unittest"""
import unittest
from unittest.mock import patch
from game import STORY, all_endings, play_once


def reachable_scenes(story):
    seen, stack = set(), ["start"]
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(name)
        for _, next_scene in story[name].get("choices", {}).values():
            stack.append(next_scene)
    return seen


class TestStoryStructure(unittest.TestCase):
    def test_every_choice_leads_to_a_real_scene(self):
        for name, scene in STORY.items():
            for label, next_scene in scene.get("choices", {}).values():
                self.assertIn(next_scene, STORY, f"{name} -> {label}")

    def test_every_scene_is_reachable(self):
        self.assertEqual(reachable_scenes(STORY), set(STORY))

    def test_every_scene_has_choices_or_an_ending(self):
        for name, scene in STORY.items():
            self.assertTrue(("choices" in scene) != ("ending" in scene), name)

    def test_story_has_both_kinds_of_endings(self):
        kinds = {STORY[name]["ending"] for name in all_endings()}
        self.assertEqual(kinds, {"escaped", "caught"})


class TestGameplay(unittest.TestCase):
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["b", "b", "a"])
    def test_vents_to_sewers_to_river(self, _input, _print):
        # This path crashed in the original version
        self.assertEqual(play_once(delay=0), "river")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["x", "", "C", "a"])
    def test_invalid_input_is_rejected_and_uppercase_works(self, _input, _print):
        self.assertEqual(play_once(delay=0), "apartments")


if __name__ == "__main__":
    unittest.main()
