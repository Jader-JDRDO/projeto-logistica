#filtragem de relatorio de entregas

import pandas as pd #importando biblioteca pandas para ler o arquivo csv
import sqlite3 #importando a conexao sql para criar um banco de dados
import matplotlib.pyplot as plt #importando a biblioteca matplot para exibir relatorios em forma de grafico 
import seaborn as sns #biblioteca que deixa os graficos mais bonitos

try:
    df_a = pd.read_csv('relatorio_abril.csv', sep=';')
    df_m= pd.read_csv('relatorio_marco.csv', sep=';')#lendo o arquivo csv e transformando em data frame
    
except FileNotFoundError: #erro de arquivo nao encontrado
    print("Erro: O arquivo 'relatorio_abril.csv' não foi encontrado!")
    exit() # encerra o script
except Exception as excecao: #erro de excecao
    print(f"Ocorreu um erro inesperado ao ler o arquivo: {excecao}")

#Carregando os dados
def limpando_dados(df): #criando funcao para facilitar o trabalho do processamento

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')#tirando espaços e formatando as strings das colunas para caixa baixa #tranformando espaços entre as palavras em _ para melhor gerenciamento de variaveis
    print(df.columns) #exibindo colunas para garantir a formataçao

    df['taxa'] = df['taxa'].str.replace(r'[R\$\s]', '', regex=True).replace(',', '.', regex=True) #tirando o R$ para o python ler como numero e tranformando virgulas em pontos para serem lidos adequadamente
    df['taxa'] = pd.to_numeric(df['taxa'], errors='coerce') # Garantindo que é formato float
    df['bairro']=df['bairro'].str.replace('ã','a',regex=True).replace('ç','c',regex=True)
    df['data_entregas'] = pd.to_datetime(df['data_entregas'], dayfirst=True)

    df['bairro'] = df['bairro'].str.strip().str.lower() # Padronizando os nomes das rotas por garantia
    df['bairro'] = df['bairro'].str.title() #aqui deixa a primeira letra maiuscula da palavra padronizado para todos
    

    coleta_dt =  pd.to_datetime(df['pedido_coletado'],format='%H:%M',errors='coerce')  #formatando a coluna pedido coletado para o tipo data e definindo que nao de erro quando a hora estiver vazia
    entrega_dt = pd.to_datetime(df['pedido_entregue'],format ='%H:%M',errors="coerce") #formatando a coluna pedido coletado para o tipo data e definindo que nao de erro quando a hora estiver vazia

    diferenca = entrega_dt - coleta_dt#calculo de tempo da coleta ate a entrega
    df['tempo_entrega(min)'] = diferenca.dt.total_seconds() / 60 #adicionando coluna tempo_entrega para exibir o tempo gasto da coleta ate a entrega formatado em minutos
    df['pedido_coletado'] = coleta_dt.dt.strftime('%H:%M') #padronizando a coluna pedido_coletado em hora e minuto
    df['pedido_entregue'] = entrega_dt.dt.strftime('%H:%M') #padronizando a coluna pedido_entregue em hora e minuto
    

    # Removendo erros (entregas negativas)
    return df[(df['tempo_entrega(min)'] > 0) & (df['taxa'] >0)].dropna()#se no dataframe a entrega tiver tempo negativo ou igual a zero ela nao sera exibida, 
                                                                            #só as que tiverem mais doque 1 min de tempo entre a coleta e a entrega
                                                                            #Removendo entregas sem valor registrado (0)

try:
    df_a = limpando_dados(df_a)
    df_m = limpando_dados(df_m) #dataframe recebe os valores da funcao
    print(df_a)
    print(df_m) #exibindo o dataframe para ver os dados formatados e limpos
    print("Dados limpos e prontos!")
   
 
except KeyError as erro: #mensagem de erro caso nao encontre uma coluna no arquivo principal
    print(f"Erro: A coluna {erro} não existe no arquivo original!")
except Exception as excecao: #mensagem de erro caso de erro no processo de limpeza de dados
    print(f"Erro na limpeza dos dados: {excecao}")

