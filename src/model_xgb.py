import os
import xgboost as xgb
import pandas as pd
import pymysql
import optuna
import shap
from datetime import datetime
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score

def cargar_datos_desde_mysql():
    load_dotenv()

    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    query = "SELECT * FROM nombre_tabla"

    df = pd.read_sql(query, connection)

    connection.close()

    X = df.drop(columns=['depresion'])  # Variables independientes
    y = df['depresion']  # Variable objetivo


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test


def objective(trial, X_train, y_train, X_test, y_test):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_loguniform('learning_rate', 0.01, 0.3),
        'colsample_bytree': trial.suggest_uniform('colsample_bytree', 0.5, 1.0),
        'subsample': trial.suggest_uniform('subsample', 0.5, 1.0),
        'gamma': trial.suggest_loguniform('gamma', 1e-8, 1.0),
        'lambda': trial.suggest_loguniform('lambda', 1e-8, 10.0),
        'alpha': trial.suggest_loguniform('alpha', 1e-8, 10.0),
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
    }
    
    model = xgb.XGBClassifier(**params)
    model.fit(X_train, y_train)

    y_pred = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred)
    
    return auc 

def entrenar_con_optuna(X_train, y_train, X_test, y_test, n_trials=50):
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X_train, y_train, X_test, y_test), n_trials=n_trials)

    best_params = study.best_params
    print(f"Mejores hiperparámetros encontrados: {best_params}")

    model_final = xgb.XGBClassifier(**best_params)
    model_final.fit(X_train, y_train)
    
    return model_final, best_params, study.best_value

def calcular_shap_values(model, X_test):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    return shap_values


def guardar_metricas(auc):
    fecha = datetime.now().strftime('%Y-%m-%d')
    with open('metricas_modelo.txt', 'a') as f:
        f.write(f"{fecha}, AUC: {auc:.2f}\n")


def guardar_shap_importance(shap_values, X_test):
    shap_importance = pd.DataFrame(shap_values, columns=X_test.columns)
    shap_importance_mean = shap_importance.abs().mean().sort_values(ascending=False)
    shap_importance_mean.to_csv('shap_importance.csv')

def entrenar_y_evaluar():
    X_train, X_test, y_train, y_test = cargar_datos_desde_mysql()

    print("Iniciando optimización de hiperparámetros con Optuna...")
    modelo, mejores_params, mejor_auc = entrenar_con_optuna(X_train, y_train, X_test, y_test)

    auc = roc_auc_score(y_test, modelo.predict_proba(X_test)[:, 1])
    print(f"AUC reevaluado: {auc:.2f}")

    guardar_metricas(auc, mejores_params)

    shap_values = calcular_shap_values(modelo, X_test)

    guardar_shap_importance(shap_values, X_test)

if __name__ == "__main__":
    entrenar_y_evaluar()