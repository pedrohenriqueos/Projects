
USE PROJETO;

SELECT NOME,EMAIL FROM CLIENTE WHERE NOME='JORGE';
SELECT NOME,EMAIL FROM CLIENTE WHERE SEXO='F';

SELECT NOME,SEXO FROM CLIENTE WHERE ENDERECO LIKE '%RJ';

SELECT NOME,SEXO,ENDERECO FROM CLIENTE WHERE ENDERECO LIKE '%CENTRO%';

/*
LIKE REDUZ A PERFORMACE, UTILIZAR APENAS QUANDO REALMENTE NECESSÁRIO.
*/
SELECT NOME,ENDERECO FROM CLIENTE WHERE SEXO='M' OR (ENDERECO LIKE '%RJ' AND ENDERECO='%CENTRO%');

SELECT NOME,EMAIL FROM CLIENTE WHERE SEXO='M' AND ENDERECO LIKE '%RJ';


SELECT COUNT(*) FROM CLIENTE;

SELECT COUNT(*) AS 'QUANTIDADE' FROM CLIENTE;

SELECT ENDERECO, COUNT(*) AS 'QUANTIDADE' FROM CLIENTE WHERE ENDERECO LIKE '%CENTRO%';

SELECT NOME, SEXO, ENDERECO
FROM CLIENTE
WHERE SEXO = 'F' OR ENDERECO LIKE '%RIO DE JANEIRO%';

/*
A ORDEM DE MULTIPLOS ELEMENTO COM O OPERADOR LOGICO OR
FAZ DIFERENÇA PARA MELHORAR A PERFORMACE DA QUERY
DAR SEMPRE PRIORIDADE PARA O QUE APARECE MAIS VEZES
NA TABELA.
*/
SELECT NOME FROM CLIENTE WHERE EMAIL IS NULL;

SELECT NOME FROM CLIENTE WHERE EMAIL IS NOT NULL;