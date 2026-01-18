# Superclases y Subclases en Programación Orientada a Objetos (Python)

Este documento explica de forma clara y progresiva los conceptos de **superclase** y **subclase** en Programación Orientada a Objetos (POO), usando Python y el ejemplo mostrado en el código.

---

## 1. ¿Qué es una clase?

Una **clase** es un molde o plantilla que define:

- **Atributos** (datos)
- **Métodos** (comportamientos)

A partir de una clase se crean **objetos**.

```python
class Persona:
    def hablar(self):
        print("Hola")
```

---

## 2. ¿Qué es un objeto?

Un **objeto** es una instancia específica de una clase.

```python
p = Persona()
p.hablar()
```

En el ejemplo, `p` es el objeto creado a partir de la clase `Persona`.
Cuando se llama a `p.hablar()`, el objeto `p` se pasa automáticamente al método y se recibe como `self`.

O de forma aún más directa:

`p` es el objeto, y `self` es la referencia a ese objeto dentro de la clase.

**Idea clave para fijar el concepto**

- Fuera de la clase → el objeto se llama `p`
- Dentro de la clase → ese mismo objeto se llama `self`

---

## 3. Superclase (clase padre)

Una **superclase** es una clase que proporciona atributos y métodos que pueden ser **heredados** por otras clases.

En el ejemplo:

```python
class Madre:
    def __init__(self):
        print("Soy Madre")
```

```python
class Padre:
    def __init__(self):
        print("Soy Padre")
```

- `Madre` y `Padre` son **superclases**
- Definen comportamiento común que puede reutilizarse

---

## 4. Subclase (clase hija)

Una **subclase** es una clase que **hereda** de una o más superclases.

```python
class Hijo(Madre, Padre):
    def __init__(self):
        Padre.__init__(self)
        print("Soy Hijo")
```

- `Hijo` es una **subclase**
- Hereda de `Madre` y `Padre`
- Esto se llama **herencia múltiple**

---

## 5. Herencia: qué significa

Cuando escribimos:

```python
class Hijo(Madre, Padre):
```

Significa:

> Un objeto `Hijo` **es también** un `Madre` y un `Padre`

La subclase:

- Reutiliza código
- Puede extender comportamiento
- Puede sobrescribir métodos

---

## 6. El método `__init__` (constructor)

El método `__init__` se ejecuta **automáticamente** al crear un objeto.

```python
hijo = Hijo()
```

Flujo en el ejemplo original:

1. Se ejecuta `Hijo.__init__`
2. Se llama manualmente a `Padre.__init__`
3. Se imprime:

```text
Soy Padre
Soy Hijo
```

⚠️ **Nota importante**: `Madre.__init__` **no se ejecuta**, porque nunca se llama.

---

## 7. Uso correcto de `super()` (forma recomendada)

En herencia múltiple, **no se debe llamar directamente a la clase padre**. La forma correcta es usar `super()`.

### Código correcto

```python
class Madre:
    def __init__(self):
        print("Soy Madre")

class Padre:
    def __init__(self):
        print("Soy Padre")

class Hijo(Madre, Padre):
    def __init__(self):
        super().__init__()
        print("Soy Hijo")

hijo = Hijo()
```

### Salida

```text
Soy Madre
Soy Padre
Soy Hijo
```

---

## 8. MRO (Method Resolution Order)

Python sigue un orden interno para resolver métodos llamado **MRO**.

```python
print(Hijo.mro())
```

Resultado:

```text
[Hijo, Madre, Padre, object]
```

Esto indica el orden en el que Python busca métodos. `super()` respeta este orden automáticamente.

---

## 9. Resumen conceptual

| Concepto   | Descripción                           |
| ---------- | ------------------------------------- |
| Clase      | Molde para crear objetos              |
| Objeto     | Instancia de una clase                |
| Superclase | Clase padre que aporta comportamiento |
| Subclase   | Clase hija que hereda                 |
| Herencia   | Reutilización de código               |
| `__init__` | Constructor                           |
| `super()`  | Llamada correcta a la superclase      |
| MRO        | Orden de resolución de métodos        |

---

## 10. Acceso a métodos y atributos en la instancia

Cuando creamos un objeto de la clase `Hijo` (se instancia), suceden dos cosas gracias a la herencia y `super()`:

1.  **Inicialización completa**: Al llamar a `super().__init__()`, se ejecutan los constructores de `Madre` y `Padre`. Esto asegura que el objeto tenga todos los **atributos** inicializados (por ejemplo, si `Madre` define `self.nombre`, el `Hijo` también lo tendrá).
2.  **Acceso total**: La instancia del hijo tiene acceso a **todos** los métodos, tanto los suyos como los de `Madre` y `Padre`.

