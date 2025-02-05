import sys
import os

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
    Ingestione -> Pulizia -> Addestramento -> Previsione -> Valutazione
    """
    logger = setup_logger(log_file_path='system.log')

    try:
        log_message(logger, '--- Avvio del sistema di monitoraggio della qualità dell\'aria ---', level='info')

        # Passaggio 1: Ingestione dei dati
        log_message(logger, '> Inizio del processo di ingestione dei dati...', level='info')
        run_data_ingestion()

        # Passaggio 2: Pulizia dei dati
        raw_data_path = os.path.join(os.getcwd(), 'dataset', 'raw', 'weather_ingested.csv')
        cleaned_data_path = os.path.join(os.getcwd(), 'dataset', 'processed', 'weather_cleaned.csv')
        log_message(logger, '> Inizio del processo di pulizia dei dati...', level='info')
        cleaned_data = clean_weather_data(raw_data_path)
        if cleaned_data is not None:
            save_clean_data(cleaned_data, cleaned_data_path)

        # Passaggio 3: Addestramento del modello
        model_output_path = os.path.join(os.getcwd(), 'models', 'random_forest_model.pkl')
        log_message(logger, '> Inizio del processo di addestramento del modello...', level='info')
        train_model(cleaned_data_path, model_output_path)

        # Passaggio 4: Previsione sui nuovi dati
        log_message(logger, '> Inizio del processo di previsione sui nuovi dati...', level='info')
        prediction_data_path = cleaned_data_path  # Per ora usiamo lo stesso file per le previsioni
        predictions = predict(prediction_data_path, model_output_path)

        # Passaggio 5: Valutazione del modello
        if predictions is not None:
            log_message(logger, '> Inizio del processo di valutazione del modello...', level='info')
            true_values = predictions['PM2.5']
            predicted_values = predictions['Prediction_PM2.5']
            report = evaluate_model(true_values, predicted_values, output_dir='evaluation_reports')
            if report is not None:
                log_message(logger, f'> Risultati della valutazione: {report}', level='info')

        log_message(logger, '--- Fine del processo di monitoraggio e previsione ---', level='info')

    except Exception as e:
        log_message(logger, f'Errore critico nel flusso principale: {e}', level='error')

if __name__ == '__main__':
    main()
