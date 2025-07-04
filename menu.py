from os import system
from datetime import datetime
from colegio import Colegio

class Menu:
    def __init__(self):
        self.colegio = Colegio()

    def solicitar_entero(self, mensaje, minimo=None):
        while True:
            try:
                valor = int(input(mensaje))
                if minimo is not None and valor < minimo:
                    print(f"Error: El número no puede ser menor que {minimo}.")
                    continue
                return valor
            except ValueError:
                print("Error: Debe ingresar un número entero válido.")

    def solicitar_cadena(self, mensaje, permitir_numeros=True, no_vacio=True):
        while True:
            valor = input(mensaje).strip()
            if no_vacio and not valor:
                print("Error: Este campo no puede estar vacío.")
                continue
            if not permitir_numeros and any(char.isdigit() for char in valor):
                print("Error: Este campo no debe contener números.")
                continue
            return valor

    def solicitar_fecha(self, mensaje):
        while True:
            fecha_str = self.solicitar_cadena(mensaje)
            try:
                return datetime.strptime(fecha_str, "%d/%m/%Y").date()
            except ValueError:
                print("Error: Formato de fecha inválido. Use dd/mm/yyyy.")

    def pausa_y_limpiar(self):
        input("\nPresione Enter para continuar...")
        system("cls")

    def seleccionar_entidad(self, tipo_entidad, estado_requerido=None, mensaje_extra=""):
        lista = getattr(self.colegio, f"{tipo_entidad.lower()}s")
        
        items_mostrables = [item for item in lista if estado_requerido is None or item.get_estado() == estado_requerido]

        if not items_mostrables:
            criterio_str = f" con estado '{estado_requerido}'" if estado_requerido else ""
            print(f"Info - No hay {tipo_entidad}s registrados{criterio_str}.")
            return None

        print(f"--- Seleccionar {tipo_entidad.capitalize()} {mensaje_extra}---")
        for i, item in enumerate(items_mostrables, 1):
            nombre = item.get_nombre() if hasattr(item, 'get_nombre') else item.get_nombre_completo()
            print(f"{i}. Código: {item.get_codigo()}, Nombre: {nombre}")

        while True:
            try:
                opcion = int(input(f"Seleccione el número del {tipo_entidad}: "))
                if 1 <= opcion <= len(items_mostrables):
                    return items_mostrables[opcion - 1]
                else:
                    print("Error - Selección fuera de rango.")
            except ValueError:
                print("Error - Ingrese un número válido.")

    def menu_gestion_entidad(self, tipo_entidad):
        while True:
            system("cls")
            print(f"==== Gestión de {tipo_entidad}s ====")
            print(f"1. Registrar Nuevo {tipo_entidad}")
            print(f"2. Listar todos los {tipo_entidad}s")
            print(f"3. Visualizar detalles de un {tipo_entidad}")
            print(f"4. Modificar {tipo_entidad}")
            print(f"5. Habilitar/Deshabilitar {tipo_entidad}")
            print("0. Volver al Menú Principal")

            opcion = self.solicitar_cadena("\nSeleccione una opción: ")

            if opcion == '1': self.registrar_entidad(tipo_entidad)
            elif opcion == '2': self.listar_entidades(tipo_entidad, f"** Listado de {tipo_entidad}s **")
            elif opcion == '3': self.visualizar_entidad(tipo_entidad)
            elif opcion == '4': self.modificar_entidad(tipo_entidad)
            elif opcion == '5': self.cambiar_estado_entidad(tipo_entidad)
            elif opcion == '0': break
            else: print("Opción no válida.")
            self.pausa_y_limpiar()

    def registrar_entidad(self, tipo):
        system("cls")
        print(f"** Registrar Nuevo {tipo} **")
        codigo = self.solicitar_entero(f"Digite el código del {tipo} (único): ", minimo=1)
        params = {'tipo': tipo, 'codigo': codigo}

        try:
            if tipo == "Estudiante":
                params['nombres'] = self.solicitar_cadena("Digite los nombres: ", permitir_numeros=False)
                params['apellidos'] = self.solicitar_cadena("Digite los apellidos: ", permitir_numeros=False)
                grado_obj = self.seleccionar_entidad("Grado", "Habilitado")
                if not grado_obj: print("Operación cancelada."); return
                params['grado'] = grado_obj

            elif tipo == "Docente":
                params['nombres'] = self.solicitar_cadena("Digite los nombres: ", permitir_numeros=False)
                params['apellidos'] = self.solicitar_cadena("Digite los apellidos: ", permitir_numeros=False)
                
                materia_obj = self.seleccionar_entidad("Materia", "Habilitado", "(debe estar habilitada)")
                if not materia_obj: print("Operación cancelada."); return
                
                aula_obj = self.seleccionar_entidad("Aula", "Habilitado", "(debe estar habilitada)")
                if not aula_obj: print("Operación cancelada."); return
                
                params['materia'] = materia_obj
                params['aula'] = aula_obj

            elif tipo in ["Materia", "Grado", "Aula"]:
                nombre = self.solicitar_cadena(f"Digite el nombre del {tipo}: ")
                params['nombre'] = nombre

        except Exception as e:
            print(f"Se canceló la operación. {e}")
            return

        resultado = self.colegio.adicionar_entidad(**params)
        if resultado is True:
            print(f"Info - El {tipo} fue creado de forma satisfactoria.")
        else:
            print(f"{resultado}")

    def listar_entidades(self, tipo, titulo):
        system("cls")
        print(titulo)
        lista = getattr(self.colegio, f"{tipo.lower()}s")
        if not lista:
            print(f"Info - No hay {tipo}s registrados.")
            return

        for item in lista:
            if tipo == "Grado":
                est_en_grado = len([e for e in self.colegio.estudiantes if e.get_grado() == item and e.get_estado() == 'Habilitado' and e.get_grado().get_estado() == 'Habilitado'])
                item.mostrar_detalles(est_en_grado)
            else:
                item.mostrar_detalles()

    def visualizar_entidad(self, tipo):
        system("cls")
        print(f"** Visualizar Detalles de {tipo} **")
        entidad = self.seleccionar_entidad(tipo)
        if entidad:
            if tipo == "Grado":
                est_en_grado = len([e for e in self.colegio.estudiantes if e.get_grado() == entidad and e.get_estado() == 'Habilitado' and e.get_grado().get_estado() == 'Habilitado'])
                entidad.mostrar_detalles(est_en_grado)
            else:
                entidad.mostrar_detalles()

    def modificar_entidad(self, tipo):
        system("cls")
        print(f"** Modificar {tipo} **")
        entidad = self.seleccionar_entidad(tipo)
        if not entidad: return

        print("Seleccione el campo a modificar:")
        campos_modificables = {
            "Estudiante": ["nombres", "apellidos", "grado"],
            "Docente": ["nombres", "apellidos", "materia", "aula"],
            "Materia": ["nombre"], "Grado": ["nombre"], "Aula": ["nombre"]
        }

        for i, campo in enumerate(campos_modificables[tipo], 1):
            print(f"{i}. {campo.capitalize()}")

        try:
            opcion = int(input("Opción: "))
            campo_a_modificar = campos_modificables[tipo][opcion - 1]
        except (ValueError, IndexError):
            print("Error - Selección no válida.")
            return

        nuevo_valor = None
        if campo_a_modificar in ["nombres", "apellidos"]:
            nuevo_valor = self.solicitar_cadena(f"Digite el nuevo valor para {campo_a_modificar}: ", permitir_numeros=False)
        elif campo_a_modificar == "nombre":
            nuevo_valor = self.solicitar_cadena(f"Digite el nuevo nombre del {tipo}: ")
        elif campo_a_modificar in ["grado", "materia", "aula"]:
            nuevo_valor = self.seleccionar_entidad(campo_a_modificar.capitalize(), "Habilitado")
            if not nuevo_valor: print("Operación cancelada."); return

        resultado = self.colegio.modificar_entidad(tipo, entidad.get_codigo(), campo_a_modificar, nuevo_valor)

        if resultado is True:
            print(f"Info - {tipo} modificado exitosamente.")
        else:
            print(f"{resultado}")

    def cambiar_estado_entidad(self, tipo):
        system("cls")
        print(f"** Habilitar/Deshabilitar {tipo} **")
        entidad = self.seleccionar_entidad(tipo)
        if not entidad: return

        estado_actual = entidad.get_estado()
        print(f"El estado actual del {tipo} es: {estado_actual}")
        nuevo_estado = "Deshabilitado" if estado_actual == "Habilitado" else "Habilitado"

        confirmacion = self.solicitar_cadena(f"¿Desea cambiar el estado a '{nuevo_estado}'? (s/n): ").lower()
        if confirmacion == 's':
            if self.colegio.cambiar_estado_entidad(tipo, entidad.get_codigo(), nuevo_estado):
                print(f"Info - El estado del {tipo} ha sido cambiado a {nuevo_estado}.")
            else:
                print(f"Error - No se pudo cambiar el estado.")
        else:
            print("Operación cancelada.")

    def menu_asistencia(self):
        while True:
            system("cls")
            print("==== Gestión de Asistencia ====")
            print("1. Registrar Asistencia de una Clase")
            print("2. Listar Registros de Asistencia")
            print("0. Volver al Menú Principal")

            opcion = self.solicitar_cadena("\nSeleccione una opción: ")
            if opcion == '1': self.registrar_asistencia()
            elif opcion == '2': self.menu_listar_asistencia()
            elif opcion == '0': break
            else: print("Opción no válida.")
            self.pausa_y_limpiar()

    def registrar_asistencia(self):
        system("cls")
        print("** Registrar Asistencia de Clase **")
        codigo = self.solicitar_entero("Digite el código para este registro (único): ", minimo=1)

        while True:
            fecha_obj = self.solicitar_fecha("Digite la fecha de la clase (dd/mm/yyyy): ")
            val_fecha = self.colegio.validar_fecha_asistencia(fecha_obj)
            if val_fecha is True: break
            print(f"Error - {val_fecha}")

        grado_obj = self.seleccionar_entidad("Grado", "Habilitado")
        if not grado_obj: self.pausa_y_limpiar(); return

        docente_obj = self.seleccionar_entidad("Docente", "Habilitado")
        if not docente_obj: self.pausa_y_limpiar(); return
        
        aula_obj = docente_obj.get_aula()

        if not aula_obj or aula_obj.get_estado() != 'Habilitado':
            print("Error - El docente no tiene un aula válida asignada o el aula está deshabilitada.")
            return

        if aula_obj.get_estado_ocupacion() == 'Ocupada':
            print(f"Error - El aula '{aula_obj.get_nombre()}' se encuentra ocupada.")
            return

        estudiantes_del_grado = [e for e in self.colegio.estudiantes if e.get_grado() == grado_obj and e.get_estado() == 'Habilitado']
        if not estudiantes_del_grado:
            print("Error - No hay estudiantes habilitados en el grado seleccionado.")
            return

        if len(estudiantes_del_grado) > aula_obj.get_capacidad():
            print(f"Advertencia: El número de estudiantes ({len(estudiantes_del_grado)}) en el grado supera la capacidad del aula ({aula_obj.get_capacidad()}).")

        presentes = []
        ausentes = []

        print(f"\n--- Registrando Asistencia para el Grado: {grado_obj.get_nombre()} ---")
        for est in estudiantes_del_grado:
            while True:
                asistio = self.solicitar_cadena(f"¿El estudiante {est.get_nombre_completo()} asistió? (s/n): ").lower()
                if asistio in ['s', 'n']: break

            if asistio == 's':
                presentes.append(est)
            else:
                tiene_excusa = self.solicitar_cadena("¿Tiene excusa? (s/n): ").lower() == 's'
                justificacion = ""
                if tiene_excusa:
                    justificacion = self.solicitar_cadena("Digite la justificación: ", no_vacio=False)
                ausentes.append((est, tiene_excusa, justificacion))

        resultado = self.colegio.registrar_asistencia(codigo, fecha_obj, aula_obj, docente_obj, grado_obj, presentes, ausentes)

        if resultado is True:
            print("Info - Asistencia registrada exitosamente.")
        else:
            print(f"{resultado}")

    def menu_listar_asistencia(self):
        system("cls")
        print("==== Listar Registros de Asistencia ====")
        print("1. Listar por Fecha")
        print("2. Listar por Estudiante")
        print("3. Listar por Grado")
        print("4. Listar por Aula")
        print("0. Volver")
        opcion = self.solicitar_cadena("\nSeleccione un criterio de listado: ")

        asistencias_filtradas = []
        if opcion == '1':
            fecha_obj = self.solicitar_fecha("Digite la fecha a consultar (dd/mm/yyyy): ")
            asistencias_filtradas = self.colegio.get_asistencias_filtradas('fecha', fecha_obj)
        elif opcion == '2':
            estudiante_obj = self.seleccionar_entidad("Estudiante")
            if estudiante_obj: asistencias_filtradas = self.colegio.get_asistencias_filtradas('estudiante', estudiante_obj)
        elif opcion == '3':
            grado_obj = self.seleccionar_entidad("Grado")
            if grado_obj: asistencias_filtradas = self.colegio.get_asistencias_filtradas('grado', grado_obj)
        elif opcion == '4':
            aula_obj = self.seleccionar_entidad("Aula")
            if aula_obj: asistencias_filtradas = self.colegio.get_asistencias_filtradas('aula', aula_obj)
        elif opcion == '0': return
        else: print("Opción no válida."); return

        if not asistencias_filtradas:
            print("\nInfo - No se encontraron registros de asistencia que coincidan con el criterio.")
        else:
            for asistencia in asistencias_filtradas:
                asistencia.mostrar_detalles()

    def menu_reportes(self):
        while True:
            system("cls")
            print("==== Menú de Reportes ====")
            print("1. Cantidad total de estudiantes del colegio")
            print("2. Cantidad de estudiantes por grado")
            print("3. Reporte de asistencia por fecha")
            print("0. Volver al Menú Principal")

            opcion = self.solicitar_cadena("\nSeleccione una opción: ")

            if opcion == '1':
                total = self.colegio.calcular_total_estudiantes()
                print(f"\nLa cantidad total de estudiantes habilitados en grados habilitados es: {total}")
            elif opcion == '2':
                por_grado = self.colegio.calcular_estudiantes_por_grado()
                print("\n** Cantidad de Estudiantes por Grado (solo grados habilitados) **")
                if not por_grado:
                    print("No hay grados o estudiantes para mostrar.")
                else:
                    for grado, cantidad in por_grado.items():
                        print(f"- {grado}: {cantidad} estudiante(s)")
            elif opcion == '3':
                
                fechas_disponibles = sorted(list(set(a.get_fecha() for a in self.colegio.asistencias)))
                if not fechas_disponibles:
                    print("\nInfo - No hay registros de asistencia con fechas para mostrar.")
                    return 

                print("\nFechas con registros de asistencia disponibles:")
                for fecha in fechas_disponibles:
                    print(f"- {fecha.strftime('%d/%m/%Y')}")
                    
                fecha_obj = self.solicitar_fecha("Digite la fecha para el reporte (dd/mm/yyyy): ")
                reporte = self.colegio.get_calculos_asistencia_por_fecha(fecha_obj)

                print(f"\n** Reporte de Asistencia para el {fecha_obj.strftime('%d/%m/%Y')} **")
                print(f"- Estudiantes con asistencia: {reporte['asistencia']}")
                print(f"- Estudiantes con inasistencia justificada: {reporte['inasistencia_justificada']}")
                print(f"- Estudiantes con inasistencia injustificada: {reporte['inasistencia_injustificada']}")
                print(f"- Total inasistencias: {reporte['inasistencia_total']}")
            elif opcion == '0':
                break
            else:
                print("Error - Opción no válida.")

            self.pausa_y_limpiar()

    def mostrar_menu_principal(self):
        while True:
            system("cls")
            print("==== Sistema de Control de Asistencia Colegio ====")
            print("1. Gestión de Estudiantes")
            print("2. Gestión de Docentes")
            print("3. Gestión de Materias")
            print("4. Gestión de Grados")
            print("5. Gestión de Aulas")
            print("6. Gestión de Asistencia")
            print("7. Reportes y Cálculos")
            print("0. Salir")

            opcion = self.solicitar_cadena("\nSeleccione una opción: ")

            if opcion == '1': self.menu_gestion_entidad("Estudiante")
            elif opcion == '2': self.menu_gestion_entidad("Docente")
            elif opcion == '3': self.menu_gestion_entidad("Materia")
            elif opcion == '4': self.menu_gestion_entidad("Grado")
            elif opcion == '5': self.menu_gestion_entidad("Aula")
            elif opcion == '6': self.menu_asistencia()
            elif opcion == '7': self.menu_reportes()
            elif opcion == '0':
                print("Saliendo del programa...")
                break
            else:
                print("Error - Opción no válida.")
                self.pausa_y_limpiar()

if __name__ == "__main__":
    menu_principal = Menu()
    menu_principal.mostrar_menu_principal()