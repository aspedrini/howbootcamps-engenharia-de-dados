# Desafio 3 - Projeto Final

# Objetivo do projeto, motivação e resultados esperados

   Este projeto surgiu da necessidade de solucionar uma dificuldade enfrentada no dia-a-dia da empresa. Hoje atuo no setor de Dados com foco em Business Intelligence, principalmente dados internos do produto (SaaS) e dados relevantes para outras áreas (marketing, revenue, squads…), tendo atuado anteriormente também com foco em demandas de clientes sob regime de consultoria para desenvolvimento. A empresa possui duas soluções de Business Intelligence para os clientes contratarem: a primeira é o Power BI extraindo dados através de um conjunto de APIs, e a segunda é através da ferramenta Zoho Analytics, alimentada por diversas pipelines e disponibilizada como white label com o logo da empresa.
   
   Esta ferramenta da Zoho depende da contratação de um plano por parte da nossa empresa, e cada categoria possui uma série de vantagens adicionais quando comparada com sua anterior, como limite de requisições nas APIs, maior limite para o número de usuários, entre outros. Além do plano contratado, ainda é possível ampliar mais os limites através da contratação de “suplementos” para o plano, como vagas extras para os clientes. O plano enterprise dá direito a 50 vagas para usuários, e a empresa suplementa com mais 20 vagas contratadas, totalizando 70.
   
   Qualquer cliente que contratar a ferramenta (também chamado de módulo) para visualizar seus dados irá ocupar uma vaga através da ativação de um email, e será este o único responsável habilitado para criação dos dashboards, porém caso o cliente desejar interromper esta contratação, seu email ainda permanece ativo no workspace do serviço da Zoho e continua ocupando uma vaga. Quando o limite das 70 vagas é atingido, clientes novos não conseguem acessar a ferramenta para criar ou modificar seus dashboards, gerando tickets para o setor de Suporte que impactam nos resultados da empresa, além de exigir tempo da equipe de Suporte e de Dados para detectar onde está o problema, já que não há nenhum aviso ou mensagem de erro.
   
   Ocasionalmente chegava para o time de dados a demanda de fazer uma checagem de quais usuários com emails ativos nos workspaces estavam realmente ativos. Para isso era necessário checar a data de seu último acesso dentro do painel do Admin da Zoho e checar se o cliente possuía o serviço ativo nas configurações da empresa (via banco de dados ou via aplicação web). Considerando que a empresa guarda todos os workspaces já ativados como registro histórico e que a checagem era manual e um por um, esta tarefa tomava um tempo considerável do responsável para ser feita com certa frequência.
   
   O projeto teve como objetivo automatizar esta rotina de checagem, conservando o histórico dos dados coletados e fornecendo as informações de maneira mais acessível através de uma ferramenta de visualização de dados, como o Power BI.

# Construção do projeto, materiais e métodos
A premissa do projeto consistiu em utilizar o acesso ao ambiente empresarial da AWS e em automatizar todas as etapas do processo.	

Para extrair os dados de suas fontes foi utilizado Python, sendo elas:
    * API 1 da Zoho - tabela com ID do cliente e número de dias desde último acesso;
    * API 2 da Zoho - tabela com o ID do cliente e o email de admin cadastrado para o workspace; e
    * Redshift - tabela contendo ID do cliente e a informação se o mesmo possui o módulo contratado/ativo.

O armazenamento dos dados coletados foi planejado a partir da estrutura de um data lake utilizando o S3 em três camadas, e para mover os dados de uma camada para outra foram utilizados scripts em Python:
    * bronze: armazena em csv as extrações realizadas diariamente, separado em subpastas para as três fontes diferentes de arquivos;
    * silver: armazena os dados concatenados por tipo de origem; e
    * gold: traz o csv final após a junção dos arquivos em um só através de suas chaves primárias, pronto para o consumo.

Exemplo das camadas:
```
Bronze
    ∟ API 1 - ultimo acesso
        ∟ 2023-07-31.csv
        ∟ 2023-07-30.csv
    ∟ API 2 - admin cadastrado
        ∟ 2023-07-31.csv
        ∟ 2023-07-30.csv
    ∟ Redshift - modulo ativo
        ∟ 2023-07-31.csv
        ∟ 2023-07-30.csv

Silver
    ∟ API 1 - concatenado
    ∟ API 2 - concatenado
    ∟ Redshift - concatenado

Gold
    ∟ tabela_final.csv
```

A orquestração de todas as funções utilizou do Apache Airflow instanciado utilizando Ubuntu no serviço EC2.

Por fim, a tabela disponível na última camada foi armazenada no Redshift e de lá carregada no Power BI para extração de informações para o monitoramento.

# Escopo da arquitetura
![Image](https://i.imgur.com/0XODBayl.png)

# Exemplo de tabela
![Image](https://i.imgur.com/MNjJDYP.png)

Na tabela de exemplo é possível ver informações relevantes para a análise, como:
O cliente de ID 1 não tem um admin ativo, logo não toma uma vaga no serviço, assim como não tem o módulo ativo;
O cliente de ID 2 não possui um admin, porém possui o módulo ativo e possivelmente está pagando por um módulo sem uso;
O cliente de ID 3 possui admin ativo e possui módulo ativo, porém está sem acessar seus dashboards há 30 dias.

Por fim, estas informações foram visualmente distribuídas num dashboard em Power BI.
