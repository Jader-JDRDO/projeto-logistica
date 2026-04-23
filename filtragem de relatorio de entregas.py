#filtragem de relatorio de entregas

import pandas as pd #importando biblioteca pandas para ler o arquivo csv
import sqlite3 #importando a conexao sql para criar um banco de dados
import matplotlib.pyplot as plt #importando a biblioteca matplot para exibir relatorios em forma de grafico 
import seaborn as sns #biblioteca que deixa os graficos mais bonitos

try:
    df = pd.read_csv('rota1.csv', sep=';')#lendo o arquivo csv e transformando em data frame
    print(df) #exibindo o data frame
except FileNotFoundError: #erro de arquivo nao encontrado
    print("Erro: O arquivo 'rota1.csv' não foi encontrado!")
    exit() # encerra o script
except Exception as excecao: #erro de excecao
    print(f"Ocorreu um erro inesperado ao ler o arquivo: {excecao}")

#Carregando os dados
def limpando_dados(df): #criando funcao para facilitar o trabalho do processamento

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')#tirando espaços e formatando as strings das colunas para caixa baixa #tranformando espaços entre as palavras em _ para melhor gerenciamento de variaveis
    print(df.columns) #exibindo colunas para garantir a formataçao

    df['taxa'] = df['taxa'].str.replace(r'[R\$\s]', '', regex=True).replace(',', '.', regex=True) #tirando o R$ para o python ler como numero e tranformando virgulas em pontos para serem lidos adequadamente
    df['taxa'] = pd.to_numeric(df['taxa'], errors='coerce') # Garantindo que é formato float

    

    df['bairro'] = df['bairro'].str.strip().str.lower() # Padronizando os nomes das rotas por garantia
    df['bairro'] = df['bairro'].str.title() #aqui deixa a primeira letra maiuscula da palavra padronizado para todos
    

    coleta_dt =  pd.to_datetime(df['pedido_coletado'],format='%H:%M',errors='coerce')  #formatando a coluna pedido coletado para o tipo data e definindo que nao de erro quando a hora estiver vazia
    entrega_dt = pd.to_datetime(df['pedido_entregue'],format ='%H:%M',errors="coerce") #formatando a coluna pedido coletado para o tipo data e definindo que nao de erro quando a hora estiver vazia

    diferenca = entrega_dt - coleta_dt#calculo de tempo da coleta ate a entrega
    df['tempo_entrega(min)'] = diferenca.dt.total_seconds() / 60 #adicionando coluna tempo_entrega para exibir o tempo gasto da coleta ate a entrega formatado em minutos
    df['pedido_coletado'] = coleta_dt.dt.strftime('%H:%M') #padronizando a coluna pedido_coletado em hora e minuto
    df['pedido_entregue'] = entrega_dt.dt.strftime('%H:%M') #padronizando a coluna pedido_entregue em hora e minuto
    

    # Removendo erros (entregas negativas)
    return df[(df['tempo_entrega(min)'] > 1) & (df['taxa'] >0)].dropna()#se no dataframe a entrega tiver tempo negativo ou igual a zero ela nao sera exibida, 
                                                                            #só as que tiverem mais doque 1 min de tempo entre a coleta e a entrega
                                                                            #Removendo entregas sem valor registrado (0)

try:
    df = limpando_dados(df) #dataframe recebe os valores da funcao
    print(df) #exibindo o dataframe para ver os dados formatados e limpos
    print("Dados limpos e prontos!")
except KeyError as erro: #mensagem de erro caso nao encontre uma coluna no arquivo principal
    print(f"Erro: A coluna {erro} não existe no arquivo original!")
except Exception as excecao: #mensagem de erro caso de erro no processo de limpeza de dados
    print(f"Erro na limpeza dos dados: {excecao}")



conn = sqlite3.connect('logistica_pessoal.db') #conexao com o banco de dados
#conn = sqlite3.connect(r'C:\Users\Jader\Documents\logistica_pessoal.db')
df.to_sql('entregas', conn, if_exists='replace', index=False) #aqui eu digo que a tabela entregas existe e que se existe refazer com os dados novos

query_top_dia = """
SELECT data_entregas, bairro, lucro_maximo, quantidade_entregas
FROM (
    SELECT 
        data_entregas, 
        bairro, 
        SUM(taxa) AS lucro_maximo,
        COUNT(*) AS quantidade_entregas,
        ROW_NUMBER() OVER(PARTITION BY data_entregas ORDER BY SUM(taxa) DESC) as rank
    FROM entregas
    GROUP BY data_entregas, bairro
)
WHERE rank = 1;
""" #filtrando a data de entrega o bairro que teve mais entregas o lucro desse bairro e quantas entregas foram feitas nesse mesmo bairro
    #se a soma das taxas daquele bairro ultrapassar a soma dos demais entao esse bairro sera o TOP do dia
    #com esse filtro os bairros TOP do dia vao ser ordenados e as respectivas quantidades vao ser exibidas
query_volume_bairro = """
SELECT 
    bairro, 
    COUNT(*) AS quantidade_entregas
FROM entregas
GROUP BY bairro
ORDER BY quantidade_entregas DESC;
"""#filtrando o a contagem de entregas em cada respectivo bairro no mes

