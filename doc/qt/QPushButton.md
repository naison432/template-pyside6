# QPushButton: Botones Interactivos

El `QPushButton` es el widget más común para recibir comandos del usuario. Se usa para ejecutar acciones, confirmar diálogos o navegar entre vistas.

---

## 1. Instanciación Básica

```python
from PySide6.QtWidgets import QPushButton

# 1. Crear el botón con texto
boton = QPushButton("Haz clic aquí")

# 2. Opcional: Crear el botón sin texto y ponerlo después
boton2 = QPushButton()
boton2.setText("Guardar cambios")
```

---

## 2. Eventos (Señales y Slots)

Lo más importante de un botón es saber cuándo el usuario lo presiona.

### La señal `clicked`

Es la señal principal. Se emite cuando el usuario presiona y suelta el botón.

```python
def guardar_datos():
    print("Datos guardados...")

boton.clicked.connect(guardar_datos)
```

### Conectando funciones con argumentos (`lambda`)

Por defecto, `clicked` no envía datos útiles (solo un booleano). Si quieres pasar tus propios argumentos a la función, usa `lambda`.

```python
def saludar(nombre):
    print(f"Hola {nombre}")

# ERROR COMÚN: Esto ejecuta la función al instante, NO al hacer clic
# boton.clicked.connect(saludar("Juan"))

# CORRECTO: Usamos lambda para crear una función anónima intermedia
boton.clicked.connect(lambda: saludar("Juan"))
```

- **`pressed`**: Se emite justo al bajar el botón (antes de soltar).
- **`released`**: Se emite al soltar el botón.
- **`toggled`**: Solo si el botón es "checkable" (interruptor). Se emite cuando cambia de encendido a apagado.

---

## 3. Configuración Común

### A. Iconos

Puedes añadir iconos fácilmente. Qt usará el estándar del sistema o tus propios archivos.

```python
from PySide6.QtGui import QIcon

boton.setIcon(QIcon("ruta/a/icono.png"))
```

### B. Botones tipo Interruptor (`setCheckable`)

Un botón puede comportarse como un interruptor (Toggle), quedándose presionado hasta que se le vuelva a dar clic.

```python
boton.setCheckable(True)

def estado_cambiado(checked):
    if checked:
        print("Botón ENCENDIDO")
    else:
        print("Botón APAGADO")

boton.toggled.connect(estado_cambiado)
```

### C. Deshabilitar (`setEnabled`)

Para evitar que el usuario haga clic (ej. si falta rellenar un formulario).

```python
boton.setEnabled(False) # Se ve gris y no responde
```

---

## 4. Estilos (QSS)

Los botones son muy personalizables. Puedes cambiar su aspecto normal, cuando el mouse pasa por encima (`:hover`) y cuando se presiona (`:pressed`).

```python
estilo = """
QPushButton {
    background-color: #2ecc71;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-size: 16px;
}

QPushButton:hover {
    background-color: #27ae60; /* Un poco más oscuro al pasar el mouse */
}

QPushButton:pressed {
    background-color: #1e8449; /* Aún más oscuro al presionar */
}

QPushButton:checked {
    background-color: #145a32; /* Color diferente cuando está "encendido" (toggle) */
    border: 2px solid #f1c40f; /* Borde para resaltar */
}
"""

boton.setStyleSheet(estilo)
```
