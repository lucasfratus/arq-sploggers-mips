import io

# Simulador de Arquitetura de Computadores

""" 
A arquitetura deve ter 32 registradores de uso geral de 64 bits cada (8 bytes);
◦ Os registradores devem ser nomeados de r0 até r31;
    ▪ Inicialmente todos eles devem conter o valor 0;
◦ É obrigatório o uso dos registradores de estado/uso específico;
    ▪ PC - Contador de programa;
    ▪ RSP - Ponteiro de pilha;
    ▪ RA - Endereço de retorno;
    ▪ OF - Registrador de 1 bit para indicar se houve overflow na última operação; 

Conjunto de instruções:
• As instruções aritméticas e de desvio só podem ter seus operandos endereçados de duas maneiras:
    ◦ Endereçamento direto por registrador;
    ◦ Endereçamento por imediato;
• As instruções de acesso à memória deverão ter um operando com endereçamento direto por registrador e um operando com endereçamento por deslocamento;
• O formato e significado das instruções que deverão ser implementadas são exibidos na Tabela 1;
• Todas as instruções deverão operar somente sobre os registradores de uso geral (r0, r1, ..., r31) e o ponteiro de pilha (RSP);
◦ Ou seja, os registradores de Overflow (OF), contador de programa PC, e endereço de retorno (RA) não devem ser manipulados diretamente pelo
programador assembly (algumas instruções irão realizar a manipulação de tais registradores);
• As operações devem ser realizadas somente com valores inteiros;
• As instruções deverão ser de tamanho fixo e deverão ter 64 bits cada (ou seja, 8 bytes);

Memória:
• A arquitetura deve ter memória estruturada em dois níveis, uma memória cache, separada em dados e instruções, e uma memória principal;
• Cada endereço de memória (tanto da principal, quanto da cache de dados ou da cache de instruções) deverá armazenar 8 bytes (ou seja, uma instrução ou um inteiro).
Obs: A limitação de 8 bytes não impede que as estruturas usadas para representar cada célula de memória possua mais informações
• A cache deve ser associativa por conjunto:
    ◦ O número de bytes por linha, linhas por conjunto e número total de conjuntos deve ser configurável;
▪ O tamanho total da cache é dado pelo produto desses 3 elementos;
◦ Use os mesmos valores para as caches de dados e instruções;
◦ Para facilidade com a manipulação dos dados da memória, o número de bytes por linha deve ser múltiplo de 8;
    ▪ Caso a dupla prefira, pode utilizar o número de palavras por linha.
    ▪ O valor máximo para bytes por linha deve ser de 1024 (no caso de palavras por linha, o valor máximo de palavras por linha deve ser 128);
Obs: A limitação de 1024 bytes por linha é referente aos dados armazenados na cache. Na implementação do simulador, estruturas auxiliares podem ser modeladas para auxiliar o controle da cache;
◦ A memória principal deverá ter seu tamanho configurável em número de bytes (também deve ser múltiplo de 8) e deverá ser maior que a memória cache;
    ▪ Caso a dupla prefira, a memória principal também pode ser configurada em número de palavras da memória.
    ▪ A medida adotada deve ser a mesma para cache e memória principal
    • Se a cache é configurada por palavras, a memória principal também deve ser medida em palavras;
    • Se a cache é configurada por bytes, a memória principal deverá ser medida em bytes
    • Caso a dupla deseje, esta opção pode ser um argumento do programa, porém, isso não é obrigatório;

Entradas:
• A entrada principal do programa deverá ser um arquivo de texto contendo um conjunto de instruções a serem executadas, onde cada instrução ocupa uma linha do arquivo.
• Alguns exemplos estão disponíveis no mesmo tópico desta especificação.
• As configurações tais como memória cache e memória principal devem ser feitas preferencialmente por argumentos passados na linha de comando, ou então um arquivo de configuração que informa esses valores

Saídas:
• A cada ciclo de instrução deverão ser exibidos na tela:
◦ Os valores armazenados na memória cache;
    ▪ Não é necessário mostrar endereços que não estejam ocupados com dados que façam parte do programa;
    ▪ Os valores exibidos devem ser separados por dados e instruções;
    ▪ As instruções podem ser mostradas na sua forma textual;
◦ Os valores armazenados em cada endereço da memória;
    ▪ As instruções podem ser mostradas na sua forma textual;
◦ Os valores armazenados em cada um dos registradores de uso geral;
◦ Os valores armazenados em cada um dos registradores de controle de
estado;
"""


