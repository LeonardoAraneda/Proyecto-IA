from normalizado import NORMALIZA
from kfold import KFOLD
from knn import KNN
from kmeans import KMEANS
from rna import RNA
menu_options = {
    1: 'Mostrar Dataframe normalizado',
    2: 'Mostrar K-Folds',
    3: 'Knn',
    4: 'RNA',
    5: 'k-Means',
    6: 'Exit',
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )


def opcion1(df_norm):
    print('\nDATAFRAME NORMALIZADO\n')
    print(df_norm)
    print('\n')


def opcion2(folds):
    print('\nFOLDS DE PRUEBA Y ENTRENAMIENDO\n')
    print(folds)
    print('\n')


def opcion3(k):
    print('\nESTADISTICAS DE RENDIMIENTO KNN\n')
    a = KNN(k)
    print(a)
    print('\n')


def opcion4(k):
    print('\nCREANDO ARCHIVO DE TIPO EXCEL CON SALIDAS Y ERROR DE RNA PASO HACIA ADELANTE\n')
    a = RNA(k)
    print(a)

def opcion5():
    print('\nPORCENTAJE DE PATRONES QUE QUEDARON AGRUPADOS CORRECTAMENTE\n')
    print("Cluster0[1,0]  Cluster1[1,0]")
    a = KMEANS()
    print(a)


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
            k = int(input("1 -- Sigmoide\n2 -- Rampa\nEliga la funcion de activacion: "))
            if k == 1 or k == 2:
                opcion4(k)
            else: 
                print("Valor no aceptado")
        elif option == 5:
            opcion5()
        elif option ==6:  
            print('Gracias, hasta luego.')
            exit()             
        else:
            print('Opcion invalida, por favor elija un número entero entre el 1 al 4.')