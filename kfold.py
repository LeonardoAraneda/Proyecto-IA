import pandas as pd
import numpy as np


class KFOLD:

    data = pd.read_excel("df_parte1_normalizado.xlsx") #variables de clases
    def __init__(self):
        None

    def detalles(self):
        self.data = self.data.rename(columns={'Unnamed: 0':'Index'})
        self.data.set_index('Index', inplace = True)


    def foldk(self, dt, i, k):
        n = len(dt)
        return dt[n*(i-1)//k:n*i//k]

    def __str__(self):
        folds = {}
        self.detalles()
        for i in range(0,5):
            test = self.foldk(self.data.sample(frac=1, random_state=1), i+1, 5)
            train = self.data.drop(labels=test.index, axis=0)
            folds[i] = {'entrenamiento': train, 'prueba': test}
        writer = pd.ExcelWriter('df_parte2_folds.xlsx')
        for i in range(0,5):
            folds[i]["prueba"].to_excel(writer, sheet_name=("test"+str(i+1)))
            folds[i]["entrenamiento"].to_excel(writer, sheet_name="train"+str(i+1))
        writer.save()
        writer.close()
        return str(folds)
        