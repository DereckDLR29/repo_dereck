# first step: define the grade notes' variables

# second step: define the grade notes' functions

import json
from statistics import mean
from typing import Dict, List
import os

ARCHIVO_DATOS = "estudiantes.json"


class Materia:
    def __init__(self, nombre: str, nota: float):
        self.nombre = nombre.strip().upper()
        self.nota = max(0.0, min(5.0, float(nota)))  # range 0.0 a 5.0

    def __str__(self):
        return f"{self.nombre:25} | {self.nota:4.1f}"


class Estudiante:
    def __init__(self, codigo: str, nombre: str):
        self.codigo = codigo.strip().upper()
        self.nombre = nombre.strip().title()
        self.materias: Dict[str, Materia] = {}  # key = subjet's name

    def agregar_materia(self, nombre_materia: str, nota: float):
        clave = nombre_materia.strip().upper()
        if clave in self.materias:
            print(f"→ La materia '{clave}' ya existe. Se sobrescribirá.")
        self.materias[clave] = Materia(nombre_materia, nota)

    def promedio(self) -> float:
        if not self.materias:
            return 0.0
        return mean(m.nota for m in self.materias.values())

    def mostrar(self):
        print(f"\n┌─ {self.codigo}  {self.nombre}")
        print(f"│  Promedio: {self.promedio():.2f}")
        if not self.materias:
            print("└─ Sin materias registradas")
        else:
            print("├─ Materias:")
            for m in self.materias.values():
                print(f"│  {m}")
            print("└" + "─" * 40)


# ──────────────────────────────────────────────
#          Funciones de archivo
# ──────────────────────────────────────────────

def cargar_datos() -> Dict[str, Estudiante]:
    if not os.path.exists(ARCHIVO_DATOS):
        return {}
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            data = json.load(f)
        estudiantes = {}
        for cod, info in data.items():
            est = Estudiante(cod, info["nombre"])
            for mat, nota in info["materias"].items():
                est.agregar_materia(mat, nota)
            estudiantes[cod] = est
        return estudiantes
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return {}


def guardar_datos(estudiantes: Dict[str, Estudiante]):
    data = {}
    for cod, est in estudiantes.items():
        data[cod] = {
            "nombre": est.nombre,
            "materias": {m.nombre: m.nota for m in est.materias.values()}
        }
    try:
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"→ Datos guardados en {ARCHIVO_DATOS}")
    except Exception as e:
        print(f"Error al guardar: {e}")


# ──────────────────────────────────────────────
#          Menú principal
# ──────────────────────────────────────────────

def mostrar_menu():
    print("\n" + "═" * 50)
    print(" SISTEMA DE ESTUDIANTES ".center(50))
    print("═" * 50)
    print(" 1. Registrar nuevo estudiante")
    print(" 2. Agregar / modificar nota")
    print(" 3. Ver información de un estudiante")
    print(" 4. Ver todos los estudiantes")
    print(" 5. Mostrar promedio general y destacado")
    print(" 6. Guardar y salir")
    print("═" * 50)


def main():
    estudiantes = cargar_datos()
    print(f"→ Se cargaron {len(estudiantes)} estudiantes del archivo")

    while True:
        mostrar_menu()
        opcion = input("→ Elige una opción (1-6): ").strip()

        if opcion == "1":
            codigo = input("Código del estudiante: ").strip().upper()
            if codigo in estudiantes:
                print("¡Ese código ya está registrado!")
                continue
            nombre = input("Nombre completo: ").strip()
            estudiantes[codigo] = Estudiante(codigo, nombre)
            print(f"→ {nombre} ({codigo}) registrado.")

        elif opcion == "2":
            codigo = input("Código del estudiante: ").strip().upper()
            if codigo not in estudiantes:
                print("Estudiante no encontrado.")
                continue
            est = estudiantes[codigo]
            materia = input("Nombre de la materia: ").strip()
            while True:
                try:
                    nota = float(input("Nota (0.0 - 5.0): "))
                    if 0 <= nota <= 5:
                        break
                    print("La nota debe estar entre 0.0 y 5.0")
                except ValueError:
                    print("Ingresa un número válido.")
            est.agregar_materia(materia, nota)
            print("→ Nota registrada/actualizada.")

        elif opcion == "3":
            codigo = input("Código: ").strip().upper()
            if codigo in estudiantes:
                estudiantes[codigo].mostrar()
            else:
                print("No se encontró ese código.")

        elif opcion == "4":
            if not estudiantes:
                print("Aún no hay estudiantes registrados.")
                continue
            print("\n" + " LISTADO GENERAL ".center(50))
            for est in estudiantes.values():
                est.mostrar()

        elif opcion == "5":
            if not estudiantes:
                print("No hay estudiantes para calcular promedios.")
                continue

            promedios = [(est.promedio(), est) for est in estudiantes.values()]
            promedios.sort(reverse=True)

            print("\n" + " ESTADÍSTICAS DEL GRUPO ".center(50))
            promedio_grupo = mean(p[0] for p in promedios)
            print(f"Promedio general del grupo: {promedio_grupo:.2f}")
            print(f"Estudiante destacado: {promedios[0][1].nombre} ({promedios[0][1].codigo}) → {promedios[0][0]:.2f}")
            print(f"Peor promedio: {promedios[-1][1].nombre} → {promedios[-1][0]:.2f}")

        elif opcion == "6":
            guardar_datos(estudiantes)
            print("\n¡Gracias por usar el sistema! Hasta luego.")
            break

        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma terminado por el usuario.")