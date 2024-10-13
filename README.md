Este projeto simula diferentes algoritmos de busca utilizando drones em um ambiente 2D. O sistema permite rodar simulações com diferentes configurações de ambiente, algoritmos de busca e quantidade de agentes (drones).

Pré-requisitos
Python 3.8+
Dependências: As bibliotecas necessárias podem ser instaladas via pip usando o seguinte comando:

pip install -r requirements.txt
Certifique-se de que as seguintes bibliotecas estão incluídas no arquivo requirements.txt:

numpy
pandas
DSSE (biblioteca de simulação)
Outras bibliotecas específicas que podem ser usadas pelo seu projeto.

Descrição dos Diretórios
AStar_search/: Contém os scripts para rodar o algoritmo A* com diferentes quantidades de drones (1, 2 ou 4) e em diferentes configurações de ambiente.

expanding_square_search/: Implementação do algoritmo de busca em quadrado expansivo, também com suporte para 1, 2 ou 4 drones em diferentes ambientes.

traditional_maritime_search/: Implementação da busca tradicional marítima, suportando 1, 2 ou 4 drones.

data/: Contém os arquivos de configuração de ambientes (.npy) que são utilizados pelas simulações.

Como Rodar a Simulação
A simulação é configurada através de três parâmetros principais:

Ambiente: Define a configuração do ambiente (ex.: config_01 ou config_02).
Algoritmo: Define o algoritmo de busca a ser utilizado (ex.: AStar, expanding, ou tradicional).
Agentes: Define a quantidade de drones (agentes) que participam da simulação (ex.: 1, 2 ou 4).
Exemplo de Uso
Para rodar uma simulação, use o script main.py e configure os parâmetros no código ou através da função simulacao().

Exemplo:
Rodando uma simulação com 4 agentes, no ambiente "config_02", usando o algoritmo A*:

Dentro do arquivo main.py, a chamada para a função simulacao() deve ser configurada da seguinte forma:

ambiente = "config_02"
algoritmo = "AStar"
agentes = 4

simulacao(ambiente, algoritmo, agentes)
Outras Configurações:
Ambientes Disponíveis:

config_01
config_02

Algoritmos Disponíveis:

tradicional: Busca marítima tradicional.
expanding: Busca em quadrado expansivo.
AStar: Algoritmo A* de busca heurística.

Agentes (Quantidade de Drones):

1, 2 ou 4 drones.

Estrutura da Função de Simulação
A função simulacao() dentro de main.py controla qual script de simulação será rodado, com base nos parâmetros fornecidos:

Resultados
Os resultados de cada simulação são exportados para arquivos CSV na pasta results/. O arquivo será nomeado de acordo com a configuração da simulação, facilitando a análise posterior.