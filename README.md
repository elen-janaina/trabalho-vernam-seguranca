# trabalho-vernam-seguranca
Implementação do Cifrador de Vernam (One-Time Pad) com Docker Compose

# Trabalho de Segurança da Informação

Este projeto é uma implementação do Cifrador de Vernam (One-Time Pad) em Python

O programa demonstra a cifragem e decifragem de arquivos, a geração de visualizações binárias e a análise de risco da reutilização de chaves (ataque "Two-Time Pad"). O projeto está containerizado com Docker para garantir a reprodutibilidade.

## Requisitos

- Docker
- Docker Compose

## Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com//elen-janaina/trabalho-vernam-seguranca.git
    cd trabalho-vernam-seguranca
    ```

2.  **Inicie o container Docker:**
    (Certifique-se de que o Docker Desktop está em execução )
    ```bash
    docker-compose up --build -d
    ```

3.  **Acesse o terminal do container:**
    ```bash
    docker exec -it vernam_app bash
    ```

4.  **Execute os comandos dentro do container:**

**Para cifrar um arquivo:**
        ```bash
        python vernam_cifrador.py cifrar <arquivo_mensagem> <arquivo_chave> <arquivo_cifrado>
        # Exemplo:
        python vernam_cifrador.py cifrar mensagem.txt chave.key cifrado.bin
        ```

**Para decifrar um arquivo:**
        ```bash
        python vernam_cifrador.py decifrar <arquivo_cifrado> <arquivo_chave> <arquivo_decifrado>
        # Exemplo:
        python vernam_cifrador.py decifrar cifrado.bin chave.key decifrado.txt
        ```
**Para demonstrar o ataque Two-Time Pad:**
        ```bash
        python vernam_cifrador.py two-time-pad <mensagem1> <mensagem2> <chave_reutilizada>
        # Exemplo:
        python vernam_cifrador.py two-time-pad mensagem.txt mensagem2.txt otp_reutilizada.key
        ```

## Estrutura do Projeto

-   `vernam_cifrador.py`: Script principal com a lógica do cifrador
-   `criar_binario.py`: Script auxiliar para gerar um arquivo binário de teste
-   `mensagem.txt`, `mensagem2.txt`, `meu_arquivo_binario.bin`: Arquivos de exemplo para testes
-   `Dockerfile`: Define o ambiente do container
-   `docker-compose.yml`: Orquestra a execução do container.
-   `requirements.txt`: Lista as dependências Python.
