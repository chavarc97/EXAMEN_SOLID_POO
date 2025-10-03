from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime

class Libro:
    def __init__(self, id, titulo, autor, isbn, disponible=True):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = disponible

class Prestamo:
    def __init__(self, id, libro_id, usuario, fecha):
        self.id = libro_id
        self.libro_id = libro_id
        self.usuario = usuario
        self.fecha = fecha
        self.devuelto = False
    

# ========================= OCP: ESTRATEGIAS DE BÚSQUEDA =========================

class EstrategiaBusqueda(ABC):
    """Clase base para estrategias de búsqueda (OCP)"""
    
    @abstractmethod
    def buscar(self, libros: List[Libro], valor) -> List[Libro]:
        pass


class BusquedaPorTitulo(EstrategiaBusqueda):
    def buscar(self, libros: List[Libro], valor: str) -> List[Libro]:
        return [libro for libro in libros if valor.lower() in libro.titulo.lower()]


class BusquedaPorAutor(EstrategiaBusqueda):
    def buscar(self, libros: List[Libro], valor: str) -> List[Libro]:
        return [libro for libro in libros if valor.lower() in libro.autor.lower()]


class BusquedaPorISBN(EstrategiaBusqueda):
    def buscar(self, libros: List[Libro], valor: str) -> List[Libro]:
        return [libro for libro in libros if libro.isbn == valor]


class BusquedaPorDisponibilidad(EstrategiaBusqueda):
    def buscar(self, libros: List[Libro], valor) -> List[Libro]:
        disponible = valor.lower() == 'true' if isinstance(valor, str) else bool(valor)
        return [libro for libro in libros if libro.disponible == disponible]


# ========================= SRP: VALIDADOR =========================

class ValidadorBiblioteca:
    """SRP: Solo responsable de VALIDAR datos"""
    
    @staticmethod
    def validar_libro(titulo: str, autor: str, isbn: str) -> str:
        """Valida datos de libro. Retorna None si es válido, mensaje de error si no."""
        if not titulo or len(titulo) < 2:
            return "Error: Título inválido"
        if not autor or len(autor) < 3:
            return "Error: Autor inválido"
        if not isbn or len(isbn) < 10:
            return "Error: ISBN inválido"
        return None
    
    @staticmethod
    def validar_usuario(usuario: str) -> str:
        """Valida nombre de usuario."""
        if not usuario or len(usuario) < 3:
            return "Error: Nombre de usuario inválido"
        return None


    
# ========================= DIP: REPOSITORIO (ABSTRACCIÓN) =========================

class IRepositorio(ABC):
    """DIP: Interfaz abstracta para persistencia"""
    
    @abstractmethod
    def guardar(self, libros: List[Libro], prestamos: List[Prestamo]) -> bool:
        pass
    
    @abstractmethod
    def cargar(self) -> Dict[str, Any]:
        pass


class RepositorioArchivo(IRepositorio):
    """DIP: Implementación concreta para archivo"""
    
    def __init__(self, archivo='biblioteca.txt'):
        self.archivo = archivo
    
    def guardar(self, libros: List[Libro], prestamos: List[Prestamo]) -> bool:
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                f.write(f"Libros: {len(libros)}\n")
                f.write(f"Préstamos: {len(prestamos)}\n")
                
                f.write("\n--- LIBROS ---\n")
                for libro in libros:
                    f.write(f"{libro.id}|{libro.titulo}|{libro.autor}|{libro.isbn}|{libro.disponible}\n")
                
                f.write("\n--- PRÉSTAMOS ---\n")
                for prestamo in prestamos:
                    f.write(f"{prestamo.id}|{prestamo.libro_id}|{prestamo.usuario}|{prestamo.fecha}|{prestamo.devuelto}\n")
            return True
        except Exception as e:
            print(f"Error guardando: {e}")
            return False
    
    def cargar(self) -> Dict[str, Any]:
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                data = f.read()
            return {'libros': [], 'prestamos': []}
        except FileNotFoundError:
            return {'libros': [], 'prestamos': []}


class RepositorioMemoria(IRepositorio):
    """DIP: Implementación en memoria (para testing)"""
    
    def __init__(self):
        self.datos = {'libros': [], 'prestamos': []}
    
    def guardar(self, libros: List[Libro], prestamos: List[Prestamo]) -> bool:
        self.datos['libros'] = libros.copy()
        self.datos['prestamos'] = prestamos.copy()
        return True
    
    def cargar(self) -> Dict[str, Any]:
        return self.datos

