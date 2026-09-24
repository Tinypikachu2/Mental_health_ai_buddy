"""A playful SpongeBob personality quiz.

Run with:
    python3 spongebob.py
"""

from __future__ import annotations

import random
import threading
import tkinter as tk
from io import BytesIO
from tkinter import ttk
from urllib.error import URLError
from urllib.request import Request, urlopen


try:
    from PIL import Image, ImageTk
except ImportError:  # Pillow is optional; the emoji fallback still works.
    Image = None
    ImageTk = None


QUESTIONS = [
    (
        "It’s your first day at the Krusty Krab. You...",
        [
            ("Flip patties with maximum enthusiasm!", "spongebob"),
            ("Make sure everyone feels welcome.", "patrick"),
            ("Ask when your lunch break is.", "squidward"),
            ("Find the best way to make a profit.", "mr_krabs"),
        ],
    ),
    (
        "Your perfect Saturday looks like...",
        [
            ("A surprise adventure with my besties!", "patrick"),
            ("Practicing a new skill until I nail it.", "spongebob"),
            ("A quiet day with music and no interruptions.", "squidward"),
            ("Counting my savings and finding a bargain.", "mr_krabs"),
        ],
    ),
    (
        "A friend is having a bad day. You...",
        [
            ("Show up with snacks and a ridiculous story.", "patrick"),
            ("Plan a whole cheer-up activity.", "spongebob"),
            ("Give them space, but secretly check in later.", "squidward"),
            ("Offer practical advice (for a small consulting fee).", "mr_krabs"),
        ],
    ),
    (
        "Pick a superpower:",
        [
            ("Unlimited optimism!", "spongebob"),
            ("Always knowing where the snacks are.", "patrick"),
            ("A force field of personal space.", "squidward"),
            ("Turning anything into a money-making opportunity.", "mr_krabs"),
        ],
    ),
    (
        "When plans go wrong, your reaction is...",
        [
            ("No worries—we can make a new plan!", "spongebob"),
            ("Maybe the wrong plan was more fun anyway.", "patrick"),
            ("I knew this would happen.", "squidward"),
            ("Who is paying for the damages?", "mr_krabs"),
        ],
    ),
]


RESULTS = {
    "spongebob": {
        "name": "SpongeBob SquarePants",
        "emoji": "🍍",
        "color": "#ffd84d",
        "tagline": "The Sunshine Sponge",
        "description": "You bring unstoppable energy, kindness, and a little bit of chaos to every room. Your laugh is basically a superpower!",
        "image": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/SpongeBob_SquarePants_character.svg/240px-SpongeBob_SquarePants_character.svg.png",
    },
    "patrick": {
        "name": "Patrick Star",
        "emoji": "⭐",
        "color": "#f39ab1",
        "tagline": "The Fun Friend",
        "description": "You are loyal, hilarious, and always ready for an adventure. Life is better when you bring the snacks and your best jokes.",
        "image": "https://upload.wikimedia.org/wikipedia/en/thumb/3/33/Patrick_Star.svg/240px-Patrick_Star.svg.png",
    },
    "squidward": {
        "name": "Squidward Tentacles",
        "emoji": "🎷",
        "color": "#9ed6c7",
        "tagline": "The Creative Introvert",
        "description": "You have excellent taste, hidden talents, and a strong appreciation for peace and quiet. Your artistic side is seriously underrated.",
        "image": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Squidward_Tentacles.svg/240px-Squidward_Tentacles.svg.png",
    },
    "mr_krabs": {
        "name": "Mr. Krabs",
        "emoji": "💰",
        "color": "#f07878",
        "tagline": "The Big-Picture Boss",
        "description": "You are ambitious, resourceful, and always thinking three steps ahead. You know how to turn a good idea into a great opportunity.",
        "image": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f8/Mr._Krabs.svg/240px-Mr._Krabs.svg.png",
    },
}


