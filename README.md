# 🏪 Sistema de Predicción de Demanda - Ferretería Costos SAC

Sistema web de predicción de demanda para productos de ferretería utilizando Machine Learning (Random Forest) con interfaz de usuario moderna y análisis estacional.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución del Proyecto](#ejecución-del-proyecto)
- [Uso del Sistema](#uso-del-sistema)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Solución de Problemas](#solución-de-problemas)

## ✨ Características

- **Dashboard Interactivo** con múltiples vistas de análisis
- **Predicción de Demanda** usando Random Forest optimizado
- **Análisis Estacional** con proyecciones mensuales
- **Gestión de Productos** con historial de ventas
- **Reentrenamiento del Modelo** en tiempo real
- **Autenticación de Usuarios** con JWT
- **Interfaz Moderna** con diseño dark mode

## 🔧 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:

### Software Requerido

1. **Python 3.8 o superior**
   - Descarga desde: https://www.python.org/downloads/
   - Durante la instalación, marca la opción "Add Python to PATH"

2. **Git** (opcional, para control de versiones)
   - Descarga desde: https://git-scm.com/downloads

3. **Editor de Código** (recomendado)
   - Visual Studio Code: https://code.visualstudio.com/

### Verificar Instalación

Abre una terminal (PowerShell o CMD) y ejecuta:

```bash
python --version
# Debería mostrar: Python 3.x.x

pip --version
# Debería mostrar: pip 2x.x.x
```

## 📦 Instalación

### Paso 1: Clonar o Descargar el Proyecto

Si tienes Git instalado:

```bash
git clone <url-del-repositorio>
cd Proyecto_ML
```

O simplemente descarga el proyecto y descomprímelo en una carpeta.

### Paso 2: Crear un Entorno Virtual

Es **altamente recomendado** usar un entorno virtual para evitar conflictos con otras instalaciones de Python.

**En Windows (PowerShell o CMD):**

```bash
# Navega a la carpeta del proyecto
cd "C:\Users\Carlos Ahumada Soles\OneDrive\Documentos\Proyecto_ML"

# Crea el entorno virtual
python -m venv venv

# Activa el entorno virtual
# En PowerShell:
.\venv\Scripts\Activate.ps1

# En CMD:
.\venv\Scripts\activate.bat
```

**En Linux/Mac:**

```bash
# Crea el entorno virtual
python3 -m venv venv

# Activa el entorno virtual
source venv/bin/activate
```

> **Nota:** Cuando el entorno virtual está activado, verás `(venv)` al inicio de tu línea de comandos.

### Paso 3: Instalar Dependencias

Con el entorno virtual activado, instala todas las dependencias necesarias:

```bash
pip install -r requirements.txt
```

Este comando instalará:
- FastAPI (framework web)
- Uvicorn (servidor ASGI)
- Pandas (manipulación de datos)
- Scikit-learn (machine learning)
- Joblib (serialización de modelos)
- Python-Jose (autenticación JWT)
- Passlib (hashing de contraseñas)
- Python-multipart (manejo de formularios)

### Paso 4: Verificar Archivos Necesarios

Asegúrate de que existan los siguientes archivos en tu proyecto:

```
Proyecto_ML/
├── ferreteria_COSTOS_ventas_2024.csv  ← Archivo de datos (IMPORTANTE)
├── model/
│   ├── rf_demand.pkl                   ← Modelo entrenado
│   ├── encoders.pkl                    ← Encoders categóricos
│   └── metrics.json                    ← Métricas del modelo
├── app/
│   ├── main.py
│   ├── router.py
│   ├── models.py
│   └── ...
└── static/
    ├── index.html
    ├── login.html
    └── ...
```

> **⚠️ IMPORTANTE:** Si no existe el archivo `ferreteria_COSTOS_ventas_2024.csv`, el sistema no funcionará correctamente.

## ⚙️ Configuración

### Entrenar el Modelo (Primera Vez)

Si no existen los archivos del modelo en la carpeta `model/`, debes entrenar el modelo primero:

```bash
python train_model_improved.py
```

Este proceso:
1. Lee los datos de `ferreteria_COSTOS_ventas_2024.csv`
2. Preprocesa y limpia los datos
3. Entrena el modelo Random Forest
4. Guarda el modelo y encoders en la carpeta `model/`
5. Calcula y guarda las métricas en `model/metrics.json`

**Tiempo estimado:** 1-3 minutos dependiendo del tamaño de los datos.

### Credenciales de Acceso

El sistema viene con un usuario predeterminado:

- **Usuario:** `admin`
- **Contraseña:** `costos1234`

> **Nota de Seguridad:** En producción, deberías cambiar estas credenciales y usar variables de entorno para la SECRET_KEY en `app/auth.py`.

## 🚀 Ejecución del Proyecto

### Iniciar el Servidor

Con el entorno virtual activado, ejecuta:

```bash
python -m uvicorn app.main:app --reload
```

**Parámetros:**
- `app.main:app` - Indica el módulo y la aplicación FastAPI
- `--reload` - Reinicia automáticamente el servidor cuando detecta cambios en el código (útil para desarrollo)

**Salida esperada:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Acceder a la Aplicación

1. Abre tu navegador web (Chrome, Firefox, Edge, etc.)
2. Navega a: **http://localhost:8000/static/login.html**
3. Ingresa las credenciales:
   - Usuario: `admin`
   - Contraseña: `costos1234`
4. Haz clic en "Iniciar Sesión"

### Detener el Servidor

Para detener el servidor, presiona `Ctrl + C` en la terminal donde está corriendo.

## 📱 Uso del Sistema

### 1. Dashboard de Predicciones

Después de iniciar sesión, verás el dashboard principal con 4 vistas:

#### 📊 Vista de Comparación
- Agrega productos para comparar su demanda estimada
- Selecciona producto, marca, categoría y precio
- Visualiza alertas y oportunidades de negocio

#### 📈 Proyección Estacional
- Proyecta la demanda de un producto a lo largo de varios meses
- Considera patrones estacionales específicos de ferretería
- Muestra métricas: promedio, pico y valle de demanda

#### 📉 Variación de Demanda
- Analiza el porcentaje de cambio mes a mes
- Identifica tendencias al alza o a la baja
- Útil para planificación de inventario

#### 🏆 Top Productos
- Genera un ranking de productos con mayor demanda estimada
- Usa precios promedio históricos automáticamente
- Configurable de 5 a 20 productos

### 2. Gestión de Productos

#### Registrar Nueva Venta
1. Haz clic en "Productos" en el menú lateral
2. Completa el formulario:
   - Fecha de venta
   - Producto (selecciona del dropdown)
   - Marca (se actualiza según el producto)
   - Categoría (se actualiza según el producto)
   - Cantidad
   - Precio unitario
3. Haz clic en "Guardar Registro"

#### Reentrenar el Modelo
1. Después de agregar nuevos registros de ventas
2. Haz clic en el botón "🔄 Reentrenar Modelo"
3. Espera a que se complete el proceso
4. Verás un mensaje: "Modelo reentrenado"

### 3. Configuración de Perfil

- **Cambiar Usuario:** Funcionalidad en desarrollo
- **Cambiar Contraseña:** Funcionalidad en desarrollo
- Visualiza las métricas actuales del modelo

## 📁 Estructura del Proyecto

```
Proyecto_ML/
│
├── app/                          # Código del backend
│   ├── __init__.py
│   ├── main.py                   # Punto de entrada FastAPI
│   ├── router.py                 # Rutas y endpoints
│   ├── models.py                 # Lógica del modelo ML
│   ├── schemas.py                # Schemas Pydantic
│   └── auth.py                   # Autenticación JWT
│
├── static/                       # Archivos frontend
│   ├── index.html                # Dashboard principal
│   ├── login.html                # Página de login
│   ├── css/
│   │   └── style.css             # Estilos
│   └── js/
│       ├── dashboard.js          # Lógica del dashboard
│       ├── login.js              # Lógica de login
│       └── chart.js              # Librería Chart.js
│
├── model/                        # Modelos entrenados
│   ├── rf_demand.pkl             # Modelo Random Forest
│   ├── encoders.pkl              # Encoders categóricos
│   └── metrics.json              # Métricas del modelo
│
├── ferreteria_COSTOS_ventas_2024.csv  # Datos de ventas
├── train_model_improved.py       # Script de entrenamiento
├── requirements.txt              # Dependencias Python
└── README.md                     # Este archivo
```

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido
- **Uvicorn** - Servidor ASGI de alto rendimiento
- **Pandas** - Análisis y manipulación de datos
- **Scikit-learn** - Machine Learning (Random Forest)
- **Joblib** - Serialización de modelos
- **Python-Jose** - Tokens JWT para autenticación
- **Passlib** - Hashing seguro de contraseñas

### Frontend
- **HTML5/CSS3** - Estructura y estilos
- **JavaScript (Vanilla)** - Lógica del cliente
- **Chart.js** - Visualización de gráficos
- **Google Fonts (Inter)** - Tipografía moderna

### Machine Learning
- **Random Forest Regressor** - Modelo principal
- **Label Encoding** - Para variables categóricas
- **Feature Engineering** - Características temporales y estadísticas

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"

**Problema:** No se encuentran los módulos instalados.

**Solución:**
```bash
# Asegúrate de que el entorno virtual esté activado
# Reinstala las dependencias
pip install -r requirements.txt
```

### Error: "Address already in use"

**Problema:** El puerto 8000 ya está siendo usado.

**Solución 1:** Detén el proceso que usa el puerto 8000

**Solución 2:** Usa un puerto diferente
```bash
python -m uvicorn app.main:app --reload --port 8001
```

### Error: "File not found: ferreteria_COSTOS_ventas_2024.csv"

**Problema:** Falta el archivo de datos.

**Solución:** Asegúrate de que el archivo CSV esté en la raíz del proyecto.

### Error: "cannot import name 'load_model'"

**Problema:** Versión desactualizada del código.

**Solución:** Asegúrate de tener la última versión del código en `app/models.py`.

### El modelo no predice correctamente

**Problema:** Modelo desactualizado o no entrenado.

**Solución:**
```bash
# Reentrena el modelo
python train_model_improved.py
```

### Error de autenticación

**Problema:** Token expirado o inválido.

**Solución:** Cierra sesión y vuelve a iniciar sesión.

### Los gráficos no se muestran

**Problema:** Chart.js no se cargó correctamente.

**Solución:**
1. Verifica tu conexión a internet (si usas CDN)
2. Recarga la página con Ctrl + F5
3. Revisa la consola del navegador (F12) para errores

## 📞 Soporte

Si encuentras problemas no listados aquí:

1. Revisa los logs del servidor en la terminal
2. Abre la consola del navegador (F12) para ver errores JavaScript
3. Verifica que todos los archivos estén en su lugar
4. Asegúrate de que el entorno virtual esté activado

## 📝 Notas Adicionales

### Desarrollo

Para desarrollo, el servidor se recarga automáticamente con `--reload`. Para producción, usa:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Backup de Datos

Es recomendable hacer backups periódicos de:
- `ferreteria_COSTOS_ventas_2024.csv`
- Carpeta `model/`

### Actualizaciones

Para actualizar las dependencias:

```bash
pip install --upgrade -r requirements.txt
```

---

**Desarrollado para Ferretería Costos SAC** 🔧

*Sistema de Predicción de Demanda con Machine Learning*
