import random as rand
import pandas as pd
import numpy as np
from faker import Faker

def generar_encuestas(num_encuestas):
    encuestas = []
    for _ in range(num_encuestas):
        encuesta = {
            'tristeza': rand.randint(0, 3),
            'pesimismo': rand.randint(0, 3),
            'fracaso': rand.randint(0, 3),
            'perdida_placer': rand.randint(0, 3),
            'culpa': rand.randint(0, 3),
            'castigo': rand.randint(0, 3),
            'disconformidad': rand.randint(0, 3),
            'autocritica': rand.randint(0, 3),
            'suicidio': rand.randint(0, 3),
            'llanto': rand.randint(0, 3),
            'agitacion': rand.randint(0, 3),
            'interes': rand.randint(0, 3),
            'indeciso': rand.randint(0, 3),
            'desvalorizacion': rand.randint(0, 3),
            'energia': rand.randint(0, 3),
            'irritabilidad': rand.randint(0, 3),
            'concentracion': rand.randint(0, 3),
            'cansancio': rand.randint(0, 3),
            'sexo': rand.randint(0, 3)
        }
        encuestas.append(encuesta)
        df_encuestas = pd.DataFrame(encuestas)
        df_encuestas['depresion'] = df_encuestas.sum(axis=1)
    return df_encuestas


def generar_usuarios(num_usuarios):
    usuarios = []
    for _ in range(num_usuarios):
        usuario = {
            'nombre': fake.name().lower(),
            'direccion': fake.address().lower(),
            'correo': fake.email().lower(),
            'telefono': fake.phone_number(),
            'profesion': fake.job().lower(),
            'genero': rand.choices(['masculino', 'femenino', 'intergenero', 'nc'], weights=[0.45, 0.45, 0.05, 0.05])[0],
            'edad': rand.randint(18, 65),
            'password': fake.password(),
            'encuesta': rand.choice(['si', 'no'])
        }
        usuarios.append(usuario)
        df_usuarios = pd.DataFrame(usuarios)
    return df_usuarios

def generar_mentores(num_mentores):
    mentores = []
    for _ in range(num_mentores):
        mentor = {
            'nombre': fake.name().lower(),
            'apellidos': fake.last_name().lower(),
            'correo': fake.email().lower(),
            'telefono': fake.phone_number(),
            'profesion': 'psicológo',
            'genero': rand.choices(['masculino', 'femenino', 'intergenero', 'nc'], weights=[0.45, 0.45, 0.05, 0.05])[0],
            'edad': rand.randint(18, 65),
            'password': fake.password(),
            'eventos': rand.choice(['si', 'no'])
        }
        mentores.append(mentor)
        df_mentores = pd.DataFrame(mentores)
    return df_mentores


if __name__ == '__main__':
    fake = Faker('es_ES')
    df_usuarios = generar_usuarios(1000)
    df_mentores = generar_mentores(100)
    df_encuestas = generar_encuestas(300)
    df_usuarios.to_csv('data/usuarios.csv', index=False)
    df_mentores.to_csv('data/mentores.csv', index=False)
    df_encuestas.to_csv('data/encuestas.csv', index=False)
    print('Datos generados y guardados exitosamente')