# Configurações da memória cache
# N_BYTES_POR_LINHA = 16 # Deve ser múltiplo de 8 e menor que 1024 (cada instrução ou inteiro ocupa no máximo 8 bytes)
# N_LINHAS_POR_CONJUNTO = 2
# N_CONJUNTOS = 2

# Configurações da memória principal
# N_BYTES_MEMORIA_PRINCIPAL = 256 # Deve ser múltiplo de 8 e maior que a memória cache



def leitura_arquivo_configuracao():
    '''
    É necessário que o arquivo de configuração esteja no mesmo diretório que o arquivo principal e que o nome seja 'arq_configuracao.txt'
    '''
    arq_configuracao = open('arq_configuracao.txt', 'r')
    linha = arq_configuracao.readlines()

    global N_BYTES_MEMORIA_PRINCIPAL
    N_BYTES_MEMORIA_PRINCIPAL = int(linha[1].split('=')[1])

    global N_BYTES_POR_LINHA
    N_BYTES_POR_LINHA = int(linha[4].split('=')[1])
    
    global N_LINHAS_POR_CONJUNTO
    N_LINHAS_POR_CONJUNTO = int(linha[6].split('=')[1])

    global N_CONJUNTOS
    N_CONJUNTOS = int(linha[8].split('=')[1])
    
    global N_BLOCOS
    N_BLOCOS = N_BYTES_MEMORIA_PRINCIPAL // N_BYTES_POR_LINHA
    
    global N_LINHAS_BLOCO
    N_LINHAS_BLOCO = (N_BYTES_MEMORIA_PRINCIPAL // 8) // N_BLOCOS

def inicializa_memoria_cache() -> dict:
    conjuntos: dict = {}
    for i in range(N_CONJUNTOS):
        conjuntos[i] = []
        for j in range(N_LINHAS_POR_CONJUNTO):
            conjuntos[i].append([-1, 0, [0] * (N_BYTES_POR_LINHA // 8)]) # [bloco, N_Acessos, [dados]]
    return conjuntos


def inicializa_memoria_principal() -> list:
    return [0] * (N_BYTES_MEMORIA_PRINCIPAL // 8)


def le_instrucoes(arquivo: str) -> list:
    with open(arquivo, 'r') as f:
        instrucoes = f.readlines()
    return instrucoes


def carrega_memoria_principal(memoria_principal: list) -> int:
    instrucoes = le_instrucoes(input('Digite o nome do arquivo de instruções: '))
    for i, instrucao in enumerate(instrucoes):
        instrucao = instrucao.strip()
        memoria_principal[i] = instrucao
    return i + 1 # Retorna o endereço da última instrução


def busca(endereco: int, cache: dict, memoria_principal: list) -> str:
    '''
    Recebe o contador de programa e a memória cache de instruções
    Retorna a instrução que está no endereço PC
    Segue a política de substituição LFU (Least Frequently Used)
    '''
    bloco = endereco // N_LINHAS_BLOCO
    conjunto = bloco % N_CONJUNTOS

    for linha in cache[conjunto]:
        if linha[0] == bloco:
            print(f'Hit')
            linha[1] += 1
            return linha[2][endereco % N_LINHAS_BLOCO]

    # Se não encontrou a instrução na cache, busca na memória principal
    print(f'Miss')
    bloco_dados = []
    for i in range(N_LINHAS_BLOCO):
        bloco_dados.append(memoria_principal[bloco * N_LINHAS_BLOCO + i])

    # Insere a instrução na cache

    # Verifica se há espaço vazio na cache
    for linha in cache[conjunto]:
        if linha[0] == -1:
            linha[0] = bloco
            linha[1] = 1
            linha[2] = bloco_dados
            return bloco_dados[endereco % N_LINHAS_BLOCO]
        
    # Se não houver espaço vazio, substitui a linha com menor número de acessos
    menor_acessos = cache[conjunto][0][1]
    linha_menor_acessos = 0
    for i, linha in enumerate(cache[conjunto]):
        if linha[1] < menor_acessos:
            menor_acessos = linha[1]
            linha_menor_acessos = i
    cache[conjunto][linha_menor_acessos][0] = bloco
    cache[conjunto][linha_menor_acessos][1] = 1
    cache[conjunto][linha_menor_acessos][2] = bloco_dados
    return bloco_dados[endereco % N_LINHAS_BLOCO]


def decodifica_instrucao(instrucao: str) -> tuple[str, list[str]]:
    '''
    Recebe instruções em formato:
        movi r6,144
        movi r1,5
        add r9,r1,r6
        addi r15,r9,1 
        movi r7,7
        add r13,r15,r7
        <instrução> <operando1>,<operando2>,<operando3>
    Retorna uma tupla com a instrução e os operandos em uma lista
    '''
    linha = instrucao.split(' ')

    operacao = linha[0]
    if len(linha) > 1:
        operandos = linha[1].split(',')
    else:
        operandos = []

    return operacao, operandos


def executa_instrucao(instrucao: str, memoria_principal: list, cache_dados: dict,  operandos: list[str], registradores: dict, PC: int, RSP: int, RA: int, OF: int) -> tuple[dict, int, int, int, int]:
    '''
    Executa a instrução com os operandos fornecidos.
    '''
    match instrucao:
        case 'add':
            registradores[operandos[0]] = registradores[operandos[1]] + registradores[operandos[2]]
            if registradores[operandos[0]] > 2**32 - 1 or registradores[operandos[0]] < -2**32:
                OF = 1
        case 'addi':
            registradores[operandos[0]] = registradores[operandos[1]] + int(operandos[2])
            if registradores[operandos[0]] > 2**32 - 1 or registradores[operandos[0]] < -2**32:
                OF = 1
        case 'sub':
            registradores[operandos[0]] = registradores[operandos[1]] - registradores[operandos[2]]
            if registradores[operandos[0]] > 2**32 - 1 or registradores[operandos[0]] < -2**32:
                OF = 1
        case 'subi':
            registradores[operandos[0]] = registradores[operandos[1]] - int(operandos[2])
            if registradores[operandos[0]] > 2**32 - 1 or registradores[operandos[0]] < -2**32:
                OF = 1
        case 'mul':
            registradores[operandos[0]] = registradores[operandos[1]] * registradores[operandos[2]]
            if registradores[operandos[0]] > 2**32 - 1 or registradores[operandos[0]] < -2**32:
                OF = 1
        case 'div':
            registradores[operandos[0]] = registradores[operandos[1]] // registradores[operandos[2]]
        case 'not': # Inverte os bits
            registradores[operandos[0]] = ~registradores[operandos[1]]
        case 'or':
            registradores[operandos[0]] = registradores[operandos[1]] | registradores[operandos[2]]
        case 'and':
            registradores[operandos[0]] = registradores[operandos[1]] & registradores[operandos[2]]
        case 'mov':
            registradores[operandos[0]] = registradores[operandos[1]]
        case 'movi':
            print(operandos[0])
            registradores[operandos[0]] = int(operandos[1])
        case 'blti':
            if registradores[operandos[0]] < int(operandos[1]):
                PC = int(operandos[2]) - 1 # Decrementa 1 pois o PC é incrementado em 1 no final do ciclo
        case 'bgti':
            if registradores[operandos[0]] > int(operandos[1]):
                PC = int(operandos[2]) - 1 # Decrementa 1 pois o PC é incrementado em 1 no final do ciclo
        case 'beqi':
            if registradores[operandos[0]] == int(operandos[1]):
                PC = int(operandos[2]) - 1 # Decrementa 1 pois o PC é incrementado em 1 no final do ciclo
        case 'blt':
            if registradores[operandos[0]] < registradores[operandos[1]]:   
                PC = int(operandos[2]) - 1 # Decrementa 1 pois o PC é incrementado em 1 no final do ciclo
        case 'bgt':
            if registradores[operandos[0]] > registradores[operandos[1]]:
                PC = registradores[operandos[2]] - 1 # Decrementa 1 pois o PC é incrementado em 1 no final do ciclo
        case 'beq':
            if registradores[operandos[0]] == registradores[operandos[1]]:
                PC = registradores[operandos[2]] - 1 # Decrementa 1 pois o PC é incrementado em 1 no final do ciclo
        case 'jr':
            PC = registradores[operandos[2]] - 1 # Decrementa 1 pois o PC é incrementado em 1 no final do ciclo
        case 'jof':
            if OF:
                PC = registradores[operandos[2]] - 1 # Decrementa 1 pois o PC é incrementado em 1 no final do ciclo
        case 'jal':
            RSP -= 1
            memoria_principal[RSP] = PC
            RA = PC
            PC = int(operandos[0]) - 1 # Decrementa 1 pois o PC é incrementado em 1 no final do ciclo
        case 'ret':
            if RSP < N_BYTES_MEMORIA_PRINCIPAL // 8:
                PC = memoria_principal[RSP]
                memoria_principal[RSP] = 0
                RSP += 1
            else:
                raise Exception('Pilha vazia, função não pode ser retornada')
        case 'lw':
            reg_end = operandos[1].split('(')[1].split(')')[0] # Registrador de endereço dentro dos parênteses
            end = int(operandos[1].split('(')[0]) + registradores[reg_end] # Endereço final -> valor do registrador + deslocamento
            
            registradores[operandos[0]] = busca(end, cache_dados, memoria_principal)
        case 'sw':
            reg_end = operandos[1].split('(')[1].split(')')[0] # Registrador de endereço dentro dos parênteses
            end = int(operandos[1].split('(')[0]) + registradores[reg_end] # Endereço final -> valor do registrador + deslocamento


            bloco = end // N_LINHAS_BLOCO
            conjunto = bloco % N_CONJUNTOS

            for linha in cache_dados[conjunto]: # Verifica se o bloco está na cache
                if linha[0] == bloco:
                    linha[2][end % N_LINHAS_BLOCO] = registradores[operandos[0]] # Atualiza o valor na cache
                    break

            memoria_principal[end] = registradores[operandos[0]] # Atualiza o valor na memória principal
            

    return registradores, PC, RSP, RA, OF


def main():

    # Variáveis globais
    leitura_arquivo_configuracao() # Lê as configurações das memórias
    # Registradores de uso geral
    registradores = {f'r{i}': 0 for i in range(32)}
    registradores['RSA'] = 0 # Registrador 'Safe address' para auxiliar instruções de acesso à memória -> Armazena a linha final dos endereços utilizados para as instruções

    # Registradores de estado/uso específico
    PC = 0
    RSP = N_BYTES_MEMORIA_PRINCIPAL // 8 # Ponteiro de pilha, inicia em len(tamanho_memoria_principal) -> fora da memória
    RA = 0
    OF = 0

    # Memória cache -> segue o modelo de cache associativa por conjunto e politica de substituição LFU (Least Frequently Used)
    cache_dados = inicializa_memoria_cache()
    cache_instr = inicializa_memoria_cache()

    # Memória principal
    memoria_principal = inicializa_memoria_principal()
    RSA = carrega_memoria_principal(memoria_principal)
    
    # Leitura das instruções
    while PC < RSA:
        linha = busca(PC, cache_instr, memoria_principal) # Busca a instrução na memória cache de instruções
        instrucao, operandos = decodifica_instrucao(linha)
        registradores, PC, RSP, RA, OF = executa_instrucao(instrucao, memoria_principal, cache_dados, operandos, registradores, PC, RSP, RA, OF)
        
        PC += 1
        print('\n')
        print('-' * 14 + f' PC = {str(PC)} ' + '-' * 14)

        print(f'\nInstrução: {linha}\n')

        print('=' * 14 + ' Registradores ' + '=' * 14)
        print('~~~~~~ Registradores de Estado/Controle ~~~~~~')
        print(f'RSP = {str(RSP)}  |  RA = {str(RA)}  |  OF = {str(OF)} |  RSA = {str(registradores["RSA"])}')

        print('\n~~~~~~ Registradores de Uso Geral ~~~~~~')
        for i in range(8):
            print(f'r{i}: {registradores[f"r{i}"]}  |  r{i + 8}: {registradores[f"r{i + 8}"]}  |  r{i + 16}: {registradores[f"r{i + 16}"]}  |  r{i + 24}: {registradores[f"r{i + 24}"]}')

        print('\n' + '=' * 14 + ' Cache de Dados ' + '=' * 14)
        for conjunto in cache_dados:
            print(f'--- Conjunto {conjunto} ---')
            for linha in cache_dados[conjunto]:
                print(f'Bloco Armazenado: {linha[0]}  |  N_Acessos: {linha[1]}  |  Dados: {linha[2]}')
            print('')

        print('=' * 14 + ' Cache de Instruções ' + '=' * 14)
        for conjunto in cache_instr:
            print(f'--- Conjunto {conjunto} ---')
            for linha in cache_instr[conjunto]:
                print(f'Bloco Armazenado: {linha[0]}  |  N_Acessos: {linha[1]}  |  Dados: {linha[2]}')
            print('')

        print('=' * 14 + ' Memória Principal ' + '=' * 14)
        for i, dado in enumerate(memoria_principal):
            if dado != 0:
                print(f'Endereço {i}: {dado}')


if __name__ == '__main__':
    main()