import sqlite3
import os

caminho_banco = "facilita.db"


if not os.path.exists(caminho_banco):
    print("Banco de dados não encontrado:", caminho_banco)
else:
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "ALTER TABLE itens_avaliacao ADD COLUMN ordem INTEGER DEFAULT 0"
        )
        print("Coluna ordem adicionada com sucesso.")
    except Exception as e:
        if "duplicate column name" in str(e).lower():
            print("A coluna ordem já existe. Nenhuma alteração necessária.")
        else:
            print("Aviso:", e)

    conn.commit()
    conn.close()

input("Pressione Enter para fechar...")