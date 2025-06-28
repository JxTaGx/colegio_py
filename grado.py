class Grado:
    def __init__(self, codigo, nombre):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__capacidad_maxima = 10
        self.__estado = "Habilitado"

    def get_codigo(self):
        return self.__codigo

    def get_nombre(self):
        return self.__nombre

    def get_capacidad_maxima(self):
        return self.__capacidad_maxima

    def get_estado(self):
        return self.__estado

    def set_nombre(self, nombre):
        self.__nombre = nombre
        
    def set_estado(self, estado):
        self.__estado = estado
        
    def set_capacidad_maxima(self, codigo):
        self.__capacidad_maxima = 0

    def mostrar_detalles(self, cantidad_actual=0):
        print("***************************************")
        print(f"Código: {self.get_codigo()}")
        print(f"Grado: {self.get_nombre()}")
        print(f"Capacidad Máxima: {self.get_capacidad_maxima()} estudiantes")
        print(f"Estudiantes Inscritos: {cantidad_actual}")
        print(f"Estado: {self.get_estado()}")
        print("***************************************")