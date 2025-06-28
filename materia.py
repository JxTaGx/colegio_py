class Materia:
    def __init__(self, codigo, nombre):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__estado = "Habilitado"

    def get_codigo(self):
        return self.__codigo

    def get_nombre(self):
        return self.__nombre

    def get_estado(self):
        return self.__estado

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_estado(self, estado):
        self.__estado = estado

    def mostrar_detalles(self):
        print("***************************************")
        print(f"Código: {self.get_codigo()}")
        print(f"Nombre: {self.get_nombre()}")
        print(f"Estado: {self.get_estado()}")
        print("***************************************")