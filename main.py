"""
By: Joaquin Millian
"""
import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Importar las clases articulo y Plotter
from Plotter import Plotter

# Importar nuestros lectores
from Readers.SQLiteReader import SQLiteReader
from Readers.dataframe_reader import DataFrameReader

# Importar nuestros Formatters
from Formatters.OHLCVFormatter import OHLCVFormatter
from Formatters.ArticleFormatter import ArticleFormatter

from scrapy.crawler import CrawlerProcess
from Scraping.scraper.spiders.spiders_sitemap import MySpyder
from Scraping.scraper.settings import ITEM_PIPELINES, USER_AGENT_LIST

import logging
from scrapy.utils.log import configure_logging

# Options de pandas para mostrar el maximo de columns y rows df
pd.set_option('display.max_columns', None)  # Para mostrar todas las columnas de un df
pd.set_option('display.max_rows', None)    # Para mostrar todas las filas de un df


'''
def main():
   # Leer el archivo de BTC
   path_ohlcv = "data/BTCUSD.csv"
   ohlcv_formatter = OHLCVFormatter()
   df_reader = DataFrameReader(path_ohlcv)
   df_reader.read()
   df = df_reader.format(ohlcv_formatter.format)

   # Articulos
   path_articles = "data/articles.csv"
   articles_formatter = ArticleFormatter()
   csv_reader = CSVReader(path_articles)
   csv_reader.read()
   articles = csv_reader.format(formatter=articles_formatter.format)

   # Representamos
   Plotter.plot_candlestick_and_articles(df, articles)
'''

# Configuración de logging
configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='scrapy.log',
    format='%(levelname)s: %(message)s',
    level=logging.WARNING
)


# Generamos un main nuevo para probar el scraper
def run_spider():
    process = CrawlerProcess(settings={
        #'LOG_LEVEL': 'ERROR',
        'ITEM_PIPELINES': ITEM_PIPELINES,
        'USER_AGENT_LIST': USER_AGENT_LIST,
    })
    # Generar el crawler con la info de la clase MySpyder
    process.crawl(MySpyder)

    # Iniciar el Crawler
    process.start()

    # Parar el Crawler
    process.stop()


def main_news():
    run_spider()


def main_represent():
    # Leemos los datos de cotización y los guardamos en un df
    path_ohlcv = "data/BTCUSD.csv"
    ohlcv_formatter = OHLCVFormatter()
    df_reader = DataFrameReader(path_ohlcv)
    df_reader.read()
    df_ohlcv = df_reader.format(ohlcv_formatter.format)

    # Creamos un objeto Reader
    dbReader = SQLiteReader()

    # Nos conectamos a la bbdd
    path_db = 'news_analyzer.db'
    dbReader.connect(path_db)

    # Leemos los articulos de la base de datos
    articles = dbReader.read("SELECT * FROM articles")

    # Cerramos bbdd
    dbReader.close()

    # Le damos el formato y orden adecuado a los articulos (fecha y demas)
    # Creamos un objeto ArticleFormatter
    article_formatter = ArticleFormatter()

    # Formateamos los articles con el formateador
    articles = article_formatter.format(articles)

    # Convertimos a DF
    df_articles = article_formatter.ListToDF(articles)

    # Buscamos noticias de español
    df_clean = article_formatter.only_englishnews(df_articles)

    # Resampleamos por sentimiento
    df_sum = article_formatter.ResampleDF(df_clean[['sentiment']], '1D')

    # Calculamos la media movil y la desviación típica semanaldel sentimiento
    df_sum['rolling_mean_sentiment'] = df_sum['sentiment'].rolling(7).mean()
    df_sum['rolling_std_sentiment'] = df_sum['sentiment'].rolling(7).std()

    # Representamos la evolución del sentimiento
    sns.set_style("darkgrid")
    fig, ax = plt.subplots(2, 1, figsize=(20, 6))

    ax[0].plot(df_ohlcv.loc['2013-04-13':, 'close'])
    ax[0].set_ylabel('Precio')

    ax[1].plot(df_sum['sentiment'], label='Sentimiento')
    ax[1].plot(df_sum['rolling_mean_sentiment'], label='Rolling_mean')
    ax[1].set_xlabel('Fecha')
    ax[1].set_ylabel('Sentimiento agregado')
    ax[1].legend()

    plt.tight_layout()
    plt.show()


# Run the script.
if __name__ == '__main__':
    # Opcciones de ejecución
    recolect_news = False
    represent_articles = True

    if recolect_news:
        main_news()

    if represent_articles:
        main_represent()