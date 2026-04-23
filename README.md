# projeto-logistica
Este projeto automatiza a análise de performance de entregas realizadas em Curitiba-PR. Ele transforma dados brutos de rotas diárias (arquivos CSV) em um banco de dados estruturado, permitindo a extração de métricas de lucro e volume por região.
Tecnologias Utilizadas

    Linguagem: Python 3.13

    Manipulação de Dados: Pandas

    Banco de Dados: SQLite3

    Visualização: Matplotlib & Seaborn

    Versionamento: Git


Funcionalidades do Projeto

    Limpeza:
        Padronização de nomes da colunas, Tratamento de strings, Calculo do tempo de entrega

    SQL:
        Agrupamento de volume mensal de pedidos e indeficaçao do melhor bairro
    
    Relatório Visual:
        Graficos mostrando o lucro máximo diário e o volume total por bairro

Visualizações Geradas

O script gera automaticamente dois arquivos de imagem para relatórios:

    lucro_bairro_por_dia.png: Destaca qual região trouxe o melhor retorno financeiro em cada data.

    quantidade_entregas_bairro.png: Exibe o ranking de bairros com maior volume de pedidos.

    
Como Executar o Projeto

    Certifique-se de ter o Python instalado.

    Instale as dependências necessárias:
        pip install pandas matplotlib seaborn
        (o sqlite3 ja vem no python por isso ja vai ser importado automaticamente)

    Coloque o arquivo rota1.csv na pasta raiz do projeto.

    Execute o script principal:
        python filtragem de relatorio de entregas.py


depois de executar vai dar boa em tudo espero ;)
