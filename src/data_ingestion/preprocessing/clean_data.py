import pandas as pd
import numpy as np
import os

def clean_data(file_path, output_path='dataset/processed/weather_cleaned.csv'):
    """
    Pulisce i dati rimuovendo valori non numerici, NaN, outlier, duplicati e normalizza i dati.

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

        # 🔍 Rimuoviamo spazi nei nomi delle colonne
        data.columns = data.columns.str.strip()

        # Controllo delle colonne richieste
        required_columns = ['PM2.5', 'PM10', 'CO', 'SO2', 'NO2', 'O3', 'temperature', 'humidity', 'wind_speed']
        for col in required_columns:
            if col not in data.columns:
                data[col] = np.nan  # Aggiungiamo colonne mancanti con NaN

        # Correggere i dati non numerici (sostituire 'error', 'unknown' con NaN)
        data.replace(['error', 'unknown'], np.nan, inplace=True)

        # Convertire le colonne in valori numerici
        numeric_columns = ['temperature', 'humidity', 'wind_speed', 'PM2.5', 'PM10', 'CO', 'SO2', 'NO2', 'O3']
        data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')

        # 🔍 Debugging del numero di righe nelle varie fasi
        print("🔍 DEBUG: Numero di righe prima della pulizia:", len(data))

        # Rimozione dei duplicati
        data.drop_duplicates(inplace=True)
        print('✅ DEBUG: Duplicati rimossi. Numero di righe:', len(data))

        # Gestione dei valori mancanti (sostituiti con la mediana per evitare eliminazione dati)
        data.fillna(data.median(numeric_only=True), inplace=True)
        print('✅ DEBUG: Valori mancanti sostituiti con la mediana. Numero di righe:', len(data))

        # Evitiamo di eliminare troppi dati con gli outlier
        for col in numeric_columns:
            if col in data.columns and data[col].notna().sum() > 5:  # Controlliamo di avere almeno 5 dati validi
                z_scores = (data[col] - data[col].mean()) / data[col].std()
                data = data[(z_scores > -3) & (z_scores < 3)]
        print('✅ DEBUG: Outlier rimossi, ma garantiamo che rimangano abbastanza dati. Numero di righe:', len(data))

        # Normalizzazione Min-Max Scaling
        for col in numeric_columns:
            if col in data.columns and data[col].notna().sum() > 0:  # Evitiamo divisioni per zero
                data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())
        print('✅ DEBUG: Dati normalizzati.')

        # 🔍 Debugging finale
        print("🔍 DEBUG: Numero finale di righe nel dataset:", len(data))
        print("🔍 DEBUG: Prime righe del dataset dopo la pulizia:")
        print(data.head())

        # Creazione della cartella di output se non esiste
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Salvataggio dei dati puliti
        data.to_csv(output_path, index=False)
        print(f'✅ Dati puliti salvati in {output_path}')

        return data

    except Exception as e:
        print(f'❌ Errore durante la pulizia dei dati: {e}')
        return None