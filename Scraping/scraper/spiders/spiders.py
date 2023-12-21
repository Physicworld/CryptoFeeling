import pandas as pd
import scrapy
from pprint import pprint
from Models.Article import Article

from Scraping.spiders.functions_coindesk import parse_featurenew, extract_other_features, extract_trendingnews, extract_newcolumnews

class MySpyder(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.coindesk.com/markets/']

    '''
        def parse(self, response):
        # Buscamos todos los urls que contengan un href
        urls = response.css('a::attr(href)').getall()

        # Filtramos de la seccion de mercados
        urls = [url for url in urls if url.startswith('/markets') or
                                       url.startswith('/tech') or
                                       url.startswith('/business') or
                                       url.startswith('/policy')]
        # Eliminar las listas repetidas
        urls = list(dict.fromkeys(urls))
        ## Nota: Funciona ya que convierte cada url a una clave, como en un dict no puede tener varias claves,
        ##       entonces elimina los duplicados, para después convertirlo a lista.
        print('Se han encontrado {} urls'.format(len(urls)))

        for url in urls:
            print(url)

        yield None
    '''
    def parse(self, response):
        # Captamos el main
        main = response.css('main')
        if main:
            # Lista de las noticias features
            news = []

            # Dentro del main, tomamos las secciones importantes
            section1 = main.css('section:nth-child(1)') # Seccion de las noticias features
            section2 = main.css('section:nth-child(2)') # Sección Trending in Markets
            section3 = main.css('section:nth-child(3)') # Seccion derecha News
            #section4 = main.css('') # Seccion de More News

            # Sección 1
            if section1:
                # Buscar la primera seccion con las noticias features
                element = section1.css('div[class="featured-leaderboardstyles__StyledWrapper-sc-15oqi80-0 bUdaRS"]')

                if element:
                    # 1) Busqueda de la noticia principal
                    article_feature = parse_featurenew(element)
                    news.append(article_feature)

                    # 2) Busqueda de las noticias features auxiliares
                    ## Obtener el elemento div
                    element2 = element.css('div.gridstyles__StyledGrid-sc-eiwl28-0.eoKngA > div.featured-leaderboardstyles__ArticlesListWrapper-sc-15oqi80-2.csmkJj')

                    ## Extraer las noticias de element2
                    div_news = element2.css('div[class="featured-leaderboardstyles__ArticleCardWrapper-sc-15oqi80-1 hBVYcp"]').getall()

                    ## Iteramos cada div_news y generamos cada articulo
                    other_features = extract_other_features(div_news)

                    # 3) Extendemos la lista con las nuevas noticias
                    news += other_features

                # Seccion 2
                if section2:
                    # 1) Buscamos el elemento div que contiene las 4 noticias
                    element3 = section2.css('div > div.defaultstyles__CategoryGriddWrapper-sc-1qah0uj-0.knJmDH > div.gridstyles__StyledGrid-sc-eiwl28-0.ceVgic')

                    # 2) Dentro extraemos las noticias
                    div_trendings = element3.css('div[class="defaultstyles__CardWrapper-sc-1qah0uj-3 bXbSYL"]').getall()

                    # 3) Extraemos la info de las noticias en cada una
                    trending_news = extract_trendingnews(div_trendings)

                    # Extend noticias
                    news += trending_news

                # Section 3
                if section3:
                    # 1) Localizar el elemento que contiene los div dentro
                    element4 = section3.css('div > div.defaultstyles__StyledWrapper-sc-q32wxa-0.cDFYcd > div > div:nth-child(2) > div > div.defaultstyles__CardColumn-sc-77yn7j-0.iJHYAG')

                    # 2) Seleccionamos las noticas dentro de element4 que son div de una clase en especifico
                    div_columnews = element4.css('div[class="side-cover-cardstyles__SideCoverCardWrapper-sc-1nd3s5z-0 bTtqXW"]').getall()

                    # 3) Extract the info of the list div_columnews
                    columnnew_news = extract_newcolumnews(div_columnews)

                    # 4) Extend news
                    news += columnnew_news

                # TO DO :
                # Section 4
                '''
                if section4:
                    print('More News')
                    print('-' * 50)
                    print(section4)
                    contenido_segundo_div = section4.css('::text').getall()
                    print(contenido_segundo_div)

                    # Seleccionamos los dos bloques iniciales de noticias
                    #articles = scrapy.Selector(text=section4).css('div[class="article-cardstyles__StyledWrapper-sc-q1x8lc-0 eJFoEa article-card default"]').getall()
                    ##main > div > div.articles-timelinestyles__StyledWrapper-sc-k3mqsf-0.gifvDT > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)
                    #for article in articles:
                        # Extract the info de cada div_block
                     #   article_title = scrapy.Selector(text=article).css('div > div.article-cardstyles__AcTitle-sc-q1x8lc-1.PUjAZ.articleTextSection > h5 > a::text').get()
                     #   print(article_title)


                    #element5 = scrapy.Selector(text=section4).css('div:nth-child(2) > div:nth-child(2) > div:nth-child(2)').get()
                    #print(element5)
                    # Captar los bloques de noticias
                    #div_blocks = scrapy.Selector(text=element5).css('div[class="article-cardstyles__StyledWrapper-sc-q1x8lc-0 eJFoEa article-card default"]').getall()
                    #print(div_blocks)
                    #if div_blocks:
                    #    print('No esta vacio')
                    #else:
                     #   print('esta vacio')
                    
                    # Loop de div_block, para extraer las noticias de cada bloque y despues su informacion
                    news_div_blocks = []
                    cont = 1
                    for div_block in div_blocks:
                        div_block_news = scrapy.Selector(text=div_block).css('div[class="article-cardstyles__AcTitle-sc-q1x8lc-1 PUjAZ articleTextSection "]').getall()

                        if div_block_news:
                            print('No esta vacio')
                        else:
                            print('esta vacio')
                        
                        # Extract the info de cada div_block
                        news_div_block = extract_div_blocknews(div_block_news)

                        # Concatenar las dos lista
                        if cont == 1:
                            news_div_blocks = news_div_block
                            cont += 1
                        else:
                            news_div_blocks += news_div_block
                            cont += 1
                        
    
                    # Mostramos las noticias dentro de news_div_blocks
                    for news in news_div_blocks:
                        pprint(news)
                        print('\n')
                    '''
                # Guardar en un archivo
                urls = []
                titles = []
                authors = []
                datetimes = []
                contents = []
                confidences = []
                sentiments = []

                for article in news:
                    urls.append(article.url)
                    titles.append(article.title)
                    authors.append(article.author)
                    datetimes.append(article.datetime)
                    contents.append(article.content)
                    confidences.append(article.confidence)
                    sentiments.append(article.sentiment)

                dict = {'url': urls, 'title': titles, 'author': authors, 'datetime': datetimes,
                        'content': contents, 'confidence': confidences, 'sentiment': sentiments}

                df = pd.DataFrame(dict)

                path = "data/articles_coindesk.csv"
                df.to_csv(path, index=False)

        else:
            #print('Error: Objeto Main NO encontrado')
            self.logger.warning('Error: Objeto Main NO encontrado')


