# El Bucle For y la Iteración en Python

El bucle `for` en Python es más que un simple contador; es una herramienta para recorrer secuencias directamente.

---

## 1. Funcionamiento Básico

**Sintaxis:**

```python
for variable in secuencia:
    # Código a ejecutar por cada elemento
```

**Desglose de la Sintaxis:**

1.  **`variable`**: Es un **nombre temporal** que tú inventas.
    - En cada vuelta del bucle, tomará el valor del siguiente elemento.
    - Puedes ponerle cualquier nombre: `i`, `fruta`, `usuario`, `x`.
2.  **`secuencia`**: Es el **objeto que quieres recorrer**.
    - Tiene que ser un "Iterable" (algo que tenga muchos elementos).
    - **Tipos válidos**: `list`, `str`, `tuple`, `dict`, `range()`, etc.

> **Conceptos Clave:**
>
> - **Iterable**: El objeto que contiene los datos (ej. una lista, un texto). Es "capaz de ser recorrido".
> - **Iterador**: El "agente" interno que recorre el iterable uno a uno.
>
> _El bucle `for` toma un **iterable**, crea un **iterador** oculto, y le pide el siguiente valor en cada vuelta._

### Ejemplos Prácticos

**1. Usando `range(inicio, fin, paso)`**:
Genera una secuencia de números.

```python
# Simple (0 al 4)
for i in range(5):
    print(i)

# Avanzado (Del 2 al 10, de 2 en 2)
for i in range(2, 11, 2):
    print(i) # 2, 4, 6, 8, 10
```

**2. Recorriendo listas**:

```python
colores = ["Rojo", "Azul", "Verde"]
for color in colores:
    print(f"Me gusta el {color}")
```

**3. Usando `enumerate()` (Índice + Valor)**:
Útil cuando necesitas saber la posición del elemento.

```python
frutas = ["Pera", "Manzana"]
for indice, fruta in enumerate(frutas):
    print(f"Fruta #{indice}: {fruta}")
```

---

## 2. Funciones que retornan Iterables (no listas)

En Python moderno, muchas funciones devuelven **objetos iterables** en lugar de listas directas. Esto es por **eficiencia de memoria**: generan el valor solo cuando se les pide, en lugar de guardar millones de datos en RAM.

| Función       | Qué devuelve | Descripción            |
| :------------ | :----------- | :--------------------- |
| `range()`     | iterable     | Secuencia de números   |
| `enumerate()` | iterable     | Pares (índice, valor)  |
| `zip()`       | iterable     | Une dos listas         |
| `map()`       | iterable     | Aplica función a todos |
| `filter()`    | iterable     | Filtra elementos       |
| `reversed()`  | iterable     | Invierte el orden      |

**Ejemplo y Visualización:**

Si haces `print(range(6))`, no ves los números, ves el objeto. Para verlos todos (solo para debug), úsalos en un `list()`.

```python
frutas = ["pera", "manzana"]

# Convertimos el objeto iterable a lista para verlo
print(list(enumerate(frutas)))
# Salida: [(0, 'pera'), (1, 'manzana')]

print(list(range(6)))
# Salida: [0, 1, 2, 3, 4, 5]
```

> **Nota de Memoria**:
>
> - `range(1000)`: Memoria **Muy Baja** (Solo guarda la fórmula de inicio y fin).
> - `[0, 1, ... 999]`: Memoria **Alta** (Guarda los 1000 números en memoria).

---

## 3. Creando tus propios Iterables (Generadores)

¿Cómo creas una función que devuelva un iterable (como `range`) en vez de una lista gigante? Usando la palabra clave **`yield`**.

A estas funciones se les llama **Generadores**.

### Diferencia clave: `return` vs `yield`

- **`return`**: Entrega el valor, limpia la memoria y **termina** la función.
- **`yield`**: Entrega el valor, **pausa** la función, y guarda su estado para continuar después.

### Ejemplo: Fábrica de Números Pares

```python
def generar_pares(limite):
    num = 0
    while num < limite:
        yield num       # PAUSA aquí y entrega 'num'
        num += 2        # La próxima vez, continua desde aquí

# Uso
mis_pares = generar_pares(10) # No se ejecuta nada todavía... solo se crea el generador.

for par in mis_pares:
    print(par) # 0, 2, 4, 6, 8
```

### ¿Por qué usar esto? (Evaluación Perezosa / Lazy Evaluation)

Si quieres leer un archivo de 10GB línea por línea:

- Con **Lista**: Cargas los 10GB en memoria -> Crash! 💥

---

## 6. Patrones Comunes con Listas (A profundidad)

Cuando recorres una lista, generalmente quieres hacer una de tres cosas: **Transformar**, **Filtrar** o **Acumular**.

### A. Transformar (Mapping)

Crear una **nueva lista** modificando cada elemento de la original.

```python
numeros = [1, 2, 3, 4]
cuadrados = []

for n in numeros:
    cuadrados.append(n * n)

print(cuadrados) # [1, 4, 9, 16]
```

### B. Filtrar (Filtering)

