# Manual de Arquitectura "Puppet Master"

Este documento define las directrices técnicas para el desarrollo y mantenimiento de la arquitectura implementada en la aplicación PySide6. El objetivo de este diseño es garantizar la escalabilidad, modularidad y mantenibilidad en sistemas con múltiples vistas (20+ módulos).

---

## 1. Filosofía de Diseño

Imagina tu aplicación como una obra de teatro de marionetas:

- **Las Marionetas (Páginas)**: Son tus módulos (`InventoryPage`, `AnalysisPage`). No saben quién está a su lado, solo saben actuar (mostrar datos, emitir señales).
- **Los Hilos (Señales y Slots)**: Son el mecanismo de comunicación.
- **El Titiritero (Puppet Master / `main.py`)**: Es el ÚNICO que ve todas las marionetas y decide quién habla con quién tirando de los hilos.

### Los 3 Mandamientos

1.  **Centralización (Registry)**: Nunca instancies páginas "al vuelo" en lugares aleatorios. Todo vive en `main.py` dentro de diccionarios centrales.
2.  **Configuración Declarativa**: Si quieres agregar una página, la agregas a una **LISTA**, no escribes código espagueti de inicialización.
3.  **Aislamiento Total**: Una página **NUNCA** debe importar a otra página. Si `PageA` necesita hablar con `PageB`, lo hace gritando al aire (Signal) y `main.py` redirige el mensaje.

---

## 2. Estructura de un Módulo

Para explicar la arquitectura, usaremos un ejemplo de un módulo de **Análisis de Datos** (`DataAnalysis`).

### Componentes de un Módulo

Un módulo completo suele tener dos partes:

1.  **Vista Principal**: Lo que se ve en el área central (`pages/DataAnalysis_page.py`).
2.  **Panel de Configuración** (Opcional): Sus ajustes (`pages/settings/ConfigData_page.py`).

---

## 3. Guía Paso a Paso: Implementando un Nuevo Módulo

Vamos a crear el módulo "DataAnalysis" desde cero.

### Paso 1: Crear la Vista (La Marioneta)

Crea el archivo `pages/DataAnalysis_page.py`.
**Nota importante**: Define tus señales (`Signal`) para todo lo que deba salir del módulo.

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal, Slot

class DataAnalysisPage(QWidget):
    # SEÑALES: La única forma de comunicarse con el exterior
    evt_solicitar_proceso = Signal(dict)  # Envía datos para procesar

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.btn_process = QPushButton("Analizar Datos")
        self.btn_process.clicked.connect(self._on_click)

        self.lbl_resultado = QLabel("Esperando análisis...")

        layout.addWidget(self.btn_process)
        layout.addWidget(self.lbl_resultado)

    def _on_click(self):
        # La página NO procesa, solo pide ayuda o avisa
        payload = {"dataset": "A", "umbral": 0.5}
        print("Módulo: Emitiendo solicitud de proceso...")
        self.evt_solicitar_proceso.emit(payload)

    @Slot(str)
    def recibir_resultado(self, resultado_texto: str):
        # Slot para recibir respuestas desde fuera
        self.lbl_resultado.setText(f"Resultado recibido: {resultado_texto}")
```

### Paso 2: Crear la Configuración (Opcional)

Crea `pages/settings/ConfigData_page.py`.

```python
from PySide6.QtWidgets import QWidget, QCheckBox, QVBoxLayout
from PySide6.QtCore import Signal, Slot

class ConfigDataPage(QWidget):
    evt_config_cambiada = Signal(bool)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.chk_mode_turbo = QCheckBox("Activar Modo Turbo")
        self.chk_mode_turbo.toggled.connect(self.evt_config_cambiada.emit)
        layout.addWidget(self.chk_mode_turbo)
