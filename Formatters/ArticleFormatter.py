import pandas as pd
import re
import datetime

from Models.Article import Article


'''
# Para pasar de una abreviatura de fecha a numero
def convert_month_to_number(text):
    # Checkear el texto
    if text == 'Jan':
        month = 1
        return month

    elif text == 'Feb':
        month = 2
        return month

    elif text == 'Mar':
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


# Dar formato de fecha a la columna de noticias
def format_date(date):
    # Separamos el string fecha por espacio en blanco
    aux = date.split(' ')
    # Resultado por ejemplo: ['Dec', '5,', '2023', 'at', '7:58', 'a.m.', 'UTC']

    # 1) Obtener mes
    month = convert_month_to_number(aux[0])

    # 2) Obtener el dia, le quitamos la coma
    day = re.sub(',', '', aux[1])
    day = int(day)

    # 3) Obtenemos el año
    year = int(aux[2])

    # 4) Obtener hora y minutos, checkeando primero el valor de a.m. y p.m.
    if aux[5] == 'a.m.':
        # Es antes del medio dia, no se suma 12h
        # Dividimos por :
        aux_hour = aux[4].split(':')

        # Guardamos los valores como entero
        hour = int(aux_hour[0])
        minutes = int(aux_hour[1])

    elif aux[5] == 'p.m.':
        # Es después del medio dia,
        # Dividimos por :
        aux_hour = aux[4].split(':')

        # Guardamos los valores como entero
        hour = int(aux_hour[0])
        minutes = int(aux_hour[1])

        # Vemos si hour es menor 12, en ese caso se le suma 12 horas, pero si es justo 12 no, porque sería al medio dias
        if hour < 12:
            hour += 12

    else:
        print('Error: Formato de fecha incorrecto')
        return None

    # Creamos el objeto fecha que es el que devolvemos
    return datetime(year=year, month=month, day=day,
                    hour=hour, minute=minutes, tzinfo=timezone.utc)
'''

class ArticleFormatter:
    # Dar formato de fecha
    def format_date(date_str):
        # Reemplazar p.m. y a.m. por PM y AM respectivamente
        date_str = re.sub('p.m.', 'PM', date_str)
        date_str = re.sub('a.m.', 'AM', date_str)

        # Quitamos at y UTC
        date_str = re.sub(' at ', ' ', date_str)
        date_str = re.sub(' UTC', '', date_str)

        # Definimos el formato esperado
        date_format = "%b %d, %Y %I:%M %p"

        return datetime.datetime.strptime(date_str, date_format)

    # Dar formato al objeto row cambiando el tipo para los elementos 3, 5 y 6
    def format_row(row):
        # Convertir a lista
        row_convert = list(row)

        row_convert[0] = int(row_convert[0])
        row_convert[4] = ArticleFormatter.format_date(row_convert[4])
        row_convert[6] = float(row_convert[6])

        return row_convert

    def format(self, data):
        # Loop a las filas de data
        data_formated = []
        for row in data:
            # Adaptamos el formato
            row_aux = ArticleFormatter.format_row(row)

            # Añadimos a la lista un objeto Article
            data_formated.append(Article(*row_aux))
        # Return de la info formateada
        return data_formated

    def ListToDF(self, data):
        articles = []

        # Loop the data para sacar las componentes
        for article in data:
            articles.append([article.id, article.url, article.title, article.author,
                             article.datetime, article.content, article.sentiment])

        # Creamos el df con la lista de articles e indicando el nombre de las columnas
        df = pd.DataFrame(articles, columns=['id', 'url', 'title', 'author', 'datetime', 'content', 'sentiment'])

        # Establecemos id como index
        df.set_index('datetime', inplace=True)

        # Ordenamos el df por index
        df.sort_index(inplace=True)

        return df

    # Collaborator: Joaquin Millian
    def only_englishnews(self, df):
        # Creamos una columna binaria si es una noticia española
        df['spanish_new'] = df['url'].apply(lambda x: bool(re.search('/es/', x)))

        # Creamos un subconjunto con solo noticias inglesas
        mask_not_spanish = df['spanish_new'] == False
        df_final = df.loc[mask_not_spanish]

        # Quitamos la columna spanish_new
        df_final.pop('spanish_new')

        return df_final

    def ResampleDF(self, df, timeframe):
        # Creamos la agrupación por suma de sentimiento
        df = df.resample(timeframe).sum()
        return df

