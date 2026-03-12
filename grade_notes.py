
import json
from statistics import mean
from typing import Dict, List
import os

ARCHIVO_DATOS = "estudiantes.json"

# definir las clases para representar estudiantes y materias

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
            print(f"→ The subject '{clave}' already exists.")
        self.materias[clave] = Materia(nombre_materia, nota)

    def promedio(self) -> float:
        if not self.materias:
            return 0.0
        return mean(m.nota for m in self.materias.values())

    def mostrar(self):
        print(f"\n┌─ {self.codigo}  {self.nombre}")
        print(f"│  Promedio: {self.promedio():.2f}")
        if not self.materias:
            print("└─ No subjects registered yet.")
        else:
            print("├─ Subjects:")
            for m in self.materias.values():
                print(f"│  {m}")
            print("└" + "─" * 40)

#          Funciones de archivo

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
        print(f"Error loading data: {e}")
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
        print(f"→ Data saved to {ARCHIVO_DATOS}")
    except Exception as e:
        print(f"Error saving data: {e}")


# ──────────────────────────────────────────────
#          Menú principal
# ──────────────────────────────────────────────

def mostrar_menu():
    print("\n" + "═" * 50)
    print(" STUDENT'S SYSTEM ".center(50))
    print("═" * 50)
    print(" 1. Record new student")
    print(" 2. add / update grade")
    print(" 3. Show student details")
    print(" 4. Show all students")
    print(" 5. Show overall average and top student")
    print(" 6. Save and exit")
    print("═" * 50)


def main():
    estudiantes = cargar_datos()
    print(f"→ {len(estudiantes)} was registered students.")

    while True:
        mostrar_menu()
        opcion = input("→ Enter an option (1-6): ").strip()

        if opcion == "1":
            while True:
                codigo = input("Student ID: ").strip().upper()
                if codigo in estudiantes:
                    print("That code already exists. Try another one.")
                    continue
                nombre = input("Full name: ").strip()
                estudiantes[codigo] = Estudiante(codigo, nombre)
                print(f"→ {nombre} ({codigo}) registered.")
                
                # Preguntar si agregar materias
                while True:
                    agregar_materia = input("Do you want to add a subject to this student? (y/n): ").strip().lower()
                    if agregar_materia == 'y':
                        materia = input("Subject name: ").strip()
                        while True:
                            try:
                                nota = float(input("Grade (0.0 - 5.0): "))
                                if 0 <= nota <= 5:
                                    break
                                print("The grade must be between 0.0 and 5.0")
                            except ValueError:
                                print("Please enter a valid number.")
                        estudiantes[codigo].agregar_materia(materia, nota)
                        print("→ Grade registered/updated.")
                    elif agregar_materia == 'n':
                        break
                    else:
                        print("Please enter 'y' or 'n'.")
                
                # Preguntar si seguir agregando estudiantes
                seguir = input("Do you want to register another student? (y/n): ").strip().lower()
                if seguir != 'y':
                    break

        elif opcion == "2":
            codigo = input("Student ID: ").strip().upper()
            if codigo not in estudiantes:
                print("Student not found.")
                continue
            est = estudiantes[codigo]
            materia = input("Subject name: ").strip()
            while True:
                try:
                    nota = float(input("Grade (0.0 - 5.0): "))
                    if 0 <= nota <= 5:
                        break
                    print("The grade must be between 0.0 and 5.0")
                except ValueError:
                    print("Please enter a valid number.")
            est.agregar_materia(materia, nota)
            print("→ Grade registered/updated.")

        elif opcion == "3":
            codigo = input("Student ID: ").strip().upper()
            if codigo in estudiantes:
                estudiantes[codigo].mostrar()
            else:
                print("Student not found.")

        elif opcion == "4":
            if not estudiantes:
                print("No students registered yet.")
                continue
            print("\n" + " STUDENT LIST ".center(50))
            for est in estudiantes.values():
                est.mostrar()

        elif opcion == "5":
            if not estudiantes:
                print("No students available to calculate averages.")
                continue

            promedios = [(est.promedio(), est) for est in estudiantes.values()]
            promedios.sort(reverse=True)

            print("\n" + " GROUP STATISTICS ".center(50))
            promedio_grupo = mean(p[0] for p in promedios)
            print(f"Overall group average: {promedio_grupo:.2f}")
            print(f"Top student: {promedios[0][1].nombre} ({promedios[0][1].codigo}) → {promedios[0][0]:.2f}")
            print(f"Lowest average: {promedios[-1][1].nombre} → {promedios[-1][0]:.2f}")

        elif opcion == "6":
            guardar_datos(estudiantes)
            print("\nThank you for using the Student's System. Goodbye!")
            break

        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram finished by user.")