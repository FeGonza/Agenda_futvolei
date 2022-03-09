import mysql.connector
from re import A
import datetime
import calendar
from tkinter import *

# conectando ao MYSQL:
def criar_conexao():
    return mysql.connector.connect(host='localhost', database='cadastro_clientes',user='root',password='feli6210')
     
def fechar_conexao(con):
    return con.close()

# Funça apenas para pode criar os horario possiveis de treino
def criar_horarios():
    dia = 1
    mes = 1
    dias_do_mes = calendar.mdays
    ano = 2022
    data_final = '2023-01-01'
    hora = 5
    minutos = 0
    segundos = '00'
    cursor = con.cursor()
    print('inicio')
    while ano < 2023:
        while mes <= 12:
            while dia < dias_do_mes[(mes)]:
                while hora <= 23:
                    while minutos <= 30:
                        dia_com_zeros = str(dia).zfill(2)
                        mes_com_zeros = str(mes).zfill(2)
                        hora_com_zeros = str(hora).zfill(2)
                        minutos_com_zeros = str(minutos).zfill(2)
                        inserir_data_treino = str(ano)+'-'+mes_com_zeros+'-'+dia_com_zeros
                        inserir_hora_treino = hora_com_zeros+':'+minutos_com_zeros
                        sql = "INSERT INTO agenda_treino (data_treino, hora_treino) VALUES (%s,%s)"
                        cursor.execute(sql,(inserir_data_treino,inserir_hora_treino))
                        minutos += 30
                    hora += 1
                    minutos = 0    
                dia += 1
                hora = 5
            mes += 1
            dia = 1    
        ano = 2023
    cursor.close()
    con.commit()
    return 0

# cadastrando o cliente
# funcao para ver se o cliente já tem cadastro / já cadastrar cliente
# Retorna o nome do cliente
def condicao_cadastrado():
    cliente_cadastrado = input("Já possue cadastro na Arena Paulada? Digite S ou N: ")
    if cliente_cadastrado.upper() == 'S':
        nome_cliente = input("Digite seu nome completo cadastrado: ")
        return nome_cliente
    elif cliente_cadastrado.upper() == 'N':
        nome_cliente = inserir_usuario()
        return nome_cliente
    else:
        print("\nCaso voce já tenha cadastro, digite S.\nCaso nao tenha cadastro, digite N.")
        return condicao_cadastrado()

# Cadastrando cliente no Banco de dados MySQL
def inserir_usuario():
    cursor = con.cursor()
    nome_cliente = input('Digite seu nome completo: ')
    data_nascimento = data_formato_ansi(input('Digite a sua data de nascimento(DD/MM/AAAA): '))
    sexo_cliente = input('Digite seu sexo (M/F): ').upper()
    cidade_cliente = input('Qual cidade reside: ')
    bairro_cliente = input('Digite o bairro: ')
    sql = "INSERT INTO alunos (nome, data_nascimento, sexo, cidade, bairro) values (%s, %s, %s, %s, %s)"
    dados_clientes = nome_cliente, data_nascimento, sexo_cliente, cidade_cliente, bairro_cliente
    cursor.execute(sql, dados_clientes)
    cursor.close()
    con.commit()
    return nome_cliente


# Corrigindo formato da data para o MYSQL
def data_formato_ansi(data):
    dia = data[:2]
    mes = data[3:5]
    ano = data[6:]
    if (len(data) == 10) and (0<int(dia)<=31) and (0<int(mes)<=12) and (len(ano)== 4) and (data[2]==data[5]=='/'):
        data_ansi_corrigida = ano + '-' + mes + '-' + dia
        return data_ansi_corrigida
    else:
        return data_formato_ansi(input('Voce pode ter digitado algo erro, poderia digitar a data neste formato DD/MM/AAAA? '))

# Verificando se esta correto
def horario_formato_ansi(horario):
    hora = horario[:2]
    minutos = horario[3:]
    if (len(horario)==5) and (horario[2] == ':') and (0 <= int(hora) <= 23) and (0 <= int(minutos) <= 60):
        horario_formatado = datetime.time(hour=int(hora), minute=int(minutos))
        if int(minutos)==30 or int(minutos)==0:
            return horario_formatado
        else:
            return horario_formato_ansi(input('As aula são apenas de 30 em 30 minutos, poderia digitar novamente o horario neste formato (HH:MM): '))    
    else: 
        return horario_formato_ansi(input('Voce pode ter digitado algo erro, poderia digitar o horario neste formato (HH:MM): '))

