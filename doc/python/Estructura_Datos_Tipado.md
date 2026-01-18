# Estructurando Datos en Python: Tipado y Autocompletado

Si vienes de TypeScript, probablemente extrañes las `Interfaces` para definir la forma de tus objetos (props) y tener autocompletado.

Aunque Python es dinámico, tiene herramientas modernas que te dan **la misma experiencia de desarrollo (DX) que TypeScript**: autocompletado, validación de tipos y seguridad.

Aquí están las mejores prácticas, de la más simple a la más potente.

---

## 1. El Problema: Diccionarios "Sueltos"

Lo clásico en Python era usar diccionarios planos. Esto es rápido pero **peligroso** y **sin autocompletado**.

```python
# ❌ MAL: Sin autocompletado, propenso a errores de dedo
usuario = {
    "nombre": "Juan",
    "edad": 30,
    "activo": True
}

print(usuario["nombree"]) # KeyError en ejecución, el editor no te avisa antes.
```

---

## 2. La Solución Ligera: `TypedDict` (Estilo TypeScript Interface)

Si te gusta usar diccionarios pero quieres que el editor sepa qué claves deben de ir. Es lo más parecido a una `interface Usuario {}` de TS.

```python
from typing import TypedDict

# Definición de la "Interfaz"
class UsuarioProps(TypedDict):
    nombre: str
    edad: int
    activo: bool

# ✅ USO
datos: UsuarioProps = {
    "nombre": "Juan",
    "edad": 30,
    "activo": True
}

# El editor ahora sabe que 'datos' tiene 'nombre'.
# Si escribes datos["n..."] te autocompletará.
```

---

## 3. La Solución Estándar: `Dataclasses` (Recomendada)

Esta es la forma **Pythonica** moderna. En lugar de diccionarios, usas clases de datos. Es más limpio, usa menos memoria y permite acceso con punto (`.`).

**Ventajas:**

- Autocompletado perfecto (`objeto.propiedad`).
- Valores por defecto.
- Código más limpio que los diccionarios.

```python
from dataclasses import dataclass

@dataclass
class Usuario:
    nombre: str
    edad: int
    activo: bool = True # Valor por defecto

# ✅ USO
# Instanciación clara
u1 = Usuario(nombre="Ana", edad=25)

print(u1.nombre) # Autocompletado full
# u1.nombre = 10 # El linter te avisará que esto está mal (espera str)
```

**Desempaquetado fácil:**
Aunque es un objeto, puedes convertirlo a tupla o dict fácilmente si lo necesitas.

```python
from dataclasses import astuple, asdict

# Desempaquetar
nombre, edad, activo = astuple(u1)
```

---

## 4. `NamedTuple`: Inmutable y Rápido

Si tus datos **nunca van a cambiar** (son de solo lectura), usa `NamedTuple`. Es como una tupla normal pero con esteroides (nombres).

```python
from typing import NamedTuple

class Coordenada(NamedTuple):
    x: int
    y: int

punto = Coordenada(10, 20)

print(punto.x) # 10
# punto.x = 5 # ❌ Error: No se puede modificar
```

---

## Resumen: ¿Cuál usar?

| Necesidad                                   | TypeScript Equivalente | Python Recomendado                       |
| :------------------------------------------ | :--------------------- | :--------------------------------------- |
| Objeto simple mutable, Props de componentes | `interface` / `type`   | **`@dataclass`** (La mejor opción gral.) |
| Objeto JSON estricto                        | `interface`            | **`TypedDict`**                          |
| Datos inmutables / Coordenadas              | `readonly interface`   | **`NamedTuple`**                         |

### Ejemplo Pro (Dataclass para Props UI)

Imagina que estás haciendo un componente de UI y quieres pasarle configuración.

```python
@dataclass
class BotonConfig:
    texto: str
    color: str = "#ffffff"
    ancho: int = 100
    icono: str | None = None # Opcional (string o nada)

# Función que recibe los props
def crear_boton(config: BotonConfig):
    print(f"Creando botón '{config.texto}' de color {config.color}")

# Uso del editor:
# Al escribir BotonConfig( el editor te mostrará qué argumentos faltan.
mi_config = BotonConfig(texto="Guardar", width=200) # Error marcado si te equivocas de nombre
```
