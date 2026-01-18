# QStackedWidget: Gestión de Páginas y Navegación

El **QStackedWidget** es un contenedor de Qt que administra un conjunto de widgets (páginas) y **muestra solo uno a la vez**. Es una pieza clave para construir interfaces con navegación sin abrir múltiples ventanas.

Se utiliza comúnmente en:

- **Wizards** (Siguiente / Anterior)
- **Menús laterales** (cambio de vistas)
- **Dashboards** y **flujos de configuración**

---

## 1. Idea conceptual

Piense en un **mazo de cartas**:

- Todas las cartas existen al mismo tiempo
- Solo una es visible
- Cambiar de carta no destruye las demás

El QStackedWidget **no crea las páginas**: solo **las administra**.

---.

## 2. Funcionamiento básico

```python
from PySide6.QtWidgets import QStackedWidget, QLabel

stack = QStackedWidget()

pagina1 = QLabel("Soy la Página 1")
pagina2 = QLabel("¡Hola desde la Página 2!")

stack.addWidget(pagina1)  # índice 0
stack.addWidget(pagina2)  # índice 1

stack.setCurrentIndex(1)  # muestra la página 2
```

Puntos clave:

- Cada página es un `QWidget`
- Al agregarlas, Qt asigna **índices** automáticamente
- Solo una página es visible a la vez

---

## 3. Métodos principales

| Método                | Descripción                                    |
| --------------------- | ---------------------------------------------- |
| `addWidget(widget)`   | Añade una página al stack y devuelve su índice |
| `setCurrentIndex(i)`  | Muestra la página con índice `i`               |
| `setCurrentWidget(w)` | Muestra la página indicada por referencia      |
| `currentIndex()`      | Devuelve el índice actual                      |
| `count()`             | Devuelve el número total de páginas            |

---

## 4. Integración típica en una ventana

El `QStackedWidget` **no es una ventana**. Debe colocarse dentro de un layout o como widget central.

```python
self.stack = QStackedWidget()
main_layout.addWidget(self.stack)
```

---

## 5. Ejemplo práctico: navegación con botones

```python
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget,
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejemplo QStackedWidget")

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Barra de navegación
        nav = QHBoxLayout()
        btn1 = QPushButton("Página 1")
        btn2 = QPushButton("Página 2")
        nav.addWidget(btn1)
        nav.addWidget(btn2)
        main_layout.addLayout(nav)

        # Stack
        self.stack = QStackedWidget()

        page1 = QLabel("PÁGINA 1")
        page1.setStyleSheet("font-size: 18px; qproperty-alignment: AlignCenter;")

        page2 = QLabel("PÁGINA 2")
        page2.setStyleSheet("font-size: 18px; qproperty-alignment: AlignCenter;")

        self.stack.addWidget(page1)
        self.stack.addWidget(page2)
        # agregar el stack al layout principal
        main_layout.addWidget(self.stack)

        # Conexiones
        btn1.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn2.clicked.connect(lambda: self.stack.setCurrentIndex(1))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = VentanaPrincipal()
    w.show()
    sys.exit(app.exec())
```

---

## 6. Índices vs referencias

- **Índices** (`setCurrentIndex`):

  - Simples y rápidos
  - Adecuados para apps pequeñas

- **Referencias** (`setCurrentWidget`):

  - Más legibles
  - Recomendadas para apps grandes o dinámicas

Ejemplo:

```python
# 'page2' es la VARIABLE que contiene el objeto QLabel (o QWidget)
self.stack.setCurrentWidget(page2)
```

---

## 7. Comportamiento importante

- Cambiar de página **no destruye** el widget anterior
- El estado se conserva (texto, checks, variables)
- Todas las páginas existen simultáneamente en memoria

---

## 8. Errores comunes

- Intentar mostrar una página **no añadida** al stack
- Usar el stack como si fuera una ventana
- No asignar layouts a las páginas

