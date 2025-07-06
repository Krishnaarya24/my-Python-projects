    #    DAILY QUOTES APP


import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import random
import threading
import time
from datetime import datetime, date

QUOTES_FILE = "quotes.json"
HISTORY_FILE = "quote_history.json"
TIME_FILE = "notify_time.json"

# Load saved quotes or use default ones
default_quotes = [
    "🌞 Believe in yourself!",
    "🚀 Stay positive, work hard, make it happen.",
    "🌈 The best time for new beginnings is now.",
    "💡 Dreams don’t work unless you do.",
    "🔥 Push yourself because no one else is going to do it for you.",
    "🌟 Success doesn’t just find you. You have to go out and get it.",
    "🏆 Great things never come from comfort zones.",
    "🧠 Don’t stop until you’re proud.",
    "🌺 Every day is a fresh start.",
    "💪 The pain you feel today will be the strength you feel tomorrow.",
    "🙌The longer you live, the more you realize that reality is just made of pain, suffering, and emptiness.",

    "🩵When a man learns to love, he must bear the risk of hatred"
]

def load_quotes():
    if os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_quotes

def save_quotes(quotes):
    with open(QUOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(quotes, f, indent=4, ensure_ascii=False)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_quote(today, quote):
    history = load_history()
    history[today] = quote
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def get_today():
    return str(date.today())
try:
    def get_today_quote():
        today = get_today()
        history = load_history()
        if today in history:
            return history[today]
        else:
            quote = random.choice(load_quotes())
            save_quote(today, quote)
            return quote
except Exception as e:
    print("something is wrong Try again please",e)

def show_quote():
    quote = get_today_quote()
    quote_label.config(text=quote)
try:
    def view_history():
        history = load_history()
        if not history:
            messagebox.showinfo("Quote History", "No quote history yet.")
            return

        history_window = tk.Toplevel(root)
        history_window.title("📚 Quote History")
        history_window.geometry("400x400")

        text = tk.Text(history_window, wrap=tk.WORD, font=("Arial", 12))
        text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        for day, quote in sorted(history.items()):
            text.insert(tk.END, f"{day}: {quote}\n\n")
except Exception as n:
    print("network error")

def add_quote():
    new_quote = simpledialog.askstring("Add New Quote", "Enter your quote:")
    if new_quote:
        quotes = load_quotes()
        if new_quote not in quotes:
            quotes.append(new_quote)
            save_quotes(quotes)
            messagebox.showinfo("Success", "Quote added!")
        else:
            messagebox.showinfo("Info", "This quote already exists.")

# Notification handling
def set_notification_time():
    time_input = simpledialog.askstring("Set Notification Time", "Enter time (HH:MM AM/PM):")
    try:
        datetime.strptime(time_input, "%I:%M %p")  # Validate format
        with open(TIME_FILE, "w") as f:
            json.dump({"time": time_input}, f)
        messagebox.showinfo("Success", f"Daily quote time set to {time_input}")
    except:
        messagebox.showerror("Error", "Invalid time format. Please use HH:MM AM/PM.")

def get_notification_time():
    if os.path.exists(TIME_FILE):
        with open(TIME_FILE, "r") as f:
            return json.load(f).get("time")
    return None

def notification_loop():
    while True:
        now = datetime.now().strftime("%I:%M %p")
        notify_time = get_notification_time()
        if notify_time == now:
            show_quote_popup()
            time.sleep(60)  # wait a minute to avoid multiple popups
        time.sleep(20)  # check every 20 seconds

def show_quote_popup():
    quote = get_today_quote()
    messagebox.showinfo("🌞 Daily Quote", quote)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("🌟 Daily Quote App")
root.geometry("400x400")
root.resizable(False, False)

# Title
title = tk.Label(root, text="💬 Daily Quote App", font=("Arial", 20, "bold"))
title.pack(pady=10)

# Quote Label
quote_label = tk.Label(root, text="", wraplength=350, font=("Arial", 14), justify="center")
quote_label.pack(pady=20)

# Buttons
btn_show = tk.Button(root, text="📜 Show Today's Quote", command=show_quote, font=("Arial", 12))
btn_show.pack(pady=5)

btn_history = tk.Button(root, text="📚 View History", command=view_history, font=("Arial", 12))
btn_history.pack(pady=5)

btn_add = tk.Button(root, text="➕ Add New Quote", command=add_quote, font=("Arial", 12))
btn_add.pack(pady=5)

btn_set_time = tk.Button(root, text="⏰ Set Notification Time", command=set_notification_time, font=("Arial", 12))
btn_set_time.pack(pady=5)

# Load today's quote on start
show_quote()

# Start notification thread
threading.Thread(target=notification_loop, daemon=True).start()

root.mainloop()
