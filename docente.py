class Docente:
    def __init__(self, codigo, nombres, apellidos, materia_obj, aula_obj):
        self.__codigo = codigo
        self.__nombres = nombres
        self.__apellidos = apellidos
        self.__materia = materia_obj
        self.__aula = aula_obj
        self.__estado = "Habilitado"

    def get_codigo(self):
        return self.__codigo

    def get_nombres(self):
        return self.__nombres

    def get_apellidos(self):
        return self.__apellidos
        
    def get_nombre_completo(self):
        return f"{self.__nombres} {self.__apellidos}"

    def get_materia(self):
        return self.__materia

    def get_aula(self):
        return self.__aula

    def get_estado(self):
        return self.__estado

    def set_nombres(self, nombres):
        self.__nombres = nombres

    def set_apellidos(self, apellidos):
        self.__apellidos = apellidos

    def set_materia(self, materia_obj):
        self.__materia = materia_obj

    def set_aula(self, aula_obj):
        self.__aula = aula_obj

    def set_estado(self, estado):
        self.__estado = estado

    def mostrar_detalles(self):
        print("***************************************")
        print(f"Código: {self.get_codigo()}")
        print(f"Nombres: {self.get_nombres()}")
        print(f"Apellidos: {self.get_apellidos()}")
        materia_nombre = self.get_materia().get_nombre() if self.get_materia() else 'No asignada'
        aula_nombre = self.get_aula().get_nombre() if self.get_aula() else 'No asignada'
        print(f"Materia que imparte: {materia_nombre}")
        print(f"Aula asignada: {aula_nombre}")
        print(f"Estado: {self.get_estado()}")
        print("***************************************")