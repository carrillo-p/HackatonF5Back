import pytest
import pandas as pd
from src.simulacion_datos import generar_encuestas, generar_usuarios, generar_mentores

def test_generar_encuestas():
    df = generar_encuestas(300)
    assert isinstance(df, pd.DataFrame), "El resultado debe ser un DataFrame"
    assert df.shape[0] == 300, "El DataFrame debe tener 100 filas"
    assert 'depresion' in df.columns, "El DataFrame debe tener una columna 'depresion'"
    assert df['depresion'].equals(df.drop(columns=['depresion']).sum(axis=1)), "La columna 'depresion' debe ser la suma de todas las demás columnas"

def test_generar_usuarios():
    df = generar_encuestas(1000)
    assert isinstance(df, pd.DataFrame), "El resultado debe ser un DataFrame"
    assert df.shape[0] == 1000, "El DataFrame debe tener 100 filas"

def test_generar_mentores():
    df = generar_encuestas(100)
    assert isinstance(df, pd.DataFrame), "El resultado debe ser un DataFrame"
    assert df.shape[0] == 100, "El DataFrame debe tener 100 filas"