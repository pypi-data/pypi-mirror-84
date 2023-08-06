# Bart Simulator (CLI)

[![PyPI version](https://badge.fury.io/py/bart-simulator.svg)](https://badge.fury.io/py/bart-simulator)
[![](https://images.microbadger.com/badges/version/cesarbruschetta/bart-simulator.svg)](https://microbadger.com/images/cesarbruschetta/bart-simulator "Get your own version badge on microbadger.com")

Send event views to Google Analytics and Generator customers or products

## Install
```
$ pip install bart-simulator
```

## Usage

```
usage: simulator [-h] [--loglevel LOGLEVEL] [--version]  ...

Send event views to Google Analytics and Generator customers or products data-
set (bart-recs CLI)

optional arguments:
  -h, --help           show this help message and exit
  --loglevel LOGLEVEL
  --version            show program's version number and exit

Commands:

    generation         Gera os data set simulados para as recomendações
    send-data-ga       Envia dados simulados para o Google Analytics
```

#### Generate DataSets
```
# Generation customers csv
$ simulator generation customers -f csv

# Generation customers json
$ simulator generation customers -f json

# Generation products csv
$ simulator generation products -f csv

# Generation products json
$ simulator generation products -f json

```
#### Full Options
```
usage: simulator generation [-h] [--desc-path DESC_PATH] [--rows ROWS]
                            --format {csv,json} [{csv,json} ...]
                            {customers,products}

positional arguments:
  {customers,products}  Arquivo que sera gerado pelo processo

optional arguments:
  -h, --help            show this help message and exit
  --desc-path DESC_PATH, -d DESC_PATH
                        Pasta onde sera salvo os dataset gerados
  --rows ROWS, -r ROWS  Quantidades de Linhas geradas
  --format {csv,json} [{csv,json} ...], -f {csv,json} [{csv,json} ...]
                        Formato do arquivo de saida que sera salvo,pode ser
                        adiciona mais de um tipo ao mesmo tempo
```

#### Send events to GA

```
$ simulator send-data-ga pageview \
    -c https://github.com/cesarbruschetta/bart-recs/datasets/customers.csv \
    -p https://github.com/cesarbruschetta/bart-recs/datasets/products.csv \
    -i 10 \
    -gaId "ga:123456789"
```

#### Full Options
```
usage: simulator send-data-ga [-h] --customers CUSTOMERS --products PRODUCTS
                              [--interactions INTERACTIONS]
                              {pageview}

positional arguments:
  {pageview}            Tipo de evento que sera enviado ao GA

optional arguments:
  -h, --help            show this help message and exit
  --ga-track-id GA_TRACK_ID, -gaId GA_TRACK_ID
                        Id de acompanhamento para o sua conta do GA
  --customers CUSTOMERS, -c CUSTOMERS
                        Caminho para o dataset de customers, em csv
  --products PRODUCTS, -p PRODUCTS
                        Caminho para o dataset de products, em csv
  --interactions INTERACTIONS, -i INTERACTIONS
                        Quantidades de interações geradas
  --random-interactions
                        Gerar uma quantidades de interações randomicas                        
```