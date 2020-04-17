
/* REFINAMENTO DE QUERYS */

SELECT C.NOME,
	   IFNULL(C.EMAIL,'SEM EMAIL') AS 'EMAIL',
	   T.DDD,
	   T.NUMERO AS 'CELULAR'
FROM CLIENTE C 
INNER JOIN TELEFONE T
ON C.IDCLIENTE = T.ID_CLIENTE
INNER JOIN ENDERECO E
ON C.IDCLIENTE = E.ID_CLIENTE
WHERE T.TIPO = 'CEL' AND E.ESTADO = 'RJ';

+---------+----------------+------+---------+
| NOME    | EMAIL          | DDD  | CELULAR |
+---------+----------------+------+---------+
| JOAO    | JOAO@IG.COM    | 85   | 9955331 |
| JOAO    | JOAO@IG.COM    | 60   | 5765547 |
| ANTONIO | SEM EMAIL      | 85   | 5557798 |
| ANTONIO | SEM EMAIL      | 91   | 8865645 |
| CELIA   | JOAO@TERRA.COM | 85   | 7865644 |
+---------+----------------+------+---------+