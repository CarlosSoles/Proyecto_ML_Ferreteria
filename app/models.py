import joblib
import pandas as pd
from pathlib import Path

# Rutas al modelo entrenado y encoders
MODEL_PATH = Path(__file__).parent.parent / "model" / "rf_demand.pkl"
ENCODERS_PATH = Path(__file__).parent.parent / "model" / "encoders.pkl"

# Variables globales
model = None
encoders = None

def load_model():
    """Cargar o recargar el modelo y encoders desde el disco."""
    global model, encoders
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
    if ENCODERS_PATH.exists():
        encoders = joblib.load(ENCODERS_PATH)
    return model, encoders

# Carga inicial
load_model()

def safe_encode(encoder, value):
    """Codificar un valor categórico usando el encoder proporcionado.
    Si el valor no está presente, intenta valores de respaldo, luego usa la primera clase.
    """
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    # Valores de respaldo que se usaron durante el entrenamiento
    defaults = ['desconocida', 'no especificado', 'sin categoría', 'boleta', 'efectivo', 'nan']
    for d in defaults:
        if d in encoder.classes_:
            return encoder.transform([d])[0]
    # Último recurso: usar la primera clase
    return encoder.transform([encoder.classes_[0]])[0]

def preprocess(payload: dict) -> pd.DataFrame:
    """Convertir payload JSON entrante a un DataFrame que coincida con el esquema esperado del modelo.
    
    El modelo mejorado espera estas 14 características en orden:
    Características base (6):
    1-6. producto, tipo_producto, marca, categoria, metodo_pago, comprobante (categóricas, codificadas)
    
    Características numéricas (8):
    7. precio_unitario
    8. mes (1-12)
    9. trimestre (1-4)
    10. dia_semana (0-6)
    11. es_fin_semana (0 o 1)
    12. producto_popularidad
    13. producto_demanda_promedio
    14. precio_relativo
    """
    # Crear DataFrame desde el payload
    df = pd.DataFrame([payload])
    
    # Asegurar que precio_unitario sea numérico
    df["precio_unitario"] = pd.to_numeric(df["precio_unitario"], errors="coerce").fillna(0)
    
    # Agregar características temporales (usar fecha actual si no se proporciona)
    from datetime import datetime
    current_date = datetime.now()
    df['mes'] = current_date.month
    df['trimestre'] = (current_date.month - 1) // 3 + 1
    df['dia_semana'] = current_date.weekday()
    df['es_fin_semana'] = 1 if current_date.weekday() >= 5 else 0
    
    # Cargar dataset para características estadísticas
    df_opts = _load_data()

    
    # Agregar características estadísticas
    producto = payload.get('producto', 'Desconocido')
    categoria = payload.get('categoria', 'Sin categoría')
    
    # Popularidad del producto
    product_counts = df_opts.groupby('producto').size()
    df['producto_popularidad'] = product_counts.get(producto, 1)
    
    # Demanda promedio por producto
    product_avg_demand = df_opts.groupby('producto')['cantidad'].mean()
    df['producto_demanda_promedio'] = product_avg_demand.get(producto, 100.0)
    if pd.isna(df['producto_demanda_promedio'].iloc[0]):
        df['producto_demanda_promedio'] = 100.0
    
    # Precio promedio por categoría
    category_avg_price = df_opts.groupby('categoria')['precio_unitario'].mean()
    categoria_precio_promedio = category_avg_price.get(categoria, df['precio_unitario'].iloc[0])
    if pd.isna(categoria_precio_promedio) or categoria_precio_promedio == 0:
        categoria_precio_promedio = df['precio_unitario'].iloc[0]
    
    # Precio relativo al promedio de la categoría
    if categoria_precio_promedio > 0:
        df['precio_relativo'] = df['precio_unitario'] / categoria_precio_promedio
    else:
        df['precio_relativo'] = 1.0
    
    # Codificar columnas categóricas (normalizar texto primero - minúsculas y quitar espacios)
    for col, encoder in encoders.items():
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
            df[col] = df[col].apply(lambda x: safe_encode(encoder, x))
    
    # Retornar características en el orden exacto que espera el modelo
    feature_order = [
        "producto",
        "tipo_producto",
        "marca",
        "categoria",
        "metodo_pago",
        "comprobante",
        "precio_unitario",
        "mes",
        "trimestre",
        "dia_semana",
        "es_fin_semana",
        "producto_popularidad",
        "producto_demanda_promedio",
        "precio_relativo"
    ]
    
    return df[feature_order]