try:
        df_consolidado = pd.concat([df_m, df_a], ignore_index=True)
        df_tempo_bairro = df_consolidado.groupby('bairro')['tempo_entrega(min)'].mean().sort_values(ascending=False).reset_index()
        plt.figure(figsize=(12, 7))
        linhas = sns.barplot(data=df_tempo_bairro, y='bairro', x='tempo_entrega(min)',hue='bairro',palette="Reds_r", legend=False)
        
        for barra in linhas.patches: #para cada barra no dicionario barras
            tamanho = barra.get_width() #pega o valor da quantidade
            plt.text(tamanho + 0.3,  #posição x um pouco depois da barra
            barra.get_y() + barra.get_height()/2, #posição y no meio da barra
            f'{int(tamanho)}', #o texto da quantidade convertida em inteiro)
            va='center', fontsize=10, fontweight='bold') #formatacao do texto em centralizado,tamanho 10, negrito
            

        plt.title('Tempo Médio Entrega por Rota: Restaurante até o Cliente (Bairro)', fontsize=14, fontweight='bold')
        plt.xlabel('Minutos (min)')
        plt.ylabel('Bairro')
        plt.grid(axis='x', linestyle='-', alpha=0.6)

        plt.tight_layout()
        plt.savefig('eficiencia_tempo_bairro.png')
        plt.show()
except KeyError as erro: #mensagem de erro caso nao encontre uma coluna no arquivo principal
    print(f"Erro: {erro} nao possibilitou fazer o grafico não existe no arquivo original!")


try:
        traducao_meses = {'February':'Fevereiro','March': 'Março','April': 'Abril','June': 'Junho'}
        
        df_linha = df_consolidado.groupby(['data_entregas']).agg({'taxa': 'sum'}).reset_index()

    
        df_linha['mes'] = df_linha['data_entregas'].dt.month_name().map(traducao_meses)
        df_linha['dia_do_mes'] = df_linha['data_entregas'].dt.day # Para alinhar dia 1 com dia 1

        plt.figure(figsize=(12, 6))

       
        sns.lineplot(data=df_linha, x='dia_do_mes', y='taxa', hue='mes', 
                    marker='o', linewidth=2, palette={'Março': 'blue', 'Abril': 'orange'})

        plt.title('Evolução do Lucro Diário: Março vs Abril', fontsize=14, fontweight='bold')
        plt.xlabel('Dia do Mês')
        plt.ylabel('Lucro Total (R$)')
        plt.xticks(range(1, 32)) # Garante que apareçam todos os dias no eixo X
        plt.grid(True, alpha=0.3)
        plt.legend(title='Mês')

        plt.tight_layout()
        plt.savefig('evolucao_comparativa_mensal.png')
        plt.show()
except Exception as e:
    print(f"Erro no gráfico de linhas: {e}")
except KeyError as erro: #mensagem de erro caso nao encontre uma coluna no arquivo principal
    print(f"Erro: {erro} nao possibilitou fazer o grafico não existe no arquivo original!")


conn = sqlite3.connect('logistica_pessoal.db') #conexao com o banco de dados
#conn = sqlite3.connect(r'C:\Users\Jader\Documents\logistica_pessoal.db')
df_consolidado.to_sql('entregas', conn, if_exists='replace', index=False) #aqui eu digo que a tabela entregas existe e que se existe refazer com os dados novos


query_volume_bairro = """
SELECT 
    bairro, 
    COUNT(*) AS quantidade_entregas
FROM entregas
GROUP BY bairro
ORDER BY quantidade_entregas DESC;
"""#filtrando o a contagem de entregas em cada respectivo bairro no mes

with sqlite3.connect('logistica_pessoal.db') as conn:
    # Salva o consolidado limpo
    
    # Busca os dados (o SQLite vai tratar a data como string ISO: yyyy-mm-dd)
    df_volume = pd.read_sql(query_volume_bairro, conn)

with sqlite3.connect('logistica_pessoal.db') as conn:
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
   
    df_consolidado.to_sql('entregas', conn, if_exists='replace', index=False)
    df_top = pd.read_sql(query_top_dia, conn)#variavel que recebeu os dados da query do top do dia e a conexao com o banco de dados
   #variavel que recebeu os dados da query do volume do bairro no mes e a conexao com o banco de dados
     #o with fecha a conexao com o banco de dados automaticamente, pois as variaveis anteriores ja armazenaram os dados que preciso para exibir os graficos

if df_top.empty or df_volume.empty:
    print("Atenção: Consultas SQL não retornaram dados. Verifique os nomes das colunas no banco.")
