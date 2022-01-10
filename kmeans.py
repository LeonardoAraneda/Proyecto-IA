import pandas as pd
import random
from scipy.spatial import distance

df = pd.DataFrame(pd.read_excel("df_parte1_normalizado.xlsx"))
df = df.set_index(df.columns.values[0])
if 'CDR' in df.columns:
    data = df.drop('CDR', axis=1)
else:
    pass
_ITER = 20

class KMEANS:
    def __init__(self):
        pass

    def inicio(self):
        centroide1 = data.iloc[random.randint(0, data.shape[0])]
        centroide2 = data.iloc[random.randint(0, data.shape[0])]
        cluster0 = pd.DataFrame()
        cluster1 = pd.DataFrame()
        for i in range(data.shape[0]):
            distancia1 = distance.euclidean(data.iloc[i], centroide1)
            distancia2 = distance.euclidean(data.iloc[i], centroide2)         
            if (distancia1 > distancia2):
                cluster0 = cluster0.append(df.iloc[i])
            else:
                cluster1 = cluster1.append(df.iloc[i])
        probabilidad = [[0,0],[0,0]]
        for k in range(len(cluster0)):
            if(cluster0.iloc[k][0] == 1):
                probabilidad[0][0] += 1
            else:
                probabilidad[0][1] += 1       
        for k in range(len(cluster1)):
            if(cluster1.iloc[k][0] == 1):
                probabilidad[1][0] += 1
            else:
                probabilidad[1][1] += 1  
        return cluster0, cluster1, probabilidad
    
    def fin(self, cluster0, cluster1, p):

        for n in range(_ITER):
            centroide1 = cluster0.mean()/cluster0.shape[0]
            centroide1 = centroide1.drop('CDR', axis=0)
            centroide2 = cluster1.mean()/cluster1.shape[0]
            centroide2 = centroide2.drop('CDR', axis=0)
            cluster0 = pd.DataFrame()
            cluster1 = pd.DataFrame()
            for i in range(data.shape[0]):
                distancia1 = distance.euclidean(data.iloc[i], centroide1)
                distancia2 = distance.euclidean(data.iloc[i], centroide2)
                if (distancia1 > distancia2):
                    cluster0 = cluster0.append(df.iloc[i])
                else:
                    cluster1 = cluster1.append(df.iloc[i])  
            probabilidad = [[0,0],[0,0]]
            for k in range(0, len(cluster0)):
                if(cluster0.iloc[k][0] == 1):
                    probabilidad[0][0] += 1
                else:
                    probabilidad[0][1] += 1
                    
            for k in range(0, len(cluster1)):
                if(cluster1.iloc[k][0] == 1):
                    probabilidad[1][0] += 1
                else:
                    probabilidad[1][1] += 1
            if probabilidad < p:
                p=probabilidad
        return p
    
    def __str__(self):
        a, b, c =self.inicio()
        d = self.fin(a, b, c)
        for i in range(len(d)):
            for j in range(len(d[i])):
                d[i][j] = round((d[i][j]/200)*100, 1)
        return (str(d))