---

## 9. Regla de oro

> **Diseña las páginas como widgets independientes y deja que el QStackedWidget solo se encargue de mostrar una a la vez.**

---

## 10. Resumen

- `QStackedWidget` es un contenedor de vistas
- Administra páginas intercambiables
- Ideal para navegación sin múltiples ventanas
- Controlado por índices o referencias

---

## 11. Truco Pro: Usando `QButtonGroup`

Si tus botones están en un `QButtonGroup`, puedes ahorrarte conectar cada botón manualmente.

La estrategia es: **Asignar a cada botón un ID igual al índice de la página que quieres mostrar.**

```python
from PySide6.QtWidgets import QButtonGroup

# ... dentro de tu clase ...

self.grupo_nav = QButtonGroup(self)

# Botón 1 -> ID 0 (Página 0)
self.grupo_nav.addButton(btn1, 0)

# Botón 2 -> ID 1 (Página 1)
self.grupo_nav.addButton(btn2, 1)

# ¡MAGIA! Una sola conexión para todos los botones
# idClicked envía el ID (0 o 1), y setCurrentIndex lo recibe directamente.
self.grupo_nav.idClicked.connect(self.stack.setCurrentIndex)
```

**Ventaja**: Si mañana añades 10 botones más, solo tienes que añadirlos al grupo con su ID. No necesitas crear 10 funciones de slot nuevas.

---

## 12. Código Completo (Ejecutable)

Aquí tienes un ejemplo listo para copiar y pegar que une todo: `QStackedWidget` + `QButtonGroup`.

```python
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QStackedWidget, QLabel, QButtonGroup)

class VentanaPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejemplo Pro: Stack + ButtonGroup")
        self.resize(400, 300)

        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        layout_principal = QVBoxLayout(central)

        # 1. Crear el Stack
        self.stack = QStackedWidget()

        # Crear 3 páginas
        pag1 = QLabel("Página de INICIO")
        pag1.setStyleSheet("background: #ffcccc; font-size: 20px; qproperty-alignment: AlignCenter;")

        pag2 = QLabel("Página de CONFIGURACIÓN")
        pag2.setStyleSheet("background: #ccffcc; font-size: 20px; qproperty-alignment: AlignCenter;")

        pag3 = QLabel("Página de AYUDA")
        pag3.setStyleSheet("background: #ccccff; font-size: 20px; qproperty-alignment: AlignCenter;")

        # Añadirlas al stack
        self.stack.addWidget(pag1) # Índex 0
        self.stack.addWidget(pag2) # Índex 1
        self.stack.addWidget(pag3) # Índex 2

        # 2. Crear los Botones y el Grupo
        layout_botones = QHBoxLayout()
        self.grupo = QButtonGroup(self)

        # Función auxiliar para crear botones
        def crear_boton(texto, id_pagina):
            btn = QPushButton(texto)
            btn.setCheckable(True) # Para que se quede marcado visualmente
            self.grupo.addButton(btn, id_pagina) # ASIGNAMOS EL ID AQUÍ (0, 1, 2...)
            layout_botones.addWidget(btn)

        crear_boton("Inicio", 0)
        crear_boton("Config", 1)
        crear_boton("Ayuda", 2)

        # Poner el primer botón como marcado por defecto
        self.grupo.button(0).setChecked(True)

        # 3. CONEXIÓN MÁGICA
        # Cuando un botón del grupo es clickeado, envía su ID --> stack cambia a ese índice
        self.grupo.idClicked.connect(self.stack.setCurrentIndex)

        # Añadir todo al layout
        layout_principal.addLayout(layout_botones)
        layout_principal.addWidget(self.stack)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPro()
    ventana.show()
    sys.exit(app.exec())
```

**Ventaja**: Si mañana añades 10 botones más, solo tienes que añadirlos al grupo con su ID. No necesitas crear 10 funciones de slot nuevas.
