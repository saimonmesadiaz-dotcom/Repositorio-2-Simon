import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Configuración de página
st.set_page_config(
    page_title="Studio Gráfico | Cuaderno Interactivo",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS: Estética de Diseñador Gráfico, Crema y Amarillo Cromo con Sombras Sólidas
st.markdown(
    """
    <style>
    /* Fondo general de la interfaz en crema cálido */
    .stApp {
        background-color: #F7F4EA;
        color: #26221D;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Barra lateral en Amarillo Cromo */
    div[data-testid="stSidebar"] {
        background-color: #F4C430 !important;
        border-right: 3px solid #26221D;
        padding: 1rem 0.7rem;
    }
    div[data-testid="stSidebar"] * {
        color: #26221D !important;
    }

    /* Hero / Portada estilo portafolio interactivo */
    .designer-hero {
        background: linear-gradient(135deg, #26221D 0%, #110F0D 100%);
        color: #F7F4EA;
        padding: 24px 32px;
        border-radius: 16px;
        box-shadow: 6px 6px 0px #F4C430;
        margin-bottom: 24px;
        border: 2px solid #26221D;
    }
    .designer-hero h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 900;
        letter-spacing: -0.5px;
    }
    .designer-hero p {
        margin: 8px 0 0 0;
        color: #D4CDC2;
        font-size: 0.98rem;
    }

    /* Contenedor principal del cuaderno */
    .notebook-card {
        background: #FFFFFF;
        border: 3px solid #26221D;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 8px 8px 0px #26221D;
    }

    /* Tarjetas de Stickers Interactivos */
    .sticker-card {
        background: #FFFFFF;
        border: 2px solid #26221D;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        font-weight: 800;
        box-shadow: 4px 4px 0px #26221D;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-bottom: 10px;
    }
    .sticker-card:hover {
        background: #FFF9C4;
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px #26221D;
    }

    /* Botones de acción principales */
    .stButton > button {
        background: #26221D !important;
        color: #F7F4EA !important;
        border: 2px solid #26221D !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        box-shadow: 3px 3px 0px #888 !important;
        transition: all 0.1s ease !important;
    }
    .stButton > button:hover {
        background: #F4C430 !important;
        color: #26221D !important;
        transform: translate(-1px, -1px);
        box-shadow: 4px 4px 0px #26221D !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Inicializar estados de la sesión
if "active_section" not in st.session_state:
  st.session_state.active_section = "🎨 Colores"

if "current_theme" not in st.session_state:
  st.session_state.current_theme = "☀️ Playero"

if "selected_color" not in st.session_state:
  st.session_state.selected_color = "#26221D"

# Cabecera / Portada Estilo Diseñador
st.markdown(
    """
    <div class="designer-hero">
        <h1>✨ STUDIO GRÁFICO INTERACTIVO</h1>
        <p>Cuaderno de autor personalizable: experimenta con paletas, disposiciones, guías y stickers temáticos vivos.</p>
    </div>
""",
    unsafe_allow_html=True,
)

# =========================================================================
# BARRA LATERAL (Amarillo Cromo): Botones cuadrados modernos y modulares
# =========================================================================
with st.sidebar:
  st.markdown(
      "<h3 style='margin-bottom:12px; font-weight:900;'>🎛️ MÓDULOS DE"
      " DISEÑO</h3>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='font-size:0.85rem; font-weight:600;'>Selecciona un apartado"
      " para desplegar:</p>",
      unsafe_allow_html=True,
  )

  sections = [
      ("🎨 Colores", "Paleta y tintas"),
      ("📐 Disposición", "Herramientas y trazo"),
      ("📏 Tamaño", "Dimensiones del lienzo"),
      ("✨ Temática", "Estilos y stickers"),
      ("📝 Renglones", "Patrones y guías"),
  ]

  # Botones interactivos de sección con iluminación si están activos
  for sec_title, sec_desc in sections:
    is_active = st.session_state.active_section == sec_title
    # Estilo visual dinámico simulado con etiquetas
    label = f"▶️ {sec_title}" if is_active else f"▫️ {sec_title}"
    if st.button(label, key=f"sec_btn_{sec_title}", use_container_width=True):
      st.session_state.active_section = sec_title
      st.rerun()

  st.markdown("---")

  # =========================================================================
  # DESPLIEGUE DE SUBCATEGORÍAS SEGÚN EL BOTÓN SELECCIONADO
  # =========================================================================
  active = st.session_state.active_section
  st.markdown(
      f"<h4 style='font-weight:800; border-bottom: 2px solid"
      f" #26221D; padding-bottom:4px;'>Configurar: {active}</h4>",
      unsafe_allow_html=True,
  )

  if active == "🎨 Colores":
    st.markdown("<p style='font-size:0.9rem;'>Elige un color rápido:</p>", unsafe_allow_html=True)
    
    # Cuadraditos de colores tipo paleta de diseño
    c1, c2, c3 = st.columns(3)
    palette = {
        "Negro": "#26221D",
        "Azul Klein": "#002FA7",
        "Rojo Pop": "#FF3366",
        "Verde Menta": "#2ECC71",
        "Mostaza": "#D4AC0D",
        "Morado": "#8E44AD"
    }
    
    for name, hex_code in palette.items():
      if st.button(name, key=f"color_swatch_{hex_code}", use_container_width=True):
        st.session_state.selected_color = hex_code

    st.markdown("<br><b>➕ Color Personalizado (Degradado/Libre):</b>", unsafe_allow_html=True)
    st.session_state.selected_color = st.color_picker(
        "Selector exacto", st.session_state.selected_color
    )
    stroke_color = st.session_state.selected_color

  elif active == "📐 Disposición":
    drawing_mode = st.selectbox(
        "Herramienta:", ("freedraw", "line", "rect", "circle", "transform")
    )
    stroke_width = st.slider("Grosor del trazo", 1, 40, 6)

  elif active == "📏 Tamaño":
    formato_hoja = st.selectbox(
        "Formato de hoja:",
        [
            "Apaisado Pro (750x450)",
            "Cuadrado Cuaderno (550x550)",
            "Amplio Estudiantil (900x500)",
        ],
    )
    if "750x450" in formato_hoja:
      canvas_width, canvas_height = 750, 450
    elif "550x550" in formato_hoja:
      canvas_width, canvas_height = 550, 550
    else:
      canvas_width, canvas_height = 900, 500

  elif active == "✨ Temática":
    st.markdown("Elige tu sticker principal:")
    if st.button("☀️ Sticker: Playero", use_container_width=True):
      st.session_state.current_theme = "☀️ Playero"
    if st.button("💖 Sticker: Enamorados", use_container_width=True):
      st.session_state.current_theme = "💖 Enamorados"
    if st.button("🎵 Sticker: Vinilos", use_container_width=True):
      st.session_state.current_theme = "🎵 Vinilos"
    if st.button("😊 Sticker: Carita Feliz", use_container_width=True):
      st.session_state.current_theme = "😊 Carita Feliz"

  elif active == "📝 Renglones":
    tipo_guia = st.selectbox(
        "Patrón de fondo:",
        [
            "Renglones de Cuaderno",
            "Cuadrícula Geométrica",
            "Puntos Minimalistas",
            "Limpio sin guías",
        ],
    )

# Valores predeterminados por seguridad
if "stroke_color" not in locals():
  stroke_color = st.session_state.selected_color
if "drawing_mode" not in locals():
  drawing_mode = "freedraw"
if "stroke_width" not in locals():
  stroke_width = 6
if "canvas_width" not in locals():
  canvas_width, canvas_height = 750, 450
if "tipo_guia" not in locals():
  tipo_guia = "Renglones de Cuaderno"

# =========================================================================
# GESTIÓN DE TEMÁTICAS Y STICKERS VIVOS
# =========================================================================
current_theme = st.session_state.current_theme

if "Playero" in current_theme:
  default_bg = "#E0F7FA"
  theme_label = "☀️ Vibe Playero & Solecitos"
  emoji_dec = "🌴 ☀️ 🌊 🏖️"
elif "Enamorados" in current_theme:
  default_bg = "#FCE4EC"
  theme_label = "💖 Vibe Enamorados & Corazones"
  emoji_dec = "💖 💌 ✨ 🌹"
elif "Vinilos" in current_theme:
  default_bg = "#EFEBE9"
  theme_label = "🎵 Vibe Vintage & Discos"
  emoji_dec = "🎵 🎧 💿 🎷"
else:
  default_bg = "#FFFDE7"
  theme_label = "😊 Vibe Pop & Caritas Felices"
  emoji_dec = "😊 ⭐ 🚀 🎨"


# Función generadora de fondos de autor con Pillow
def crear_fondo_designer(width, height, bg_hex, guia, theme):
  bg_rgb = tuple(int(bg_hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
  img = Image.new("RGB", (width, height), bg_rgb)
  draw = ImageDraw.Draw(img)

  # Colores de margen y guías según temática
  if "Playero" in theme:
    margen_color = (0, 150, 136)
    guia_color = (178, 235, 242)
  elif "Enamorados" in theme:
    margen_color = (216, 27, 96)
    guia_color = (248, 187, 208)
  elif "Vinilos" in theme:
    margen_color = (121, 85, 72)
    guia_color = (215, 204, 200)
  else:
    margen_color = (253, 216, 53)
    guia_color = (255, 245, 157)

  # Margen de cuaderno elegante
  draw.line([(55, 0), (55, height)], fill=margen_color, width=3)

  if guia == "Renglones de Cuaderno":
    step = 42
    for y in range(step, height, step):
      draw.line([(0, y), (width, y)], fill=guia_color, width=1)
  elif guia == "Cuadrícula Geométrica":
    step = 35
    for x in range(0, width, step):
      draw.line([(x, 0), (x, height)], fill=guia_color, width=1)
    for y in range(0, height, step):
      draw.line([(0, y), (width, y)], fill=guia_color, width=1)
  elif guia == "Puntos Minimalistas":
    step = 30
    for x in range(30, width, step):
      for y in range(30, height, step):
        draw.ellipse([(x - 1, y - 1), (x + 1, y + 1)], fill=margen_color)

  return img


bg_image = crear_fondo_designer(
    canvas_width, canvas_height, default_bg, tipo_guia, current_theme
)

# =========================================================================
# LAYOUT PRINCIPAL: Canvas + Stickers Interactivos a la Mano Derecha
# =========================================================================
col_main, col_stickers = st.columns([3, 1], gap="medium")

with col_main:
  st.markdown('<div class="notebook-card">', unsafe_allow_html=True)

  canvas_result = st_canvas(
      fill_color="rgba(244, 196, 48, 0.2)",
      stroke_width=stroke_width,
      stroke_color=stroke_color,
      background_color=default_bg,
      background_image=bg_image,
      height=canvas_height,
      width=canvas_width,
      drawing_mode=drawing_mode,
      key=f"canvas_designer_{canvas_width}_{canvas_height}_{current_theme}_{tipo_guia}",
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
          label="💾 Guardar Creación",
          data=byte_im,
          file_name="diseno_cuaderno.png",
          mime="image/png",
          use_container_width=True,
      )
    else:
      st.button("💾 Guardar Creación", disabled=True, use_container_width=True)

  st.markdown("</div>", unsafe_allow_html=True)

with col_stickers:
  st.markdown(
      "<h3 style='font-weight:900;'>📌 Stickers Vivos</h3>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='font-size:0.85rem; color:#555;'>Toca un sticker para cambiar"
      " el mood al instante:</p>",
      unsafe_allow_html=True,
  )

  # Botones interactivos que actúan como stickers de cuaderno reales
  if st.button("☀️ Solecito Playero", use_container_width=True):
    st.session_state.current_theme = "☀️ Playero"
    st.rerun()

  if st.button("💖 Corazón Enamorado", use_container_width=True):
    st.session_state.current_theme = "💖 Enamorados"
    st.rerun()

  if st.button("🎵 Disco Vinilo Retro", use_container_width=True):
    st.session_state.current_theme = "🎵 Vinilos"
    st.rerun()

  if st.button("😊 Carita Feliz Pop", use_container_width=True):
    st.session_state.current_theme = "😊 Carita Feliz"
    st.rerun()

  st.markdown("---")
  st.markdown(
      f"""
    <div style="background: #FFFFFF; border: 2px solid #26221D; border-radius: 12px; padding: 14px; box-shadow: 4px 4px 0px #26221D; text-align: center;">
        <p style="font-size:0.75rem; font-weight:700; margin:0; color:#777;">ESTADO TEMÁTICO</p>
        <p style="font-size:0.95rem; font-weight:900; margin:5px 0 0 0; color:#26221D;">{theme_label}</p>
        <p style="font-size:1.4rem; margin:8px 0 0 0;">{emoji_dec}</p>
    </div>
    """,
      unsafe_allow_html=True,
  )