Crear una nueva lista solo con los elementos que cumplan una condición.

```python
numeros = [10, 5, 20, 3, 8]
mayores_de_cinco = []

for n in numeros:
    if n > 5:
        mayores_de_cinco.append(n)

print(mayores_de_cinco) # [10, 20, 8]
```

### C. Acumular (Reduction)

Convertir toda la lista en **un solo valor** (suma, promedio, texto unido).

```python
precios = [100, 200, 50]
total = 0

for precio in precios:
    total += precio

print(total) # 350
```

---

## 7. List Comprehensions (Nivel Pro)

Python tiene una forma corta y elegante de hacer **Transformaciones** y **Filtros** en una sola línea.

**Sintaxis:**
`[expresion for variable in secuencia if condicion]`

### 1. Reemplazando Transformación (Map)

```python
# Versión Larga
cuadrados = []
for n in numeros:
    cuadrados.append(n * n)

# Versión Pro (Comprehension)
cuadrados = [n * n for n in numeros]
```

### 2. Reemplazando Filtro (Filter)

```python
# Versión Larga
pares = []
for n in numeros:
    if n % 2 == 0:
        pares.append(n)

# Versión Pro (Comprehension)
pares = [n for n in numeros if n % 2 == 0]
```

---

## 8. Iteración con Diccionarios

Los diccionarios (`dict`) tienen estructuras especiales (clave-valor), por lo que podemos recorrerlos de varias formas.

### A. Recorriendo solo las Claves (Default)

Si haces un `for` directo sobre el diccionario, Python te entrega las **claves**.

```python
usuario = {
    "nombre": "Ana",
    "edad": 30,
    "ciudad": "Madrid"
}

for k in usuario:
    print(k)
# Salida: nombre, edad, ciudad
```

### B. Recorriendo Clave y Valor (`.items()`)

Es la forma más común y útil. Usamos el **desempaquetado** de tuplas.

```python
for clave, valor in usuario.items():
    print(f"La clave {clave} tiene el valor {valor}")

# Salida:
# La clave nombre tiene el valor Ana
# La clave edad tiene el valor 30
# ...
```

### C. Recorriendo solo Valores (`.values()`)

Si no te importan las claves y solo quieres los datos.

```python
for valor in usuario.values():
    print(valor)
# Salida: Ana, 30, Madrid
```

---

## 9. Procesando Listas de Diccionarios

Esta es una de las estructuras de datos más comunes en el mundo real (ej. respuestas de APIs, bases de datos). Tienes una lista, y cada elemento dentro es un diccionario.

```python
usuarios = [
    {"id": 1, "nombre": "Ana", "rol": "Admin"},
    {"id": 2, "nombre": "Beto", "rol": "User"},
    {"id": 3, "nombre": "Carla", "rol": "User"}
]

for usuario in usuarios:
    # En cada vuelta, 'usuario' es un diccionario completo
    print(f"Hola {usuario['nombre']}, tu rol es {usuario['rol']}")

# Filtrando en una lista de diccionarios
admins = [u for u in usuarios if u['rol'] == "Admin"]
print(admins) # [{'id': 1, 'nombre': 'Ana', 'rol': 'Admin'}]
```

---

## 10. Iteración con Tuplas (y Listas de Tuplas)

Las tuplas son muy similares a las listas, pero **inmutables** (no puedes cambiarlas). Sin embargo, su superpoder en los bucles es el **desempaquetado (unpacking)**.

### A. Iterando una sola Tupla

Funciona exactamente igual que una lista.

```python
dimensiones = (1920, 1080)

for dim in dimensiones:
    print(dim)
# Salida: 1920, 1080
```

### B. Iterando una Lista de Tuplas (Desempaquetado)

Este es un patrón muy común cuando trabajas con coordenadas, puntos o datos pareados. En lugar de recibir la tupla entera, extraes sus valores directamente en el `for`.

**Ejemplo: Coordenadas (x, y)**

```python
puntos = [
    (10, 20),
    (5, 15),
    (8, 4)
]

# Método aburrido (sin desempaquetar)
for punto in puntos:
    print(f"X: {punto[0]}, Y: {punto[1]}")

# Método PRO (con desempaquetado)
# Python asigna automáticamente el primer valor a 'x' y el segundo a 'y'
for x, y in puntos:
    print(f"X: {x}, Y: {y}")
```

### C. ¿Qué pasa si la tupla tiene más datos?

El número de variables en el `for` debe coincidir con el tamaño de las tuplas.

```python
# Lista de tuplas: (Nombre, Edad, Puesto)
empleados = [
    ("Ana", 25, "Dev"),
    ("Luis", 30, "Diseño")
]

for nombre, edad, puesto in empleados:
    print(f"{nombre} trabaja de {puesto}")
```

### D. Ignorando valores (`_`)

Si la tupla tiene 3 valores pero solo te importa uno, usa `_` para decirle a Python "ignora esto".

```python
# Solo me interesa el puesto
for _, _, puesto in empleados:
    print(f"Puesto ocupado: {puesto}")
```
