import numpy as np
import pandas as pd


class NORMALIZA:
    
    df = pd.read_csv("oasis_cross-sectional.csv") #variables de clases
    def __init__(self):
        pass

    def detalles(self):#Funcion encargada de corregir el nombre de la variable y transformar los datos categoricos a numericos.
        self.df = self.df.rename(columns={'M/F':'Sex'})
        #Inicio "limpieza" de datos--------
        self.df.dropna(subset=['Educ'],inplace=True) 
        self.df.drop(columns=['ID','Hand','SES'], axis = 1, inplace=True)
        self.df.dropna(axis=1,inplace=True)
        self.df = self.df.fillna("", inplace=False)
        #Fin "limpieza" de datos----------
        for i in range(len(self.df)):#Ciclo que recorre por filas para convertir datos no numericos a numericos.
            if self.df.loc[self.df.index[i],'Sex']=='F':
                self.df.loc[self.df.index[i],'Sex']=0
            else:
                self.df.loc[self.df.index[i],'Sex']=1
        self.df=self.df[['CDR','Sex','Age','Educ','MMSE','eTIV','nWBV','ASF']]


    def balance(self):
        #Ciclo que recorre todas las filas del dataframe para agrupar aquellos valores distintos a 0
        for i in range(len(self.df)):
            if self.df.loc[self.df.index[i],'CDR']!=0.0:
                self.df.loc[self.df.index[i],'CDR']=1.0
        self.df['CDR'] = self.df['CDR'].apply(np.int64)
        count = self.df["CDR"].value_counts()
        #Funcion encargada de eliminar de forma aleatorea filas que provocan un desbalanceo
        for i, row in count.items():
            if row > 100:
                indices = self.df[self.df["CDR"]== i].sample(n=(row - 100), random_state=1).index
                self.df = self.df.drop(labels=indices, axis=0)

    def normalizado(self):
        for i in self.df.columns:#recorrido por columna que retorna la misma columna balanceada
            if i != "CDR":
                self.df[i] = (self.df[i]-self.df[i].mean())/self.df[i].std()

    def __str__(self):#Funcion principal que retorna el df en un formato string y crea un archivo de tipo excel
        self.detalles()# aplicada todas las funciones para estar normalizado
        self.balance()
        self.normalizado()
        self.df.to_excel('df_parte1_normalizado.xlsx')
        aux = self.df.to_string()
        return aux