### ¿A qué métodos accede la instancia?

La respuesta es: **A todos.**

El objeto `hijo` no está limitado a los métodos de su clase. Como hereda de `Madre` y `Padre`, puede usar sus métodos como si fueran propios.

```python
class Madre:
    def cantar(self):
        print("Lalalala")

class Padre:
    def bailar(self):
        print("Bailando")

class Hijo(Madre, Padre):
    def programar(self):
        print("Escribiendo código")

# Instancia
pepe = Hijo()

# Acceso total
pepe.programar() # ✅ Método de Hijo
pepe.cantar()    # ✅ Método de Madre
pepe.bailar()    # ✅ Método de Padre
```

**Conclusión**: La instancia accede a los métodos del Hijo **Y** también a los de Madre y Padre. No hay distinción al usarlos.

---

## 11. Métodos de clase y `cls`

Hasta ahora hemos usado `self`, que representa a la **instancia** (el objeto concreto). Pero existe otro concepto llamado **`cls`**.

### ¿Qué es `cls`?

- **`self`**: Referencia al **objeto** (ej. "pepe").
- **`cls`**: Referencia a la **clase** (ej. "Persona" o "Hijo").

### ¿Cuándo se usa?

Se usa dentro de métodos especiales marcados con `@classmethod`. Esto permite trabajar con datos que pertenecen a **toda la clase** y no solo a un objeto.

```python
class Persona:
    especie = "Humano"  # Atributo de clase (compartido)

    def __init__(self, nombre):
        self.nombre = nombre  # Atributo de instancia (único por objeto)

    # Método normal (de instancia)
    def saludar(self):
        print(f"Hola, soy {self.nombre}")

    # Método de clase (usa cls)
    @classmethod
    def cambiar_especie(cls, nueva_especie):
        cls.especie = nueva_especie  # Cambia para TODOS
```

### Ejemplo de uso

```python
p1 = Persona("Juan")
p2 = Persona("Ana")

# Cambiamos la especie para TODOS usando la clase
Persona.cambiar_especie("Superhumano")

print(p1.especie)  # Imprime: Superhumano
print(p2.especie)  # Imprime: Superhumano
```

Esto aplica un cambio **global**: se modifica el atributo de clase `especie`, por lo que el cambio afecta a **todas** las instancias existentes y futuras de la clase.

Un método `@classmethod` permite modificar el **estado de la clase**, y ese cambio se refleja automáticamente en todos los objetos que dependen de ella.

> **Nota**: `cls` es solo una convención, igual que `self`, pero es importantísimo respetarla para que otros programadores entiendan tu código.

---

## 12. Verificación de atributos (`hasattr`)

**`hasattr`** es una función integrada de Python que sirve para **preguntar** si un objeto tiene cierto atributo o método.

Significa **"Has Attribute"** (¿Tiene atributo?).

### ¿Para qué sirve?

Sirve para **evitar errores** (`AttributeError`) antes de intentar usar algo que quizás no existe en el objeto. Es muy útil cuando trabajas con herencia o con objetos dinámicos donde no estás 100% seguro de qué propiedades tienen.

### Sintaxis

`hasattr(objeto, "nombre_del_atributo")` -> Devuelve `True` o `False`.

### Ejemplo

Imagina que tienes objetos que a veces tienen el método `hablar` y a veces no.

```python
class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre


u1 = Usuario("Naison")


print(hasattr(u1, "nombre"))
```

### Salida

```text
True
```

---

## 13. Patrón Singleton (Método explícito)

A veces necesitamos garantizar que una clase tenga **una única instancia** en todo el programa (ej. Conexión a Base de Datos, Configuración).

Aunque se puede hacer con `__new__` (implícito), una forma más clara y segura es usar un **método explícito** (`get_instance`).

### Estructura

1.  Usamos una variable de clase `_instancia` para guardar el objeto único.
2.  Creamos un `@classmethod` que revisa:
    - Si `_instancia` ya existe, la devuelve.
    - Si no existe, la crea, la guarda y la devuelve.

### Código

```python
class BaseDeDatos:
    _instancia = None  # Aquí guardaremos la única instancia

    @classmethod
    def get_instance(cls):
        if cls._instancia is None:
            # Si no existe, la creamos
            print("👤 Creando nueva instancia de BD...")
            cls._instancia = BaseDeDatos()
        return cls._instancia

    def __init__(self):
        print("Iniciando conexión...")

# Uso
print("1. Pidiendo instancia 1:")
bd1 = BaseDeDatos.get_instance()

print("\n2. Pidiendo instancia 2:")
bd2 = BaseDeDatos.get_instance()

print(f"\n¿Son el mismo objeto? {bd1 is bd2}")
```

