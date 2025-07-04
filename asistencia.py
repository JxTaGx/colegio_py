class Asistencia:
    def __init__(self, codigo, fecha, aula_obj, docente_obj, materia_obj, grado_obj, presentes, ausentes):
        self.__codigo = codigo
        self.__fecha = fecha 
        self.__aula = aula_obj
        self.__docente = docente_obj
        self.__materia = materia_obj
        self.__grado = grado_obj
        self.__estudiantes_presentes = presentes 
        self.__estudiantes_ausentes = ausentes

    def get_codigo(self):
        return self.__codigo

    def get_fecha(self):
        return self.__fecha

    def get_aula(self):
        return self.__aula

    def get_docente(self):
        return self.__docente
    
    def get_materia(self):
        return self.__materia
    
    def get_grado(self):
        return self.__grado

    def get_presentes(self):
        return self.__estudiantes_presentes

    def get_ausentes(self):
        return self.__estudiantes_ausentes
    
    def get_listar(self):
        for 

    def mostrar_detalles(self):
        print("\n================ REGISTRO DE ASISTENCIA ================")
        print(f"Código de Asistencia: {self.get_codigo()}")
        print(f"Fecha: {self.get_fecha().strftime('%d/%m/%Y')}")
        print(f"Grado: {self.get_grado().get_nombre()}")
        print(f"Aula: {self.get_aula().get_nombre()}")
        print(f"Docente: {self.get_docente().get_nombre_completo()}")
        print(f"Materia: {self.get_materia().get_nombre()}")
        
        print("\n--- Estudiantes Presentes ---")
        if self.get_presentes():
            for est in self.get_presentes():
                print(f"  - {est.get_nombre_completo()} (Cód: {est.get_codigo()})")
        else:
            print("  No se registraron estudiantes presentes.")
            
        print("\n--- Estudiantes Ausentes ---")
        if self.get_ausentes():
            for est, excusa, justificacion in self.get_ausentes():
                estado_excusa = "CON Excusa" if excusa else "SIN Excusa"
                detalle_justificacion = f" (Justificación: {justificacion})" if excusa and justificacion else ""
                print(f"  - {est.get_nombre_completo()} (Cód: {est.get_codigo()}) - {estado_excusa}{detalle_justificacion}")
        else:
            print("  No se registraron estudiantes ausentes.")
        print("========================================================\n")