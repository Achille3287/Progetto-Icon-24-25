import pandas as pd
import numpy as np
import os

def clean_data(file_path, output_path='dataset/processed/weather_cleaned.csv'):
    """
    Pulisce i dati rimuovendo NaN, outlier, duplicati e normalizza i dati.

    Args:
        file_path (str): Percorso del file CSV grezzo.
        output_path (str): Percorso del file pulito da salvare.

    Returns:
        pd.DataFrame: DataFrame pulito.
    """
    try:
        # Caricamento dei dati
        print(f'> Caricamento dei dati da {file_path}...')
        data = pd.read_csv(file_path)

        # Controllo delle colonne
        required_columns = ['PM2.5', 'PM10', 'CO', 'SO2', 'NO2', 'O3', 'temperature', 'humidity', 'wind_speed']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Le seguenti colonne sono mancanti nel file CSV: {missing_columns}")

        # Rimozione dei duplicati
        data.drop_duplicates(inplace=True)
        print('> Duplicati rimossi.')

        # Gestione dei valori mancanti (sostituiti con la mediana)
        data.fillna(data.median(), inplace=True)
        print('> Valori mancanti sostituiti con la mediana.')

        # Rimozione degli outlier (Z-score)
        for col in required_columns:
            z_scores = (data[col] - data[col].mean()) / data[col].std()
            data = data[(z_scores > -3) & (z_scores < 3)]
        print('> Outlier rimossi.')

        # Normalizzazione Min-Max
        for col in required_columns:
            data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())
        print('> Dati normalizzati (Min-Max Scaling).')

        # Salvataggio dei dati puliti
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        data.to_csv(output_path, index=False)
        print(f'> Dati puliti salvati in {output_path}')

        return data

    except Exception as e:
        print(f"Errore durante la pulizia dei dati: {e}")
        return None