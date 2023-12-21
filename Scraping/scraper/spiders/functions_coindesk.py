import re
from datetime import datetime
import scrapy
from Models.Article import Article

def convert_month_to_number(text):
    # Checkear el texto
    month = 0
    if text == 'Jan':
        month = 1
        return month

    elif text == 'Feb':
        month = 2
        return month

    elif text == 'Marc':
        month = 3
        return month

    elif text == 'Apr':
        month = 4
        return month

    elif text == 'May':
        month = 5
        return month

    elif text == 'Jun':
        month = 6
        return month

    elif text == 'Jul':
        month = 7
        return month

    elif text == 'Aug':
        month = 8
        return month

    elif text == 'Sep':
        month = 9
        return month

    elif text == 'Oct':
        month = 10
        return month

    elif text == 'Nov':
        month = 11
        return month

    elif text == 'Dec':
        month = 12
        return month

    else:
        print('Error, Mes erróneo')
        return None

def convert_fecha_to_datetime(date):
    aux = []

    # Dividimos los strings por espacios en blanco
    aux = date.split(' ')
    # resultado ['Mes', 'Dia,', 'Año']

    # Quitar la coma de Dia y sustituirla por nada
    aux[1] = re.sub(',', '', aux[1])

    # Convertir el Mes de manera escrita (ej:November) en numero
    aux[0] = convert_month_to_number(aux[0])

    # Crear la fecha a partir de aux
    new_date = datetime(int(aux[2]), int(aux[0]), int(aux[1]))
    # Nota: convertimos los string a entero, realmente el de mes (aux[0]) no haria falta
    #      porque la función convert_month_to_number devuelve un entero.

    # Return New dates
    return new_date

def parse_featurenew(element):
    # Obtenemos los atributos de las webs
    url = element.css('div.gridstyles__StyledGrid-sc-eiwl28-0.eoKngA > div.featured-leaderboardstyles__ArticleCardWrapper-sc-15oqi80-1.hJDHQZ > div.article-cardstyles__StyledWrapper-sc-q1x8lc-0.eJFoEa.article-card.default > div > div.article-cardstyles__AcTitle-sc-q1x8lc-1.PUjAZ.articleTextSection > h3 > a::attr(href)').get()
    titulo = element.css('div.gridstyles__StyledGrid-sc-eiwl28-0.eoKngA > div.featured-leaderboardstyles__ArticleCardWrapper-sc-15oqi80-1.hJDHQZ > div.article-cardstyles__StyledWrapper-sc-q1x8lc-0.eJFoEa.article-card.default > div > div.article-cardstyles__AcTitle-sc-q1x8lc-1.PUjAZ.articleTextSection > h3 > a::text').get()
    content = element.css('div.gridstyles__StyledGrid-sc-eiwl28-0.eoKngA > div.featured-leaderboardstyles__ArticleCardWrapper-sc-15oqi80-1.hJDHQZ > div.article-cardstyles__StyledWrapper-sc-q1x8lc-0.eJFoEa.article-card.default > div > div.article-cardstyles__AcTitle-sc-q1x8lc-1.PUjAZ.articleTextSection > div.display-desktop-block.display-tablet-block.display-mobile-block > p > span::text').get()
    author = element.css('div.gridstyles__StyledGrid-sc-eiwl28-0.eoKngA > div.featured-leaderboardstyles__ArticleCardWrapper-sc-15oqi80-1.hJDHQZ > div.article-cardstyles__StyledWrapper-sc-q1x8lc-0.eJFoEa.article-card.default > div > div.article-cardstyles__AcTitle-sc-q1x8lc-1.PUjAZ.articleTextSection > div.article-cardstyles__AcMeta-sc-q1x8lc-2.czpIgS.articleMetaSection > div.display-desktop-block.display-tablet-block.display-mobile-block.ac-authors > div > a > span::text').get()
    fecha = element.css('div.gridstyles__StyledGrid-sc-eiwl28-0.eoKngA > div.featured-leaderboardstyles__ArticleCardWrapper-sc-15oqi80-1.hJDHQZ > div.article-cardstyles__StyledWrapper-sc-q1x8lc-0.eJFoEa.article-card.default > div > div.article-cardstyles__AcTitle-sc-q1x8lc-1.PUjAZ.articleTextSection > div.article-cardstyles__AcMeta-sc-q1x8lc-2.czpIgS.articleMetaSection > div.timing-data > div.display-desktop-block.display-tablet-block.display-mobile-block.ac-publishing-date > div.display-desktop-block.display-tablet-block.display-mobile-block > span::text').get()
    # Nota: Para obtener el texto se usa ::text después de la ruta, y para un atributo ::attr(nombre)

    # Convertir fecha a datetime
    fecha = convert_fecha_to_datetime(fecha)

    # Devolvemos un diccionario con la info
    #dict = {'url': url, 'titulo': titulo, 'content': content, 'author': author, 'fecha': fecha}

    # Devolvemos un objeto Article
    return Article(url=url, title=titulo, author=author, datetime=datetime, content=content, confidence=0.0, sentiment=0.0)

