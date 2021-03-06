
CREATE TABLE CURSOS(
	IDCURSO INT PRIMARY KEY AUTO_INCREMENT,
	NOME VARCHAR(30),
	HORAS INT,
	VALOR FLOAT(10,2),
	ID_PREREQ INT
);

ALTER TABLE CURSOS ADD CONSTRAINT FK_PREREQ
FOREIGN KEY(ID_PREREQ) REFERENCES CURSOS(IDCURSO);

INSERT INTO CURSOS VALUES(NULL,'BD RELACIONAL',20,400.0,NULL);
INSERT INTO CURSOS VALUES(NULL,'BUSINESS INTELIGENCE',40,800.0,1);
INSERT INTO CURSOS VALUES(NULL,'RELATORIO AVANCADOS',20,600.0,2);
INSERT INTO CURSOS VALUES(NULL,'LOGICA PROGRAM',20,400.0,NULL);
INSERT INTO CURSOS VALUES(NULL,'RUBY',30,500.0,4);

/* MINHA SOLUCAO */
CREATE VIEW V_RELATORIO AS
SELECT A.IDCURSO , A.NOME
FROM CURSOS A
INNER JOIN CURSOS B
ON B.ID_PREREQ = A.IDCURSO;

SELECT NOME,
       VALOR,
	   HORAS,
	   IFNULL((SELECT NOME FROM V_RELATORIO WHERE V_RELATORIO.IDCURSO=CURSOS.ID_PREREQ),'SEM REQUISITO') REQUISITO
FROM CURSOS;

/* SOLUCAO DO PROFESSOR */
SELECT C.NOME AS CURSO,
	   C.VALOR AS VALOR,
	   C.HORAS AS CARGA,
	   IFNULL(P.NOME,'---') AS PREREQ
FROM CURSOS C
LEFT JOIN CURSOS P /* UNIÃO DE CONJUNTOS, SELECIONA O LADO ESQUERDO DA UNIÃO */
ON P.IDCURSO = C.ID_PREREQ;