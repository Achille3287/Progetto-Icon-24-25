import pandas as pd
import joblib
import os
from utils.logger import setup_logger, log_message

def predict(file_path, model_path, output_path='dataset/predicted/predicted_results.csv'):
    """
    Carica il modello e prevede i valori di qualità dell'aria sui nuovi dati.

    Args:
        file_path (str): Percorso del file CSV con i dati di input.
        model_path (str): Percorso del file del modello pre-addestrato.
        output_path (str): Percorso per salvare il file CSV con le previsioni.

    Returns:
        pd.DataFrame: DataFrame con le previsioni.
    """
    logger = setup_logger(log_file_path='system.log')

    try:
        # Verifica se il file CSV esiste
        if not os.path.exists(file_path):
            log_message(logger, f'Errore: File dei dati non trovato al percorso {file_path}', level='error')
            return None

        # Verifica se il file del modello esiste
        if not os.path.exists(model_path):
            log_message(logger, f'Errore: Modello non trovato al percorso {model_path}', level='error')
            return None

        # Caricamento dei dati
        log_message(logger, f'> Caricamento dei dati da {file_path}...', level='info')
        data = pd.read_csv(file_path)

        if data.empty:
            log_message(logger, '> Il file di dati è vuoto.', level='warning')
            return None

        # Verifica che le colonne esistano
        required_columns = ['PM2.5', 'PM10', 'CO', 'SO2', 'NO2', 'O3', 'temperature', 'humidity', 'wind_speed']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            log_message(logger, f'Errore: Mancano le seguenti colonne nel file: {missing_columns}', level='error')
            return None

        # Prepara i dati di input (X)
        X = data[required_columns]

        # Caricamento del modello
        log_message(logger, f'> Caricamento del modello da {model_path}...', level='info')
        model = joblib.load(model_path)

        # Esecuzione delle previsioni
        log_message(logger, '> Esecuzione delle previsioni...', level='info')
        predictions = model.predict(X)

        # Aggiunta delle previsioni ai dati
        data['Prediction_PM2.5'] = predictions
        log_message(logger, '> Previsioni completate con successo.', level='info')

        # Salvataggio del file CSV con le previsioni
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            data.to_csv(output_path, index=False)
            log_message(logger, f'> File con previsioni salvato in: {output_path}', level='info')

        return data

    except Exception as e:
        log_message(logger, f'Errore durante la previsione: {e}', level='error')
        return None