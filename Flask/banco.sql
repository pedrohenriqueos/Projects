CREATE DATABASE db;

USE db;

CREATE TABLE users(
	IDUSERS INT PRIMARY KEY AUTO_INCREMENT,
	nome VARCHAR(50) NOT NULL,
	senha VARCHAR(50) NOT NULL
);

CREATE TABLE quest(
	IDQUEST INT PRIMARY KEY AUTO_INCREMENT,
	link_prob VARCHAR(70) NOT NULL,
	ansOJ ENUM('AC','WA','TLE','MLE','RE') NOT NULL,
	link_sub VARCHAR(70),
	referencia ENUM('Y','N') NOT NULL,
	id_users INT NOT NULL, /* FOREIGN KEY */
	id_onlinejudge INT NOT NULL /* FOREIGN KEY */
);

CREATE TABLE OnlineJudge(
	IDONLINEJUDGE INT PRIMARY KEY AUTO_INCREMENT,
	nome VARCHAR(30)
);

ALTER TABLE quest ADD CONSTRAINT FK_quest_users
FOREIGN KEY(id_users) REFERENCES users(IDUSERS);

ALTER TABLE quest ADD CONSTRAINT FK_quest_Judge
FOREIGN KEY(id_onlinejudge) REFERENCES OnlineJudge(IDONLINEJUDGE);

INSERT INTO users VALUES(NULL,'pedro','teste');

INSERT INTO OnlineJudge VALUES(NULL,'codeforces'),(NULL,'URI'),(NULL,'neps'),(NULL,'SPOJ');

INSERT INTO quest (link_prob,ansOJ,link_sub,referencia,id_users,id_onlinejudge)
VALUES('https://codeforces.com/contest/1335/problem/A','AC','https://codeforces.com/contest/1335/submission/76502127','N',1,1),
('https://codeforces.com/contest/1335/problem/B','AC','N',1,1);

