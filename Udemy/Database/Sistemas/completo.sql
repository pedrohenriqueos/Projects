/*
A ORDEM DAS COLUNAS É IMPORTANTE PARA A ORGANIZAÇÃO
NO BANCO DE DADOS
*/
CREATE DATABASE COMERCIO;

USE COMERCIO;

CREATE TABLE CLIENTE(
	IDCLIENTE INT PRIMARY KEY AUTO_INCREMENT,
	NOME VARCHAR(30) NOT NULL,
	SEXO ENUM('M','F') NOT NULL,
	EMAIL VARCHAR(50) UNIQUE,
	CPF VARCHAR(15) UNIQUE NOT NULL
);

CREATE TABLE TELEFONE(
	IDTELEFONE INT PRIMARY KEY AUTO_INCREMENT,
	TIPO ENUM('COM','RES','CEL'),
	DDD VARCHAR(5),
	NUMERO VARCHAR(10),
	ID_CLIENTE INT,
	FOREIGN KEY(ID_CLIENTE)
	REFERENCES CLIENTE(IDCLIENTE)
);

CREATE TABLE ENDERECO(
	IDENDERECO INT PRIMARY KEY AUTO_INCREMENT,
	CIDADE VARCHAR(30) NOT NULL,
	RUA VARCHAR(30) NOT NULL,
	ESTADO CHAR(2) NOT NULL,
	BAIRRO VARCHAR(30) NOT NULL,
	ID_CLIENTE INT UNIQUE,
	FOREIGN KEY(ID_CLIENTE)
	REFERENCES CLIENTE(IDCLIENTE)
);

