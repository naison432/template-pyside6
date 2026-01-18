# Arquitectura "Puppet Master"

Este documento describe la arquitectura de software implementada en la aplicación PySide6. El objetivo principal es garantizar la escalabilidad para más de 20 módulos industriales, manteniendo un bajo acoplamiento y una alta cohesión.

## 1. Principios Fundamentales

La arquitectura se rige por tres reglas obligatorias:

1.  **Centralización de Instancias (Registry Pattern)**: No existen variables sueltas para las páginas. Todas se gestionan en diccionarios centrales.
2.  **Configuración Declarativa**: La estructura del menú y las páginas se definen en listas constantes, no en código imperativo disperso.
3.  **Desacoplamiento Total (Signals & Slots)**: Las páginas de cálculo NO conocen a las páginas de configuración (y viceversa). Toda comunicación es indirecta.

---

## 2. Estructura del "Puppet Master" (`main.py`)

La clase `Ventana` actúa como el controlador maestro. Su responsabilidad es orquestar, no implementar lógica de negocio.

### A. Configuración Declarativa

Al inicio de `main.py`, se definen las estructuras de menú:

```python
MAIN_MENU_CONFIG = [
    MenuItemProp(key="vigas", text="Vigas", icon="beam.svg", page_class=VigasPage),
    # ...
]
```

### B. El Registro (The Registry)

En lugar de `self.page_vigas = VigasPage()`, usamos diccionarios dinámicos:

- `self.pages`: Almacena `{ 'clave_unica': instancia_pagina }`
- `self.config_pages`: Almacena `{ 'clave_unica': instancia_config }`

Esto permite iterar, buscar y gestionar módulos de forma genérica.

### C. Ciclo de Vida de Inicialización

El método `_inicializar_paginas()` recorre la configuración, instancia las clases (Lazy Instantiation es posible si se requiere en el futuro) y las registra tanto en el sistema interno como en la UI (`register_page`).

---

## 3. Comunicación Desacoplada

Para evitar el "Spaghetti Code" donde todos importan a todos, usamos estrictamente el sistema de Señales y Slots de Qt.

### Regla de Oro:

**"Un módulo nunca importa a otro módulo hermano."**

### El Patrón

1.  **Emisor (Ej. `VigasPage`)**: Define una `Signal`.

    ```python
    class VigasPage(QWidget):
        evt_solicitar_calculo = Signal(float)

        def pedir_calculo(self):
            self.evt_solicitar_calculo.emit(10.5)
    ```

2.  **Receptor (Ej. `ConfigVigasPage`)**: Define un `Slot`.

    ```python
    class ConfigVigasPage(QWidget):
        @Slot(float)
        def recibir_solicitud(self, valor):
            procesar(valor)
    ```

3.  **Orquestador (`main.py`)**: Es el ÚNICO que conoce a ambos y los conecta.
    ```python
    def _conectar_logica_negocio(self):
        emisora = self.pages["vigas"]
        receptora = self.config_pages["config_vigas"]

        emisora.evt_solicitar_calculo.connect(receptora.recibir_solicitud)
    ```

---

## 4. Flujo de Trabajo para Añadir un Nuevo Módulo

1.  **Crear la Vista**: Crear `pages/NuevoModulo_page.py`.
2.  **Crear la Configuración** (Opcional): Crear `pages/settings/ConfigNuevo_page.py`.
3.  **Registrar**: Añadir entradas en `MAIN_MENU_CONFIG` y/o `CONFIG_MENU_CONFIG` en `main.py`.
4.  **Conectar**: Si hay comunicación, añadir la conexión en `_conectar_logica_negocio()` en `main.py`.

No es necesario tocar `main_ui.py` ni la lógica de inicialización del Sidebar.
