import csv
import os

ARCHIVO_PATH = "./Data.csv"

class Persona:
    listado = []

    def __init__(self, cedula = 0, nombre = "", apellido = "", edad = 0, ahorros = 0.0, genero = False, estado_legal = False, grado = 0):
        
        self.__cedula = cedula
        self.__nombre = nombre
        self.__apellido = apellido
        self.__edad = edad
        self.__ahorros = ahorros
        self.__genero = genero
        self.__estado_legal = estado_legal
        self.__grado = grado

    def imprimir(self):
        print("Cedula: {}".format(self.__cedula))
        print("Nombre: {}".format(self.__nombre))
        print("Apellido: {}".format(self.__apellido))
        print("Edad: {}".format(self.__edad))
        print("Ahorros: {}".format(self.__ahorros))
        print("Genero: {}".format(self.__leerGenero()))
        print("Estado Legal: {}".format(self.__leerEstadoLegal()))
        print("Grado: {}".format(self.__grado + 1))

    def obtenerLineaCsv(self):
        return "{},{},{},{},{},{},{},{}".format(
            self.__cedula,
            self.__nombre,
            self.__apellido,
            self.__edad,
            self.__ahorros,
            int(self.__genero),
            int(self.__estado_legal),
            self.__grado
        )

    def __leerGenero(self):
        return "Mujer" if self.__genero else "Hombre"
    def __leerEstadoLegal(self):
        return "Casado" if self.__estado_legal else "Soltero"

    def leerCedula(self):
        return self.__cedula
    def leerNombre(self):
        return self.__nombre
    def leerApellido(self):
        return self.__apellido
    def leerEdad(self):
        return self.__edad
    def leerAhorros(self):
        return self.__ahorros
    def leerGenero(self):
        return self.__genero
    def leerEstadoLegal(self):
        return self.__estado_legal
    def leerGrado(self):
        return self.__grado
    
    def definirCedula(self, Cedula):
        self.__cedula = Cedula
    def definirNombre(self, Nombre):
        self.__nombre = Nombre
    def definirApellido(self, Apellido):
        self.__apellido = Apellido
    def definirEdad(self, Edad):
        self.__edad = Edad
    def definirAhorros(self, Ahorros):
        self.__ahorros = Ahorros
    def definirGenero(self, Genero):
        self.__genero = Genero
    def definirEstadoLegal(self, EstadoLegal):
        self.__estado_legal = EstadoLegal
    def definirGrado(self, Grado):
        self.__grado = Grado

    def obtenerBitPack(self):
        bp = 0
        bp |= (int(self.__edad) & 0xff) << 12
        bp |= (int(self.__genero) & 0xf) << 2*4
        bp |= (int(self.__estado_legal) & 0xf) << 1*4
        bp |= (int(self.__grado) & 0xf)

        return bp

class Registro:
    def __init__(self, locacion_de_registro):
        self.__listado = []
        self.__locacion_de_registro = locacion_de_registro
        try:
            if not os.path.exists(locacion_de_registro):
                return
            excepcion = "Formato de archivo es invalido: "
            with open(locacion_de_registro, "r") as fp:
                c_obj = csv.reader(fp)
                for fila in c_obj:
                    if(len(fila) < 8):
                        raise IOError(excepcion + "Tamaño de linea invalido")
                    try:
                        self.__listado.append(Persona(
                            cedula =        fila[0],
                            nombre =        fila[1],
                            apellido =      fila[2],
                            edad =          int(fila[3]),
                            ahorros =       float(fila[4]),
                            genero =        bool(int(fila[5])),
                            estado_legal =  bool(int(fila[6])),
                            grado =         int(fila[7])
                        ))
                    except Exception as e:
                        raise IOError(excepcion + str(e))

        except Exception as e:
            print("No se puede abrir \"" + locacion_de_registro + "\": " + str(e))
            pass

    def escribirRegistro(self):
        try:
            with open(self.__locacion_de_registro, "w") as fp:
                for persona in self.__listado:
                    fp.write(persona.obtenerLineaCsv() + ",{0:05x}".format(persona.obtenerBitPack()) + "\n")
        except Exception as e:
            print("No se puede escribir en el archivo \"" + self.__locacion_de_registro + "\": " + str(e))
            pass

    def obtenerListado(self):
        return self.__listado

    def obtenerNumeroDeEntradas(self):
        return len(self.__listado)

    def agregarAListado(self, persona):
        self.__listado.append(persona)

    def buscarEnListado(self, cedula):
        numero = 0
        for persona in self.__listado:
            if persona.leerCedula() == cedula:
                return persona, numero
            else:
                numero += 1
        return Persona(), -1
    
    def modificarListado(self, persona, numero):
        try:
            self.__listado[numero] = persona
            return True
        except:
            return False
    
    def borrarDelListado(self, cedula):
        persona, numero = self.buscarEnListado(cedula)

        if numero > -1:
            self.__listado.remove(persona)
            return True
        else:
            return False