#========================== EJERCICIO 2 =============================================
class RepositorioBiblioteca:
    def __init__(self,archivo):
        self.archivo = archivo
        self.libros = []
        self.prestamos = []

    def _guardar_en_archivo_libros(self):
        with open(self.archivo, 'w') as f:
            for libro in self.libros:
                f.write(f"{libro.id},{libro.titulo},{libro.autor},{libro.isbn},{libro.disponible}\n")

    def guardar_libro(self, libro: Libro, validacion: ValidadorBiblioteca) -> str:
        error = validacion.validar_libro(libro.titulo, libro.autor, libro.isbn)
        if error:
            return error
        self.libros.append(libro)
        self._guardar_en_archivo_libros()
        return f"Libro '{libro.titulo}' agregado exitosamente"
    
 
class RepositorioPrestamos:
    def __init__(self, archivo_prestamos='prestamos.txt'):
        self.archivo_prestamos = archivo_prestamos
        self.prestamos = []
        self.contador_prestamo = 1

    def realizar_prestamo(self, libro: Libro, usuario) -> str:
        error = ValidadorBiblioteca.validar_usuario(usuario) 
        if error:
            return error
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prestamo = Prestamo(self.contador_prestamo, libro.id, usuario, date)
        self.prestamos.append(prestamo)
        self.contador_prestamo += 1
        
        libro.disponible = False
        self.guardar_en_archivo_prestamos(prestamo)
        return f"Préstamo realizado: {prestamo}"
    
    def guardar_en_archivo_prestamos(self, prestamo: Prestamo):
        with open(self.archivo_prestamos, 'a') as f:
            f.write(f"{prestamo.id},{prestamo.libro_id},{prestamo.usuario},{prestamo.fecha},{prestamo.devuelto}\n")
            
#=======================================================================
    

# ========================= SRP: NOTIFICADOR =========================
class ServicioNotificaciones:
    """SRP: Solo responsable de NOTIFICAR"""
    
    def notificar_prestamo(self, usuario: str, libro_titulo: str):
        print(f"[NOTIFICACIÓN] {usuario}: Préstamo de '{libro_titulo}'")
    
    def notificar_devolucion(self, usuario: str, libro_titulo: str):
        print(f"[NOTIFICACIÓN] {usuario}: Devolución de '{libro_titulo}'")


# ========================= SISTEMA BIBLIOTECA COMPLETO =========================