### Salida

```text
1. Pidiendo instancia 1:
👤 Creando nueva instancia de BD...
Iniciando conexión...

2. Pidiendo instancia 2:

¿Son el mismo objeto? True
```

**Ventaja**: Sabes explícitamente cuándo estás pidiendo la instancia única (`get_instance()`) y evitas la "magia" oculta de `__new__`.

---

## 14. Comparativa: ¿Qué pasa si NO usamos Singleton?

Si usamos una clase normal, cada vez que la llamamos se crea un objeto **nuevo y diferente**.

```python
class BaseDeDatosNormal:
    def __init__(self):
        print("Iniciando conexión...")

# Uso
bd1 = BaseDeDatosNormal()
bd2 = BaseDeDatosNormal()

print(f"¿Son el mismo objeto? {bd1 is bd2}")
```

### Salida

```text
Iniciando conexión...
Iniciando conexión...
¿Son el mismo objeto? False
```

### Ventajas del Singleton

1.  **Recursos controlados**: Evita abrir 50 conexiones a la base de datos si solo necesitas una compartida.
2.  **Estado global consistente**: Si cambias una configuración en una parte del programa, el cambio se refleja en **todas** partes (porque es el mismo objeto).
3.  **Ahorro de memoria**: Solo existe 1 objeto en vez de miles.

---

## 15. Resumen

### Clases y objetos

- **Clase**: Plantilla para crear objetos.
- **Objeto**: Instancia de una clase.
- **Atributos**: Variables que definen el estado.
- **Métodos**: Funciones que definen el comportamiento.

### Herencia

- **Superclase**: Clase padre que aporta comportamiento.
- **Subclase**: Clase hija que hereda.
- **`__init__`**: Constructor que inicializa atributos.
- **`super()`**: Llama a la superclase correctamente.

### Métodos de clase y `cls`

- **`self`**: Referencia al objeto (instancia).
- **`cls`**: Referencia a la clase (molde).
- **`@classmethod`**: Método que trabaja con la clase en sí.

### Singleton

- **Patrón Singleton**: Garantiza una única instancia de una clase.
- **`_instancia`**: Variable de clase que almacena la **instancia única**.
- **`get_instance`**: Método explícito para obtener la instancia.

### Ventajas del Singleton

1.  **Recursos controlados**: Evita abrir conexiones innecesarias.
2.  **Estado global consistente**: Cambios en una parte afectan a todas.
3.  **Ahorro de memoria**: Solo existe 1 objeto en vez de miles.

### Comparativa

- **Singleton**: Una instancia única (útil para configuraciones globales).
- **Clase normal**: Cada vez que se llama se crea un nuevo objeto (útil para operaciones individuales).

---

## 16. Ejercicios prácticos

1.  **Herencia múltiple**: Crea una jerarquía de clases con herencia múltiple y verifica el MRO.
2.  **Método explícito**: Implementa el patrón Singleton en una clase de base de datos.
3.  **Verificación de atributos**: Crea una clase con atributos dinámicos y verifica si existen ciertos atributos en instancias.

---

## 17. Pasando datos al Constructor (Best Practices)

Cuando pasas datos a una clase (especialmente listas, diccionarios o configuraciones), es vital usar **Type Hints** (pistas de tipo) para que el editor te ayude y el código sea legible.

### Forma Recomendada

```python
from typing import List, Dict, Union

class ProcesadorDatos:
    # Especificamos QUÉ esperamos recibir
    def __init__(self, items: List[int], config: Dict[str, str], nombre: str):
        self.items = items
        self.config = config
        self.nombre = nombre

    def procesar(self):
        print(f"Procesando {len(self.items)} items para {self.nombre}...")

# Uso
mis_datos = [1, 2, 3, 4, 5]
mi_config = {"modo": "turbo", "idioma": "es"}

# El editor ahora sabe si estás pasando los tipos correctos
procesador = ProcesadorDatos(mis_datos, mi_config, "Servidor 1")
procesador.procesar()
```

### Ventajas

1.  **Autocompletado**: Tu editor (VS Code, PyCharm) sabrá que `self.items` es una lista y te sugerirá `.append()`, `.pop()`, etc.
2.  **Menos Errores**: Si intentas pasar un texto donde va una lista, las herramientas de análisis (mypy, pylance) te avisarán.
3.  **Documentación viva**: No necesitas comentar "esto es una lista", el código lo dice.
