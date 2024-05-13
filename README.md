# Projeto de Extração e Análise de Dados Web

Este projeto combina técnicas avançadas de extração de dados da web, processamento de linguagem natural e armazenamento de vetores para criar uma solução integrada que permite a coleta, processamento e recuperação eficiente de informações da internet.

## Descrição Geral

O projeto foi desenvolvido com o objetivo de criar uma ferramenta robusta que possa navegar automaticamente por páginas da web, extrair informações úteis, processá-las usando modelos de linguagem avançados para transformá-las em embeddings de sentenças e armazenar esses dados de forma que possam ser rapidamente acessados e consultados. Este processo permite a análise de grandes volumes de texto e a recuperação de informações com base no conteúdo semântico.

## Estrutura do Projeto

O projeto é composto por três componentes principais:

1. **Extrator de Dados (`extracao.py`)**
2. **Processador de Linguagem Natural (`cli.py`)**
3. **Banco de Dados de Vetores (`db.py`)**

### 1. Extrator de Dados (`extracao.py`)

Este script é responsável por navegar em sites específicos e extrair o conteúdo das páginas. Utiliza técnicas de raspagem web para coletar dados, que são posteriormente limpos de quaisquer elementos HTML desnecessários, convertendo o conteúdo em texto puro para processamento posterior.

#### Tecnologias Utilizadas:
- `requests`: Para realizar requisições HTTP.
- `re`: Para limpeza de dados usando expressões regulares.
- `pandas`: Para armazenar e manipular os dados coletados.

### 2. Processador de Linguagem Natural (`cli.py`)

Após a coleta de dados, o texto é processado usando um modelo de transformadores para gerar embeddings de sentenças. Estes embeddings são representações vetoriais de alta dimensão que capturam o contexto semântico das sentenças, facilitando buscas e análises mais profundas.

#### Tecnologias Utilizadas:
- `SentenceTransformer`: Para gerar embeddings de alta qualidade.
- `Flask`: Para criar uma interface de usuário simples através de um servidor web.

### 3. Banco de Dados de Vetores (`db.py`)

Os embeddings gerados são armazenados em um banco de dados de vetores fornecido pelo Pinecone. Isso permite consultas eficientes e escaláveis baseadas no conteúdo semântico das informações armazenadas.

#### Tecnologia Utilizada:
- `Pinecone`: Um serviço de banco de dados de vetores que oferece alta performance em operações de busca por similaridade.

## Motivação

A principal motivação para o desenvolvimento deste projeto foi a necessidade de uma ferramenta capaz de entender e organizar a vasta quantidade de informações disponíveis na internet de forma rápida e eficiente. Com o aumento contínuo do volume de dados online, torna-se essencial ter ferramentas que possam extrair e analisar informações de forma automatizada, reduzindo a necessidade de intervenção humana e aumentando a acessibilidade a insights significativos.

## Considerações Finais

Este projeto exemplifica a integração de várias tecnologias e disciplinas dentro do campo da ciência da computação para enfrentar desafios reais do mundo da informação. Através do uso estratégico de raspagem web, processamento de linguagem natural e bancos de dados especializados, podemos criar soluções que não apenas automatizam tarefas repetitivas, mas também fornecem novas maneiras de entender e utilizar as informações que coletamos.
