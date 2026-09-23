import sqlite3

import pandas as pd


conn = sqlite3.connect("facilita.db")

tabelas = [
	"clientes",
	"almoxarifados",
	"controle_publicacoes",
	"demandas",
	"itens_avaliacao",
	"relatorios_avaliacao",
]

for tabela in tabelas:
	df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)
	arquivo = f"{tabela}.csv"
	df.to_csv(arquivo, index=False, encoding="utf-8-sig")
	print(f"Exportado: {arquivo}")

conn.close()

print("\nExportação concluída!")
