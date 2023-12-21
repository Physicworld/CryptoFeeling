import datetime


# Creamos clase article castando sus parametros para que solo se permitan si son de este tipo
class Article:
    # Función constructora
    def __init__(self,
                 id: int,
                 url: str,
                 title: str,
                 author: str,
                 datetime: datetime.datetime,
                 content: str,
                 sentiment: float):
        self.id = id
        self.url = url
        self.title = title
        self.author = author
        self.datetime = datetime
        self.content = content
        self.sentiment = sentiment
    '''
    def __init__(self,
                 url: str,
                 title: str,
                 author: str,
                 datetime: datetime.datetime,
                 content: str,
                 confidence: float,
                 sentiment: float):
        self.url = url
        self.title = title
        self.author = author
        self.datetime = datetime
        self.content = content
        self.confidence = confidence
        self.sentiment = sentiment
    '''
