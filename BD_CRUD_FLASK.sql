CREATE DATABASE crud;

CREATE TABLE prendasderopa (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE animales (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE comida (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE estudiantes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

INSERT INTO animales (nombre)
VALUES
('Perro'),
('Gato');

INSERT INTO comida (nombre)
VALUES
('Yapingacho'),
('Arepa');

INSERT INTO estudiantes (nombre)
VALUES
('Eryx'),
('Mateo');

INSERT INTO prendasderopa (nombre)
VALUES
('Camisa'),
('Pantalon');