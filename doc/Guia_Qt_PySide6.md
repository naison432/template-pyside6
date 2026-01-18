# Guía Completa de Qt para Python (PySide6)

Este documento sirve como referencia para los conceptos fundamentales de desarrollo de interfaces gráficas con **Qt** y **PySide6**.

---

## 1. Conceptos Fundamentales

### ¿Qué es Qt?

Qt es un framework multiplataforma para crear interfaces gráficas (GUI). **PySide6** es el binding oficial de Python para Qt 6.

### El Ciclo de Vida (`QApplication`)

Toda aplicación Qt necesita **una (y solo una)** instancia de `QApplication`. Es la que gestiona el bucle de eventos (clics, teclado, redibujado).

```python
from PySide6.QtWidgets import QApplication, QWidget
import sys

app = QApplication(sys.argv)  # 1. Crear la App

ventana = QWidget()           # 2. Crear ventana
ventana.show()                # 3. Mostrar ventana

sys.exit(app.exec())          # 4. Iniciar bucle de eventos
```

---

```python
class ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mi app")
        self.resize(700, 600)
        mainContainer = QWidget(self)
        self.setCentralWidget(mainContainer)
        # 3. layout_main = QVBoxLayout : organizador horizontal
        self.layout_main = QHBoxLayout(mainContainer)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windows = ventana()
    windows.show()
    sys.exit(app.exec())
```

---

## 2. Tipos de Ventanas

### `QWidget`

Es el bloque de construcción básico. Cualquier cosa que veas en pantalla es un widget. Si se usa como contenedor principal, es una ventana simple.

### `QMainWindow`

Es una ventana completa que ya viene preparada con:

- Barra de Menú
- Barra de Herramientas
- Barra de Estado
- Un widget central (`setCentralWidget`)

---

## 3. Signals & Slots (Señales y Slots)

Es el mecanismo de comunicación de Qt.

- **Signal (Señal)**: Es una notificación que se emite automáticamente cuando ocurre un evento. No ejecuta lógica por sí misma; solo informa que algo ha sucedido.
  - **Ejemplo**:
    - Un botón fue clickeado
    - Un valor cambió
    - Una acción terminó
- **Slot**: Es una función que responde a una señal.
  - Contiene la lógica que se ejecuta cuando la señal se emite.
  - Puede entenderse como **una función que maneja (handle) el evento notificado por la señal**. **(Equivalente al "Handler" en React)**.

### Relación Signal y Slot

Cuando una señal se emite, Qt llama automáticamente al slot conectado. **El slot solo se ejecuta si la señal se emite.**

**Ejemplo Conceptual:**

- **Signal**: "botón clickeado"
- **Slot**: `cerrar_ventana()`

**Flujo:**

1.  El usuario hace clic en el botón
2.  Qt emite la señal `clicked`
3.  El slot `cerrar_ventana()` se ejecuta

### Ejemplo de conexión

```python
boton = QPushButton("Haz clic")
boton.clicked.connect(mi_funcion)  # CONEXIÓN

def mi_funcion():
    print("¡Botón presionado!")
```

---

## 4. Layouts (Organización)

Los layouts organizan los widgets automáticamente, redimensionándolos cuando la ventana cambia de tamaño.

| Layout            | Descripción                                              |
| :---------------- | :------------------------------------------------------- |
| **`QVBoxLayout`** | Organiza widgets verticalmente (uno tras otro).          |
| **`QHBoxLayout`** | Organiza widgets horizontalmente (uno al lado del otro). |
| **`QGridLayout`** | Organiza widgets en una cuadrícula (filas y columnas).   |

---

## 5. Estilos (QSS - Qt Style Sheets)

Qt permite personalizar la apariencia usando una sintaxis muy similar a CSS de web.

```python
boton.setStyleSheet("""
    QPushButton {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
""")
```

### ✨ Estilos Dinámicos (Temas)

Para implementar temas (Dark/Light) y usar variables como `@primary_color`, necesitas un **Theme Manager**.

👉 **[Ver Guía de Estilos Dinámicos y ThemeManager](qt/Estilos_Dinamicos.md)**

---

