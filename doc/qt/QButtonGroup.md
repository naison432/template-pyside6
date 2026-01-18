# QButtonGroup: Agrupando Botones Lógicamente

`QButtonGroup` **NO es un widget visible**. Es una clase lógica que sirve para administrar un grupo de botones.

Se usa principalmente para:

1.  **Exclusividad Mutua**: Que solo un botón del grupo pueda estar activo a la vez (como los Radio Buttons).
2.  **Manejo Centralizado**: Conectar una sola señal para manejar los clics de MUCHOS botones.

### ¡Ojo! No es un Layout

`QButtonGroup` **NO organiza los botones en la pantalla**.

- Para decidir **dónde** se ven (arriba, abajo, izquierda), usas un **Layout** (`QVBoxLayout`, `QHBoxLayout`).
- Para decidir **cómo se comportan** (si son exclusivos o compartir señal), usas `QButtonGroup`.

## **¡Usas los dos juntos!**

## 1. Uso Básico: Exclusividad (Radio Buttons)

Por defecto, si agrupas botones que son "checkables", `QButtonGroup` asegura que solo uno esté marcado.

```python
from PySide6.QtWidgets import QButtonGroup, QPushButton, QWidget, QVBoxLayout

# Crear el grupo (es invisible)
grupo = QButtonGroup(self)

# Crear botones
b1 = QPushButton("Opción A")
b1.setCheckable(True)

b2 = QPushButton("Opción B")
b2.setCheckable(True)

# Añadirlos al grupo para que sean exclusivos
grupo.addButton(b1)
grupo.addButton(b2)

# NOTA: Si no especificas ID, Qt asigna uno negativo automáticamente.
# b1 tendrá ID -2, b2 ID -3, etc. NO empiezan en 0.
```

---

## 2. Uso Avanzado: ID y Señales Centralizadas

Imagina que tienes 10 botones. En lugar de conectar 10 señales (`b1.clicked`, `b2.clicked`...), conectas **una sola** del grupo.

### Asignar IDs

Puedes darle un número (ID) a cada botón para identificarlo.

```python
grupo.addButton(boton_guardar, 1)
grupo.addButton(boton_borrar, 2)
grupo.addButton(boton_cancelar, 3)
```

### Conectar la señal del grupo

`QButtonGroup` tiene la señal `buttonClicked` que te dice cuál botón se presionó.

```python
def manejar_grupo(boton_presionado):
    id = grupo.id(boton_presionado)
    print(f"Presionaste el botón {id}: {boton_presionado.text()}")

# Nota: En PySide6 a veces necesitas especificar el tipo
grupo.buttonClicked.connect(manejar_grupo)
```

---

## 3. Métodos Útiles

- `checkedButton()`: Devuelve el botón que está activo actualmente.
- `buttons()`: Devuelve una lista con todos los botones del grupo.
- `setExclusive(False)`: Si quieres usar el grupo solo para organizar señales, pero permitir selección múltiple (o ninguna).

---

## 4. Receta Común: Barra de Navegación (Sidebar)

El uso más potente es combinar `QButtonGroup` con `QStackedWidget` para crear menús laterales.

1.  Creas un `QStackedWidget` con tus páginas (página 0, página 1, etc.).
2.  Creas tus botones y los añades al grupo con **el mismo ID que el índice de su página**.
3.  Conectas la señal `idClicked` del grupo al slot `setCurrentIndex` del stack.

```python
# 1. El Stack
stack = QStackedWidget()
stack.addWidget(pagina_home)   # Índice 0
stack.addWidget(pagina_perfil) # Índice 133

# 2. Los Botones (Sidebar) - Asignamos ID manual que coincide con el stack
grupo = QButtonGroup(self)
grupo.addButton(btn_home, 0)   # ID 0
grupo.addButton(btn_perfil, 1) # ID 1

# 3. La Conexión Mágica
# Al hacer clic en btn_home, envía 0 -> el stack cambia al índice 0
grupo.idClicked.connect(stack.setCurrentIndex)
```

---

## 5. Ejemplo Completo: Sidebar Profesional

Aquí tienes un código listo para ejecutar con estilos y estructura profesional.

