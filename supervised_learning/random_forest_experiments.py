import pandas as pd
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import matplotlib.pyplot as plt

def run_experiment(data_path, model_output_path='models/random_forest_experiment.pkl'):
    """ Esegui l'esperimento di Random Forest """
    try:
        # Controllo del file di input
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"File di dati non trovato: {data_path}")

        # Caricamento dei dati
        print(f'> Caricamento dei dati da {data_path}...')
        data = pd.read_csv(data_path)

        # Controllo delle colonne mancanti
        required_columns = ['PM2.5', 'PM10', 'CO', 'SO2', 'NO2', 'O3', 'temperature', 'humidity', 'wind_speed']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Le seguenti colonne sono mancanti nel file CSV: {missing_columns}")

        # Prepara i dati
        X = data[required_columns]
        y = data['PM2.5']

        # Rimuovi i NaN
        X = X.fillna(0)

        # Divisione in train e test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Creazione e addestramento del modello
        print('> Inizio addestramento del modello Random Forest...')
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Salva il modello
        save_model(model, model_output_path)

        # Valutazione del modello
        evaluate_model(model, X_test, y_test)

        # Visualizzazione dei risultati
        visualize_results(model, X_test, y_test)

    except Exception as e:
        print(f'Errore durante l\'esecuzione dell\'esperimento: {e}')

def tune_hyperparameters(X_train, y_train):
    """ Ottimizza gli iperparametri del modello """
    param_grid = {'n_estimators': [100, 200, 300], 'max_depth': [10, 20, None], 'random_state': [42]}
    grid_search = GridSearchCV(RandomForestRegressor(), param_grid, cv=3, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_

def save_model(model, model_output_path):
    """ Salva il modello su disco """
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(model, model_output_path)
    print(f'> Modello salvato in {model_output_path}')

def evaluate_model(model, X_test, y_test):
    """ Calcola e salva le metriche di valutazione """
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = mse ** 0.5
    print(f'> MAE: {mae}, MSE: {mse}, RMSE: {rmse}')
    
    # Salva le metriche in un file
    os.makedirs('evaluation_reports', exist_ok=True)
    with open('evaluation_reports/random_forest_metrics.txt', 'w') as f:
        f.write(f'MAE: {mae}\nMSE: {mse}\nRMSE: {rmse}\n')

def visualize_results(model, X_test, y_test):
    """ Visualizza le previsioni rispetto ai valori reali """
    predictions = model.predict(X_test)
    plt.scatter(y_test, predictions)
    plt.xlabel('Valori Reali')
    plt.ylabel('Previsioni')
    plt.title('Previsioni Random Forest vs Valori Reali')
    os.makedirs('evaluation_reports', exist_ok=True)
    plt.savefig('evaluation_reports/random_forest_predictions.png')
    plt.close()
    print('> Grafico delle previsioni salvato in evaluation_reports/random_forest_predictions.png')
