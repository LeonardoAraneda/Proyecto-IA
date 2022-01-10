import numpy as np
import pandas as pd

# Parametros de la red
_N = 2# Neuronas en la capa oculta
_ITER = 100

class RNA:

    def __init__(self, k):
        self.k = k

    def sigmoid(self, x):# Funcion sigmoide de x
        return 1 / (1 + np.exp(-x))

    def relu(self, X):# Funcion rampa de x
        return np.maximum(0,X)

    def entrenamiento(self, datos, clase, wt1, wt2):
        d = {}
        predict = pd.DataFrame()
        for indice_fila, fila in datos.iterrows():
            if self.k == 1:
                z = self.sigmoid(np.matmul(fila, wt1))# Operaciones en la primer capa
                y_ = self.sigmoid(np.matmul(wt2, z))# Calcular la salida de la neurona de salida
            else:
                z = self.relu(np.matmul(fila, wt1))# Operaciones en la primer capa
                y_ = self.relu(np.matmul(wt2, z))# Calcular la salida de la neurona de salida
            d['Clase real'] = clase.loc[indice_fila, 'CDR']
            d['Valor de salida'] = y_
            predict = predict.append(d, ignore_index = True)    
        error = np.square(np.subtract([clase], [predict["Valor de salida"]])).mean() # Calcular el error cuadratico medio
        predict = predict.append({'Clase real': "ECM: "+str(error)}, ignore_index=True) # Almacenar los errores de la red en un ciclo   
        return predict

    def __str__(self):
        writer = pd.ExcelWriter('df_parte5_rna.xlsx')
        for i in range(5):
            print("Entrenando folds: "+str(i+1))
            # Variables de inicialización
            df = pd.read_excel(io = "df_parte2_folds.xlsx", sheet_name="train"+str(i+1)) # leer archivo excel, Hoja de trabajo
            df = df.set_index(df.columns.values[0])
            # Datos de entrada
            datos = df.iloc[:, df.columns != "CDR"]
            clase = df.iloc[:, df.columns == "CDR"]
            m, k = datos.shape
            wt1 = (np.random.rand(k,_N)*0.98)+0.01# Inicializacion de pesos sinapticos
            wt2 = (np.random.rand(_N)*0.98)+0.01# Inicializacion de pesos sinapticos
            for j in range(_ITER):
                p = self.entrenamiento(datos, clase, wt1, wt2)#Inicializar la red
            p.to_excel(writer, sheet_name=("Fold "+str(i+1)))
        writer.save()
        writer.close()
        return str("Listo\n")


    

