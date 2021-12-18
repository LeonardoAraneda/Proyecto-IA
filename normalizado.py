import numpy as np
import pandas as pd


class NORMALIZA:
    
    df = pd.read_csv("oasis_cross-sectional.csv") #variables de clases
    def __init__(self):
        """self.df = pd.read_csv("oasis_cross-sectional.csv")"""  """Instancia de los objetos """

    def arreglos(self):
        self.df = self.df.rename(columns={'M/F':'Sex'})
        self.df.dropna(subset=['Educ'],inplace=True)
        self.df.drop(columns=['ID','Hand','SES'], axis = 1, inplace=True)
        self.df.dropna(axis=1,inplace=True)
        self.df = self.df.fillna("", inplace=False)
        for i in range(len(self.df)):
            if self.df.loc[self.df.index[i],'Sex']=='F':
                self.df.loc[self.df.index[i],'Sex']=0
            else:
                self.df.loc[self.df.index[i],'Sex']=1
        self.df=self.df[['CDR','Sex','Age','Educ','MMSE','eTIV','nWBV','ASF']]


    def balance(self):
        for i in range(len(self.df)):
            if self.df.loc[self.df.index[i],'CDR']!=0.0:
                self.df.loc[self.df.index[i],'CDR']=1.0
        self.df['CDR'] = self.df['CDR'].apply(np.int64)
        count = self.df["CDR"].value_counts()
        for i, row in count.items():
            if row > 100:
                indices = self.df[self.df["CDR"]== i].sample(n=(row - 100), random_state=1).index
                self.df = self.df.drop(labels=indices, axis=0)

    def normalizado(self):
        for i in self.df.columns:
            if i != "CDR":
                self.df[i] = (self.df[i]-self.df[i].mean())/self.df[i].std()

    def __str__(self):
        self.arreglos()
        self.balance()
        self.normalizado()
        self.df.to_excel('df_parte1_normalizado.xlsx')
        aux = self.df.to_string()
        return aux

        