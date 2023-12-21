from scrapy.crawler import CrawlerProcess
from Scraping.scraper.spiders.spiders_sitemap import MySpyder

import logging
from scrapy.utils.log import configure_logging

# Configuración de logging
configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='scrapy.log',
    format='%(levelname)s: %(message)s',
    level=logging.WARNING
)


def run_spyder():
    # Definir el objeto process, para tener solo errores
    # process = CrawlerProcess(get_project_settings())

    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'ERROR',
    })

    # Generar el crawler con la info de la clase MySpyder
    process.crawl(MySpyder)

    # Iniciar el Crawler
    process.start()

    # Parar el Crawler
    process.stop()
