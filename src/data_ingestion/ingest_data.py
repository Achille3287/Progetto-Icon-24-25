import pandas as pd
import os
import numpy as np

def run_data_ingestion():
    """
    Funzione principale per la raccolta e l'ingestione dei dati.
    """
    try:
        # Percorso al file di esempio
        data_path = os.path.join(os.getcwd(), 'dataset', 'weather_data.csv')
        
        if not os.path.exists(data_path):
            print(f'Errore: File non trovato al percorso {data_path}')
            return
        
        # Caricamento dei dati
        print(f'> Caricamento del file {data_path}...')
        weather_data = pd.read_csv(data_path)

        # 🔍 Puliamo i nomi delle colonne rimuovendo spazi
        weather_data.columns = weather_data.columns.str.strip()

        # Debug: Stampiamo le colonne per conferma
        print("🔍 DEBUG: Colonne dopo la rimozione degli spazi:", weather_data.columns)

        # Definiamo tutte le colonne che devono esistere nel dataset
        required_columns = ['timestamp', 'location', 'temperature', 'humidity', 'wind_speed',
                            'wind_direction', 'pressure', 'precipitation', 
                            'PM2.5', 'PM10', 'CO', 'SO2', 'NO2', 'O3']

        # Aggiungiamo eventuali colonne mancanti con NaN
        for col in required_columns:
            if col not in weather_data.columns:
                weather_data[col] = np.nan  

        # 🔍 DEBUG: Stampiamo le colonne dopo la modifica
        print("✅ DEBUG: Colonne finali nel dataset dopo la modifica:", weather_data.columns)

        # Creiamo la cartella se non esiste
        raw_data_path = os.path.join(os.getcwd(), 'dataset', 'raw', 'weather_ingested.csv')
        os.makedirs(os.path.dirname(raw_data_path), exist_ok=True)

        # Salviamo il file corretto
        weather_data.to_csv(raw_data_path, index=False)
        print(f'✅ Dati salvati in formato grezzo in: {raw_data_path}')

    except Exception as e:
        print(f'❌ Errore durante l\'ingestione dei dati: {e}')
