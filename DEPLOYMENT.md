# 🚀 Guía de Despliegue en Render

Esta guía te llevará paso a paso para desplegar tu aplicación de predicción de demanda en Render.

## 📋 Pre-requisitos

Antes de comenzar, asegúrate de tener:

- ✅ Cuenta en [GitHub](https://github.com)
- ✅ Cuenta en [Render](https://render.com) (puedes usar tu cuenta de GitHub para registrarte)
- ✅ Tu código subido a un repositorio de GitHub
- ✅ Los archivos de configuración creados (`render.yaml`, `requirements.txt`, `.gitignore`)

## 🔧 Paso 1: Preparar el Repositorio en GitHub

### 1.1 Hacer Commit de los Cambios

```bash
git add .
git commit -m "Configuración para despliegue en Render"
git push origin develop
```

### 1.2 Verificar Archivos Importantes

Asegúrate de que estos archivos estén en tu repositorio:

- ✅ `requirements.txt` - Dependencias Python
- ✅ `render.yaml` - Configuración de Render
- ✅ `ferreteria_COSTOS_ventas_2024.csv` - Datos de ventas
- ✅ `model/rf_demand.pkl` - Modelo entrenado
- ✅ `model/encoders.pkl` - Encoders
- ✅ `model/metrics.json` - Métricas del modelo

## 🌐 Paso 2: Crear Web Service en Render

### 2.1 Acceder a Render

1. Ve a [https://render.com](https://render.com)
2. Haz clic en **"Sign In"** o **"Get Started"**
3. Inicia sesión con tu cuenta de GitHub

### 2.2 Crear Nuevo Web Service

1. En el Dashboard de Render, haz clic en **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio de GitHub:
   - Si es la primera vez, autoriza a Render para acceder a tus repositorios
   - Busca tu repositorio: `Proyecto_ML_Ferreteria`
   - Haz clic en **"Connect"**

### 2.3 Configurar el Web Service

Completa el formulario con la siguiente información:

**Información Básica:**
- **Name:** `ferreteria-costos-ml` (o el nombre que prefieras)
- **Region:** `Oregon (US West)` (o la más cercana a ti)
- **Branch:** `develop` (o `main` si usas esa rama)
- **Root Directory:** (dejar en blanco)

**Build & Deploy:**
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Plan:**
- Selecciona **"Free"** (plan gratuito)

### 2.4 Configurar Variables de Entorno

Antes de hacer clic en "Create Web Service", desplázate hasta la sección **"Environment Variables"** y agrega:

1. Haz clic en **"Add Environment Variable"**
2. Agrega las siguientes variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `tu-clave-secreta-super-segura-aqui-123456` |
| `ENVIRONMENT` | `production` |
| `PYTHON_VERSION` | `3.11.0` |

> **⚠️ IMPORTANTE:** Genera una SECRET_KEY segura. Puedes usar este comando en tu terminal local:
> ```bash
> python -c "import secrets; print(secrets.token_urlsafe(32))"
> ```

### 2.5 Crear el Servicio

1. Revisa que toda la configuración esté correcta
2. Haz clic en **"Create Web Service"**
3. Render comenzará a construir y desplegar tu aplicación

## ⏳ Paso 3: Esperar el Despliegue

### 3.1 Monitorear el Proceso

1. Verás los logs en tiempo real
2. El proceso puede tardar **5-10 minutos** la primera vez
3. Busca estos mensajes en los logs:

```
==> Building...
==> Installing dependencies...
==> Starting service...
INFO:     Uvicorn running on http://0.0.0.0:XXXX
INFO:     Application startup complete.
```

### 3.2 Posibles Errores Comunes

**Error: "Module not found"**
- Solución: Verifica que `requirements.txt` tenga todas las dependencias

**Error: "File not found: ferreteria_COSTOS_ventas_2024.csv"**
- Solución: Asegúrate de que el archivo CSV esté en el repositorio

**Error: "Port already in use"**
- Solución: Verifica que el comando de inicio use `$PORT` (variable de Render)

## ✅ Paso 4: Verificar el Despliegue

### 4.1 Acceder a tu Aplicación

1. Una vez completado el despliegue, verás un mensaje: **"Your service is live 🎉"**
2. Render te proporcionará una URL como: `https://ferreteria-costos-ml.onrender.com`
3. Haz clic en la URL para abrir tu aplicación

### 4.2 Probar la Aplicación

1. **Página de Login:**
   - Deberías ver la página de login
   - URL: `https://tu-app.onrender.com/static/login.html`

2. **Iniciar Sesión:**
   - Usuario: `admin`
   - Contraseña: `costos1234`

3. **Probar Funcionalidades:**
   - ✅ Dashboard de predicciones
   - ✅ Agregar productos a comparación
   - ✅ Ver gráficos (Comparación, Temporal, Variación, Top)
   - ✅ Registrar nueva venta
   - ✅ Reentrenar modelo

## 🔄 Paso 5: Actualizaciones Futuras

### 5.1 Despliegue Automático

Render está configurado para redesplegar automáticamente cuando hagas push a tu rama:

```bash
# Hacer cambios en tu código
git add .
git commit -m "Descripción de cambios"
git push origin develop
```

Render detectará el push y redesplegará automáticamente.

### 5.2 Ver Logs

Para ver los logs de tu aplicación:
1. Ve al Dashboard de Render
2. Selecciona tu servicio
3. Haz clic en la pestaña **"Logs"**

## ⚠️ Limitaciones del Plan Gratuito

Ten en cuenta estas limitaciones:

- 🛌 **Auto-sleep:** El servicio se "duerme" después de 15 minutos de inactividad
- ⏰ **Wake-up time:** Tarda ~30-50 segundos en "despertar" en la primera solicitud
- 💾 **RAM:** 512 MB de memoria RAM
- ⏱️ **Horas:** 750 horas de uso por mes
- 🔄 **Builds:** Tiempo de build limitado

## 🆘 Solución de Problemas

### Problema: La aplicación no carga

**Solución:**
1. Verifica los logs en Render
2. Asegúrate de que el servicio esté "Running" (no "Sleeping")
3. Espera 30-60 segundos si acabas de acceder

### Problema: Error 500 al hacer predicciones

**Solución:**
1. Verifica que los archivos del modelo estén en el repositorio
2. Revisa los logs para ver el error específico
3. Asegúrate de que `ferreteria_COSTOS_ventas_2024.csv` exista

### Problema: Login no funciona

**Solución:**
1. Verifica que la variable `SECRET_KEY` esté configurada
2. Limpia las cookies del navegador
3. Intenta en modo incógnito

## 📊 Monitoreo

### Ver Métricas del Servicio

En el Dashboard de Render puedes ver:
- 📈 CPU y memoria usada
- 🌐 Tráfico de red
- ⏱️ Tiempo de respuesta
- 📉 Errores y logs

## 🎉 ¡Listo!

Tu aplicación de predicción de demanda ahora está desplegada y accesible desde cualquier lugar del mundo.

**URL de tu aplicación:** `https://ferreteria-costos-ml.onrender.com`

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs en Render
2. Consulta la [documentación de Render](https://render.com/docs)
3. Verifica que todos los archivos necesarios estén en el repositorio

**¡Felicidades por tu despliegue! 🚀**
