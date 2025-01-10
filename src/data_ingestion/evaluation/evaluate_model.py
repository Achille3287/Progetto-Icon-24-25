import pandas as pd
import os
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

def evaluate_model(true_values, predicted_values, output_dir='evaluation_reports'):
    """
    Valuta il modello confrontando i valori reali con i valori predetti.
    Calcola MAE, MSE, RMSE e genera un grafico Predizione vs. Valore Reale.

    Args:
        true_values (array-like): Valori reali.
        predicted_values (array-like): Valori predetti dal modello.
        output_dir (str): Directory dove salvare il report e i grafici.

    Returns:
        dict: Dizionario con i risultati di MAE, MSE, RMSE.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)

        # Calcolo delle metriche
        mae = mean_absolute_error(true_values, predicted_values)
        mse = mean_squared_error(true_values, predicted_values)
        rmse = np.sqrt(mse)

        # Report di valutazione
        report = {
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse
        }

        print(f'> Risultati della valutazione: MAE={mae:.4f}, MSE={mse:.4f}, RMSE={rmse:.4f}')

        # Salvataggio del report
        report_path = os.path.join(output_dir, 'evaluation_report.txt')
        with open(report_path, 'w') as f:
            f.write('--- Report di Valutazione del Modello ---\\n')
            f.write(f'MAE: {mae:.4f}\\n')
            f.write(f'MSE: {mse:.4f}\\n')
            f.write(f'RMSE: {rmse:.4f}\\n')

        print(f'> Report salvato con successo in: {report_path}')

        # Generazione del grafico Predizioni vs. Valori Reali
        plt.figure(figsize=(8, 6))
        plt.scatter(true_values, predicted_values, alpha=0.5, label='Predetto vs. Reale')
        plt.plot([min(true_values), max(true_values)], [min(true_values), max(true_values)], color='red', linestyle='--', label='Perfetto')
        plt.xlabel('Valori Reali')
        plt.ylabel('Valori Predetti')
        plt.title('Confronto Valori Reali vs. Valori Predetti')
        plt.legend()
        plot_path = os.path.join(output_dir, 'prediction_vs_real.png')
        plt.savefig(plot_path)
        plt.close()

        print(f'> Grafico salvato con successo in: {plot_path}')

        return report

    except Exception as e:
        print(f'Errore durante la valutazione del modello: {e}')
        return None
