import pandas as pd

class KFOLD:
    data = pd.read_excel("df_parte1_normalizado.xlsx") #variables de clases
    def __init__(self):
        pass

    def detalles(self):#funcion encargada de asignar el indice correspondiente
        self.data = self.data.rename(columns={'Unnamed: 0':'Index'})
        self.data.set_index('Index', inplace = True)

    def foldk(self, dt, i, k):#funcion que recorre en funcion de el k elegido
        n = len(dt)
        return dt[n*(i-1)//k:n*i//k]

    def __str__(self):#funion principal que retorna los folds creados
        folds = {}
        self.detalles()
        for i in range(5):#ciclo que asigna el test y el train correspondiente
            test = self.foldk(self.data.sample(frac=1, random_state=1), i+1, 5)
            train = self.data.drop(labels=test.index, axis=0)
            folds[i] = {'entrenamiento': train, 'prueba': test}
        writer = pd.ExcelWriter('df_parte2_folds.xlsx')
        for i in range(5):
            folds[i]["prueba"].to_excel(writer, sheet_name=("test"+str(i+1)))
            folds[i]["entrenamiento"].to_excel(writer, sheet_name="train"+str(i+1))
        writer.save()
        writer.close()
        return str(folds)  