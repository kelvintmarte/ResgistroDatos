import csv

ARCHIVO_PATH = "./Data.csv"

def escribeEnCsv(archivo, data):
    for item in data:
        archivo.write("{},".format(item))
    archivo.write("\n")

def leerCsv(archivo):
    listado = []
    c = csv.reader(archivo)
    for row in c:
        listado.append(row)
    return listado

def imprimeEntrada(entrada):
    for cell in entrada:
        print(cell + " ", end="")
    print("")

def main():
    command = ""
    while(command != "salir"):
        print("agregar: Agregar un registro")
        print("buscar: Buscar un registro")
        print("mostrar: Mostrar registros")
        print("salir: Salir")
        
        print("\n")
        
        print("Que desea hacer: ", end="")
        command = input()

        if command == "agregar":
            with open(ARCHIVO_PATH, "a") as archivo:
                print("Nombre: ", end="")
                nombre = input()
                
                print("Cedula: ", end="")
                cedula = input()
                
                print("Edad: ", end="")
                edad = input()

                print("\n")

                escribeEnCsv(archivo, {edad, cedula, nombre})
            
        elif command == "buscar":
            print("Cedula a buscar: ", end="")
            cedula = input()
            with open(ARCHIVO_PATH, "r") as archivo:
                listado = leerCsv(archivo)
                encontrado = False
                for row in listado:
                    if row[1] == cedula:
                        print("Entrada encontrada: ", end="")
                        imprimeEntrada(row)
                        encontrado = True
                        break
                if not encontrado:
                    print("Cedula \"{}\", no encontrada".format(cedula))
            
        elif command == "mostrar":
            with open(ARCHIVO_PATH, "r") as archivo:
                listado = leerCsv(archivo)
                for row in listado:
                    imprimeEntrada(row)

if __name__ == "__main__":
    main()