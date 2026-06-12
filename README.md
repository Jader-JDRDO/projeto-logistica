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
    Houve diversas alteraçoes de horários e taxas durante esse periodo de tres meses variando de 5 a a 8 horas por dia de trabalho.
    No entanto, ao fazer uma visualização geral ainda é notavel que o bairro agua verde e portao sao os bairros com maior volume de
    pedidos comparado aos demais, porem os mais rentavel para bater a meta de R$ 20,00 Reais de lucro por hora seriam os bairros de CIC,
    Batel, Rebouças e Novo Mundo/Capão Raso, pois, nao sao demasiados distantes dos restaurantes e as rotas de ida e volta são de facil
    acesso por conta das viás rápidas alem do valor da taxa nesses bairros contribuirem para em diversos dias bater a meta de lucro
    diario por hora comparado com os bairros de taxa mínima e bem próximos como Agua Verde, Santa Quiteria, Guaira e Vila Izabel.
    Contudo, os dias que mais geravam lucro eram majoritariamente Sexta-Feira e Sabado no qual o volume de pedidos criavam mais rotas 
    e contribuiram para ultrapassar a meta de lucro por hora. Em contra-partida, os demais aconteciam o completo oposto em relação a
    a volumes de entregas e rotas ucrativas disponiveis.
    Ao fim da analise, conclui-se que bairros com facil acesso a viás rápidas ou avenidas corroboram para a eficiência das entregas
    independente do dia da semana, mas para bater a meta de lucro, o cenario ideal seria focar em rotas para bairros não tao distantes
    e com facil acesso.
    

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

