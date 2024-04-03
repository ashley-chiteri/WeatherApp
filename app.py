#author:  Ashley Chiteri
import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap
# importing sensitive info like api keys from hidden files
import creds

#get the weather information from openweathermap API
def getWeather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={creds.API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    #return the information in json
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp']
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']


    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)



#search for the weather for the city
def search():
    city = cityEntry.get()
    result = getWeather(city)
    if result is None:
        return
    icon_url, temperature, description, city, country = result
    locationLabel.configure(text=f"{city}, {country}")

    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    iconLabel.configure(image=icon)
    iconLabel.image = icon

    temperatureLabel.configure(text=f"Temperature: {temperature:.2f}°c")
    descriptionLabel.configure(text=f"Description: {description}")



root = ttkbootstrap.Window(themename="solar")
root.title("Weather App")
root.geometry("400x400")


cityEntry = ttkbootstrap.Entry(root, font="sans-serif, 18")
cityEntry.pack(pady=10)

searchButton  = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
searchButton.pack(pady=10)


locationLabel = tk.Label(root, font="sans-serif, 25")
locationLabel.pack(pady=20)

iconLabel = tk.Label(root)
iconLabel.pack()

temperatureLabel = tk.Label(root, font="sans-serif, 18")
temperatureLabel.pack()

descriptionLabel = tk.Label(root, font="sans-serif, 18")
descriptionLabel.pack()

root.mainloop()