def extract_other_features(div_news):
    # Variables auxiliareas
    other_features = []

    # Loop for the div_news
    for div_new in div_news:
        div_new_url = scrapy.Selector(text=div_new).css('div.article-cardstyles__StyledWrapper-sc-q1x8lc-0.eJFoEa.article-card.default > div > div.article-cardstyles__AcTitle-sc-q1x8lc-1.PUjAZ.articleTextSection > h6 > a::attr(href)').get()
        div_new_titulo = scrapy.Selector(text=div_new).css('div.article-cardstyles__StyledWrapper-sc-q1x8lc-0.eJFoEa.article-card.default > div > div.article-cardstyles__AcTitle-sc-q1x8lc-1.PUjAZ.articleTextSection > h6 > a::text').get()
        div_new_author = scrapy.Selector(text=div_new).css('div.article-cardstyles__StyledWrapper-sc-q1x8lc-0.eJFoEa.article-card.default > div > div.article-cardstyles__AcTitle-sc-q1x8lc-1.PUjAZ.articleTextSection > div.article-cardstyles__AcMeta-sc-q1x8lc-2.czpIgS.articleMetaSection > div.display-desktop-block.display-tablet-block.display-mobile-block.ac-authors > div > a > span::text').get()
        div_new_fecha = scrapy.Selector(text=div_new).css('div.article-cardstyles__StyledWrapper-sc-q1x8lc-0.eJFoEa.article-card.default > div > div.article-cardstyles__AcTitle-sc-q1x8lc-1.PUjAZ.articleTextSection > div.article-cardstyles__AcMeta-sc-q1x8lc-2.czpIgS.articleMetaSection > div.timing-data > div.display-desktop-block.display-tablet-block.display-mobile-block.ac-publishing-date > div.display-desktop-block.display-tablet-block.display-mobile-block > span::text').get()
        div_new_content = scrapy.Selector(text=div_new).css('div.article-cardstyles__StyledWrapper-sc-q1x8lc-0.eJFoEa.article-card.default > div > div.article-cardstyles__AcTitle-sc-q1x8lc-1.PUjAZ.articleTextSection > div.display-desktop-block.display-tablet-block.display-mobile-block > span > span::text').get()

        # Convertir a fecha
        div_new_fecha = convert_fecha_to_datetime(div_new_fecha)

        # Convertir a diccionario
        article_aux = Article(url=div_new_url, title=div_new_titulo, author=div_new_author, datetime=div_new_fecha, content=div_new_content, confidence=0.0, sentiment=0.0)

        # Append en other_features
        other_features.append(article_aux)

    # Return de other_features
    return other_features

