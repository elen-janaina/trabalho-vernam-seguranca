import os

# Define o nome do arquivo
nome_do_arquivo = "meu_arquivo_binario.bin"

# Define o tamanho do arquivo em bytes
tamanho_do_arquivo = 500

# Gera 500 bytes  aleatórios
dados_aleatorios = os.urandom(tamanho_do_arquivo)

# Abre o arquivo
with open(nome_do_arquivo, 'wb') as f:
    f.write(dados_aleatorios)

print(f"Arquivo binário '{nome_do_arquivo}' com {tamanho_do_arquivo} bytes foi criado")
