# Fundamentos de Python

Esta guía cubre los conceptos esenciales para empezar a programar en Python.

---

## 1. Variables y Tipos de Datos

Python es de **tipado dinámico**, no necesitas declarar el tipo de variable.

```python
nombre = "Ana"       # String (str)
edad = 25            # Entero (int)
altura = 1.65        # Flotante (float)
es_estudiante = True # Booleano (bool)
```

### Tipos de Datos Principales

- **`int`**: Números enteros (1, -5, 100).
- **`float`**: Números con decimales (3.14, -0.01).
- **`str`**: Texto ("Hola", 'Mundo').
- **`bool`**: Lógica (True, False).

---

## 2. Estructuras de Datos Básicas

### Listas (`list`)

Colección ordenada y modificable.

```python
frutas = ["manzana", "banana", "cereza"]
frutas.append("naranja")  # Añadir
print(frutas[0])          # Acceder (índice 0)
```

### Tuplas (`tuple`)

Colección ordenada e **inmutable** (no se puede cambiar).

```python
coordenadas = (10, 20)
```

### Diccionarios (`dict`)

Pares clave-valor.

```python
persona = {
    "nombre": "Juan",
    "edad": 30
}
print(persona["nombre"])
```

---

## 3. Control de Flujo

### Condicionales (`if`, `elif`, `else`)

```python
nota = 8
if nota >= 9:
    print("Excelente")
elif nota >= 5:
    print("Aprobado")
else:
    print("Reprobado")
```

### Bucles (`for`, `while`)

**Bucle `for`** (Iterar sobre secuencias):

Se utiliza para recorrer listas, tuplas, strings o rangos numéricos.

👉 **[Ver Guía Completa de Bucles, Iterables y Generadores](python/Bucle_For.md)**

**Bucle `while`** (Mientras sea verdad):

```python
contador = 0
while contador < 3:
    print("Hola")
    contador += 1
```

---

## 4. Funciones

Bloques de código reutilizables.

```python
def saludar(nombre):
    return f"Hola, {nombre}!"

mensaje = saludar("Carlos")
print(mensaje)
```

---

## 5. Entrada y Salida

```python
# Entrada
nombre = input("¿Cómo te llamas? ")

# Salida
print(f"Mucho gusto, {nombre}")
```

---

## 6. Tipado y Organización de Datos (Estilo TypeScript)

Si vienes de lenguajes con tipado estático como TypeScript o Java, Python ofrece herramientas modernas para estructurar tus datos con autocompletado y validación.

👉 **[Ver Guía de Estructuras, Dataclasses y TypedDict](python/Estructura_Datos_Tipado.md)**

---

## 7. Rutas y Archivos: ¿Por qué no encuentra mi archivo?

Si tienes problemas cargando imágenes o archivos porque "no los encuentra", el problema suele ser las **rutas relativas**.

👉 **[Ver Guía Maestra de Rutas y Paths](python/Rutas_y_Paths.md)**