# Ruta al dataset usado para opciones de dropdowns
DATA_PATH = Path(__file__).parent.parent / "ferreteria_COSTOS_ventas_2024.csv"
_df_options = None

def _load_data():
    """Función auxiliar para cargar y preprocesar el dataframe de opciones."""
    global _df_options
    if _df_options is None:
        if not DATA_PATH.exists():
            # Retornar DF vacío con columnas esperadas si falta el archivo
            _df_options = pd.DataFrame(columns=['producto', 'tipo_producto', 'marca', 'categoria', 'cantidad', 'precio_unitario', 'metodo_pago'])
        else:
            _df_options = pd.read_csv(DATA_PATH)
            
        # Aplicar estrategia de relleno
        _df_options['marca'] = _df_options['marca'].fillna('Desconocida')
        _df_options['tipo_producto'] = _df_options['tipo_producto'].fillna('No especificado')
        _df_options['categoria'] = _df_options['categoria'].fillna('Sin categoría')
        
        # Asegurar que las columnas numéricas sean realmente numéricas
        # coerce errors convertirá strings no numéricos a NaN
        if 'cantidad' in _df_options.columns:
            _df_options['cantidad'] = pd.to_numeric(_df_options['cantidad'], errors='coerce').fillna(0)
        if 'precio_unitario' in _df_options.columns:
            _df_options['precio_unitario'] = pd.to_numeric(_df_options['precio_unitario'], errors='coerce').fillna(0)
            
    return _df_options

def get_options():
    """Retornar valores únicos para dropdowns y mapeos para selects dependientes."""
    df = _load_data()
    
    # Construir mapeos de producto -> marcas / categorias
    product_mappings = {}
    if 'producto' in df.columns:
        unique_products = sorted(df['producto'].astype(str).unique().tolist())
    else:
        unique_products = []
    
    for prod in unique_products:
        subset = df[df['producto'] == prod]
        categorias_prod = sorted(subset['categoria'].astype(str).unique().tolist())
        categorias_prod = [c for c in categorias_prod if c.lower() not in ['sin categoría', 'sin categoria']]
        # Calculate average price
        avg_price = 10.0
        if 'precio_unitario' in subset.columns and not subset.empty:
            avg_price = float(subset['precio_unitario'].mean())
            if pd.isna(avg_price):
                avg_price = 10.0
        
        product_mappings[prod] = {
            "marcas": sorted(subset['marca'].astype(str).unique().tolist()),
            "categorias": categorias_prod,
            "avg_price": avg_price
        }
    
    # Filter out unwanted values
    categorias = []
    if 'categoria' in df.columns:
        categorias = sorted(df['categoria'].astype(str).unique().tolist())
        categorias = [c for c in categorias if c.lower() not in ['sin categoría', 'sin categoria']]
    
    # Calculate average prices by category
    category_prices = {}
    for cat in categorias:
        subset = df[df['categoria'] == cat]
        avg_price = 10.0
        if 'precio_unitario' in subset.columns and not subset.empty:
            avg_price = float(subset['precio_unitario'].mean())
            if pd.isna(avg_price):
                avg_price = 10.0
        category_prices[cat] = avg_price
    
    return {
        "producto": unique_products,
        "tipo_producto": sorted(df['tipo_producto'].astype(str).unique().tolist()) if 'tipo_producto' in df.columns else [],
        "marca": sorted(df['marca'].astype(str).unique().tolist()) if 'marca' in df.columns else [],
        "categoria": categorias,
        "metodo_pago": sorted(df['metodo_pago'].dropna().unique().tolist()) if "metodo_pago" in df.columns else ["efectivo", "tarjeta", "transferencia"],
        "mappings": product_mappings,
        "category_prices": category_prices,
    }

