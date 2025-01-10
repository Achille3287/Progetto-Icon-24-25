import pandas as pd
import os

def clean_weather_data(file_path):
    """
    Pulisce i dati meteorologici grezzi.
    - Rimuove i valori non numerici.
    - Corregge gli outlier (ad esempio, umidità > 100).
    - Gestisce i valori mancanti (NaN) sostituendoli con la media o interpolandoli.

    Args:
        file_path (str): Il percorso del file CSV grezzo.

    Returns:
        pd.DataFrame: DataFrame con i dati puliti.
    """
    try:
        if not os.path.exists(file_path):
            print(f'Errore: File non trovato al percorso {file_path}')
            return None

        # Caricamento dei dati
        print(f'> Caricamento del file grezzo {file_path}...')
        weather_data = pd.read_csv(file_path)

        # Conversione delle colonne numeriche (gestione errori e NaN)
        numeric_columns = ['temperature', 'humidity', 'wind_speed', 'wind_direction', 'pressure', 'precipitation']
        for col in numeric_columns:
            weather_data[col] = pd.to_numeric(weather_data[col], errors='coerce')

        # Rimozione degli outlier (umidità > 100 o < 0, velocità del vento negativa, ecc.)
        weather_data.loc[weather_data['humidity'] > 100, 'humidity'] = 100
        weather_data.loc[weather_data['humidity'] < 0, 'humidity'] = 0

        # Sostituzione dei NaN con la media della colonna
        for col in numeric_columns:
            if col in weather_data.columns:
                mean_value = weather_data[col].mean()
                weather_data[col].fillna(mean_value, inplace=True)

        print('> Dati puliti con successo. Ecco un\'anteprima:')
        print(weather_data.head())

        return weather_data

    except Exception as e:
        print(f'Errore durante la pulizia dei dati: {e}')
        return None


def save_clean_data(df, output_path):
    """
    Salva i dati puliti in un file CSV.

    Args:
        df (pd.DataFrame): DataFrame da salvare.
        output_path (str): Percorso del file CSV di output.
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f'> Dati puliti salvati con successo in: {output_path}')
    except Exception as e:
        print(f'Errore durante il salvataggio dei dati puliti: {e}')