class SistemaBiblioteca:
    """
    Sistema de Biblioteca aplicando los 3 principios SOLID:
    
    OCP: Usa estrategias de búsqueda extensibles
    SRP: Delega validación, persistencia y notificación
    DIP: Depende de abstracción IRepositorio, no de implementación concreta
    
    RESPONSABILIDAD ÚNICA: Coordinar la lógica de negocio de la biblioteca
    """
    
    def __init__(self, 
                 repositorio: IRepositorio,
                 validador: ValidadorBiblioteca,
                 notificador: ServicioNotificaciones):
        """
        Constructor con INYECCIÓN DE DEPENDENCIAS (DIP).
        Recibe abstracciones, no implementaciones concretas.
        """
        # Dependencias inyectadas
        self.repositorio = repositorio      # DIP: Abstracción
        self.validador = validador           # SRP: Validación
        self.notificador = notificador       # SRP: Notificación
        
        # Estado interno
        self.libros = []
        self.prestamos = []
        self.contador_libro = 1
        self.contador_prestamo = 1
        
        # OCP: Estrategias de búsqueda (extensible)
        self.estrategias_busqueda = {
            'titulo': BusquedaPorTitulo(),
            'autor': BusquedaPorAutor(),
            'isbn': BusquedaPorISBN(),
            'disponible': BusquedaPorDisponibilidad()
        }
    
    # ==================== GESTIÓN DE LIBROS ====================
    
    def agregar_libro(self, titulo: str, autor: str, isbn: str) -> str:
        """
        Agrega un libro al sistema.
        
        Aplica SRP:
        1. Delega validación a ValidadorBiblioteca
        2. Ejecuta lógica de negocio
        3. Delega persistencia a IRepositorio
        """
        # 1. Validar (SRP: delega)
        error = self.validador.validar_libro(titulo, autor, isbn)
        if error:
            return error
        
        # 2. Lógica de negocio
        libro = Libro(self.contador_libro, titulo, autor, isbn)
        self.libros.append(libro)
        self.contador_libro += 1
        
        # 3. Persistir (DIP: usa abstracción)
        self.repositorio.guardar(self.libros, self.prestamos)
        
        return f"Libro '{titulo}' agregado exitosamente"
    
    def buscar_libro(self, criterio: str, valor) -> List[Libro]:
        """
        Busca libros usando estrategias (OCP).
        
        OCP: Abierto a extensión (agregar estrategias), 
             cerrado a modificación (sin if/elif).
        """
        estrategia = self.estrategias_busqueda.get(criterio)
        
        if not estrategia:
            print(f"Criterio '{criterio}' no válido")
            return []
        
        return estrategia.buscar(self.libros, valor)
    
    def registrar_estrategia_busqueda(self, nombre: str, estrategia: EstrategiaBusqueda):
        """
        OCP: Permite agregar nuevas estrategias sin modificar código.
        """
        self.estrategias_busqueda[nombre] = estrategia
    
    def obtener_todos_libros(self) -> List[Libro]:
        """Retorna todos los libros."""
        return self.libros
    
    def obtener_libros_disponibles(self) -> List[Libro]:
        """Retorna solo libros disponibles."""
        return [libro for libro in self.libros if libro.disponible]
    
    # ==================== GESTIÓN DE PRÉSTAMOS ====================
    
    def realizar_prestamo(self, libro_id: int, usuario: str) -> str:
        """
        Realiza un préstamo de libro.
        
        Aplica SRP:
        1. Valida usuario
        2. Valida disponibilidad
        3. Ejecuta lógica de negocio
        4. Persiste
        5. Notifica
        """
        # 1. Validar usuario (SRP: delega)
        error = self.validador.validar_usuario(usuario)
        if error:
            return error
        
        # 2. Buscar y validar libro
        libro = self._buscar_libro_por_id(libro_id)
        if not libro:
            return "Error: Libro no encontrado"
        
        if not libro.disponible:
            return "Error: Libro no disponible"
        
        # 3. Lógica de negocio
        prestamo = Prestamo(
            self.contador_prestamo,
            libro_id,
            usuario,
            datetime.now().strftime("%Y-%m-%d")
        )
        self.prestamos.append(prestamo)
        self.contador_prestamo += 1
        libro.disponible = False
        
        # 4. Persistir (DIP: usa abstracción)
        self.repositorio.guardar(self.libros, self.prestamos)
        
        # 5. Notificar (SRP: delega)
        self.notificador.notificar_prestamo(usuario, libro.titulo)
        
        return f"Préstamo realizado a {usuario}"
    
    def devolver_libro(self, prestamo_id: int) -> str:
        """
        Devuelve un libro prestado.
        """
        # Buscar préstamo
        prestamo = self._buscar_prestamo_por_id(prestamo_id)
        if not prestamo:
            return "Error: Préstamo no encontrado"
        
        if prestamo.devuelto:
            return "Error: Libro ya devuelto"
        
        # Buscar libro y actualizar
        libro = self._buscar_libro_por_id(prestamo.libro_id)
        if libro:
            libro.disponible = True
        
        # Actualizar préstamo
        prestamo.devuelto = True
        
        # Persistir
        self.repositorio.guardar(self.libros, self.prestamos)
        
        # Notificar
        if libro:
            self.notificador.notificar_devolucion(prestamo.usuario, libro.titulo)
        
        return "Libro devuelto exitosamente"
    
    def obtener_prestamos_activos(self) -> List[Prestamo]:
        """Retorna préstamos no devueltos."""
        return [p for p in self.prestamos if not p.devuelto]
    
    def obtener_historial_prestamos(self) -> List[Prestamo]:
        """Retorna todos los préstamos."""
        return self.prestamos
    
    # ==================== MÉTODOS AUXILIARES ====================
    
    def _buscar_libro_por_id(self, libro_id: int) -> Libro:
        """Busca un libro por su ID."""
        for libro in self.libros:
            if libro.id == libro_id:
                return libro
        return None
    
    def _buscar_prestamo_por_id(self, prestamo_id: int) -> Prestamo:
        """Busca un préstamo por su ID."""
        for prestamo in self.prestamos:
            if prestamo.id == prestamo_id:
                return prestamo
        return None
    

        
        
    
# ========================= FUNCIÓN MAIN COMPLETA =========================

