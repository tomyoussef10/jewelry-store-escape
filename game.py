"""
Jewelry Store Escape: a choose-your-own-adventure game in Python.

Author: Thomas Youssef

Started as a CS 115 project at Stevens Institute of Technology and
rebuilt as a personal project. The story is stored as data (a graph of
scenes), so new scenes and endings can be added without changing the
game logic.
"""

import time

# Each scene has text and either choices (letter -> (label, next scene))
# or an ending ("escaped" or "caught").
STORY = {
    "start": {
        "text": "You just robbed a jewelry store. Alarms are ringing and police are on the way.",
        "choices": {
            "a": ("Walk out the front door", "front_door"),
            "b": ("Crawl through the air vents", "vents"),
            "c": ("Run up the stairs", "rooftop"),
        },
    },
    "front_door": {
        "text": "You step outside straight into the flashing lights of three police cars.",
        "ending": "caught",
    },
    "vents": {
        "text": "You squeeze into the vents. Ahead, the duct splits into three pathways.",
        "choices": {
            "a": ("Crawl left", "security_room"),
            "b": ("Crawl straight", "sewers"),
            "c": ("Crawl right", "rooftop"),
        },
    },
    "security_room": {
        "text": "You drop out of the vent into the security room, right in front of a guard.",
        "ending": "caught",
    },
    "sewers": {
        "text": "The vent drops you into the sewers. It's dark, and you hear sirens above.",
        "choices": {
            "a": ("Follow the tunnel toward the river", "river"),
            "b": ("Climb the nearest manhole ladder", "manhole"),
            "c": ("Hide and wait for the sirens to fade", "wait_sewers"),
        },
    },
    "river": {
        "text": "The tunnel opens onto the riverbank. You slip away into the night.",
        "ending": "escaped",
    },
    "manhole": {
        "text": "You push up the manhole cover in the middle of a police checkpoint.",
        "ending": "caught",
    },
    "wait_sewers": {
        "text": "Hours pass. The sirens fade, and you climb out on a quiet street.",
        "ending": "escaped",
    },
    "rooftop": {
        "text": "You burst onto the rooftop. A helicopter spotlight is sweeping the block.",
        "choices": {
            "a": ("Hop across the apartment buildings", "apartments"),
            "b": ("Climb down the fire escape", "fire_escape"),
            "c": ("Hide behind the air conditioning units", "ac_units"),
        },
    },
    "apartments": {
        "text": "You leap from roof to roof and disappear into an apartment stairwell.",
        "ending": "escaped",
    },
    "fire_escape": {
        "text": "You reach the alley just as a police dog rounds the corner.",
        "ending": "caught",
    },
    "ac_units": {
        "text": "The spotlight passes over you, but the guard dog upstairs doesn't miss your scent.",
        "ending": "caught",
    },
}


def all_endings(story=STORY):
    return [name for name, scene in story.items() if "ending" in scene]


def ask_for_choice(choices):
    """Keep asking until the player types one of the valid letters."""
    while True:
        answer = input("Type your choice and press <Enter>: ").strip().lower()
        if answer in choices:
            return answer
        print(f"Please type one of: {', '.join(choices)}")


def print_choices(choices):
    for letter, (label, _) in choices.items():
        print(f"  {letter}) {label}")


def play_once(story=STORY, delay=0.8):
    """Play one run of the story and return the name of the ending reached."""
    scene_name = "start"
    while True:
        scene = story[scene_name]
        print("\n" + scene["text"])
        time.sleep(delay)
        if "ending" in scene:
            if scene["ending"] == "escaped":
                print("Congrats! You escaped!")
            else:
                print("You got caught. Game over.")
            return scene_name
        print_choices(scene["choices"])
        letter = ask_for_choice(scene["choices"])
        scene_name = scene["choices"][letter][1]


def main():
    print("=== Escape from the Jewelry Store ===")
    found = set()
    total = len(all_endings())
    while True:
        found.add(play_once())
        print(f"\nYou have found {len(found)} of {total} endings.")
        if len(found) == total:
            print("You found every ending. Thanks for playing!")
            break
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            break


if __name__ == "__main__":
    main()
