-- Executar como administrador do MySQL, na primeira configuração.
CREATE DATABASE IF NOT EXISTS atividade CHARACTER SET utf8mb4;
CREATE USER IF NOT EXISTS 'aluno'@'localhost' IDENTIFIED BY 'senha_didatica';
GRANT ALL PRIVILEGES ON atividade.* TO 'aluno'@'localhost';
-- A tabela usuarios será criada pelo SQLAlchemy ao iniciar o FastAPI.