def main():
    """
    Función principal que demuestra el sistema completo.
    """
    print("=" * 70)
    print("SISTEMA BIBLIOTECA - APLICANDO SOLID COMPLETO")
    print("=" * 70)
    
    # ============ CONFIGURACIÓN (Inyección de Dependencias) ============
    print("\n[CONFIGURACIÓN]")
    print("✓ Creando ValidadorBiblioteca...")
    validador = ValidadorBiblioteca()
    
    print("✓ Creando RepositorioArchivo...")
    repositorio = RepositorioArchivo('biblioteca_completa.txt')
    
    print("✓ Creando ServicioNotificaciones...")
    notificador = ServicioNotificaciones()
    
    print("✓ Inicializando SistemaBiblioteca...")
    sistema = SistemaBiblioteca(repositorio, validador, notificador)
    
    # ============ AGREGAR LIBROS ============
    print("\n" + "=" * 70)
    print("1. AGREGAR LIBROS")
    print("=" * 70)
    print(sistema.agregar_libro("Cien Años de Soledad", "Gabriel García Márquez", "9780060883287"))
    print(sistema.agregar_libro("El Principito", "Antoine de Saint-Exupéry", "9780156012195"))
    print(sistema.agregar_libro("1984", "George Orwell", "9780451524935"))
    print(sistema.agregar_libro("Don Quijote", "Miguel de Cervantes", "9788424934484"))
    
    # ============ BÚSQUEDA (OCP) ============
    print("\n" + "=" * 70)
    print("2. BÚSQUEDAS (Aplicando OCP)")
    print("=" * 70)
    
    print("\n📖 Búsqueda por título:")
    resultados = sistema.buscar_libro('titulo', 'Cien')
    for libro in resultados:
        print(f"   - {libro.titulo} por {libro.autor}")
    
    print("\n👤 Búsqueda por autor:")
    resultados = sistema.buscar_libro('autor', 'Orwell')
    for libro in resultados:
        print(f"   - {libro.titulo} por {libro.autor}")
    
    print("\n🔢 Búsqueda por ISBN:")
    resultados = sistema.buscar_libro('isbn', '9780156012195')
    for libro in resultados:
        print(f"   - {libro.titulo}")
    
    print("\n✅ Búsqueda por disponibilidad:")
    resultados = sistema.buscar_libro('disponible', 'true')
    print(f"   Libros disponibles: {len(resultados)}")
    for libro in resultados:
        print(f"   - {libro.titulo}")
    
    # ============ PRÉSTAMOS ============
    print("\n" + "=" * 70)
    print("3. REALIZAR PRÉSTAMOS")
    print("=" * 70)
    print(sistema.realizar_prestamo(1, "Juan Pérez"))
    print(sistema.realizar_prestamo(3, "María García"))
    
    # ============ LIBROS DISPONIBLES ============
    print("\n" + "=" * 70)
    print("4. LIBROS DISPONIBLES")
    print("=" * 70)
    disponibles = sistema.obtener_libros_disponibles()
    print(f"Total disponibles: {len(disponibles)}")
    for libro in disponibles:
        print(f"   - {libro.titulo}")
    
    # ============ PRÉSTAMOS ACTIVOS ============
    print("\n" + "=" * 70)
    print("5. PRÉSTAMOS ACTIVOS")
    print("=" * 70)
    activos = sistema.obtener_prestamos_activos()
    print(f"Total activos: {len(activos)}")
    for prestamo in activos:
        libro = sistema._buscar_libro_por_id(prestamo.libro_id)
        print(f"   - {libro.titulo} → {prestamo.usuario}")
    
    # ============ DEVOLUCIÓN ============
    print("\n" + "=" * 70)
    print("6. DEVOLVER LIBRO")
    print("=" * 70)
    print(sistema.devolver_libro(1))
    
    #=========== Prestamos activos tras devolución ============
    print("\n" + "=" * 70)
    print("7. PRÉSTAMOS ACTIVOS TRAS DEVOLUCIÓN")
    print("=" * 70)
    activos = sistema.obtener_prestamos_activos()
    print(f"Total activos: {len(activos)}")
    
    # ============ RESUMEN FINAL ============
    print("\n" + "=" * 70)
    print("✅ PRINCIPIOS SOLID APLICADOS:")
    print("=" * 70)
    print("✓ OCP: Estrategias de búsqueda extensibles")
    print("✓ SRP: Validador, Repositorio y Notificador separados")
    print("✓ DIP: Sistema depende de abstracciones (IRepositorio)")
    print("=" * 70)


if __name__ == "__main__":
    main()