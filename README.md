# repo_dereck
# Student Management System

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

## Description

This project **is designed to** manage basic student information including names, enrolled subjects, and grades.  
It **is intended to** provide a simple way to store and persist student records in a JSON file for small-scale academic use or educational purposes.

## How it works

1. The program maintains a dictionary where each key is a student code (string) and each value is an `Estudiante` object.
2. The `guardar_datos()` function receives this dictionary as parameter.
3. It creates a new simplified dictionary structure suitable for JSON serialization.
4. For each student, it extracts the name and builds a sub-dictionary of subject names → grades.
5. The resulting data structure is written to a file (whose path is stored in the constant `ARCHIVO_DATOS`) using the `json` module.
6. The function uses `ensure_ascii=False` to correctly handle accented characters (e.g. Spanish names).
7. It prints a success message when the save completes or shows an error message if something fails.

## Status

> The project is currently being developed as a basic prototype.  
> The save functionality works correctly for the core use case, but loading and full CRUD operations are still in progress.
