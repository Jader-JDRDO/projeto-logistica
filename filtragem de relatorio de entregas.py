#filtragem de relatorio de entregas

import pandas as pd #importando biblioteca pandas para ler o arquivo csv
import sqlite3 #importando a conexao sql para criar um banco de dados
import matplotlib.pyplot as plt #importando a biblioteca matplot para exibir relatorios em forma de grafico 

#Carregando os dados
df = pd.read_csv('rota1.csv', sep = ';') #lendo o arquivo csv e transformando em data frame
 #exibindo o data frame

# 2. Limpeza (O que você aprendeu no quiz!)
df.columns = df.columns.str.strip().str.lower()
df.columns = df.columns.str.replace(' ', '_')
print(df.columns) #exibindo colunas para garantir a formataçao
df['taxa'] = df['taxa'].str.replace('R$', '', regex=False).str.replace(',', '.') #tirando o R$ para o python ler como numero
df['taxa'] = pd.to_numeric(df['taxa'], errors='coerce') # Garantindo que é formato float
df = df.dropna(subset=['taxa']) # Removendo entregas sem valor registrado
df['bairro'] = df['bairro'].str.strip().str.lower() # Padronizando os nomes das rotas por garantia
df['bairro'] = df['bairro'].str.title() #aqui deixa a primeira letra maiuscula da palavra padronizado para todos

coleta_dt =  pd.to_datetime(df['pedido_coletado'],format='%H:%M')
entrega_dt = pd.to_datetime(df['pedido_entregue'],format ='%H:%M')

diferenca = entrega_dt - coleta_dt
df['tempo_entrega(min)'] = diferenca.dt.total_seconds() / 60
df['pedido_coletado'] = coleta_dt.dt.strftime('%H:%M')
df['pedido_entregue'] = entrega_dt.dt.strftime('%H:%M')

# 4. Remove erros (entregas negativas)
df = df[df['tempo_entrega(min)'] > 0]
print("Dados limpos e prontos!")

print(df)



conn = sqlite3.connect('logistica_pessoal.db') #conexao com o banco de dados
#conn = sqlite3.connect(r'C:\Users\Jader\Documents\logistica_pessoal.db')
df.to_sql('entregas', conn, if_exists='replace', index=False) #aqui eu digo que a tabela entregas existe e que se existe refazer

#query_top_dia = """
#SELECT data_entregas, bairro, MAX(lucro_total) as lucro_maximo
#FROM (
    #SELECT data_entregas, bairro, SUM(taxa) AS lucro_total
   # SELECT lucro_maximo, COUNT(lucro_total) as quantidade_entregas
   # FROM entregas
   # GROUP BY data_entregas, bairro
#)
#GROUP BY data_entregas;
#"""
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
"""
query_volume_bairro = """
SELECT 
    bairro, 
    COUNT(*) AS quantidade_entregas
FROM entregas
GROUP BY bairro
ORDER BY quantidade_entregas DESC;
"""


df_top = pd.read_sql(query_top_dia, conn)
df_volume = pd.read_sql(query_volume_bairro, conn)
conn.close()

total_entregas_bairro = df_top['quantidade_entregas'].sum()
plt.figure(figsize=(12, 6))
bars = plt.bar(df_top['data_entregas'], df_top['lucro_maximo'], color='skyblue')

#for bar, bairro in zip(bars, df_top['bairro']):
    #yval = bar.get_height()
    #plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, bairro, 
             #ha='center', va='bottom', fontweight='bold', color='darkblue')
for bar, bairro, qtd in zip(bars, df_top['bairro'], df_top['lucro_maximo']):
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, 
             f'{bairro}\n({int(qtd)})', 
             ha='center', va='bottom', fontweight='bold', color='darkblue', fontsize=9)

plt.title('Bairro Mais Lucrativo por Dia (Top Performance)', fontsize=14)
plt.xlabel('Data')
plt.ylabel('Lucro do Melhor Bairro (R$)')
plt.xticks(rotation=45)
plt.ylim(0, df_top['lucro_maximo'].max() + 5) # Dá um espaço no topo para o texto
plt.tight_layout()
plt.savefig('lucro_bairro_por_dia.png')
plt.show()




total_entregas = df_volume['quantidade_entregas'].sum()
plt.figure(figsize=(10, 6))
# Usando gráfico de barras horizontais (barh) para facilitar a leitura dos nomes
bars_a = plt.barh(df_volume['bairro'], df_volume['quantidade_entregas'], color='salmon')
for bar in bars_a:
    width = bar.get_width() # Pega o valor da quantidade
    plt.text(width + 0.3,  # Posição X (um pouco depois da barra)
             bar.get_y() + bar.get_height()/2, # Posição Y (no meio da barra)
             f'{int(width)}', # O texto (a quantidade convertida em inteiro)
             va='center', fontsize=10, fontweight='bold')
plt.annotate(f'Total Geral: {total_entregas}', 
             xy=(0.80, 0.95), xycoords='axes fraction', 
             fontsize=12, fontweight='bold', color='white',
             bbox=dict(boxstyle="round,pad=0.5", fc="darkred", ec="black", alpha=0.8))
plt.title('Quantidade Total de Entregas por Bairro no MES', fontsize=14)
plt.xlabel('Número de Entregas')
plt.ylabel('Bairro')
plt.tight_layout()
plt.savefig('quantidade_entregas_bairro.png')
plt.show()