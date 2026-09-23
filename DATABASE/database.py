import sqlite3
from pathlib import Path


# Local onde o banco de dados será armazenado
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

DATABASE = DATA_DIR / "facilita.db"


def conectar():
	"""Cria uma conexão com o banco de dados."""
	return sqlite3.connect(DATABASE)


def criar_tabelas():
	"""Cria as tabelas iniciais do sistema."""

	conexao = conectar()
	cursor = conexao.cursor()

	# Tabela de usuários
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS usuarios (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			nome TEXT NOT NULL,
			email TEXT UNIQUE NOT NULL,
			senha TEXT NOT NULL,
			perfil TEXT NOT NULL
		)
	""")

	# Tabela de clientes
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS clientes (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			nome TEXT NOT NULL,
			tipo TEXT NOT NULL,
			municipio TEXT,
			responsavel TEXT,
			email TEXT,
			telefone TEXT,
			observacoes TEXT,
			ativo INTEGER DEFAULT 1
		)
	""")

	# Tabela de demandas
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS demandas (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			cliente_id INTEGER NOT NULL,
			titulo TEXT NOT NULL,
			descricao TEXT,
			status TEXT DEFAULT 'A Fazer',
			prioridade TEXT DEFAULT 'Normal',
			responsavel TEXT,
			prazo TEXT,
			criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
			concluido_em TEXT,
			FOREIGN KEY (cliente_id) REFERENCES clientes(id)
		)
	""")

	# Tabela de anotações
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS anotacoes (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			cliente_id INTEGER NOT NULL,
			autor TEXT NOT NULL,
			texto TEXT NOT NULL,
			criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (cliente_id) REFERENCES clientes(id)
		)
	""")

	conexao.commit()
	conexao.close()
