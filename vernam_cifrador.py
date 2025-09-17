import os  # Gerar chaves, manipular nomes de arquivos
import argparse  # Modos cifrar e decifrar
import math  # Para cálculos 
from PIL import Image  # Para criar e salvar as imagens

# Função que aplica a operação XOR
def aplicar_xor(bytes1, bytes2):
    # Resultado do XOR, byte a byte, entre os dois dados.
    return bytes([b1 ^ b2 for b1, b2 in zip(bytes1, bytes2)])

# Cria as imagens em preto e branco a partir de um arquivo
def gerar_visualizacao_binaria(arquivo_entrada, arquivo_saida_imagem):
    try:
        # Abre e le todos os bytes do arquivo de entrada
        with open(arquivo_entrada, 'rb') as f:
            dados_bytes = f.read()
        # Se o arquivo estiver vazio, avisa e para a função
        if not dados_bytes:
            print(f"Aviso:O arquivo '{arquivo_entrada}' está vazio")
            return

        # Converte a sequência de bytes em uma lista de bits (0s e 1s)
        bits = [int(b) for byte in dados_bytes for b in format(byte, '08b')]
        
        # Calcula as dimensões da imagem para que ela seja quadrada
        total_bits = len(bits)
        largura = int(math.sqrt(total_bits))
        altura = (total_bits + largura - 1) // largura

        # Cria uma nova imagem em escala de cinza 
        imagem = Image.new('L', (largura, altura), color=0)
        pixels = imagem.load()

        # Pinta cada pixel da imagem: preto para bit 0, branco para bit 1
        for i, bit in enumerate(bits):
            pixels[i % largura, i // largura] = bit * 255

        # Salva a imagem gerada no disco
        imagem.save(arquivo_saida_imagem)
        print(f"Visualização binária salva em '{arquivo_saida_imagem}'")
    # Erros caso o arquivo não seja encontrado
    except FileNotFoundError:
        print(f"Erro:Arquivo de entrada não encontrado em '{arquivo_entrada}'")
    # Erros durante a geração da imagem
    except Exception as e:
        print(f"Erro ao gerar visualização para {arquivo_entrada}: {e}")

# Modo cifrar
def cifrar(args):
    print("\n--- Modo cifrar ---")
    try:
        # Pega o nome do arquivo de entrada para usar nos nomes das imagens
        nome_base = os.path.splitext(os.path.basename(args.arquivo_entrada))[0]

        # Le a mensagem
        with open(args.arquivo_entrada, 'rb') as f:
            mensagem = f.read()
        print(f"Mensagem lida de '{args.arquivo_entrada}' ({len(mensagem)} bytes).")

        # Gera uma chave aleatória do mesmo tamanho da mensagem
        chave = os.urandom(len(mensagem))
        # Salva a chave em um arquivo
        with open(args.arquivo_chave, 'wb') as f: f.write(chave)
        print(f"Chave gerada e salva: {args.arquivo_chave}")

        # Cifra a mensagem usando a função XOR
        texto_cifrado = aplicar_xor(mensagem, chave)
        # Salva o resultado cifrado em um arquivo
        with open(args.arquivo_saida, 'wb') as f: f.write(texto_cifrado)
        print(f"Arquivo cifrado e salvo: {args.arquivo_saida}")

        # Chama a função para gerar as imagens da mensagem, chave e texto cifrado
        print("\n--- Gerando visualizações ---")
        gerar_visualizacao_binaria(args.arquivo_entrada, f'visual_{nome_base}_original.png')
        gerar_visualizacao_binaria(args.arquivo_chave, f'visual_{nome_base}_chave.png')
        gerar_visualizacao_binaria(args.arquivo_saida, f'visual_{nome_base}_cifrado.png')
    except FileNotFoundError:
        print(f"Erro: Arquivo de mensagem '{args.arquivo_entrada}' não encontrado")
    except Exception as e:
        print(f"Ocorreu um erro ao cifrar:{e}")

# Função para o modo decifrar
def decifrar(args):
    print("\n--- Modo decifrar ---")
    try:
        # Pega o nome do arquivo para nomear a imagem de saída
        nome_base = os.path.splitext(os.path.basename(args.arquivo_entrada))[0]

        # Le o arquivo cifrado e o arquivo da chave.
        with open(args.arquivo_entrada, 'rb') as f: texto_cifrado = f.read()
        with open(args.arquivo_chave, 'rb') as f: chave = f.read()
        
        # Garante que a chave e o texto cifrado tem o mesmo tamanho
        if len(texto_cifrado) != len(chave):
            raise ValueError("Erro: Arquivo cifrado e chave devem ter o mesmo tamanho")

        # Decifra o texto aplicando o XOR novamente
        texto_decifrado = aplicar_xor(texto_cifrado, chave)
        # Salva a mensagem original recuperada
        with open(args.arquivo_saida, 'wb') as f: f.write(texto_decifrado)
        print(f"Arquivo decifrado e salvo em: {args.arquivo_saida}")
        
        # Gera a visualização do arquivo decifrado para confirmar que é igual ao original
        print("\n--- Gerando visualização ---")
        gerar_visualizacao_binaria(args.arquivo_saida, f'visual_{nome_base}_decifrado.png')
    except FileNotFoundError:
        print(f"Erro: Arquivo '{args.arquivo_entrada}' ou '{args.arquivo_chave}' não encontrado")
    except Exception as e:
        print(f"Ocorreu um erro ao decifrar:{e}")

# Mostra o ataque two-time pad
def demonstrar_two_time_pad(args):
    print("\n--- TWO-TIME PAD ---")
    try:
        # Le as duas mensagens
        with open(args.mensagem1, 'rb') as f: m1 = f.read()
        with open(args.mensagem2, 'rb') as f: m2 = f.read()

        # Usa o menor tamanho entre as duas mensagens para a analisar
        tamanho = min(len(m1), len(m2))
        if tamanho < 200: print(f"Aviso: Mensagens com menos de 200 bytes ({tamanho} bytes)")
        if tamanho == 0: raise ValueError("Arquivos de mensagem não podem estar vazios")
        m1, m2 = m1[:tamanho], m2[:tamanho]
        print(f"Analisando os primeiros {tamanho} bytes de '{args.mensagem1}' e '{args.mensagem2}'")

        # Gera UMA UNICA chave para ser reutilizada
        chave = os.urandom(tamanho)
        with open(args.arquivo_chave, 'wb') as f: f.write(chave)
        print(f"Chave única reutilizada salva em '{args.arquivo_chave}'")

        # Cifra as DUAS mensagens com a MESMA chave
        c1, c2 = aplicar_xor(m1, chave), aplicar_xor(m2, chave)
        with open('c1_resultado_ataque.bin', 'wb') as f: f.write(c1)
        with open('c2_resultado_ataque.bin', 'wb') as f: f.write(c2)

        # Simula o ataque: faz o XOR entre os dois textos cifrados
        c1_xor_c2 = aplicar_xor(c1, c2)
        # Faz o XOR entre as duas mensagens originais para provar a teoria
        m1_xor_m2 = aplicar_xor(m1, m2)

        # Compara os resultados para confirmar a vulnerabilidade
        if c1_xor_c2 == m1_xor_m2:
            print("\nSUCESSO: Prova C1 \u2295 C2 = M1 \u2295 M2 confirmada!")
            print("A chave foi eliminada, vazando informações sobre as mensagens originais")
            with open('resultado_ataque_xor.bin', 'wb') as f: f.write(c1_xor_c2)
        
            # Gera as imagens que provam visualmente o vazamento de informacao
            print("\n--- Gerando visualizações da análise ---")
            gerar_visualizacao_binaria(args.mensagem1, 'visual_ataque_m1.png')
            gerar_visualizacao_binaria(args.mensagem2, 'visual_ataque_m2.png')
            gerar_visualizacao_binaria('resultado_ataque_xor.bin', 'visual_ataque_resultado_xor.png')
            print("\nANÁLISE: Abra 'visual_ataque_resultado_xor.png'. Pixels pretos indicam onde as mensagens originais eram IGUAIS. Isso é vazamento de informação!")
        else:
            print("\nFALHA na prova C1 \u2295 C2 = M1 \u2295 M2.")
    except FileNotFoundError:
        print(f"Erro: Arquivo '{args.mensagem1}' ou '{args.mensagem2}' não encontrado")
    except Exception as e:
        print(f"Ocorreu um erro no modo two-time-pad: {e}")

if __name__ == "__main__":
    # Cria o "parser" principal
    parser = argparse.ArgumentParser(description="Implementação do Cifrador de Vernam com visualização e análise de risco")
    # Cria os sub-comandos
    subparsers = parser.add_subparsers(dest='modo', required=True, help="Modo de operação")

    # Define o comando cifrar e seus argumentos 
    p_cifrar = subparsers.add_parser('cifrar', help="Cifra um arquivo")
    p_cifrar.set_defaults(func=cifrar)
    p_cifrar.add_argument('arquivo_entrada', help="Arquivo da mensagem (ex: mensagem.txt)")
    p_cifrar.add_argument('arquivo_chave', help="Nome para o arquivo da chave (ex: chave.key)")
    p_cifrar.add_argument('arquivo_saida', help="Nome para o arquivo cifrado (ex: cifrado.bin)")

    # Define o comando decifrar e seus argumentos
    p_decifrar = subparsers.add_parser('decifrar', help="Decifra um arquivo")
    p_decifrar.set_defaults(func=decifrar)
    p_decifrar.add_argument('arquivo_entrada', help="Arquivo cifrado (ex: cifrado.bin)")
    p_decifrar.add_argument('arquivo_chave', help="Arquivo da chave (ex: chave.key)")
    p_decifrar.add_argument('arquivo_saida', help="Nome para o arquivo decifrado (ex: decifrado.txt)")

    # Define o comando two-time-pad 
    p_ttp = subparsers.add_parser('two-time-pad', help="Demonstra o risco de reutilizar uma chave")
    p_ttp.set_defaults(func=demonstrar_two_time_pad)
    p_ttp.add_argument('mensagem1', help="Primeiro arquivo de mensagem (ex: mensagem.txt)")
    p_ttp.add_argument('mensagem2', help="Segundo arquivo de mensagem (ex: mensagem2.txt)")
    p_ttp.add_argument('arquivo_chave', help="Nome para a chave reutilizada (ex: chave_reutilizada.key)")

    # Le o que o usuário digitou no terminal
    args = parser.parse_args()
    # Chama a funcao correspondente ao modo escolhido pelo usuário 
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
