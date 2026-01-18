# QLabel: Visualización de Texto e Imágenes

El `QLabel` (Etiqueta) es el widget más básico pero esencial de Qt. Su función principal es mostrar texto o imágenes al usuario. No es interactivo por defecto (no se puede editar).

---

## 1. Instanciación Básica

Crear una etiqueta es muy simple.

```python
from PySide6.QtWidgets import QLabel

# 1. Crear la etiqueta (puedes pasar el texto directamente)
etiqueta = QLabel("Hola Mundo")

# 2. Opcional: Establecer el padre (si estás dentro de una clase)
# etiqueta = QLabel("Hola Mundo", self)
```

---

## 2. Configuración Común

Métodos que usarás el 90% del tiempo.

### A. Cambiar el Texto Dinámicamente

```python
etiqueta.setText("Nuevo Texto")
texto_actual = etiqueta.text() # Obtener el texto
```

### B. Alineación (`setAlignment`)

Controla dónde aparece el texto dentro del recuadro de la etiqueta.

```python
from PySide6.QtCore import Qt

# Centro absoluto (Horizontal + Vertical)
etiqueta.setAlignment(Qt.AlignCenter)

# A la derecha y centrado verticalmente
etiqueta.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
```

### C. Ajuste de Texto (`setWordWrap`)

Si el texto es muy largo, esto hace que salte de línea automáticamente en lugar de cortarse.

```python
etiqueta.setWordWrap(True)
```

---

## 3. Estilizando con QSS (Hojas de Estilo)

`QLabel` soporta hojas de estilo muy potentes (similares a CSS web).

### Ejemplo Básico

```python
# Color de letra (color) y fondo (background-color)
etiqueta.setStyleSheet("color: white; background-color: blue;")
```

### Ejemplo Avanzado (Bordes y Fuentes)

Podemos darle un look moderno con bordes redondeados y fuentes grandes.

```python
estilo = """
QLabel {
    color: #333333;              /* Color de texto gris oscuro */
    background-color: #f0f0f0;   /* Fondo gris claro */
    font-size: 18px;             /* Tamaño de letra */
    font-weight: bold;           /* Negrita */
    font-family: 'Arial';        /* Tipo de letra */

    border: 2px solid #555555;   /* Borde sólido */
    border-radius: 10px;         /* Esquinas redondeadas */
    padding: 10px;               /* Espacio interior */
}
"""
etiqueta.setStyleSheet(estilo)
```

> **Nota:** El `padding` es crucial cuando usas bordes, para que el texto no toque las líneas.

---

## 4. Mostrando Imágenes

`QLabel` también sirve para mostrar imágenes usando `setPixmap`.

```python
from PySide6.QtGui import QPixmap

# Cargar imagen
imagen = QPixmap("ruta/a/mi_imagen.png")

# Asignar a la etiqueta
etiqueta.setPixmap(imagen)

# Opcional: Que la imagen se ajuste al tamaño de la etiqueta
etiqueta.setScaledContents(True)
```
