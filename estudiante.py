class Estudiante:
    def __init__(self, codigo, nombres, apellidos, grado_obj):
        self.__codigo = codigo
        self.__nombres = nombres
        self.__apellidos = apellidos
        self.__grado = grado_obj
        self.__estado = "Habilitado" 

    def get_codigo(self):
        return self.__codigo

    def get_nombres(self):
        return self.__nombres

    def get_apellidos(self):
        return self.__apellidos
        
    def get_nombre_completo(self):
        return f"{self.__nombres} {self.__apellidos}"

    def get_grado(self):
        return self.__grado

    def get_estado(self):
        return self.__estado

    def set_nombres(self, nombres):
        self.__nombres = nombres

    def set_apellidos(self, apellidos):
        self.__apellidos = apellidos

    def set_grado(self, grado_obj):
        self.__grado = grado_obj

    def set_estado(self, estado):
        self.__estado = estado

    def mostrar_detalles(self):
        print("***************************************")
        print(f"Código: {self.get_codigo()}")
        print(f"Nombres: {self.get_nombres()}")
        print(f"Apellidos: {self.get_apellidos()}")
        grado_nombre = self.get_grado().get_nombre() if self.get_grado() else 'No asignado'
        print(f"Grado: {grado_nombre}")
        print(f"Estado: {self.get_estado()}")
        print("***************************************")