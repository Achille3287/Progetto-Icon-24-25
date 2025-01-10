import pandas as pd
import os

def run_data_ingestion():
    """
    Funzione principale per la raccolta e l'ingestione dei dati.
    """
    try:
        # Percorso al file di esempio (può essere sostituito con API o sensore)
        data_path = os.path.join(os.getcwd(), 'dataset', 'weather_data.csv')
        
        if not os.path.exists(data_path):
            print(f'Errore: File non trovato al percorso {data_path}')
            return
        
        # Caricamento dei dati dal file CSV
        print(f'> Caricamento del file {data_path}...')
        weather_data = pd.read_csv(data_path)
        
        # Visualizzazione delle prime righe del file
        print(f'> Anteprima dei dati:\n{weather_data.head()}')

        # Simulazione del salvataggio in formato "grezzo"
        raw_data_path = os.path.join(os.getcwd(), 'dataset', 'raw', 'weather_ingested.csv')
        weather_data.to_csv(raw_data_path, index=False)
        print(f'> Dati salvati in formato grezzo in: {raw_data_path}')

    except Exception as e:
        print(f'Errore durante l\'ingestione dei dati: {e}')
