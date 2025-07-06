#    WEATHER AND NEWS APP


import requests
import tkinter as tk

WEATHER_API_KEY = "331e41eab28b444f04c97592e320e7ad"
NEWS_API_KEY = "26de5699aabf400cbf7fb6ae274baadf"
  
def get_info():
    place = entry.get()
    if not place:
        result_label.config(text="Please enter a location.")
        news_label.config(text="")
        return

    # Weather API
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={place}&appid={WEATHER_API_KEY}&units=metric"

    try:
        weather_res = requests.get(weather_url)
        weather_res.raise_for_status()
        weather_data = weather_res.json()

        weather = weather_data["weather"][0]["description"]
        temp = weather_data["main"]["temp"]
        weather_output = f"🌤️ Weather: {weather.title()}, {temp}°C"

    except Exception:
        weather_output = "Could not fetch weather data."

    # News API (search headlines related to city/state)
    news_url = f"https://newsapi.org/v2/everything?q={place}&apiKey={NEWS_API_KEY}&pageSize=3"

    try:
        news_res = requests.get(news_url)
        news_res.raise_for_status()
        news_data = news_res.json()

        articles = news_data.get("articles", [])
        if articles:
            news_output = "\n📰 Top News:\n"
            for i, article in enumerate(articles):
                title = article["title"]
                source = article["source"]["name"]
                news_output += f"{i+1}. {title} ({source})\n"
        else:
            news_output = "No news found for this location."

    except Exception:
        news_output = "Could not fetch news data."

    # Update UI
    result_label.config(text=weather_output)
    news_label.config(text=news_output)

# GUI Setup
root = tk.Tk()
root.title("Weather + News App")
root.geometry("400x400")

tk.Label(root, text="Enter city or State:", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(root, font=("Arial", 12), width=30)
entry.pack(pady=5)

tk.Button(root, text="Get Info", command=get_info, font=("Arial", 11)).pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 11), wraplength=350, justify="left")
result_label.pack(pady=10)

news_label = tk.Label(root, text="", font=("Arial", 10), wraplength=380, justify="left")
news_label.pack(pady=10)

root.mainloop()