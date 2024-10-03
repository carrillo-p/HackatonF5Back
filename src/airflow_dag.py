from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import model_xgb  # Tu script

# Definir los argumentos predeterminados del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Crear el DAG para reentrenar el modelo mensualmente
dag = DAG(
    'mlops_reentrenamiento_mensual',
    default_args=default_args,
    description='Pipeline de reentrenamiento del modelo cada mes',
    schedule_interval='@monthly',
)

# Definir la tarea para ejecutar el reentrenamiento
reentrenar_modelo = PythonOperator(
    task_id='reentrenar_modelo',
    python_callable=model_xgb.entrenar_y_evaluar,
    dag=dag,
)