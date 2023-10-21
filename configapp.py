import json

def load_configurations(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            configuracoes = json.load(arquivo)
        return configuracoes
    except FileNotFoundError:
        print(f"O arquivo {nome_arquivo} não foi encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"O arquivo {nome_arquivo} não é um JSON válido.")
        return None