```python
import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QLabel,
    QButtonGroup,
)
from PySide6.QtCore import Qt


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Lateral con QButtonGroup")
        self.resize(800, 500)

        # --- ESTRUCTURA BASE ---
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        # Layout principal horizontal: [ Sidebar | Contenido ]
        layout_principal = QHBoxLayout(widget_central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # ---------------------------------------------------------
        # 1. EL SIDEBAR (Contenedor de botones)
        # ---------------------------------------------------------
        sidebar = QWidget()
        sidebar.setStyleSheet("background-color: #2c3e50;")
        layout_sidebar = QVBoxLayout(sidebar)
        layout_sidebar.setContentsMargins(0, 0, 0, 0)
        layout_sidebar.setSpacing(0)

        # Creación de los botones
        btn_home = QPushButton("Inicio")
        btn_dashboard = QPushButton("Dashboard")
        btn_perfil = QPushButton("Perfil Usuario")
        btn_ajustes = QPushButton("Configuración")

        # Estilo básico para que parezca un menú
        estilo_btn = """
            QPushButton {
                color: white; border: none; padding: 15px; text-align: left; font-size: 14px;
            }
            QPushButton:hover { background-color: #34495e; }
            QPushButton:checked {
                background-color: #34495e;
                border-left: 4px solid #3498db; /* Indicador visual de activo */
            }
        """

        # ---------------------------------------------------------
        # 2. EL GRUPO DE BOTONES (QButtonGroup)
        # ---------------------------------------------------------
        self.grupo_botones = QButtonGroup(self)
        self.grupo_botones.setExclusive(True)  # Solo un botón activo a la vez

        # Lista auxiliar para configurar botones en bucle
        # (Botón, ID) -> El ID debe coincidir con el índice del stack
        botones_config = [
            (btn_home, 0),
            (btn_dashboard, 1),
            (btn_perfil, 2),
            (btn_ajustes, 3),
        ]

        for boton, id_asignado in botones_config:
            boton.setStyleSheet(estilo_btn)
            boton.setCheckable(
                True
            )  # Necesario para que QButtonGroup gestione el estado
            layout_sidebar.addWidget(boton)

            # AQUÍ ASIGNAMOS EL ID MANUALMENTE
            self.grupo_botones.addButton(boton, id_asignado)

        layout_sidebar.addStretch()  # Empuja los botones hacia arriba

        # ---------------------------------------------------------
        # 3. EL STACK (Las páginas)
        # ---------------------------------------------------------
        self.stack = QStackedWidget()

        # Añadimos páginas en el orden exacto de los IDs de arriba
        self.stack.addWidget(
            self.crear_pagina_demo("Página INICIO", "#ecf0f1")
        )  # Índice 0
        self.stack.addWidget(
            self.crear_pagina_demo("Página DASHBOARD", "#bdc3c7")
        )  # Índice 1
        self.stack.addWidget(
            self.crear_pagina_demo("Página PERFIL", "#95a5a6")
        )  # Índice 2
        self.stack.addWidget(
            self.crear_pagina_demo("Página AJUSTES", "#7f8c8d")
        )  # Índice 3

        # ---------------------------------------------------------
        # 4. LA CONEXIÓN (Signal & Slot)
        # ---------------------------------------------------------
        # Cuando el grupo detecta un clic, emite el ID del botón (ej: 2).
        # El stack recibe ese entero y cambia a ese índice (ej: índice 2).
        self.grupo_botones.idClicked.connect(self.stack.setCurrentIndex)

        # Añadimos los widgets al layout principal
        layout_principal.addWidget(sidebar, 1)  # Sidebar ocupa el 15-20% aprox
        layout_principal.addWidget(self.stack, 4)  # Contenido ocupa el resto

        # Estado inicial: Simulamos clic en el botón 0 para arrancar
        btn_home.click()

    def crear_pagina_demo(self, texto, color):
        """Helper rápido para crear páginas visuales"""
        pagina = QWidget()
        pagina.setStyleSheet(f"background-color: {color};")
        lay = QVBoxLayout(pagina)
        lbl = QLabel(texto)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        lay.addWidget(lbl)
        return pagina


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
```
