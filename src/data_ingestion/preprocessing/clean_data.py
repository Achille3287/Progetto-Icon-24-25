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
        print("🔍 DEBUG: Contiamo i NaN in ogni colonna prima della pulizia:\n", data.isna().sum())

        # Rimozione dei duplicati
        data.drop_duplicates(inplace=True)
        print("🔍 DEBUG: Numero di righe dopo la rimozione di duplicati:", len(data))

        # Gestione dei valori mancanti (sostituiti con la mediana solo nelle colonne necessarie)
        for col in numeric_columns:
            if col in data.columns:
                median_value = data[col].median()
                if np.isnan(median_value):  # Se tutta la colonna è NaN
                    median_value = 0  # Sostituiamo con 0 come default
                data.loc[:, col] = data[col].fillna(median_value)
        print("🔍 DEBUG: Dopo riempimento NaN, contiamo i NaN per colonna:\n", data.isna().sum())

        # Evitiamo di eliminare troppi dati con gli outlier
        for col in numeric_columns:
            if col in data.columns and data[col].notna().sum() > 5:  # Controlliamo di avere almeno 5 dati validi
                z_scores = (data[col] - data[col].mean()) / data[col].std()
                data = data[(z_scores > -3) & (z_scores < 3)]
        print("🔍 DEBUG: Numero di righe dopo la rimozione outlier:", len(data))
        print("🔍 DEBUG: Contiamo i NaN dopo la rimozione outlier:\n", data.isna().sum())

        # Normalizzazione Min-Max Scaling
        for col in numeric_columns:
            if col in data.columns and data[col].notna().sum() > 0:  # Evitiamo divisioni per zero
                data.loc[:, col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())
        print('✅ DEBUG: Dati normalizzati.')

        # Rimuoviamo eventuali NaN nel target prima dell'addestramento
        data = data.dropna(subset=['PM2.5'])
        print("🔍 DEBUG: Contiamo i NaN dopo la rimozione della colonna target:\n", data.isna().sum())

        # Debug per controllare la directory di salvataggio
        print(f'🔍 DEBUG: Verifica della directory di output: {os.path.dirname(output_path)}')

        # Creazione della cartella di output se non esiste
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Debugging finale prima del salvataggio
        print("🔍 DEBUG: Anteprima dei dati prima del salvataggio:")
        print(data.head())

        # Salvataggio dei dati puliti
        data.to_csv(output_path, index=False)
        print(f'✅ Dati puliti salvati in {output_path}')

        return data

    except Exception as e:
        print(f'❌ Errore durante la pulizia dei dati: {e}')
        return None
