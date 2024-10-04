CREATE DATABASE IF NOT EXISTS safe_soul;
USE safe_soul;

-- Crear la tabla de usuarios
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(64) NOT NULL,
    name VARCHAR(100) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    profession VARCHAR(100),
    gender ENUM('masculino', 'femenino', 'intergenero', 'nc'),
    age INT,
    is_mentor BOOLEAN DEFAULT FALSE,
    wants_survey BOOLEAN DEFAULT FALSE,
    wants_events BOOLEAN DEFAULT FALSE
);

-- Crear la tabla de encuestas
CREATE TABLE surveys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    tristeza INT,
    pesimismo INT,
    fracaso INT,
    perdida_placer INT,
    culpa INT,
    castigo INT,
    disconformidad INT,
    autocritica INT,
    suicidio INT,
    llanto INT,
    agitacion INT,
    interes INT,
    indeciso INT,
    desvalorizacion INT,
    energia INT,
    irritabilidad INT,
    concentracion INT,
    cansancio INT,
    sexo INT,
    depresion INT

    FOREIGN KEY (user_id) REFERENCES users(id)
);