## 📝 PREGUNTAS TEÓRICAS (10 puntos)

### Pregunta 1: LSP (5 pts)

**a) (5 pts)** Explica qué es LSP y cómo se aplica al ejemplo:

```python
class Usuario:
    def calcular_limite_prestamos(self):
        return 3

class Estudiante(Usuario):
    def calcular_limite_prestamos(self):
        return 3
```

**Respuesta:**

```El
_________________________________________________________________
El Principio de Sustitución de Liskov (LSP) establece que los objetos de una clase derivada deben poder reemplazar a los objetos de la clase base sin alterar el comportamiento correcto del programa.

Este código SÍ cumple con LSP porque:
Estudiante puede sustituir a Usuario sin problemas
Ambos retornan el mismo valor (3 préstamos)
El comportamiento esperado se mantiene
No hay sorpresas ni comportamientos inesperados

Sin embargo, sería más útil si Estudiante tuviera su propio límite (por ejemplo, 5) manteniendo el contrato del método.

_________________________________________________________________
```

**b) (5 pts)** Da un ejemplo que VIOLE LSP y explica por qué:

```python
class Usuario:
    def calcular_limite_prestamos(self):
        return 3  # Retorna un número

class UsuarioInvitado(Usuario):
    def calcular_limite_prestamos(self):
        raise Exception("Los invitados no pueden pedir préstamos")
        # ❌ VIOLACIÓN: Lanza excepción en lugar de retornar número
```

Este código **VIOLA LSP** porque:

1. **Cambio de contrato**: La clase base promete retornar un número entero, pero la subclase lanza una excepción.
2. **No es sustituible**: Si tenemos código que espera un `Usuario`:

```python
   def procesar_prestamo(usuario: Usuario):
       limite = usuario.calcular_limite_prestamos()
       print(f"Límite: {limite}")  # ← Esto falla con UsuarioInvitado
```

3. **Comportamiento inesperado**: El código que funciona con `Usuario` NO funciona con `UsuarioInvitado`, violando el principio de sustitución.

**Solución correcta:**

```python
class UsuarioInvitado(Usuario):
    def calcular_limite_prestamos(self):
        return 0  # ✅ Retorna número (cero préstamos permitidos)
```

### Pregunta 2: ISP (5 pts)

**a) (5 pts)** ¿Por qué esta interfaz VIOLA ISP?

```python
class IGestionBiblioteca:
    def agregar_libro(self): pass
    def buscar_libro(self): pass
    def realizar_prestamo(self): pass
    def generar_reporte(self): pass
    def hacer_backup(self): pass
```

**Respuesta:**

```
_________________________________________________________________
Esta interfaz VIOLA ISP porque:

Demasiado grande: Obliga a todas las clases que la implementen a definir TODOS los métodos, incluso los que no necesitan.
Acopla responsabilidades diferentes:

Gestión de libros (agregar, buscar)
Gestión de préstamos (realizar_prestamo)
Reportes (generar_reporte)
Mantenimiento (hacer_backup)
_________________________________________________________________
```

**b) (5 pts)** Propón cómo segregar esta interfaz:

```
Interface 1: IGestionLibros
Métodos: agregar_libro(), buscar_libro()

Interface 2: IGestionPrestamos  
Métodos: realizar_prestamo(), devolver_libro()

Interface 3: IAdministracion
Métodos: generar_reporte(), hacer_backup()
```

---