# confirmando se o cliente esta cadastrado
def verificar_cadastro(nome):
    cursor = con.cursor()
    sql = "SELECT nome FROM alunos"
    cursor.execute(sql)
    todos_nomes = cursor.fetchall()
    for i in todos_nomes:
        if i[0].upper() == nome.upper():
            return print('Aluno(a) Cadastrado(a) :)')
    print('Voce digitou um nome não cadastrado.')
    return verificar_cadastro(condicao_cadastrado())
            
    cursor.close()
    return 1
    


# Perguntando ao cliente qual horario ele deseja treinar
# returnar tupla
def pergunta_horario_treino():
    data_desejada = data_formato_ansi(input('Digite a data que deseja treinar (DD/MM/AAAA): '))
    condicao_ver_horarios_disponiveis = input('Deseja ver os horarios diponiveis? S/N: ')
    if condicao_ver_horarios_disponiveis.upper() == 'S':
        visualizar_horarios_disponiveis(data_desejada)
    hora_desejada = horario_formato_ansi(input('Digite o horario que deseja treinar (HH:MM): '))
    return data_desejada, hora_desejada

def agendamento(data_hora_desejada,nome=None):
    cursor = con.cursor()
    sql = "SELECT * FROM agenda_treino WHERE (data_treino = %s and hora_treino = %s)"
    cursor.execute(sql, data_hora_desejada)
    horario_selecionado = cursor.fetchall()
    qtd_vagas = 0 
    for i in horario_selecionado[0]:
        if i == None:
            qtd_vagas+=1
    preenche_espaco_aluno = (6-qtd_vagas)+1       
    tupla_nome_data_hora = (preenche_espaco_aluno, nome, data_hora_desejada[0], data_hora_desejada[1])
    if qtd_vagas > 0:
        sql2 = "UPDATE agenda_treino SET aluno%s = %s WHERE (data_treino = %s and hora_treino = %s)"
        cursor.execute(sql2, tupla_nome_data_hora)
        fim = ('Horario da %s reservado, voce é %s° aluno(a) cadastrado(a) neste horario' % (data_hora_desejada[1], preenche_espaco_aluno))
    else:
        print('Esta turma já esta completa.')
        deseja_continuar = input('Caso deseja escolher outro horario digite S, caso contrario digite N: ')
        if deseja_continuar.upper() == 'S':
            fim = agendamento(pergunta_horario_treino(),nome)   
        else:
            fim = ('Que pena, não encontrou horario ideal para voce?')
    print('-'*80) 
    cursor.close()
    con.commit()                    
    return fim

def visualizar_horarios_disponiveis(data_desejada):
    cursor = con.cursor()
    sql = "SELECT * FROM agenda_treino where (data_treino = %s)"
    cursor.execute(sql, (data_desejada,))
    dia = cursor.fetchall()
    for i in dia:
        str_hora = str(i[1])
        print(str_hora[:-3],':', end=" ")
        vagas = 0
        for j in i:            
            if j == None:
                vagas+=1
        qtd_alunos = 6-vagas        
        if qtd_alunos == 6:
            print('Nao possue mais vagas.')
        elif qtd_alunos == 0:
            print('Ainda nao temos alunos(as) neste horario. 6 vagas')
        elif qtd_alunos == 1:
            print('1 aluno(a) neta aula. Ainda temos %s vagas' % vagas)
        else:
            print('%s alunos(as) nesta aula. Ainda temos %s vagas' % (qtd_alunos, vagas))
    cursor.close()


def rodar_programa():
## INICIO DO PROGRAMA 
    con = criar_conexao()

    # identificando o cliente 
    nome = condicao_cadastrado()
    condicao_cadastro = verificar_cadastro(nome)

    # Agendamento do cliente        
    data_hora_desejada = pergunta_horario_treino()
    cadastro = agendamento(data_hora_desejada,nome)  
    print(cadastro)  
    print('-'*80) 
    print('A Arena Paulada agradece.\nSiga no Instagram @ArenaPauladaftv\nCaso tenha alguma duvida sobre nosso trabalho, entre em contato via Whats App\nFelipe: (11) 99999-9999')
    print('-'*80)

    fechar_conexao(con)

if __name__ == '__main__':
    con = criar_conexao()
    rodar_programa()
    fechar_conexao(con)