#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
import requests
import os


def get_api_key(file_name):
    """
    Args:
        file_name (str): API key file name (full path)

    Returns:
        str: String representing the API key
    """
    with open(file_name) as f:
        return f.readline().strip()


def get_weather(city):
    """
    Fetch weather data for a given city from OpenWeatherMap API.
        This version is hard-coded for Australian cities (AU) only.

    Args:
        city (str): Name of the city to fetch weather data for.

    Returns:
        str: Formatted weather information including temperature, pressure,
             humidity, and description. If the city is not found, returns
             'City not found.'
    """
    # api_key = 'your-hardcoded-key-comment-out-the-next-2-lines'
    api_key_file = os.getenv('JD_OPENWEATHER_API_KEY')
    api_key = get_api_key(api_key_file)
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + ",AU&appid=" + api_key + "&units=metric"

    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        temperature = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        description = weather["description"]

        weather_info = (
            f"Temperature: {temperature}°C\n"
            f"Pressure: {pressure} hPa\n"
            f"Humidity: {humidity}%\n"
            f"Description: {description}"
        )
    else:
        weather_info = "City not found."

    return weather_info


def show_weather():
    """
    Display weather data for the city entered in the GUI entry widget.
    """
    city = city_entry.get()
    weather_info = get_weather(city)
    weather_label.config(text=weather_info)


# GUI setup
root = tk.Tk()
root.title("Weather App (Australia)")

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

city_label = ttk.Label(mainframe, text="Enter City Name:")
city_label.grid(row=0, column=0, sticky=tk.W)

city_entry = ttk.Entry(mainframe, width=20)
city_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

search_button = ttk.Button(mainframe, text="Get Weather", command=show_weather)
search_button.grid(row=1, column=0, columnspan=2, pady=10)

weather_label = ttk.Label(mainframe, text="", justify="left")
weather_label.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
