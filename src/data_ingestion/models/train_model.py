import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

def train_model(data_path, model_output_path, checkpoint_dir='models/model_checkpoints'):
    """
    Addestra un modello di Random Forest per prevedere la qualità dell'aria.

    Args:
        data_path (str): Percorso del file CSV con i dati di training.
        model_output_path (str): Percorso per salvare il modello addestrato.
        checkpoint_dir (str): Directory dove salvare i checkpoint del modello.
    """
    try:
        # Verifica che il file di dati esista
        if not os.path.exists(data_path):
            print(f'Errore: File di dati non trovato al percorso {data_path}')
            return None

        # Caricamento dei dati
        print(f'> Caricamento dei dati da {data_path}...')
        data = pd.read_csv(data_path)

        # Verifica che il file non sia vuoto
        if data.empty:
            print('> Il file di dati è vuoto.')
            return None

        # Separazione delle variabili di input (X) e target (y)
        X = data[['PM2.5', 'PM10', 'CO', 'SO2', 'NO2', 'O3', 'temperature', 'humidity', 'wind_speed']]
        y = data['PM2.5']  # Supponiamo di voler prevedere la colonna PM2.5

        # Divisione dei dati in train e test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Creazione del modello RandomForest
        print('> Inizio del processo di addestramento del modello Random Forest...')
        model = RandomForestRegressor(n_estimators=100, random_state=42)

        # Ciclo di addestramento con checkpoint ogni 10 epoche
        for epoch in range(1, 31):  # Simuliamo 30 epoche
            print(f'> Addestramento epoca {epoch}...')
            model.fit(X_train, y_train)  # Addestra il modello per ogni epoca

            # Salvataggio del checkpoint ogni 10 epoche
            if epoch % 10 == 0:  
                checkpoint_path = os.path.join(checkpoint_dir, f'checkpoint_{epoch}.pkl')
                os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
                joblib.dump(model, checkpoint_path)
                print(f'> Checkpoint salvato: {checkpoint_path}')

        # Salvataggio del modello finale
        os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
        joblib.dump(model, model_output_path)
        print(f'> Modello finale salvato con successo in {model_output_path}')

        return model

    except Exception as e:
        print(f'Errore durante l\'addestramento del modello: {e}')
        return None