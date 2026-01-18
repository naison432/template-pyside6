# Rutas y Paths en Python: ¿Relativo a qué?

Una de las confusiones más grandes en Python es: _¿Desde dónde busca Python mis archivos?_

La respuesta corta: **Depende de desde dónde ejecutas el comando `python`**.

---

## 1. El Problema del "Current Working Directory" (CWD)

Cuando escribes una ruta relativa como `"assets/imagen.png"`, Python la busca **relativa a la carpeta donde abriste la terminal**, NO relativa al archivo `.py` que estás programando.

### Ejemplo del desastre:

```text
proyecto/
├── main.py
└── data/
    ├── script.py
    └── archivo.txt
```

Si en `script.py` haces:

```python
open("archivo.txt")
```

1.  Si ejecutas desde `proyecto/data/`: `python script.py` -> **FUNCIONA** ✅
2.  Si ejecutas desde `proyecto/`: `python data/script.py` -> **FALLA** ❌ (Busca `proyecto/archivo.txt` y no existe).

---

## 2. La Solución Pro: Rutas Absolutas Dinámicas

Para que tu código funcione siempre, sin importar desde dónde lo ejecutes, debes construir la ruta basándote en la **ubicación del propio archivo `.py`**.

### La Variable Mágica `__file__`

Esta variable contiene la ruta completa del archivo actual.

### Usando `os.path` (Forma Clásica)

```python
import os

# 1. Obtener la carpeta donde vive este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Construir la ruta al archivo que quieres
ruta_archivo = os.path.join(BASE_DIR, "archivo.txt")

# 3. Usar esa ruta segura
open(ruta_archivo)
```

### Usando `pathlib` (Forma Moderna 🐍 recomendada)

Es más elegante y orientado a objetos.

```python
from pathlib import Path

# 1. Obtener carpeta actual
BASE_DIR = Path(__file__).parent

# 2. Construir ruta (usa el operador /)
ruta_archivo = BASE_DIR / "archivo.txt"

# 3. Abrir
with open(ruta_archivo) as f:
    print(f.read())
```

---

## 3. Rutas en Imports (`from ... import ...`)

Los `imports` funcionan diferente. No miran archivos, miran **Módulos y Paquetes**.

Python busca imports en una lista de carpetas llamada `sys.path`.
Por defecto, `sys.path` incluye:

1.  La carpeta del script que ejecutaste (el "Entry Point").
2.  Las librerías instaladas (`site-packages`).

### ¿Relativo al archivo o al proyecto?

- **Imports Absolutos** (Recomendado): Empiezan desde la raíz de tu proyecto (donde está el `main.py`).

  ```python
  from components.Sidebar import Sidebar  # Busca carpeta 'components' en la raíz
  ```

- **Imports Relativos** (Puntos): Relativos al archivo actual.
  ```python
  from .clase_vecina import MiClase  # En la misma carpeta
  from ..padre import OtraClase      # En la carpeta anterior
  ```
  _Nota: Los imports relativos suelen dar problemas si ejecutas el archivo directamente. Úsalos solo dentro de paquetes (librerías)._

---

## Resumen

| Tipo de Ruta        | ¿A quién es relativa?               | ¿Cuándo usar?                                          |
| :------------------ | :---------------------------------- | :----------------------------------------------------- |
| `"archivo.txt"`     | A la **Terminal** (CWD)             | Solo scripts rápidos de un uso.                        |
| `os.path.join(...)` | Al **Archivo `.py`**                | **SIEMPRE** para cargar recursos (imágenes, json, db). |
| `import x`          | Al **sys.path** (Raíz del proyecto) | Para importar código Python.                           |
