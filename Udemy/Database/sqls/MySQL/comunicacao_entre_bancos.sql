
CREATE DATABASE LOJA;
USE LOJA;

CREATE TABLE PRODUTO(
	IDPRODUTO INT PRIMARY KEY AUTO_INCREMENT,
	NOME VARCHAR(30),
	VALOR FLOAT(10,2)
);

CREATE DATABASE P_BACKUP;

USE P_BACKUP;

CREATE TABLE BKP_PRODUTO(
	IDBKP INT PRIMARY KEY AUTO_INCREMENT,
	IDPRODUTO INT,
	NOME VARCHAR(30),
	VALOR FLOAT(10,2)
);

USE LOJA;

INSERT INTO P_BACKUP.BKP_PRODUTO VALUES(NULL,1000,'TESTE',0.0);

SELECT * FROM P_BACKUP.BKP_PRODUTO;

DELIMITER $
CREATE TRIGGER BACKUP_PRODUTO
BEFORE INSERT ON PRODUTO
FOR EACH ROW
BEGIN
	INSERT INTO P_BACKUP.BKP_PRODUTO
	VALUES(NULL,NEW.IDPRODUTO,NEW.NOME,NEW.VALOR);

END
$
DELIMITER ;

INSERT INTO PRODUTO VALUES(NULL,'LIVRO MODELAGEM',50.00);
INSERT INTO PRODUTO VALUES(NULL,'LIVRO BI',80.00);
INSERT INTO PRODUTO VALUES(NULL,'LIVRO ORACLE',70.00);
INSERT INTO PRODUTO VALUES(NULL,'LIVRO SQL SERVER',100.00);

SELECT * FROM PRODUTO;
SELECT * FROM P_BACKUP.BKP_PRODUTO;

DELIMITER $
CREATE TRIGGER BACKUP_PRODUTO_DEL
BEFORE DELETE ON PRODUTO
FOR EACH ROW
BEGIN

	INSERT INTO P_BACKUP.BKP_PRODUTO
	VALUES(NULL,OLD.IDPRODUTO,OLD.NOME,OLD.VALOR);

END
$
DELIMITER ;

DELETE FROM PRODUTO
WHERE IDPRODUTO=2;

SELECT * FROM P_BACKUP.BKP_PRODUTO;

DROP TRIGGER BACKUP_PRODUTO;

DELIMITER $
CREATE TRIGGER BACKUP_PRODUTO
AFTER INSERT ON PRODUTO
FOR EACH ROW
BEGIN
	INSERT INTO P_BACKUP.BKP_PRODUTO
	VALUES(NULL,NEW.IDPRODUTO,NEW.NOME,NEW.VALOR);

END
$
DELIMITER ;

INSERT INTO PRODUTO VALUES(NULL,'LIVRO C#',100.00);

SELECT * FROM PRODUTO;
SELECT * FROM P_BACKUP.BKP_PRODUTO;

ALTER TABLE P_BACKUP.BKP_PRODUTO
ADD EVENTO CHAR(1);

DROP TRIGGER BACKUP_PRODUTO_DEL;

DELIMITER $
CREATE TRIGGER BACKUP_PRODUTO_DEL
BEFORE DELETE ON PRODUTO
FOR EACH ROW
BEGIN

	INSERT INTO P_BACKUP.BKP_PRODUTO
	VALUES(NULL,OLD.IDPRODUTO,OLD.NOME,OLD.VALOR,'D');

END
$
DELIMITER ;

DELETE FROM PRODUTO WHERE IDPRODUTO = 4;

DROP TRIGGER BACKUP_PRODUTO;

DELIMITER $
CREATE TRIGGER BACKUP_PRODUTO
AFTER INSERT ON PRODUTO
FOR EACH ROW
BEGIN
	INSERT INTO P_BACKUP.BKP_PRODUTO
	VALUES(NULL,NEW.IDPRODUTO,NEW.NOME,NEW.VALOR,'I');

END
$
DELIMITER ;
