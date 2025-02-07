import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Aggiunta del percorso src al sys.path per evitare problemi di import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src/data_ingestion')))

# Import corretti basati sui file presenti nel progetto
from data_ingestion.ingest_data import run_data_ingestion
from data_ingestion.preprocessing.clean_data import clean_data
from data_ingestion.models.train_model import train_model
from data_ingestion.models.predict import predict
from data_ingestion.evaluation.evaluate_model import evaluate_model
from data_ingestion.evaluation.utils.logger import setup_logger, log_message

def main():
    """
    Flusso completo del sistema di monitoraggio e previsione della qualità dell'aria.
    Ingestione -> Pulizia -> Addestramento -> Previsione -> Valutazione -> Visualizzazione
    """
    logger = setup_logger(log_file_path='system.log')

    try:
        log_message(logger, '--- Avvio del sistema di monitoraggio della qualità dell\'aria ---', level='info')

        # Passaggio 1: Ingestione dei dati
        log_message(logger, '> Inizio del processo di ingestione dei dati...', level='info')
        run_data_ingestion()
        print("✅ DEBUG: Processo di ingestione completato.")

        # Passaggio 2: Pulizia dei dati
        raw_data_path = os.path.join(os.getcwd(), 'dataset', 'raw', 'weather_ingested.csv')
        cleaned_data_path = os.path.join(os.getcwd(), 'dataset', 'processed', 'weather_cleaned.csv')
        log_message(logger, '> Inizio del processo di pulizia dei dati...', level='info')
        print("✅ DEBUG: Inizio pulizia dati...")
        cleaned_data = clean_data(raw_data_path)
        print("✅ DEBUG: Dati puliti.")

        if cleaned_data is not None:
            os.makedirs(os.path.dirname(cleaned_data_path), exist_ok=True)
            cleaned_data.to_csv(cleaned_data_path, index=False)
            print(f"✅ DEBUG: Dati salvati in {cleaned_data_path}")
        else:
            raise ValueError("❌ Errore: La pulizia dei dati ha restituito None!")

        # Passaggio 3: Addestramento del modello
        model_output_path = os.path.join(os.getcwd(), 'models', 'random_forest_model.pkl')
        log_message(logger, '> Inizio del processo di addestramento del modello...', level='info')
        print("✅ DEBUG: Inizio addestramento modello...")
        train_model(cleaned_data_path, model_output_path)

        # Passaggio 4: Previsione sui nuovi dati
        log_message(logger, '> Inizio del processo di previsione sui nuovi dati...', level='info')
        print("✅ DEBUG: Inizio previsione...")
        prediction_data_path = cleaned_data_path
        predictions = predict(prediction_data_path, model_output_path)

        # Passaggio 5: Valutazione del modello
        if predictions is not None:
            log_message(logger, '> Inizio del processo di valutazione del modello...', level='info')
            print("✅ DEBUG: Inizio valutazione modello...")
            true_values = predictions.get('PM2.5')
            predicted_values = predictions.get('Prediction_PM2.5')
            if true_values is not None and predicted_values is not None:
                report = evaluate_model(true_values, predicted_values, output_dir='evaluation_reports')
                print(f"✅ DEBUG: Risultati valutazione modello: {report}")
            else:
                print("❌ Errore: Le colonne di verità o previsione sono mancanti nel dataset!")
        else:
            print("❌ Errore: La previsione non ha prodotto dati validi!")

        log_message(logger, '--- Fine del processo di monitoraggio e previsione ---', level='info')

    except Exception as e:
        log_message(logger, f'Errore critico nel flusso principale: {e}', level='error')
        print(f"❌ ERRORE CRITICO: {e}")

if __name__ == '__main__':
    main()
