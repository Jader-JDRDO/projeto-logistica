#filtragem de relatorio de entregas

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

#Carregando os dados
df = pd.read_csv('rota1.csv', sep = ';')
print(df)

# 2. Limpeza (O que você aprendeu no quiz!)
df.columns = df.columns.str.strip().str.lower()
print(df.columns) #exibindo colunas para garantir a formataçao
df['taxa'] = df['taxa'].str.replace('R$', '', regex=False).str.replace(',', '.') #tirando o R$ para o python ler como numero
df['taxa'] = pd.to_numeric(df['taxa'], errors='coerce') # Garantindo que é formato float
df = df.dropna(subset=['taxa']) # Removendo entregas sem valor registrado
df['bairro'] = df['bairro'].str.strip().str.upper() # Padronizando os nomes das rotas

print("Dados limpos e prontos!")

#conn = sqlite3.connect('logistica_pessoal.db') aqui deu problema com a leitura de pastas do windows logo tive que pegar o diretorio completo
# O 'r' antes das aspas ajuda o Python a ler as barras do Windows
conn = sqlite3.connect(r'C:\Users\Jader\Documents\logistica_pessoal.db')
df.to_sql('entregas', conn, if_exists='replace', index=False) #aqui eu digo que a tabela entregas existe e é baseada no banco de dados

# Query para saber qual rota é a mais lucrativa (R$)
query = """
SELECT 
    rota, 
    COUNT(*) AS total_entregas,
    SUM(taxa) AS faturamento_total,
    AVG(taxa) AS ticket_medio
FROM entregas
GROUP BY rota
ORDER BY ticket_medio DESC;

"""
query_bairro = """
SELECT 
    bairro, 
    SUM(taxa) AS faturamento_total
FROM entregas
GROUP BY bairro
ORDER BY faturamento_total DESC;
"""

ranking = pd.read_sql(query, conn)
ranking_bairro = pd.read_sql(query_bairro, conn)

conn.close()

# Criando o gráfico
ranking.plot(kind='bar', x='rota', y='faturamento_total', color='skyblue')

plt.title('Faturamento Total por Rota')
plt.xlabel('Rotas')
plt.ylabel('R$ Faturado')
plt.xticks(rotation=45) # Inclina os nomes para não amontoar
plt.tight_layout()

# Salva o gráfico como uma imagem para você subir no GitHub!
plt.savefig('faturamento_rotas.png')


# Configura o tamanho da imagem
plt.figure(figsize=(10, 6))

# Cria o gráfico de barras horizontais
plt.barh(ranking_bairro['bairro'], ranking_bairro['faturamento_total'], color='teal')

# Perfumaria (Títulos e Legendas)
plt.xlabel('Faturamento Total (R$)')
plt.ylabel('Bairros')
plt.title('Bairros mais Lucrativos - Logística Pessoal')
plt.gca().invert_yaxis()  # Deixa o maior faturamento no topo
plt.tight_layout()

# Salva e mostra
plt.savefig('faturamento_por_bairro.png')
plt.show()
