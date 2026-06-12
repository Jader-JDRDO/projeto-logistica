# projeto-logistica
Este projeto automatiza a análise de performance de entregas realizadas em Curitiba-PR com objetivo de fazer R$ 20,00/Hora por dia trabalhado. Ele transforma dados brutos de rotas diárias (arquivos CSV) em um banco de dados estruturado, permitindo a extração de métricas de lucro e volume por região.

Tecnologias Utilizadas

    Linguagem: Python 3.13

    Manipulação de Dados: Pandas

    Banco de Dados: SQLite3

    Visualização: Matplotlib & Seaborn

    Versionamento: Git


Funcionalidades do Projeto:

    ETL (Extract, Transform, Load):
        Limpeza automática de strings, normalização de bairros e conversão de valores monetários.

    Limpeza:
        Padronização de nomes da colunas, Tratamento de strings, Calculo do tempo de entrega

    SQL:
        Agrupamento de volume mensal de pedidos e indeficaçao do melhor bairro

    Análise Temporal:
        Cálculo de tempo real de entrega (Coleta vs Entrega) e produtividade por dia da semana.
    
    Relatório Visual:
        Geração de gráficos comparativos de faturamento e eficiência (Earning Per Hour - EPH).

Visualizações Geradas

O script gera automaticamente quatro arquivos de imagem para relatórios:

    lucro_total_diario_comparativo.png: Comparação de faturamento real entre os meses (Março vs Abril vs Maio).
    

    quantidade_entregas_bairro.png: Ranking total de volume nos bairros de CURITIBA - PR .
    

    eficiencia_dia_semana.png: Médias de lucro por hora, facilitando o planejamento de escalas.
    

    lucro_por_hora_diario.png: Lucro médio de entregas em cada dia de acordo com a meta de lucro/hora 
    

Conclusão
   Durante o período de três meses analisado, houve variações na jornada diária de trabalho (oscilando entre 5 a 8 horas por dia) 
   e alteração nas taxas. A análise de dados gerou os seguintes *insights*:

    Volume vs. Rentabilidade:
        Embora os bairros Água Verde e Portão concentrem o maior volume absoluto de pedidos, eles operam com taxas mínimas devido 
        à proximidade dos restaurantes. 

    Zonas de Alta Performance:
        Para atingir a meta de R$ 20,00/hora (EPH), as regiões mais rentáveis identificadas foram CIC, Batel, Rebouças e 
        Novo Mundo/Capão Raso. Apesar de não serem colados aos centros de coleta, o valor elevado da taxa dessas regiões somado ao
        fácil acesso por vias rápidas e avenidas estruturais otimiza o tempo de deslocamento de ida e volta, elevando a margem de lucro.

    Sazonalidade Temporal:
        Os dias com maior pico de faturamento e densidade de rotas lucrativas foram majoritariamente as Sextas-feiras e Sábados.
        Nos demais dias da semana, a escassez de volume impacta diretamente a eficiência das rotas disponíveis.

    Conclusão Geral: O sucesso operacional da rota não depende apenas da distância, mas sim da conectividade urbana. Bairros com acesso
    direto a vias rápidas corroboram para a velocidade de entrega e eficiência do EPH, mitigando o impacto de dias com menor volume de pedidos.
    

Como Executar o Projeto

    Certifique-se de ter o Python 3.10+ instalado.

    Instale as dependências necessárias:
        pip install pandas matplotlib seaborn
        (o sqlite3 ja vem no python por isso ja vai ser importado automaticamente)

    Coloque o arquivos relatorio_marco.csv, relatorio_abril.csv e relatorio_maio.csv na pasta raiz do projeto.

    Execute o script principal:
        python "analise_relatorio_logistica.py"


Depois de executar vai dar boa em tudo espero ;)


Sobre o Desenvolvedor

Profissional em transição de carreira para area de Análise de Dados, com background técnico em TI e experiência prática no setor logístico. Este projeto une o conhecimento de backend (Python/SQL) com a vivência operacional para criar soluções de otimização financeira.

