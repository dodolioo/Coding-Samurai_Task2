import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_KEY = '65b48328a311b97c29de348f0af7368a'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


def get_weather(city, unit):
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric' if unit == 'Celsius' else 'imperial'
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def show_weather():
    city = city_entry.get()
    unit = unit_var.get()

    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    try:
        weather_data = get_weather(city, unit)
        display_weather(weather_data, unit)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get weather data: {e}")


def display_weather(weather_data, unit):
    city_name = weather_data['name']
    country = weather_data['sys']['country']
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    weather_description = weather_data['weather'][0]['description'].capitalize()

    result_text.set(f"Weather in {city_name}, {country}:\n"
                    f"Temperature: {temp}°{unit[0]}\n"
                    f"Humidity: {humidity}%\n"
                    f"Wind Speed: {wind_speed} {'m/s' if unit == 'Celsius' else 'mph'}\n"
                    f"Condition: {weather_description}")


root = tk.Tk()
root.title("Weather Forecast Application")
root.geometry("400x300")


ttk.Label(root, text="Enter city:").pack(pady=5)
city_entry = ttk.Entry(root)
city_entry.pack(pady=5)


unit_var = tk.StringVar(value='Celsius')
ttk.Label(root, text="Select unit:").pack(pady=5)
unit_frame = ttk.Frame(root)
unit_frame.pack(pady=5)
ttk.Radiobutton(unit_frame, text='Celsius', variable=unit_var, value='Celsius').pack(side=tk.LEFT, padx=5)
ttk.Radiobutton(unit_frame, text='Fahrenheit', variable=unit_var, value='Fahrenheit').pack(side=tk.LEFT, padx=5)


ttk.Button(root, text="Get Weather", command=show_weather).pack(pady=20)


result_text = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_text, wraplength=300)
result_label.pack(pady=10)


root.mainloop()
