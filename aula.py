class Aula:
    def __init__(self, codigo, nombre):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__capacidad = 10
        self.__estado = "Habilitado"
        self.__estado_ocupacion = "Disponible"

    def get_codigo(self):
        return self.__codigo

    def get_nombre(self):
        return self.__nombre

    def get_capacidad(self):
        return self.__capacidad
    
    def get_estado(self):
        return self.__estado
    
    def get_estado_ocupacion(self):
        return self.__estado_ocupacion

    def set_nombre(self, nombre):
        self.__nombre = nombre
    
    def set_estado(self, estado):
        self.__estado = estado

    def set_estado_ocupacion(self, estado_ocupacion):
        self.__estado_ocupacion = estado_ocupacion

    def mostrar_detalles(self):
        print("***************************************")
        print(f"Código: {self.get_codigo()}")
        print(f"Nombre/Ubicación: {self.get_nombre()}")
        print(f"Capacidad: {self.get_capacidad()} estudiantes")
        print(f"Estado: {self.get_estado()}")
        print(f"Ocupación Actual: {self.get_estado_ocupacion()}")
        print("***************************************")