# Jerarquía de Clases de ui_main.py

Esta es la estructura visual y lógica de tu aplicación principal (`Interface`), desglosada por componentes y responsabilidad.

## 1. Estructura Visual (Árbol de Widgets)

La ventana se divide horizontalmente en dos grandes áreas: el Menú Lateral (**Sidebar**) y el Área de Trabajo (**Canvas**).

```text
Interface (QMainWindow)
└── QWidget (Widget Central - "mainContainer")
    └── QHBoxLayout (Layout Horizontal Principal)
        ├── 1. Sidebar (QFrame)
        │      ├── QVBoxLayout
        │      ├── MenuButton (QPushButton)
        │      ├── [Lista de SidebarButton...] (Fixed options)
        │      ├── SidebarScrollArea (QScrollArea)
        │      │   └── SidebarContentWidget
        │      │       └── [Lista de SidebarButton...] (Scroll options)
        │      └── ConfigButton (QPushButton)
        │
        └── 2. Canvas (QFrame)
               └── QStackedLayout (Gestionado por el Router)
                   ├── HomePage (QWidget)
                   ├── DashboardPage (QWidget)
                   └── [Otras páginas...]
```

---

## 2. Componentes Clave

### A. `Interface` (Main Window)

- **Rol:** Es el "Director de Orquesta".
- **Responsabilidad:**
  - Crea la ventana principal.
  - Inicializa el `Sidebar` y el `Canvas`.
  - Configura el `Router` para conectar ambos.
  - Define las rutas iniciales (`register_route`).

### B. `Sidebar`

- **Rol:** Panel de Navegación.
- **Responsabilidad:**
  - Muestra los botones.
  - Gestiona su propia animación (colapsar/expandir).
  - **No decide qué página mostrar**, solo le dice al `Router`: _"Oye, navega a 'home_view'"_.

### C. `Canvas`

- **Rol:** Pantalla / Lienzo.
- **Responsabilidad:**
  - Es un contenedor vacío (`QFrame`) al inicio.
  - Su único trabajo es ocupar el espacio derecho y **dejarse llenar** por el Router.

### D. `Router` (Lógica Invisible)

- **Rol:** El Cerebro de Navegación (Singleton).
- **Responsabilidad:**
  - Vive separado de la UI, pero tiene una referencia al `Canvas`.
  - Cuando el `Sidebar` pide navegar, el `Router`:
    1.  Busca la clase de la página (ej. `HomePage`).
    2.  Instancia la página.
    3.  La pone dentro del `Canvas` (usando `QStackedLayout`).

---

## 3. Flujo de Datos (Ejemplo: Click en "Home")

1.  **Usuario** hace clic en el botón "Home" del `Sidebar`.
2.  **`Sidebar`** ejecuta: `Router.instance().navigate("home_view")`.
3.  **`Router`** busca quién es "home_view" -> Encuentra `HomePage`.
4.  **`Router`** crea `new_page = HomePage()`.
5.  **`Router`** inserta `new_page` dentro del `Canvas`.
6.  **`Interface`** se actualiza mostrando la nueva página a la derecha.
