import pandas as pd
import numpy as np
import scipy.spatial

test = {}
train = {}
for i in range(5):#lectura de archivo tipo excel de folds
    test[i] = pd.read_excel(io = "df_parte2_folds.xlsx", sheet_name="test"+str(i+1))
    train[i] = pd.read_excel(io = "df_parte2_folds.xlsx", sheet_name="train"+str(i+1))

class KNN:
    def __init__(self, k):
        self.k = k#cantidad de vecinos más proximos

    def disteuclidiana(self, test, train):
        del test['CDR'] #Se borra temporalmente la columna elegida como clase tanto en test como en train
        del train['CDR']
        return  scipy.spatial.distance.euclidean(train, test)

    def kvecinos(self, test, train, newdict):
        newdict = pd.DataFrame()
        d = {}
        for j in range(len(test)):
            aux = pd.DataFrame()
            for q in range(len(train)):
                #calculo de la distancia euclidiana
                distancia = self.disteuclidiana(test.iloc[j], train.iloc[q])
                #alojamiento de datos escenciales
                d['Distancia'] = distancia
                d['CDR_test'] = test.loc[test.index[j], 'CDR']
                d['CDR_train'] = train.loc[train.index[q], 'CDR']  
                aux = aux.append(d, ignore_index=True)
            #orden de datos en funcion a la distancia mas corta
            aux = aux.sort_values('Distancia')
            #agrega a un dataframe las k distancias más cortas
            newdict = newdict.append(aux[0:self.k], ignore_index=True) 
        return newdict  

    def prediccion(self, distancias):
        aux = pd.DataFrame()
        data = pd.DataFrame()
        d = {}
        count0 = 0
        count1 = 0
        for i in range(0,40):#recorre el dataframe de distancias
            min = self.k*i
            max = self.k*(i+1)
            #se recorre las k distancias por fila de testeo
            aux = distancias[min:max].reset_index()
            #se predice la clase por votacion
            for j in range(self.k):
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
            #se genera un nuevo dataframe con la fila de testeo, su clase y su clase predicha
            data = data.append(d, ignore_index=True)
        return data

    def aciertos(self, prediccion, f):
        prob = {}
        exito = 0
        fracaso = 0 
        #se cuenta los aciertos
        for j in range(0, 40):
            if prediccion.loc[prediccion.index[j], 'CDR_test'] == prediccion.loc[prediccion.index[j], 'CDR_predictorio']:
                exito = exito+1
            else: 
                fracaso=fracaso+1
        #se genera un nuevo dataframe con los datos que se desea imprimir en pantalla
        prob['Folds'] = int(f)
        prob['N° Aciertos'] = exito
        prob['N° Errores'] = fracaso
        prob['% Acierto Local'] = (exito*100)/(exito+fracaso)
        return prob

    def detalles(self):#correccion de indices
        aux = pd.DataFrame(test[1])
        if 'Index' in aux.columns:
            for i in range(5): 
                aux = pd.DataFrame(test[i])
                aux.set_index('Index', inplace = True)
                test[i] = aux
                aux = pd.DataFrame(train[i])
                aux.set_index('Index', inplace = True)
                train[i] = aux
        else:
            pass

    def __str__(self):#funcion principal
        split = {}
        acierto =pd.DataFrame({})
        self.detalles()
        for i in range(0, 5):
            split[i] = {}
            split[i] = self.kvecinos(test[i], train[i], split[i])    
            split[i] = self.prediccion(split[i])
            aux = self.aciertos(split[i], i)
            acierto = acierto.append(aux, ignore_index=True)
        acierto['% Acierto Global']= acierto['% Acierto Local'].sum(axis=0)/acierto.shape[0]
        acierto['Desviacion Estandar'] = np.std(acierto['% Acierto Local'])
        acierto['Folds'] = acierto['Folds'].apply(np.int64)
        acierto.set_index('Folds', inplace = True)
        return acierto.to_string()