def extract_trendingnews(div_trendings):
    # Variables auxiliares
    news_group = []

    # Loop to the news
    for div_trending in div_trendings:
        div_trending_url = scrapy.Selector(text=div_trending).css('div > div.side-cover-cardstyles__SideCoverCardData-sc-1nd3s5z-2.gnuOAQ > a::attr(href)').get()
        div_trendig_title = scrapy.Selector(text=div_trending).css('div > div.side-cover-cardstyles__SideCoverCardData-sc-1nd3s5z-2.gnuOAQ > a > div > h2::text').get()
        div_trendig_fecha = scrapy.Selector(text=div_trending).css('div > div.side-cover-cardstyles__SideCoverCardData-sc-1nd3s5z-2.gnuOAQ > div > div > span::text').get()
        div_trendig_fecha = convert_fecha_to_datetime(div_trendig_fecha)

        # Convertir a un articulo
        articulo_aux = Article(url=div_trending_url, title=div_trendig_title, author='', datetime=div_trendig_fecha, content='', confidence=0.0, sentiment=0.0)

        # Append en news_group
        news_group.append(articulo_aux)

    # Return news_group
    return news_group

def extract_newcolumnews(div_columnews):
    # Variables necesarias
    news_group = []

    # Loop a las news internas de div_columnew
    for div_columnew in div_columnews:
        div_columnew_url = scrapy.Selector(text=div_columnew).css('div.side-cover-cardstyles__SideCoverCardData-sc-1nd3s5z-2.gnuOAQ > a::attr(href)').get()
        div_columnew_title = scrapy.Selector(text=div_columnew).css('div.side-cover-cardstyles__SideCoverCardData-sc-1nd3s5z-2.gnuOAQ > a > div > h2::text').get()
        div_columnew_author = scrapy.Selector(text=div_columnew).css('div.side-cover-cardstyles__SideCoverCardData-sc-1nd3s5z-2.gnuOAQ > div > div.card-authorsstyles__CardAuthorsWrapper-sc-1apfzbw-0.gJMKuU > a::text').get()
        div_columnew_fecha = scrapy.Selector(text=div_columnew).css('div.side-cover-cardstyles__SideCoverCardData-sc-1nd3s5z-2.gnuOAQ > div > div.card-datestyles__CardDateWrapper-sc-y5z1ee-0.eeyqKG > span::text').get()

        div_columnew_fecha = convert_fecha_to_datetime(div_columnew_fecha)

        # Convertir a un diccionario
        articulo_aux = Article(url=div_columnew_url, title=div_columnew_title, author=div_columnew_author, datetime=div_columnew_fecha, content='', confidence=0.0, sentiment=0.0)

        # Append en news_group
        news_group.append(articulo_aux)

    # Return news_group
    return news_group

def extract_div_blocknews(div_block_news):
    # Variables auxiliares
    news_group = []

    # Loop para las noticias de div_block_news
    for div_block_new in div_block_news:
        div_block_new_title = scrapy.Selector(text=div_block_new).css('h5 > a::text').get()
        div_block_new_url = scrapy.Selector(text=div_block_new).css('h5 > a::attr(href)').get()
        div_block_new_content = scrapy.Selector(text=div_block_new).css('div.display-desktop-block.display-tablet-block.display-mobile-block > p > span::text').get()
        div_block_new_fecha = scrapy.Selector(text=div_block_new).css('div.article-cardstyles__AcMeta-sc-q1x8lc-2.czpIgS.articleMetaSection > div.timing-data > div.display-desktop-block.display-tablet-block.display-mobile-none.ac-publishing-date > div.display-desktop-block.display-tablet-block.display-mobile-block > span::text').get()

        # convert fecha to datetime
        div_block_new_fecha = convert_fecha_to_datetime(div_block_new_fecha)

        # Almacenar en un diccionario
        dict_new = {'url': div_block_new_url, 'title': div_block_new_title, 'content': div_block_new_content, 'fecha': div_block_new_fecha}

        # Append en news_group
        news_group.append(dict_new)

    # Return news_group
    return news_group
