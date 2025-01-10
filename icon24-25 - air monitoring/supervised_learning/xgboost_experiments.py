import pandas as pd
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import matplotlib.pyplot as plt

def run_experiment(data_path, model_output_path='models/xgboost_experiment.pkl'):
    data = pd.read_csv(data_path)
    X = data[['PM2.5', 'PM10', 'CO', 'SO2', 'NO2', 'O3', 'temperature', 'humidity', 'wind_speed']]
    y = data['PM2.5']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = XGBRegressor()
    model.fit(X_train, y_train)
    save_model(model, model_output_path)
    evaluate_model(model, X_test, y_test)
    visualize_results(model, X_test, y_test)

def tune_hyperparameters(X_train, y_train):
    param_grid = {'n_estimators': [100, 200, 300], 'learning_rate': [0.01, 0.1, 0.2], 'max_depth': [3, 6, 10]}
    grid_search = GridSearchCV(XGBRegressor(), param_grid, cv=3, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_

def save_model(model, model_output_path):
    joblib.dump(model, model_output_path)

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = mse ** 0.5
    print(f'MAE: {mae}, MSE: {mse}, RMSE: {rmse}')

def visualize_results(model, X_test, y_test):
    predictions = model.predict(X_test)
    plt.scatter(y_test, predictions)
    plt.xlabel('Valori Reali')
    plt.ylabel('Previsioni')
    plt.title('Previsioni XGBoost vs Valori Reali')
    plt.savefig('evaluation_reports/xgboost_predictions.png')
