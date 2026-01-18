# Estilos Dinámicos y Temas en PySide6

PySide6 no tiene un sistema de temas nativo "dark/light" automático. Para lograrlo profesionalmente, usamos un sistema de **Variables CSS (QSS)** y un **Gestor de Temas**.

---

## 1. La Estrategia: "Variables" en QSS

Como QSS (Qt Style Sheets) no soporta variables nativas (como `--color` en CSS), nosotros **simulamos variables** usando marcadores de posición en el archivo QSS y reemplazándolos con Python antes de cargar el estilo.

### El Archivo `template.qss`

En lugar de escribir colores fijos, escribimos "tags" que empiezan con `@`:

```css
/* template.qss */
QMainWindow {
  background-color: @main_bg; /* Variable */
  color: @text_main; /* Variable */
}
QPushButton:hover {
  background-color: @accent_color;
}
```

---

## 2. El Gestor (`ThemeManager`)

Es una clase **Singleton** (solo existe una instancia) que:

1.  Lee el `template.qss`.
2.  Tiene un diccionario de "Paletas" (Dark, Light, Blue...).
3.  Reemplaza las variables `@...` con los colores reales.
4.  Aplica el resultado con `app.setStyleSheet(...)`.

### Estructura Recomendada (`styles/themes.py`)

Usamos `Enum` para evitar errores de escritura ("magic strings").

```python
from enum import Enum

class ThemeType(str, Enum):
    DARK = "dark"
    LIGHT = "light"

THEME_PALETTES = {
    ThemeType.DARK: {
        "@main_bg": "#121212",
        "@text_main": "#ffffff",
        # ...
    },
    ThemeType.LIGHT: {
        "@main_bg": "#ffffff",
        "@text_main": "#000000",
        # ...
    }
}
```

---

## 3. Cómo Cambiar el Tema

Desde cualquier parte de tu app (ej. un botón o menú):

```python
from styles.themes import ThemeManager, ThemeType

# Aplicar tema Oscuro
ThemeManager.instance().apply_theme(ThemeType.DARK)

# Rotar al siguiente tema (toggle)
ThemeManager.instance().next_theme()
```

---

## 4. Iconos Dinámicos (El problema del SVG negro)

Los iconos SVG tienen un color fijo. Si tu icono es negro y cambias a Tema Oscuro, no se verá.

Para arreglarlo, `ThemeManager` tiene una utilidad `get_colored_icon` que:

1.  Carga el SVG.
2.  Crea una máscara en memoria.
3.  Lo "pinta" del color del texto actual (`@text_main`).

```python
# En tus componentes (ej. SidebarButton)
icon_path = "assets/icons/home.svg"

# ❌ Mal: Se ve del color original del archivo
# self.setIcon(QIcon(icon_path))

# ✅ Bien: Se pinta según el tema actual
custom_icon = ThemeManager.instance().get_colored_icon(icon_path)
self.setIcon(custom_icon)
```

Al cambiar el tema, debes llamar a `setIcon` de nuevo para que se repinte con el nuevo color.

---

## 5. Optimización (Caché y Pathlib)

El repintado de iconos puede ser costoso si se hace cada vez que se pide un icono. Por eso, el `ThemeManager` implementa un sistema de **Caché**:

1.  **Clave de Caché**: `(ruta_archivo, color)`.
2.  Si pides el mismo icono con el mismo color, devuelve la instancia ya creada en memoria.
3.  **Pathlib**: Se usa `pathlib` internamente para manejar rutas de forma robusta entre sistemas operativos (Windows/Linux/Mac).

Al cambiar de tema (`apply_theme`), la caché se limpia automáticamente (`self._icon_cache.clear()`) para asegurar que los nuevos iconos usen los colores correctos.
