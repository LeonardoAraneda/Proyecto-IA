import pandas as pd
import numpy as np
from normalizado import NORMALIZA
from kfold import KFOLD
from knn import KNN

menu_options = {
    1: 'Mostrar Dataframe normalizado',
    2: 'Mostrar K-Folds',
    3: 'Knn',
    4: 'Exit',
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )


def opcion1(df_norm):
    print('DATAFRAME NORMALIZADO\n')
    print(df_norm)
    print('\n')


def opcion2(folds):
    print('FOLDS DE PRUEBA Y ENTRENAMIENDO\n')
    print(folds)
    print('\n')


def opcion3():
     print('Handle option \'Option 3\'')

if __name__=='__main__':
    new_df = NORMALIZA()
    folds = KFOLD()
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Ingrese su opcion: '))
        except:
            print('Entrada errone, por favor ingrese un numero entero')

        if option == 1:
           opcion1(new_df)
        elif option == 2:
            opcion2(folds)
        elif option == 3:
            k = int(input("Ingrese el valor de k vecinos: "))
            if k == 3 or k == 5 or k == 7:
                opcion3(k)
            else: 
                print("Valor no aceptado")
        elif option == 4:
            print('Gracias, hasta luego.')
            exit()
        else:
            print('Opcion invalida, por favor elija un número entero entre el 1 al 4.')



"""if __name__ == "__main__":
    seguir = True
    new_df = NORMALIZA()
    while seguir:
        #k = int(input("Ingrese el valor de k: "))

        seguir = input("¿Desea seguir? (s/n): ") == "s"""