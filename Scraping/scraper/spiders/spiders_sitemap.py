import scrapy

from Scraping.scraper.items import ArticleItem
from scrapy.linkextractors import LinkExtractor
from Scraping.scraper.settings import DEFAULT_REQUEST_HEADERS

urls_tag = ['https://www.coindesk.com/sitemap/' + str(i) for i in range(1, 125)]

class MySpyder(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.coindesk.com/',
                  'https://www.coindesk.com/markets',
                 'https://www.coindesk.com/policy',
                 'https://www.coindesk.com/business',
                 'https://www.coindesk.com/tech',
                 'https://www.coindesk.com/livewire']

    # Para recorrer las 125 paginas
    start_urls.extend(urls_tag)

    def parse(self, response):
        # Definimos Link extractor
        link_extractor = LinkExtractor(
            allow=('/business', '/markets', '/policy', '/tech'),
            deny=('/podcasts', '/videos', '/author', '/page', '/tag', '/category', '/events', '/releases', '/es/')
        )

        # Iniciamos la extracción
        links = link_extractor.extract_links(response)

        # Quitamos los links de los enlaces a la web de markets, business, tech and policy
        '''links = [link for link in links if link.url != 'https://www.coindesk.com/markets/'
                  and link.url != 'https://www.coindesk.com/policy/'
                  and link.url != 'https://www.coindesk.com/business/'
                  and link.url != 'https://www.coindesk.com/tech/']'''

        # Quitamos los duplicados
        links = list(dict.fromkeys(links))
        print('Se han encontrado {} links distintos\n'.format(len(links)))

        # Seguimos los links para extraer la info del artículo
        cont = 1
        for link in links:
            print(f"Link {cont}/{len(links)}")
            cont += 1
            yield response.follow(link.url, self.parse_article)

    def parse_article(self, response):
        print(response.url)
        # Extraemos los atributos de la noticia
        #title = response.css('h1[class="typography__StyledTypography-sc-owin6q-0 bSOJsQ"]::text').get()
        title = response.css('h1::text').get()
        author = response.css('.at-authors a::text').get()
        #datetime = response.css('span[class="typography__StyledTypography-sc-owin6q-0 hcIsFR"]::text').get()
        datetime = response.css('at-created .typography__StyledTypography-sc-owin6q-0::text').get()
        paragrahs = response.css('.typography__StyledTypography-sc-owin6q-0.dbtmOA.at-text p::text').getall()
        text = ' '.join(paragrahs)  # Juntamos todos los parrafos

        # Chequear si title, author y datetime existen sino ponerlo como Unknown
        title = title if title else 'Unknown'
        author = author if author else 'Unknown'
        datetime = datetime if datetime else 'Unknown'

        # Revisar si algún campos de los tres es Unknown
        '''
        if title == 'Unknown' or author == 'Unknown' or datetime == 'Unknown':
            pass
        else:
            yield ArticleItem(url=response.url,
                              title=title,
                              author=author,
                              content=text,
                              datetime=datetime,
                              sentiment=0.0)
        '''