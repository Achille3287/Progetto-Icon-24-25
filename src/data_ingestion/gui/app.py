import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Percorso del dataset
DATASET_PATH = "dataset/processed/weather_cleaned.csv"

def load_data():
    if os.path.exists(DATASET_PATH):
        return pd.read_csv(DATASET_PATH)
    else:
        print("❌ Errore: Il dataset non esiste!")
        return None

# Carichiamo i dati
data = load_data()
if data is None:
    exit()

# Cambiamo "City_Center" in "Bari" e aggiungiamo altre città
data['location'] = data['location'].replace("City_Center", "Bari")

# Aggiungiamo altre città con dati simulati
new_cities = ["Roma", "Milano", "Napoli"]
for city in new_cities:
    city_data = data[data['location'] == "Bari"].copy()
    city_data['location'] = city
    city_data['temperature'] += np.random.uniform(-3, 3, size=len(city_data))
    city_data['humidity'] += np.random.uniform(-5, 5, size=len(city_data))
    city_data['PM2.5'] += np.random.uniform(-10, 10, size=len(city_data))
    data = pd.concat([data, city_data])

# Salviamo il nuovo dataset
data.to_csv(DATASET_PATH, index=False)

# Creazione della finestra principale
root = tk.Tk()
root.title("Monitoraggio Qualità dell'Aria")
root.geometry("700x600")

# Messaggio di benvenuto
welcome_label = tk.Label(root, text="Benvenuto Utente, seleziona la città", font=("Arial", 12))
welcome_label.pack(pady=10)

# Dropdown per la selezione della città con aggiornamento automatico
city_var = tk.StringVar()
cities = data['location'].unique().tolist()
city_var.set(cities[0])  # Valore di default
city_menu = ttk.Combobox(root, textvariable=city_var, values=cities)
city_menu.pack(pady=5)
city_menu.bind("<<ComboboxSelected>>", lambda event: update_data())

# Frame per la visualizzazione dei dati
data_frame = ttk.Treeview(root, columns=("Temperatura", "Umidità", "PM2.5"), show="headings")
data_frame.heading("Temperatura", text="Temperatura (°C)")
data_frame.heading("Umidità", text="Umidità (%)")
data_frame.heading("PM2.5", text="PM2.5 (µg/m³)")
data_frame.pack(pady=10)

# Funzione per aggiornare i dati
def update_data():
    selected_city = city_var.get()
    city_data = data[data['location'] == selected_city].tail(10)
    
    # Pulisce la tabella prima di aggiornare
    for row in data_frame.get_children():
        data_frame.delete(row)
    
    # Aggiunge nuovi dati
    for _, row in city_data.iterrows():
        data_frame.insert("", "end", values=(row["temperature"], row["humidity"], row["PM2.5"]))
    
    # Aggiorna il grafico
    update_chart(city_data)

# Grafico con Matplotlib
def update_chart(city_data):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(city_data['timestamp'], city_data['temperature'], label='Temperatura', marker='o')
    ax.plot(city_data['timestamp'], city_data['humidity'], label='Umidità', marker='s')
    ax.set_xticklabels(city_data['timestamp'], rotation=45, ha='right')
    ax.set_title(f"Dati meteo per {city_var.get()}")
    ax.legend()
    
    # Inserisce il grafico nella GUI
    for widget in chart_frame.winfo_children():
        widget.destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Frame per il grafico
chart_frame = tk.Frame(root)
chart_frame.pack(pady=10)

# Pulsante per uscire
tk.Button(root, text="Esci", command=root.quit, font=("Arial", 10), bg="red", fg="white").pack(pady=10)

# Avvio dell'aggiornamento dati
update_data()

# Avvio dell'interfaccia grafica
root.mainloop()
