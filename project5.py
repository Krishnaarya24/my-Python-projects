        #  STONE PAPER SCICCOR GAME





import tkinter as tk
import random

# Emoji representations
emojis = {
    "Stone": "🪨",
    "Paper": "📄",
    "Scissor": "✂️"
}

class SPSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stone Paper Scissors")
        self.root.geometry("400x480")
        self.root.config(bg="#f9f9f9")

        self.choices = ["Stone", "Paper", "Scissor"]
        self.user_score = 0
        self.computer_score = 0

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Stone 🪨 Paper 📄 Scissor ✂️", font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=15)

        self.result_label = tk.Label(self.root, text="Make your move!", font=("Arial", 14), bg="#f9f9f9", fg="blue")
        self.result_label.pack(pady=10)

        self.choice_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#f9f9f9")
        self.choice_label.pack(pady=5)

        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=("Arial", 12), bg="#f9f9f9")
        self.score_label.pack(pady=10)

        button_frame = tk.Frame(self.root, bg="#f9f9f9")
        button_frame.pack(pady=20)

        for choice in self.choices:
            btn = tk.Button(button_frame, text=f"{choice} {emojis[choice]}", font=("Arial", 12), width=14,
                            command=lambda c=choice: self.play_round(c))
            btn.pack(pady=5)

        self.reset_btn = tk.Button(self.root, text="🔄 Restart", font=("Arial", 12), command=self.reset_game)
        self.reset_btn.pack(pady=15)

    def play_round(self, user_choice):
        comp_choice = random.choice(self.choices)
        result = self.get_winner(user_choice, comp_choice)

        if result == "win":
            self.user_score += 1
            result_text = f"You Win! {emojis[user_choice]} beats {emojis[comp_choice]}"
        elif result == "lose":
            self.computer_score += 1
            result_text = f"You Lose! {emojis[comp_choice]} beats {emojis[user_choice]}"
        else:
            result_text = f"Draw! Both chose {emojis[user_choice]}"

        # Show choices
        self.choice_label.config(
            text=f"You chose: {user_choice} {emojis[user_choice]}\nComputer chose: {comp_choice} {emojis[comp_choice]}"
        )
        self.result_label.config(text=result_text)
        self.score_label.config(text=self.get_score_text())

    def get_winner(self, user, comp):
        if user == comp:
            return "draw"
        if (user == "Stone" and comp == "Scissor") or \
           (user == "Paper" and comp == "Stone") or \
           (user == "Scissor" and comp == "Paper"):
            return "win"
        else:
            return "lose"

    def get_score_text(self):
        return f"👤 You: {self.user_score}   🤖 Computer: {self.computer_score}"

    def reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.result_label.config(text="Make your move!")
        self.choice_label.config(text="")
        self.score_label.config(text=self.get_score_text())


if __name__ == "__main__":
    root = tk.Tk()
    app = SPSApp(root)
    root.mainloop()
