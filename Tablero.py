import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Configuración de página
st.set_page_config(
    page_title="Mi Cuaderno Interactivo",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS avanzados: Fondo crema, barra amarilla cromo, botones cuadrados iluminados y stickers interactivos
st.markdown(
    """
    <style>
    /* Fondo general de la interfaz en color crema cálido */
    .stApp {
        background-color: #F7F4EA;
        color: #2D2A26;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Barra lateral con color amarillo cromo elegante */
    div[data-testid="stSidebar"] {
        background-color: #F4D03F !important;
        border-right: 2px solid #D4AC0D;
        padding-top: 10px;
    }
    
    /* Encabezado */
    .notebook-header {
        background: linear-gradient(135deg, #2C3E50 0%, #1A252F 100%);
        border-left: 8px solid #E74C3C;
        padding: 20px 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.08);
        color: white;
    }
    .notebook-header h1 {
        margin: 0;
        font-size: 1.7rem;
        font-weight: 800;
    }
    .notebook-header p {
        margin: 5px 0 0 0;
        color: #BDC3C7;
        font-size: 0.9rem;
    }

    /* Contenedor del Cuaderno */
    .notebook-container {
        background: #FFFFFF;
        border: 2px solid #D6D0C4;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }

    /* Estilo de los Stickers interactivos en la barra lateral derecha */
    .sticker-card {
        background: #FFFFFF;
        border: 2px solid #E0DCD0;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 8px;
        text-align: center;
        font-weight: 700;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.05);
        cursor: pointer;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Inicializar estados de la sesión para las secciones y la temática de stickers
if "seccion_activa" not in st.session_state:
  st.session_state.seccion_activa = "Temática"

if "sticker_tematica" not in st.session_state:
  st.session_state.sticker_tematica = "☀️ Playero (Solecitos)"

# Portada / Cabecera
st.markdown(
    """
    <div class="notebook-header">
        <h1>📖 Cuaderno Interactivo Personalizable</h1>
        <p>Elige tus herramientas, cambia de temática con los stickers y diseña tu espacio.</p>
    </div>
""",
    unsafe_allow_html=True,
)

# =========================================================================
# BARRA LATERAL: Botones cuadrados con iluminación/sombra y grises
# =========================================================================
with st.sidebar:
  st.markdown("### 🎛️ Panel de Control")
  st.markdown(
      "<p style='font-size:0.85rem; color:#5D4037;'>Selecciona un apartado:</p>",
      unsafe_allow_html=True,
  )

  # Creamos una botonera cuadrada distribuida en columnas para simular opciones independientes
  b_col1, b_col2 = st.columns(2)

  sections = ["Temática", "Colores", "Disposición", "Tamaño", "Renglones"]
  # Mapeo visual de los botones
  for i, sec in enumerate(sections):
    is_active = st.session_state.seccion_activa == sec
    # Estilo dinámico: si está activo se ilumina (fondo oscuro con sombra), si no, gris suave
    btn_label = f"📍 {sec}" if is_active else sec

    # Distribución en 2 columnas
    target_col = b_col1 if i % 2 == 0 else b_col2
    with target_col:
      if st.button(
          btn_label, key=f"sec_btn_{sec}", use_container_width=True
      ):
        st.session_state.seccion_activa = sec
        st.rerun()

  st.markdown("---")

  # =========================================================================
  # DESPLIEGUE DE SUBCATEGORÍAS SEGÚN EL BOTÓN SELECCIONADO
  # =========================================================================
  activa = st.session_state.seccion_activa

  if activa == "Temática":
    st.markdown("#### 🎨 Elige tu Sticker / Temática")
    opciones_tematica = [
        "☀️ Playero (Solecitos)",
        "💖 Enamorados (Corazones)",
        "🎵 Vinilos Vintage (Música)",
    ]
    st.session_state.sticker_tematica = st.radio(
        "Temática activa:", opciones_tematica, label_visibility="collapsed"
    )

  elif activa == "Colores":
    st.markdown("#### 🖍️ Paleta de Tinta")
    color_opcion = st.selectbox(
        "Elige color:",
        [
            "Blanco Tiza",
            "Azul Océano",
            "Rojo Pasión",
            "Verde Esmeralda",
            "Negro Carbón",
        ],
    )
    colores_map = {
        "Blanco Tiza": "#FFFFFF",
        "Azul Océano": "#2980B9",
        "Rojo Pasión": "#C0392B",
        "Verde Esmeralda": "#27AE60",
        "Negro Carbón": "#2C3E50",
    }
    stroke_color = colores_map[color_opcion]
    usar_libre = st.checkbox("Usar color personalizado")
    if usar_libre:
      stroke_color = st.color_picker("Elige color libre", "#2980B9")

  elif activa == "Disposición":
    st.markdown("#### 📐 Herramienta de Trazo")
    drawing_mode = st.selectbox(
        "Herramienta:", ("freedraw", "line", "rect", "circle", "transform")
    )
    stroke_width = st.slider("Grosor del trazo", 1, 35, 6)

  elif activa == "Tamaño":
    st.markdown("#### 📏 Dimensiones del Tablero")
    formato_hoja = st.selectbox(
        "Formato:",
        [
            "Apaisado Estándar (750x450)",
            "Cuadrado Proporcional (500x500)",
            "Amplio (900x500)",
        ],
    )
    if "750x450" in formato_hoja:
      canvas_width, canvas_height = 750, 450
    elif "500x500" in formato_hoja:
      canvas_width, canvas_height = 500, 500
    else:
      canvas_width, canvas_height = 900, 500

  elif activa == "Renglones":
    st.markdown("#### 📝 Patrón de Fondo")
    tipo_guia = st.selectbox(
        "Guías:",
        [
            "Renglones de Cuaderno",
            "Cuadrícula",
            "Puntos (Bullet)",
            "Sin Guías",
        ],
    )

# Valores predeterminados seguros por si el usuario cambia de sección
if "stroke_color" not in locals():
  stroke_color = "#2C3E50"
if "stroke_width" not in locals():
  stroke_width = 6
if "drawing_mode" not in locals():
  drawing_mode = "freedraw"
if "canvas_width" not in locals():
  canvas_width, canvas_height = 750, 450
if "tipo_guia" not in locals():
  tipo_guia = "Renglones de Cuaderno"

# =========================================================================
# CONFIGURACIÓN DE TEMÁTICAS SEGÚN EL STICKER SELECCIONADO
# =========================================================================
tematica_actual = st.session_state.sticker_tematica

if "Playero" in tematica_actual:
  default_bg = "#E0F7FA"  # Celeste suave estilo cielo/playa
  sticker_display = "☀️ Solecito Playero Activo"
elif "Enamorados" in tematica_actual:
  default_bg = "#FCE4EC"  # Rosado romántico
  sticker_display = "💖 Corazones San Valentín Activo"
else:  # Vinilos Vintage
  default_bg = "#EFEBE9"  # Papel envejecido / tonos café disco
  sticker_display = "🎵 Vinilos Retro & Discos Activo"


# Función generadora del fondo según la temática y guías
def crear_fondo_tematico(width, height, bg_hex, guia, tematica):
  bg_rgb = tuple(int(bg_hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
  img = Image.new("RGB", (width, height), bg_rgb)
  draw = ImageDraw.Draw(img)

  # Color de líneas y márgenes
  guia_color = (200, 195, 185)
  margen_color = (
      (231, 76, 60)
      if "Playero" in tematica
      else ((194, 24, 91) if "Enamorados" in tematica else (93, 64, 55))
  )

  # Margen de cuaderno
  draw.line([(55, 0), (55, height)], fill=margen_color, width=2)

  if guia == "Renglones de Cuaderno":
    step = 40
    for y in range(step, height, step):
      draw.line([(0, y), (width, y)], fill=guia_color, width=1)
  elif guia == "Cuadrícula":
    step = 35
    for x in range(0, width, step):
      draw.line([(x, 0), (x, height)], fill=guia_color, width=1)
    for y in range(0, height, step):
      draw.line([(0, y), (width, y)], fill=guia_color, width=1)
  elif guia == "Puntos (Bullet)":
    step = 30
    for x in range(30, width, step):
      for y in range(30, height, step):
        draw.ellipse([(x - 1, y - 1), (x + 1, y + 1)], fill=guia_color)

  return img


bg_image = crear_fondo_tematico(
    canvas_width, canvas_height, default_bg, tipo_guia, tematica_actual
)

# =========================================================================
# LAYOUT PRINCIPAL: Canvas + Stickers Interactivos a la Derecha
# =========================================================================
col_main, col_stickers = st.columns([3, 1], gap="medium")

with col_main:
  st.markdown('<div class="notebook-container">', unsafe_allow_html=True)

  canvas_result = st_canvas(
      fill_color="rgba(41, 128, 185, 0.15)",
      stroke_width=stroke_width,
      stroke_color=stroke_color,
      background_color=default_bg,
      background_image=bg_image,
      height=canvas_height,
      width=canvas_width,
      drawing_mode=drawing_mode,
      key=f"canvas_{canvas_width}_{canvas_height}_{tematica_actual}_{tipo_guia}",
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
          file_name="apunte_tematico.png",
          mime="image/png",
          use_container_width=True,
      )
    else:
      st.button("💾 Guardar Página", disabled=True, use_container_width=True)

  st.markdown("</div>", unsafe_allow_html=True)

with col_stickers:
  st.markdown("### 🏷️ Stickers Temáticos")
  st.markdown(
      "<p style='font-size:0.8rem; color:#5D4037;'>Selecciona un sticker para cambiar el ambiente del cuaderno:</p>",
      unsafe_allow_html=True,
  )

  # Botones interactivos que actúan como stickers reales para cambiar la temática de golpe
  if st.button("☀️ Sticker: Playero", use_container_width=True):
    st.session_state.sticker_tematica = "☀️ Playero (Solecitos)"
    st.rerun()

  if st.button("💖 Sticker: Enamorados", use_container_width=True):
    st.session_state.sticker_tematica = "💖 Enamorados (Corazones)"
    st.rerun()

  if st.button("🎵 Sticker: Vinilos", use_container_width=True):
    st.session_state.sticker_tematica = "🎵 Vinilos Vintage (Música)"
    st.rerun()

  st.markdown("---")
  st.markdown(f"**Estado actual:**\n{sticker_display}")
