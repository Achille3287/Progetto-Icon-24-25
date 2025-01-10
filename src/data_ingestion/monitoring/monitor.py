import pandas as pd
import os
import time

def monitor_air_quality(file_path, thresholds=None, check_interval=10):
    """
    Monitora in tempo reale i dati di qualità dell'aria.
    
    Args:
        file_path (str): Percorso del file CSV contenente i dati di qualità dell'aria.
        thresholds (dict): Dizionario con le soglie per le variabili monitorate. Es: {'PM2.5': 50, 'PM10': 100}
        check_interval (int): Intervallo di tempo (in secondi) tra una verifica e l'altra.
    """
    if thresholds is None:
        thresholds = {'PM2.5': 50, 'PM10': 100, 'CO': 9, 'SO2': 20, 'NO2': 40, 'O3': 70}
    
    try:
        print('> Inizio del monitoraggio in tempo reale...')
        
        while True:
            if not os.path.exists(file_path):
                print(f'Errore: File non trovato al percorso {file_path}')
                time.sleep(check_interval)
                continue
            
            # Caricamento dei dati più recenti
            air_quality_data = pd.read_csv(file_path)
            
            if air_quality_data.empty:
                print(f'> Nessun dato disponibile nel file {file_path}')
                time.sleep(check_interval)
                continue

            latest_data = air_quality_data.tail(1).iloc[0]  # Ottiene l'ultima riga dei dati
            
            for parameter, threshold in thresholds.items():
                if parameter in latest_data:
                    value = latest_data[parameter]
                    if pd.to_numeric(value, errors='coerce') > threshold:
                        print(f'⚠️ Attenzione! {parameter} ha superato la soglia di {threshold}. Valore attuale: {value}')
            
            print(f'> Verifica completata. Prossima verifica tra {check_interval} secondi...')
            time.sleep(check_interval)

    except Exception as e:
        print(f'Errore durante il monitoraggio: {e}')