## 6. Estructura recomendada de un Proyecto

Es buena práctica separar la lógica de la vista, usualmente creando una clase para la ventana principal.

---

## 7. Jerarquía de Clases Comunes

Entender la herencia es clave para saber qué métodos tiene cada widget.

```text
QObject (Base de todo, Signals & Slots)
└── QWidget (Elemento visual básico, tiene geometría)
    ├── QFrame (Widget con marco/borde)
    │   ├── [QLabel](qt/QLabel.md) (Texto e Imágenes)
    │   ├── QLCDNumber
    │   └── QAbstractScrollArea
    │       └── QTextEdit
    ├── QAbstractButton (Botones)
    │   ├── [QPushButton](qt/QPushButton.md)
    │   ├── QCheckBox
    │   └── QRadioButton
    ├── QMainWindow (Ventana principal compleja)
    └── QDialog (Ventana de diálogo)

### Clases Lógicas (No Visuales)
- [QButtonGroup](qt/QButtonGroup.md) (Agrupación de botones)
```

**Regla de oro**:

- Todo lo que tiene un `QWidget` (ej. `show()`, `resize()`), lo tiene un `QPushButton` (porque hereda de él).

---

## 8. ¿Por qué QMainWindow y luego QWidget?

Es una duda muy común: _"¿Por qué tengo que crear un `QWidget` extra dentro de `QMainWindow`?"_

### La razón técnica

`QMainWindow` **NO es un contenedor normal**. Tiene una estructura interna rígida diseñada para alojar barras:

```text
 _________________________________________
|           Barra de Menú                 |
|_________________________________________|
|           Barra de Herramientas         |
|_________________________________________|
|                                         |
|           (Zona Central)                |
| <--- AQUÍ VA TU WIDGET CENTRAL --->     |
|                                         |
|_________________________________________|
|           Barra de Estado               |
|_________________________________________|
```

1.  **El Problema**: `QMainWindow` no te deja usar `setLayout()` directamente. Si intentas `self.setLayout(layout)`, fallará o se verá mal, porque choca con las barras reservadas.
2.  **La Solución**: Creas un `QWidget` simple (un lienzo en blanco), le pones tu layout a ESE widget, y luego le dices a la ventana principal: _"Toma, este es tu widget central"_.

````python
class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Crear el contenedor central (Lienzo)
        contenedor = QWidget()

        # 2. Crear y asignar el layout al contenedor
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Botón"))
        contenedor.setLayout(layout)


---

## 9. Contenedores Específicos

Además del `QWidget` básico, Qt ofrece contenedores con superpoderes para organizar tu UI:

### A. Para Agrupar (`QGroupBox`)
Crea un recuadro con título alrededor de los widgets. Ideal para formularios.
```python
grupo = QGroupBox("Datos Personales")
layout_grupo = QVBoxLayout()
layout_grupo.addWidget(QLabel("Nombre:"))
layout_grupo.addWidget(QLineEdit())
grupo.setLayout(layout_grupo)
````

### B. Para Pestañas (`QTabWidget`)

Organiza el contenido en hojas/tabs independientes.

```python
tabs = QTabWidget()
tabs.addTab(pagina1_widget, "General")
tabs.addTab(pagina2_widget, "Configuración")
```

### C. Para Scroll (`QScrollArea`)

Si tu contenido es muy largo y no cabe en la ventana, esto le pone barras de desplazamiento.

```python
scroll = QScrollArea()
scroll.setWidget(widget_contenido_largo)
scroll.setWidgetResizable(True) # Importante para que se ajuste bien
```

### D. Para Páginas Ocultas (`QStackedWidget`)

Una pila de widgets donde solo se ve **uno a la vez**. Es la base para hacer sistemas de navegación.

👉 **[Ver Guía Detallada de QStackedWidget](qt/QStackedWidget.md)**

### E. Para Zonas Redimensionables (`QSplitter`)

Permite al usuario arrastrar una barra divisoria para ajustar el tamaño de dos áreas.

```python
splitter = QSplitter(Qt.Horizontal)
splitter.addWidget(widget_izq)
splitter.addWidget(widget_der)
```
