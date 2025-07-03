from datetime import date
from estudiante import Estudiante
from docente import Docente
from materia import Materia
from grado import Grado
from aula import Aula
from asistencia import Asistencia

class Colegio:
    def __init__(self):
        self.estudiantes = []
        self.docentes = []
        self.materias = []
        self.grados = []
        self.aulas = []
        self.asistencias = []
        self.max_aulas = 20

    def buscar_por_codigo(self, lista, codigo):
        for item in lista:
            if item.get_codigo() == codigo:
                return item
        return None

    def adicionar_entidad(self, tipo, **kwargs):
        codigo = kwargs['codigo']
        lista = getattr(self, f"{tipo.lower()}s")

        if self.buscar_por_codigo(lista, codigo):
            return f"Error - Ya existe un(a) {tipo} con el código {codigo}."

        if tipo == "Estudiante":
            grado_obj = kwargs['grado']
            est_en_grado = len([e for e in self.estudiantes if e.get_grado() == grado_obj and e.get_estado() == 'Habilitado' and e.get_grado().get_estado() == 'Habilitado'])

            if est_en_grado >= grado_obj.get_capacidad_maxima():
                return f"Error - El grado '{grado_obj.get_nombre()}' ha alcanzado su capacidad máxima."
            entidad = Estudiante(kwargs['codigo'], kwargs['nombres'], kwargs['apellidos'], grado_obj)

        elif tipo == "Docente":
            for d in self.docentes:
                if d.get_estado() == "Habilitado":
                    if d.get_materia() == kwargs['materia']:
                        return f"Error - La materia '{kwargs['materia'].get_nombre()}' ya está asignada a otro docente."
                    if d.get_aula() == kwargs['aula']:
                        return f"Error - El aula '{kwargs['aula'].get_nombre()}' ya está asignada a otro docente."

            entidad = Docente(kwargs['codigo'], kwargs['nombres'], kwargs['apellidos'], kwargs['materia'], kwargs['aula'])

        elif tipo == "Materia":
            entidad = Materia(kwargs['codigo'], kwargs['nombre'])

        elif tipo == "Grado":
            entidad = Grado(kwargs['codigo'], kwargs['nombre'])

        elif tipo == "Aula":
            if len([a for a in self.aulas if a.get_estado() == "Habilitado"]) >= self.max_aulas:
                return f"Error - Se ha alcanzado el número máximo de {self.max_aulas} aulas habilitadas."
            entidad = Aula(kwargs['codigo'], kwargs['nombre'])

        else:
            return "Error - Tipo de entidad no reconocido."

        lista.append(entidad)
        return True

    def modificar_entidad(self, tipo, codigo, campo, nuevo_valor):
        lista = getattr(self, f"{tipo.lower()}s")
        entidad = self.buscar_por_codigo(lista, codigo)
        if not entidad: return f"Error - {tipo} con código {codigo} no encontrado."

        if campo == "codigo": return "Error - El código no se puede modificar."

        setter_name = f"set_{campo}"
        if hasattr(entidad, setter_name):
            if tipo == "Estudiante" and campo == "grado":
                est_en_grado = len([e for e in self.estudiantes if e.get_grado() == nuevo_valor and e.get_estado() == 'Habilitado' and e.get_grado().get_estado() == 'Habilitado'])
                if est_en_grado >= nuevo_valor.get_capacidad_maxima():
                    return f"Error - El grado '{nuevo_valor.get_nombre()}' ya ha alcanzado su capacidad máxima."

            if tipo == "Docente" and campo in ["materia", "aula"]:
                for d in self.docentes:
                    if d.get_estado() == "Habilitado" and d != entidad:
                        if campo == "materia" and d.get_materia() == nuevo_valor:
                            return f"Error - La materia '{nuevo_valor.get_nombre()}' ya está asignada a otro docente."
                        if campo == "aula" and d.get_aula() == nuevo_valor:
                            return f"Error - El aula '{nuevo_valor.get_nombre()}' ya está asignada a otro docente."
            setter = getattr(entidad, setter_name)
            setter(nuevo_valor)
            return True
        else:
            return f"Error - Campo a modificar '{campo}' no es válido."

    def cambiar_estado_entidad(self, tipo, codigo, nuevo_estado):
        lista = getattr(self, f"{tipo.lower()}s")
        entidad = self.buscar_por_codigo(lista, codigo)
        if not entidad: return False
        
        if tipo == "Grado" and nuevo_estado == "Deshabilitado":
            estudiantes_afectados = len([e for e in self.estudiantes if e.get_grado() == entidad and e.get_estado() == 'Habilitado'])
            if estudiantes_afectados > 0:
                print(f"Advertencia: Al deshabilitar el grado '{entidad.get_nombre()}', {estudiantes_afectados} estudiantes ya no contarán en los reportes de estudiantes activos por grado.")

        entidad.set_estado(nuevo_estado)
        return True

    def validar_fecha_asistencia(self, fecha_obj):
        fecha_inicio_escolar = date(2025, 1, 20)
        if fecha_obj < fecha_inicio_escolar or fecha_obj > date.today():
            return f"La fecha debe estar dentro del año escolar (desde {fecha_inicio_escolar.strftime('%d/%m/%Y')} hasta hoy)."

        if fecha_obj.weekday() >= 5:
            return "No se puede registrar asistencia en fines de semana (días no hábiles)."
        return True

    def registrar_asistencia(self, codigo, fecha_obj, aula_obj, docente_obj, grado_obj, presentes, ausentes):
        if self.buscar_por_codigo(self.asistencias, codigo): return "Error - Ya existe un registro de asistencia con ese código."

        for est in presentes:
            asistencias_hoy = self.get_asistencias_filtradas('fecha', fecha_obj)
            for asistencia_existente in asistencias_hoy:
                if est in asistencia_existente.get_presentes():
                    return f"Error - El estudiante {est.get_nombre_completo()} ya tiene asistencia registrada hoy."

        materia_obj = docente_obj.get_materia()
        nueva_asistencia = Asistencia(codigo, fecha_obj, aula_obj, docente_obj, materia_obj, grado_obj, presentes, ausentes)
        self.asistencias.append(nueva_asistencia)

        aula_obj.set_estado_ocupacion("Ocupada")
        return True

    # --- MÉTODOS PARA REPORTES ---

    def calcular_total_estudiantes(self):
        return len([e for e in self.estudiantes if e.get_estado() == 'Habilitado' and e.get_grado() and e.get_grado().get_estado() == 'Habilitado'])

    def calcular_estudiantes_por_grado(self):
        est_por_grado = {g.get_nombre(): 0 for g in self.grados if g.get_estado() == 'Habilitado'}
        for est in self.estudiantes:
            if est.get_estado() == 'Habilitado' and est.get_grado() and est.get_grado().get_estado() == 'Habilitado':
                grado_nombre = est.get_grado().get_nombre()
                if grado_nombre in est_por_grado:
                    est_por_grado[grado_nombre] += 1
        return est_por_grado

    def get_asistencias_filtradas(self, filtro, valor):
        if filtro == "fecha":
            return [a for a in self.asistencias if a.get_fecha() == valor]
        elif filtro == "estudiante":
            return [a for a in self.asistencias if valor in a.get_presentes() or any(valor == aus[0] for aus in a.get_ausentes())]
        elif filtro == "grado":
            return [a for a in self.asistencias if a.get_grado() == valor]
        elif filtro == "aula":
            return [a for a in self.asistencias if a.get_aula() == valor]
        return []

    def get_calculos_asistencia_por_fecha(self, fecha_obj):
        reporte = {'presentes': set(), 'inasistentes_justificados': set(), 'inasistentes_injustificados': set()}
        asistencias_del_dia = self.get_asistencias_filtradas('fecha', fecha_obj)

        for asistencia in asistencias_del_dia:
            for est in asistencia.get_presentes():
                reporte['presentes'].add(est.get_codigo())
            for est, excusa, _ in asistencia.get_ausentes():
                if est.get_codigo() not in reporte['presentes']:
                    if excusa:
                        reporte['inasistentes_justificados'].add(est.get_codigo())
                    else:
                        reporte['inasistentes_injustificados'].add(est.get_codigo())
        
        codigos_presentes = reporte['presentes']
        reporte['inasistentes_justificados'] -= codigos_presentes
        reporte['inasistentes_injustificados'] -= codigos_presentes


        return {
            'asistencia': len(reporte['presentes']),
            'inasistencia_justificada': len(reporte['inasistentes_justificados']),
            'inasistencia_injustificada': len(reporte['inasistentes_injustificados']),
            'inasistencia_total': len(reporte['inasistentes_justificados']) + len(reporte['inasistentes_injustificados'])
        }