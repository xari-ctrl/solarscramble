#!/usr/bin/env python3
"""Solar Scramble - unscramble the cosmos, build your streak, reach the stars.

Terminal version of the Solar Scramble web game. Run with:  python3 solarscramble.py
Commands during a round: type your guess, "hint" for a hint (-2), or "quit" to exit.
"""
import json
import random
from pathlib import Path

WORDS = [
    ("mercury", "The smallest planet and closest to the Sun."),
    ("venus", "The hottest planet in our solar system."),
    ("earth", "The only known planet with life."),
    ("mars", "The red planet."),
    ("jupiter", "The largest planet in the solar system."),
    ("saturn", "This planet is famous for its rings."),
    ("uranus", "An ice giant that rotates on its side."),
    ("neptune", "The farthest major planet from the Sun."),
    ("asteroid", "A rocky object that orbits the Sun."),
    ("comet", "An icy object that can grow a glowing tail."),
    ("galaxy", "A huge collection of stars, gas, and dust."),
    ("orbit", "The curved path of one object around another."),
]
ROUNDS = 5
SCORES_FILE = Path(__file__).with_name("solarscramble_scores.json")


def scramble(word):
    letters = list(word)
    while True:
        random.shuffle(letters)
        mixed = "".join(letters)
        if mixed != word:
            return mixed


def load_scores():
    try:
        return json.loads(SCORES_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_score(name, score):
    scores = load_scores()
    scores.append({"name": name[:18], "score": score})
    scores.sort(key=lambda s: s["score"], reverse=True)
    SCORES_FILE.write_text(json.dumps(scores[:10], indent=2))


def show_leaderboard():
    scores = load_scores()
    print("\n=== Leaderboard ===")
    if not scores:
        print("No scores yet. Claim the first place.")
    for i, item in enumerate(scores[:5], 1):
        print(f"{i}. {item['name']} - {item['score']} pts")
    print()


def play():
    score = streak = 0
    for rnd in range(1, ROUNDS + 1):
        word, hint = random.choice(WORDS)
        hint_used = False
        print(f"\nRound {rnd}/{ROUNDS} | Score {score} | Streak {streak}")
        print("  " + " ".join(scramble(word).upper()))
        while True:
            guess = input("Your answer (or 'hint'/'quit'): ").strip().lower()
            if not guess:
                continue
            if guess == "quit":
                return None
            if guess == "hint":
                if hint_used:
                    print("Hint already used this round.")
                else:
                    hint_used = True
                    print(f"Hint: {hint}")
                continue
            if guess == word:
                streak += 1
                score += max(2, 10 - (2 if hint_used else 0) + streak * 2)
                print("Correct!")
                break
            streak = 0
            print("Not quite. Try again.")
    return score


def main():
    print("Solar Scramble\nUnscramble the cosmos, build your streak, reach the stars.")
    show_leaderboard()
    while True:
        score = play()
        if score is None:
            print("Goodbye, Astronaut!")
            return
        name = input(f"\nGame over! Your score is {score}. Enter your name: ").strip() or "Astronaut"
        save_score(name, score)
        show_leaderboard()
        if input("Play again? (y/n): ").strip().lower() != "y":
            return


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye, Astronaut!")