with sqlite3.connect('logistica_pessoal.db') as conn:
    df.to_sql('entregas', conn, if_exists='replace', index=False)
    df_top = pd.read_sql(query_top_dia, conn)#variavel que recebeu os dados da query do top do dia e a conexao com o banco de dados
    df_volume = pd.read_sql(query_volume_bairro, conn)#variavel que recebeu os dados da query do volume do bairro no mes e a conexao com o banco de dados
     #o with fecha a conexao com o banco de dados automaticamente, pois as variaveis anteriores ja armazenaram os dados que preciso para exibir os graficos

sns.set_theme(style="dark") #definindo o tema de fundo dos graficos
total_entregas_bairro = df_top['quantidade_entregas'].sum() #soma das entregas no bairro a partir da variavel que recebeu os dados do Top do dia
plt.figure(figsize=(12, 7)) #dimensoes do grafico que quero que tenha os dados coletados do top do dia
barras = sns.barplot(x=df_top['data_entregas'], y=df_top['lucro_maximo'], palette="viridis") #variavel barras recebendo os dados da data de entrega e lucro maximo para o eixo x e y do grafico

for barra, bairro, qtd in zip(barras.patches, df_top['bairro'], df_top['lucro_maximo']): #para cada barra, bairro e quantidade dentro do dicionario barras e de acordo com os dados do data frame, fazer:
    yvalor = barra.get_height() #o valor do eixo y sera o tamanho dos dados que foi pego da contagem de barra e tranformando em altura no grafico
    barras.annotate(f'{bairro}\n(R$ {int(qtd)},00)',#o texto que sera exibido na barra ao decorrer do eixo x e uma distancia de 0,5 da borda da barra
            xy = (barra.get_x() + barra.get_width()/2, yvalor),
            xytext= (0,5), #textos que vao aparecer no em cima de cada bairra com seu respectivo dado filtrado do bairro e a quantidade em inteiros
            textcoords="offset points",
            ha='center', va='bottom', fontweight='bold', color='darkblue', fontsize=9) #formatacao do texto, centralizada, em cima da barra, negrito, cor azul e tamanho da fonte 9

plt.title('Bairro Mais Lucrativo por Dia (Top Performance)', fontsize=14) #titulo do grafico com tamanho 14
plt.xlabel('Data') #parte inferior do grafico com a legenda data 
plt.ylabel('Lucro do Melhor Bairro (R$)') #parte lateral do grafico com legenda do lucro do bairro
plt.xticks(rotation=45) #direçao da rotacao do texto na legenda do eixo x
plt.ylim(0, df_top['lucro_maximo'].max() + 5) # Dá um espaço no topo para o texto
plt.tight_layout()#garantindo que todos as informaçoes apareçam no grafico sem areas cortadas ou incompletas
plt.savefig('lucro_bairro_por_dia.png') #criando uma figura a partir do texto   
sns.despine()# Remove as bordas desnecessárias
plt.show() #exibindo a figura formada

total_entregas = df_volume['quantidade_entregas'].sum() #soma das entregas no totais de todos os bairros a partir da variavel que recebeu os dados do volumes
plt.figure(figsize=(10, 6))#dimensoes do grafico que quero que tenha os dados coletados do top do dia

# Usando gráfico de barras horizontais (barh) para facilitar a leitura dos nomes
barras_a = plt.barh(df_volume['bairro'], df_volume['quantidade_entregas'], color='darkred') #variavel barras recebendo os dados do bairro e quantidade de entregas para o eixo x e y do grafico

for barra in barras_a: #para cada barra no dicionario barras
    tamanho = barra.get_width() #pega o valor da quantidade
    plt.text(tamanho + 0.3,  #posição x um pouco depois da barra
             barra.get_y() + barra.get_height()/2, #posição y no meio da barra
             f'{int(tamanho)}', #o texto da quantidade convertida em inteiro)
             va='center', fontsize=10, fontweight='bold') #formatacao do texto em centralizado,tamanho 10, negrito
plt.annotate(f'Total Geral: {total_entregas}', #legenda com o total das entregas
             xy=(0.80, 0.95), xycoords='axes fraction', #posiçao da legenda dentro do grafico
             fontsize=12, fontweight='bold', color='white', #formatacao do texto tamanho 12, negrito,cor branca
             bbox=dict(boxstyle="round,pad=0.5", fc="darkred", ec="black", alpha=0.8)) #adicionando borda circular de 0.5 de espessura e cor vermelha no interior e preto na cor da borda
plt.title('Quantidade Total de Entregas por Bairro no MES', fontsize=14) #titulo do grafico com tamanho 14
plt.xlabel('Número de Entregas') #parte inferior do grafico com a legenda numero de entregas
plt.ylabel('Bairro')#parte lateral do grafico com legenda do bairro
plt.tight_layout() #garantindo que todos as informaçoes apareçam no grafico sem areas cortadas ou incompletas
plt.savefig('quantidade_entregas_bairro.png')#criando uma figura a partir do texto  
plt.show()#exibindo a figura formada