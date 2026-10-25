import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Configuración de página
st.set_page_config(
    page_title="Mi Cuaderno Personalizable",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS: Estética de Cuaderno Escolar, Stickers y Tarjetas Visuales
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F3F0EA;
        color: #2C2A29;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Cabecera estilo portada de cuaderno */
    .notebook-header {
        background: linear-gradient(135deg, #2C3E50 0%, #1A252F 100%);
        border-left: 8px solid #E74C3C;
        padding: 22px 28px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        color: white;
    }
    .notebook-header h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .notebook-header p {
        margin: 5px 0 0 0;
        color: #BDC3C7;
        font-size: 0.95rem;
    }

    /* Tarjetas de opciones en barra lateral */
    .sidebar-card {
        background: #FFFFFF;
        border: 1px solid #E0DCD0;
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }

    /* Contenedor del Cuaderno / Pizarra */
    .notebook-container {
        background: #FFFFFF;
        border: 2px solid #D6D0C4;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }

    /* Estilo de los Stickers decorativos laterales */
    .sticker-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
        padding-top: 10px;
    }
    .sticker-badge {
        background: #FFF9E6;
        border: 2px dashed #F1C40F;
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 700;
        color: #7F6000;
        transform: rotate(-1.5deg);
        box-shadow: 2px 3px 8px rgba(0,0,0,0.06);
        text-align: center;
    }
    .sticker-badge.blue {
        background: #EBF5FB;
        border-color: #3498DB;
        color: #1B4F72;
        transform: rotate(1deg);
    }
    .sticker-badge.pink {
        background: #FADBD8;
        border-color: #E74C3C;
        color: #78281F;
        transform: rotate(-1deg);
    }
    .sticker-badge.green {
        background: #EAFAF1;
        border-color: #27AE60;
        color: #145A32;
        transform: rotate(1.5deg);
    }

    div[data-testid="stSidebar"] {
        background-color: #FAFAF7 !important;
        border-right: 1px solid #E5E0D5;
    }
    
    .stButton > button {
        background: #2C3E50 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: none !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Portada / Cabecera
st.markdown(
    """
    <div class="notebook-header">
        <h1>📖 Mi Cuaderno Personalizable</h1>
        <p>Tu espacio escolar y creativo a medida: ajusta el papel, los colores de tiza y decora tu entorno.</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Barra lateral de configuración personalizada
with st.sidebar:
  st.markdown("### 🛠️ Personalización")

  st.markdown("---")
  st.markdown("**1. Formato de Hoja (Dimensiones)**")
  formato_hoja = st.radio(
      "Selecciona el tamaño:",
      (
          "Apaisado Estándar (750x450)",
          "Cuadrado Proporcional (500x500)",
          "Formato Amplio (900x500)",
      ),
      label_visibility="collapsed",
  )

  if "750x450" in formato_hoja:
    canvas_width, canvas_height = 750, 450
  elif "500x500" in formato_hoja:
    canvas_width, canvas_height = 500, 500
  else:
    canvas_width, canvas_height = 900, 500

  st.markdown("---")
  st.markdown("**2. Estilo de Papel Escolar (Fondo)**")
  tipo_fondo = st.radio(
      "Fondo de cuaderno:",
      (
          "Crema Papel Escolar",
          "Verde Pizarra Clásica",
          "Papel Kraft Reciclado",
          "Blanco Limpio",
      ),
      label_visibility="collapsed",
  )

  if tipo_fondo == "Crema Papel Escolar":
    default_bg = "#FBF8EF"
    default_stroke = "#2C3E50"
  elif tipo_fondo == "Verde Pizarra Clásica":
    default_bg = "#1E3F20"
    default_stroke = "#FFFFFF"
  elif tipo_fondo == "Papel Kraft Reciclado":
    default_bg = "#EEDCC5"
    default_stroke = "#3D2314"
  else:
    default_bg = "#FFFFFF"
    default_stroke = "#111827"

  st.markdown("---")
  st.markdown("**3. Patrón de Guía / Líneas**")
  tipo_guia = st.radio(
      "Guías:", ("Renglones de Cuaderno", "Cuadrícula", "Puntos", "Ninguna"), label_visibility="collapsed"
  )

  st.markdown("---")
  st.markdown("**4. Herramienta y Tiza**")
  drawing_mode = st.selectbox(
      "Herramienta de trazo:", ("freedraw", "line", "rect", "circle", "transform")
  )
  stroke_width = st.slider("Grosor del lápiz / tiza", 1, 35, 6)

  # Paleta de colores estilo kit escolar
  st.markdown("Palette de Tinta / Tiza:")
  colores_opciones = {
      "Blanco Tiza": "#FFFFFF",
      "Azul Clásico": "#2980B9",
      "Rojo Nota": "#C0392B",
      "Verde Oscuro": "#196F3D",
      "Amarillo Marcador": "#F39C12",
      "Negro Carbón": "#2C3E50",
  }

  col_c1, col_c2, col_c3 = st.columns(3)
  selected_color = default_stroke
  # Selector rápido mediante colores
  color_elegido = st.selectbox("Elige color rápido:", list(colores_opciones.keys()))
  stroke_color = colores_opciones[color_elegido]

  # Opción extra de color personalizado con degradado/selector libre
  usar_personalizado = st.checkbox("Usar selector de color libre")
  if usar_personalizado:
    stroke_color = st.color_picker("Elige tu color exacto", default_stroke)


# Función generadora de fondos de cuaderno con Pillow
def crear_fondo_cuaderno(width, height, bg_hex, guia):
  bg_rgb = tuple(int(bg_hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
  img = Image.new("RGB", (width, height), bg_rgb)
  draw = ImageDraw.Draw(img)

  # Determinar color de guías según el fondo
  luminance = 0.299 * bg_rgb[0] + 0.587 * bg_rgb[1] + 0.114 * bg_rgb[2]
  if luminance < 100:  # Fondo oscuro (pizarra verde)
    guia_color = (255, 255, 255, 45)
    margen_color = (231, 76, 60, 150)
  else:  # Fondo claro (papel)
    guia_color = (200, 190, 175)
    margen_color = (231, 76, 60, 100)

  # Dibujar margen vertical estilo cuaderno escolar a la izquierda
  draw.line([(55, 0), (55, height)], fill=margen_color[:3], width=2)

  if guia == "Renglones de Cuaderno":
    step = 40
    for y in range(step, height, step):
      draw.line([(0, y), (width, y)], fill=guia_color[:3], width=1)

  elif guia == "Cuadrícula":
    step = 35
    for x in range(0, width, step):
      draw.line([(x, 0), (x, height)], fill=guia_color[:3], width=1)
    for y in range(0, height, step):
      draw.line([(0, y), (width, y)], fill=guia_color[:3], width=1)

  elif guia == "Puntos":
    step = 30
    for x in range(30, width, step):
      for y in range(30, height, step):
        draw.ellipse([(x - 1, y - 1), (x + 1, y + 1)], fill=guia_color[:3])

  return img


# Generar imagen de fondo
bg_image = crear_fondo_cuaderno(canvas_width, canvas_height, default_bg, tipo_guia)

# Layout principal: Dividido entre el tablero central y el panel de stickers a la derecha
col_main, col_stickers = st.columns([3, 1], gap="medium")

with col_main:
  st.markdown(
      '<div class="notebook-container">', unsafe_allow_html=True
  )

  canvas_result = st_canvas(
      fill_color="rgba(41, 128, 185, 0.15)",
      stroke_width=stroke_width,
      stroke_color=stroke_color,
      background_color=default_bg,
      background_image=bg_image,
      height=canvas_height,
      width=canvas_width,
      drawing_mode=drawing_mode,
      key=f"canvas_cuaderno_{canvas_width}_{canvas_height}_{tipo_fondo}_{tipo_guia}_{default_bg}",
  )

  st.markdown("<br>", unsafe_allow_html=True)
  b_col1, b_col2 = st.columns(2)

  with b_col1:
    if st.button("🗑️ Limpiar Hoja", use_container_width=True):
      st.rerun()

  with b_col2:
    has_image = False
    img_pil = None
    try:
      if canvas_result is not None and canvas_result.image_data is not None:
        img_data = canvas_result.image_data
        if np.any(img_data):
          img_pil = Image.fromarray(img_data.astype("uint8"), "RGBA")
          has_image = True
    except Exception:
      has_image = False

    if has_image and img_pil is not None:
      buf = io.BytesIO()
      img_pil.save(buf, format="PNG")
      byte_im = buf.getvalue()

      st.download_button(
          label="💾 Guardar Página",
          data=byte_im,
          file_name="mi_apunte_cuaderno.png",
          mime="image/png",
          use_container_width=True,
      )
    else:
      st.button("💾 Guardar Página", disabled=True, use_container_width=True)

  st.markdown("</div>", unsafe_allow_html=True)

with col_stickers:
  st.markdown("### 📌 Mis Stickers")
  st.markdown(
      """
    <div class="sticker-container">
        <div class="sticker-badge">⭐ ¡Excelente Apunte!</div>
        <div class="sticker-badge blue">📌 Recordatorio Clave</div>
        <div class="sticker-badge pink">💡 Idea Brillante</div>
        <div class="sticker-badge green">🚀 Focus Mode ON</div>
        <div class="sticker-badge">✨ Estilo Personal</div>
    </div>
    """,
      unsafe_allow_html=True,
  )