class SpongeBobQuiz:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Which Bikini Bottom Bestie Are You?")
        self.root.geometry("760x700")
        self.root.minsize(650, 600)
        self.root.configure(bg="#fff8e7")

        self.question_index = 0
        self.scores = {key: 0 for key in RESULTS}
        self.image = None
        self.answer_buttons: list[ttk.Button] = []
        self.progress = tk.DoubleVar(value=0)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Quiz.TButton", font=("Helvetica", 13, "bold"), padding=14)
        self.style.configure("Start.TButton", font=("Helvetica", 15, "bold"), padding=14)
        self.style.configure("Quiz.Horizontal.TProgressbar", troughcolor="#ffe9a8", background="#20b8c5")

        self.container = tk.Frame(root, bg="#fff8e7")
        self.container.pack(fill="both", expand=True, padx=34, pady=26)
        self.show_welcome()

    def clear(self) -> None:
        for widget in self.container.winfo_children():
            widget.destroy()

    def title_label(self, text: str, size: int = 28) -> tk.Label:
        return tk.Label(
            self.container,
            text=text,
            font=("Helvetica", size, "bold"),
            fg="#164c63",
            bg="#fff8e7",
            wraplength=680,
        )

    def show_welcome(self) -> None:
        self.clear()
        tk.Label(self.container, text="🌊  BIKINI BOTTOM PERSONALITY QUIZ  🌊",
                 font=("Helvetica", 12, "bold"), fg="#e8753d", bg="#fff8e7").pack(pady=(24, 12))
        self.title_label("Which SpongeBob character are you?").pack(pady=8)
        tk.Label(self.container, text="Answer five totally scientific questions to reveal your underwater alter ego!",
                 font=("Helvetica", 14), fg="#4f6670", bg="#fff8e7", wraplength=620).pack(pady=12)
        tk.Label(self.container, text="🧽   ⭐   🎷   💰", font=("Helvetica", 58), bg="#fff8e7").pack(pady=24)
        ttk.Button(self.container, text="LET'S GET JELLYFISHING!  →", style="Start.TButton",
                   command=self.start_quiz).pack(pady=18)
        tk.Label(self.container, text="No wrong answers. Only very important Bikini Bottom vibes.",
                 font=("Helvetica", 10, "italic"), fg="#8b9a9d", bg="#fff8e7").pack(pady=12)

    def start_quiz(self) -> None:
        self.question_index = 0
        self.scores = {key: 0 for key in RESULTS}
        self.show_question()

    def show_question(self) -> None:
        self.clear()
        question, choices = QUESTIONS[self.question_index]
        number = self.question_index + 1
        self.progress.set((number - 1) / len(QUESTIONS) * 100)

        top = tk.Frame(self.container, bg="#fff8e7")
        top.pack(fill="x", pady=(6, 25))
        tk.Label(top, text=f"QUESTION {number} OF {len(QUESTIONS)}", font=("Helvetica", 11, "bold"),
                 fg="#e8753d", bg="#fff8e7").pack(anchor="w")
        ttk.Progressbar(top, variable=self.progress, maximum=100,
                        style="Quiz.Horizontal.TProgressbar").pack(fill="x", pady=(8, 0))

        self.title_label(question, 24).pack(pady=(18, 25))
        self.answer_buttons = []
        for index, (answer, character) in enumerate(choices):
            button = ttk.Button(self.container, text=f"{chr(65 + index)}   {answer}",
                                style="Quiz.TButton",
                                command=lambda key=character, button_index=index: self.choose_answer(key, button_index))
            button.pack(fill="x", pady=6)
            self.answer_buttons.append(button)

    def choose_answer(self, character: str, button_index: int) -> None:
        self.scores[character] += 1
        for button in self.answer_buttons:
            button.state(["disabled"])
        selected = self.answer_buttons[button_index]
        selected.configure(text="✓  " + selected.cget("text"), state="disabled")
        self.root.after(350, self.next_question)

    def next_question(self) -> None:
        self.question_index += 1
        if self.question_index < len(QUESTIONS):
            self.show_question()
        else:
            self.show_result()

    def show_result(self) -> None:
        self.clear()
        winner = max(self.scores, key=self.scores.get)
        result = RESULTS[winner]
        self.progress.set(100)

        tk.Label(self.container, text="✨ YOUR BIKINI BOTTOM MATCH ✨",
                 font=("Helvetica", 12, "bold"), fg="#e8753d", bg="#fff8e7").pack(pady=(2, 8))
        tk.Label(self.container, text=result["emoji"], font=("Helvetica", 42),
                 bg="#fff8e7").pack()
        tk.Label(self.container, text=result["name"], font=("Helvetica", 30, "bold"),
                 fg=result["color"], bg="#fff8e7").pack(pady=(0, 2))
        tk.Label(self.container, text=result["tagline"], font=("Helvetica", 14, "italic"),
                 fg="#4f6670", bg="#fff8e7").pack()

        photo_frame = tk.Frame(self.container, bg=result["color"], padx=5, pady=5)
        photo_frame.pack(pady=15)
        self.photo_label = tk.Label(photo_frame, text=result["emoji"], font=("Helvetica", 70),
                                    width=10, height=3, bg="#ffffff")
        self.photo_label.pack()
        threading.Thread(target=self.load_photo, args=(result["image"],), daemon=True).start()

        tk.Label(self.container, text=result["description"], font=("Helvetica", 13),
                 fg="#344b55", bg="#fff8e7", wraplength=610, justify="center").pack(pady=7)
        score_text = "   ".join(f"{RESULTS[key]['emoji']} {value}" for key, value in self.scores.items())
        tk.Label(self.container, text=f"Your vibe score:  {score_text}", font=("Helvetica", 10),
                 fg="#71858b", bg="#fff8e7").pack(pady=10)
        ttk.Button(self.container, text="PLAY AGAIN  ↻", style="Start.TButton",
                   command=self.start_quiz).pack(pady=10)
        self.confetti()

    def load_photo(self, url: str) -> None:
        if Image is None:
            return
        try:
            request = Request(url, headers={"User-Agent": "SpongeBobQuiz/1.0"})
            with urlopen(request, timeout=5) as response:
                image_data = response.read()
            image = Image.open(BytesIO(image_data)).convert("RGBA")
            image.thumbnail((210, 190))
            photo = ImageTk.PhotoImage(image)
            self.root.after(0, lambda: self.set_photo(photo))
        except (URLError, TimeoutError, OSError):
            return

    def set_photo(self, photo: object) -> None:
        self.image = photo
        self.photo_label.configure(image=self.image, text="")

    def confetti(self) -> None:
        colors = ["#ffd84d", "#20b8c5", "#f07878", "#9ed6c7", "#f39ab1"]
        for _ in range(24):
            label = tk.Label(self.container, text=random.choice(["✦", "•", "★"]),
                             font=("Helvetica", random.randint(10, 20), "bold"),
                             fg=random.choice(colors), bg="#fff8e7")
            label.place(relx=random.random(), rely=random.uniform(0.02, 0.98))


if __name__ == "__main__":
    root = tk.Tk()
    SpongeBobQuiz(root)
    root.mainloop()