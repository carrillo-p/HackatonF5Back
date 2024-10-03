import xgboost as xgb
import pandas as pd
import optuna
import shap
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error

df = pd.read_csv('data/encuestas.csv')

X = df.drop(columns=['depresion'])  # Variables independientes
y = df['depresion']  # Variable objetivo


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 300),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'gamma': trial.suggest_uniform('gamma', 0, 5),
        'reg_alpha': trial.suggest_uniform('reg_alpha', 0, 10),
        'reg_lambda': trial.suggest_uniform('reg_lambda', 0, 10),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'colsample_bytree': trial.suggest_uniform('colsample_bytree', 0.5, 1),
        'subsample': trial.suggest_uniform('subsample', 0.5, 1),  
        'learning_rate': trial.suggest_uniform('learning_rate', 0.01, 0.3),  
        'scale_pos_weight': trial.suggest_uniform('scale_pos_weight', 1, 10)
    }
    
    
    model = XGBRegressor(**params, eval_metric='rmse')
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    
    return mse

study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=100)

best_params = study.best_params
print(f"Mejores hiperparámetros: {best_params}")

model_final = XGBRegressor(**best_params, eval_metric='rmse')
model_final.fit(X_train, y_train)

y_pred_final = model_final.predict(X_test)

mse_final = mean_squared_error(y_test, y_pred_final)
print(f"Error cuadrático medio final: {mse_final}")

explainer = shap.Explainer(model_final)
shap_values = explainer.shap_values(X_test)

shap_importance = pd.DataFrame(shap_values, columns=X_test.columns)
shap_importance_mean = shap_importance.abs().mean().sort_values(ascending=False)
shap_importance_mean.to_csv('shap_importance.csv')
