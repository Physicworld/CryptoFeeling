import pandas as pd

class DataFrameReader:
    # Función constructora
    def __init__(self, filename):
        self.filename = filename
        self.data = None

    # Función de lectura
    def read(self):
        self.data = pd.read_csv(self.filename)
        return self.data

    # Función para el formato
    def format(self, formatter):
        self.data = formatter(self.data)
        return self.data