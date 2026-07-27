import psycopg2
import os
import sys

#Criei essa função porque o IP do computador mudava toda hora, então utilizo o arquivo config.txt na pasta do servidor para que todo mundo tenha acesso e mude quando necessáro
def carregar_configuracoes(nome_arquivo="config.txt"):
    configs = {}
    try:
        # Garante que o script procure o arquivo na pasta do executável
        caminho_base = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
        caminho_arquivo = os.path.join(caminho_base, nome_arquivo)

        with open(caminho_arquivo, "r") as f:
            for linha in f:
                if "=" in linha:
                    chave, valor = linha.strip().split("=", 1)
                    configs[chave] = valor
        return configs
    except FileNotFoundError:
        print(f"Erro: O arquivo {nome_arquivo} não foi encontrado na pasta do programa.")
        return None

#função conectar simples, coisa do SQL
def conectar():
    config = carregar_configuracoes()
    
    if not config:
        return None

    try: 
        conexao = psycopg2.connect(
            host=config.get("host"),
            database=config.get("database"),
            user=config.get("user"),
            password=config.get("password"),
            connect_timeout=5
        )
        print(f"Conectado com sucesso {config.get('host')}")
        return conexao
    except Exception as e:
        print(f"Erro ao conectar no banco de dados: {e}")
        return None

# Uso:
conexao = conectar()