else:
        
        df_top['data_entregas'] = pd.to_datetime(df_top['data_entregas'])
        df_top['mes_aux'] = df_top['data_entregas'].dt.month

        df_marco = df_top[df_top['mes_aux'] == 3].copy()
        df_abril = df_top[df_top['mes_aux'] == 4].copy()

        df_marco['data_entregas'] = df_marco['data_entregas'].dt.strftime('%d/%m')
        df_abril['data_entregas'] = df_abril['data_entregas'].dt.strftime('%d/%m')

      
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        sns.set_theme(style="dark")

        
        
        barras_marco = sns.barplot(data=df_marco,x='data_entregas', y='lucro_maximo', hue='data_entregas',palette="viridis",ax=ax1,legend=False)
        for barra, bairro, qtd in zip(barras_marco.patches, df_marco['bairro'], df_marco['lucro_maximo']): #para cada barra, bairro e quantidade dentro do dicionario barras e de acordo com os dados do data frame, fazer:
            yvalor = barra.get_height() #o valor do eixo y sera o tamanho dos dados que foi pego da contagem de barra e tranformando em altura no grafico
            barras_marco.annotate(f'{bairro}\n(R$ {int(qtd)},00)',#o texto que sera exibido na barra ao decorrer do eixo x e uma distancia de 0,5 da borda da barra
                    xy = (barra.get_x() + barra.get_width()/2, yvalor),
                    xytext= (0,3), #textos que vao aparecer no em cima de cada bairra com seu respectivo dado filtrado do bairro e a quantidade em inteiros
                    textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold', color='darkblue', fontsize=7)
        ax1.set_title('MARÇO/2026', fontsize=14, fontweight='bold')
        ax1.set_xlabel('')
        ax1.set_ylabel('Lucro (R$)')
        ax1.tick_params(axis='x', rotation=45)
        
        barras_abril = sns.barplot(data=df_abril,x='data_entregas', y='lucro_maximo', hue='data_entregas',palette="viridis",ax=ax2,legend=False)
        for barra, bairro, qtd in zip(barras_abril.patches, df_abril['bairro'], df_abril['lucro_maximo']): #para cada barra, bairro e quantidade dentro do dicionario barras e de acordo com os dados do data frame, fazer:
            yvalor = barra.get_height() #o valor do eixo y sera o tamanho dos dados que foi pego da contagem de barra e tranformando em altura no grafico
            barras_abril.annotate(f'{bairro}\n(R$ {int(qtd)},00)',#o texto que sera exibido na barra ao decorrer do eixo x e uma distancia de 0,5 da borda da barra
                    xy = (barra.get_x() + barra.get_width()/2, yvalor),
                    xytext= (0,3), #textos que vao aparecer no em cima de cada bairra com seu respectivo dado filtrado do bairro e a quantidade em inteiros
                    textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold', color='darkblue', fontsize=7)
        ax2.set_title('ABRIL/2026', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Lucro (R$)') #parte lateral do grafico com legenda do lucro do bairro
        ax2.set_xlabel('')
        ax2.tick_params(axis='x', rotation=45) #direçao da rotacao do texto na legenda do eixo x
        plt.tight_layout()
        plt.ylim(0, df_top['lucro_maximo'].max() + 5)
        sns.despine()# Remove as bordas desnecessárias
        plt.savefig('comparativo_top_mensal_empilhado.png')
        plt.show()

        
        total_entregas = df_volume['quantidade_entregas'].sum() #soma das entregas no totais de todos os bairros a partir da variavel que recebeu os dados do volumes
        plt.figure(figsize=(12, 7))#dimensoes do grafico que quero que tenha os dados coletados do top do dia

        # Usando gráfico de barras horizontais (barh) para facilitar a leitura dos nomes
        barras_a = plt.barh(df_volume['bairro'], df_volume['quantidade_entregas'], color='green') #variavel barras recebendo os dados do bairro e quantidade de entregas para o eixo x e y do grafico

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
        plt.title('Quantidade Total de Entregas por Bairro', fontsize=14) #titulo do grafico com tamanho 14
        plt.xlabel('Número de Entregas') #parte inferior do grafico com a legenda numero de entregas
        plt.ylabel('Bairro')#parte lateral do grafico com legenda do bairro
        plt.tight_layout() #garantindo que todos as informaçoes apareçam no grafico sem areas cortadas ou incompletas
        plt.savefig('quantidade_entregas_bairro.png')#criando uma figura a partir do texto  
        plt.show()#exibindo a figura formada