```

### Paso 3: Registro Declarativo (`main.py`)

Ahora le decimos al **Puppet Master** que estas páginas existen. Edita `main.py`.

**A. Importar las clases**

```python
from pages.DataAnalysis_page import DataAnalysisPage
# Si tienes configuración
from pages.settings.ConfigData_page import ConfigDataPage
```

**B. Agregar al Menú Principal**
Busca la lista `MAIN_MENU_CONFIG` y agrega tu `MenuItemProp`. La `key` es crucial.

```python
MAIN_MENU_CONFIG = [
    # ... otros items ...
    MenuItemProp(
        key="analysis",          # ID ÚNICO
        text="Análisis de Datos",
        icon="chart_pie.svg",    # Asegúrate de que el icono exista en assets/icons
        page_class=DataAnalysisPage
    ),
]
```

**C. Agregar al Menú de Configuración (Si aplica)**
Busca `CONFIG_MENU_CONFIG`.

```python
CONFIG_MENU_CONFIG = [
    # ...
    {"key": "config_analysis", "text": "Conf. Análisis", "page_class": ConfigDataPage},
]
```

### Paso 4: Conectar los Hilos (`main.py`)

Si tu módulo necesita hablar con su configuración (o con otro módulo), debes conectarlos explícitamente en `main.py`.

Como usamos **Lazy Loading** (las páginas se crean solo cuando se visitan), la conexión debe hacerse en el momento de la creación.

Ve al método `_conectar_modulo_dinamico` en `main.py`:

```python
    def _conectar_modulo_dinamico(self, key: str, instance: QWidget):
        # ... conexiones existentes ...

        # NUEVA CONEXIÓN PARA ANÁLISIS
        if key == "analysis" and "config_analysis" in self.config_pages:
            config_page = self.config_pages["config_analysis"]

            # Conectar: Cuando el módulo pida proceso -> Config hace algo (ejemplo)
            # O mejor aún, conectar señales de config hacia el módulo

            # Ejemplo: Si cambia la config, avisar al módulo
            config_page.evt_config_cambiada.connect(instance.recibir_resultado)

            print("   [Conexión] DataAnalysis <-> ConfigAnalysis establecida.")
```

---

## 4. Reglas para Lógica de Negocio y Estado

### ¿Dónde guardo los datos?

- **Estado de UI efímero**: Dentro de la propia página (ej. texto de un input).
- **Datos persistentes globales**: En una clase de Servicio o Gestor (ej. `DatabaseManager`, `ProjectManager`) que ambos módulos importen, O pasados a través de señales.

### Ejemplo de Comunicación Compleja

Si `DataAnalysisPage` necesita un dato que solo tiene `InventoryPage`:

1.  `DataAnalysisPage` emite `evt_necesito_inventario = Signal()`.
2.  `InventoryPage` tiene un método público `obtener_inventario() -> list`.
3.  En `main.py`:

```python
# Cuidado con el orden de carga. Si Inventory no ha sido visitado, NO EXISTE.
# Por eso se recomienda usar Servicios compartidos para datos, no pedir datos directos a otras vistas.
```

**Mejor práctica**: Usa un **Servicio Singleton** para datos compartidos.
`services/DataStore.py` -> Importado por `DataAnalysisPage` y `InventoryPage`.

La arquitectura Puppet Master es para **Coordinación de Flujos**, no necesariamente para transporte masivo de datos.

---

## 5. Resumen de Buenas Prácticas

| ✅ DO (Hacer)                         | ❌ DON'T (No Hacer)                                   |
| :------------------------------------ | :---------------------------------------------------- |
| Definir menús en `MAIN_MENU_CONFIG`   | Agregar botones manuales `sidebar.add_button(...)`    |
| Usar `Signals` para salir del módulo  | Guardar referencias `self.parent.otra_pagina`         |
| Conectar todo en `main.py`            | Importar `DataAnalysisPage` dentro de `InventoryPage` |
| Usar IDs únicos (`key`) en minúsculas | Usar nombres de variables globales dispersas          |

---

## 6. Depuración

Si algo no funciona:

1.  **Revisa la consola**: `main.py` tiene prints (`🚀`, `🔄`, `⏳`) que te dicen qué se está cargando y cuándo.
2.  **Verifique las Keys**: Si la `key` en `MAIN_MENU_CONFIG` no coincide con lo que esperas en `_conectar_modulo_dinamico`, la conexión nunca ocurrirá.
3.  **Lazy Loading**: Recuerda que `_conectar_modulo_dinamico` solo se ejecuta la **primera vez** que visitas la página. Si cambias el código de conexión, reinicia la app.
