import pandas as pd
import numpy as np
import scipy.spatial

class KNN:
    def __init__(self, folds, k):
        self.folds = folds
        self.k = k

    def disteuclidiana(test, train):
        del test['CDR'] #Se borra temporalmente la columna elegida como clase tanto en test como en train
        del train['CDR']
        return  scipy.spatial.distance.euclidean(train, test)

    def kvecinos(self, test, train, newdict):
        newdict = pd.DataFrame()
        d = {}
        for j in range(len(test)):
            aux = pd.DataFrame()
            for q in range(len(train)):
                distancia = self.disteuclidiana(test.iloc[j], train.iloc[q])
                d['Distancia'] = distancia
                d['CDR_test'] = test.loc[test.index[j], 'CDR']
                d['CDR_train'] = train.loc[train.index[q], 'CDR']  
                aux = aux.append(d, ignore_index=True)
            aux = aux.sort_values('Distancia')
            newdict = newdict.append(aux[0:self.k], ignore_index=True) 
        return newdict  


    def prediccion(self, distancias):
        aux = pd.DataFrame()
        data = pd.DataFrame()
        d = {}
        count0 = 0
        count1 = 0
        for i in range(0,40):
            min = self.k*i
            max = self.k*(i+1)
            aux = distancias[min:max].reset_index()
            for j in range(0, self.k):
                if aux.loc[aux.index[j], 'CDR_train'] == 1.0:
                    count1+=1
                else: 
                    count0+=1
            if count1 > count0:
                d['CDR_predictorio'] = 1
            else:
                d['CDR_predictorio'] = 0
            d['CDR_test'] = aux.loc[aux.index[0], 'CDR_test']
            count0 = 0
            count1 = 0
            data = data.append(d, ignore_index=True)
        return data

    def aciertos(self, prediccion, f):
        prob = {}
        exito = 0
        fracaso = 0 
        for j in range(0, 40):
            if prediccion.loc[prediccion.index[j], 'CDR_test'] == prediccion.loc[prediccion.index[j], 'CDR_predictorio']:
                exito = exito+1
            else: 
                fracaso=fracaso+1
        prob['Folds'] = int(f)
        prob['N° Aciertos'] = exito
        prob['N° Errores'] = fracaso
        prob['% Acierto Local'] = (exito*100)/(exito+fracaso)
        return prob

    def __str__(self):
        split = {}
        acierto =pd.DataFrame({})
        for i in range(0, 5):
            split[i] = {}
            split[i] = self.kvecinos(self.folds[i]["prueba"], self.folds[i]["entrenamiento"], split[i])    
            split[i] = self.prediccion(split[i])
            aux = self.aciertos(split[i], i)
            acierto = acierto.append(aux, ignore_index=True)
        acierto['% Acierto Global']= acierto['% Acierto Local'].sum(axis=0)/acierto.shape[0]
        acierto['Desviacion Estandar'] = np.std(acierto['% Acierto Local'])
        acierto['Folds'] = acierto['Folds'].apply(np.int64)
        acierto.set_index('Folds', inplace = True)
        return acierto.to_string()