def crearPersona():
    print("Cedula: ", end="")
    cedula = input()
    print("Nombre: ", end="")
    nombre = input()
    print("Apellido: ", end="")
    apellido = input()
    print("Edad: ", end="")
    edad = int(input())
    print("Ahorros: ", end="")
    ahorros = float(input())
    print("Genero: ", end="")
    genero = False if input().lower() == "hombre" else True
    print("Estado Legal: ", end="")
    estado_legal = True if input().lower() == "casado" else False
    print("Grado: ", end="")
    grado = int(input())

    print("\n")

    return Persona(
        cedula = cedula,
        nombre = nombre,
        apellido = apellido,
        edad = edad,
        ahorros = ahorros,
        genero = genero,
        estado_legal = estado_legal,
        grado = grado
    )

def main():
    print("Inicializando con archivo \"" + ARCHIVO_PATH + "\"...")
    try:
        registro = Registro(ARCHIVO_PATH)
        print(str(registro.obtenerNumeroDeEntradas()) + " entradas encontradas!")
    except Exception as e:
        print("Error leyendo \"" + ARCHIVO_PATH + "\": " + str(e))

    command = ""
    while(command != "salir"):
        print()

        print("==========================MENU=========================")
        print("salir: Salir")
        print("buscar: Buscar un registro")
        print("mostrar: Mostrar registros")
        print("borrar: Borrar un registro")
        print("agregar: Agregar un registro")
        print("modificar: Modificar un registro")
        print("confirmar: Escribe los registros en memoria al archivo")
        print("=======================================================")

        print()
        
        print("$ ", end="")
        command = input()

        if command == "agregar":
            try:
                registro.agregarAListado(crearPersona())
            except Exception as e:
                print("No se puede crear registro: " + str(e))
            
        elif command == "buscar":
            print("Cedula a buscar: ", end="")
            cedula = input()
            persona, numero = registro.buscarEnListado(cedula)
            if numero > -1:
                print("Entrada encontrada: ", end="")
                persona.imprimir()
                print()
            else:
                print("Cedula \"{}\", no encontrada".format(cedula))
        
        elif command == "modificar":
            print("Cedula del registro a modificar: ", end="")
            cedula = input()

            x, numero = registro.buscarEnListado(cedula)
            if numero > -1:
                try:
                    registro.modificarListado(crearPersona(), numero)
                    print("Registro modificado correctamente!")
                except Exception as e:
                    print("Error modificando registro: " + str(e))
        
        elif command == "borrar":
            print("Cedula del registro a borrar: ", end="")
            cedula = input()
            
            if registro.borrarDelListado(cedula):
                print("Registro borrado correctamente")
            else:
                print("Registro no encontrado")
            
        elif command == "mostrar":
            print("Entradas en la base de datos: ")
            numero = 1
            for persona in registro.obtenerListado():
                print("{}.-".format(numero))
                persona.imprimir()
                numero += 1
                print()

        elif command == "confirmar":
            print("Escribiendo " + str(registro.obtenerNumeroDeEntradas()) + " entradas...")
            registro.escribirRegistro()
            print("Completado!")

                
if __name__ == "__main__":
    main()