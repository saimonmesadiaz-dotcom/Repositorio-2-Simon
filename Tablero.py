import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Configuración de página
st.set_page_config(
    page_title="Studio Gráfico | Cuaderno de Arte",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS: Estética Neo-Artesanal, Tonos Crema, Barra Amarillo Cromo Ancha y Tarjetas de Autor
st.markdown(
    """
    <style>
    /* Fondo general de toda la aplicación en crema cálido y acogedor */
    .stApp {
        background-color: #F7F4EA;
        color: #2D2A26;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Barra lateral muy amplia en Amarillo Cromo elegante */
    div[data-testid="stSidebar"] {
        background-color: #F4C430 !important;
        border-right: 3px solid #2D2A26;
        padding: 1.5rem 1rem;
        min-width: 320px !important;
    }
    div[data-testid="stSidebar"] * {
        color: #2D2A26 !important;
    }

    /* Portada / Header principal del estudio de arte */
    .art-hero {
        background: #FFFDF7;
        color: #2D2A26;
        padding: 24px 32px;
        border-radius: 16px;
        box-shadow: 6px 6px 0px #2D2A26;
        margin-bottom: 24px;
        border: 3px solid #2D2A26;
    }
    .art-hero h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: -0.5px;
    }
    .art-hero p {
        margin: 8px 0 0 0;
        color: #6E685F;
        font-size: 1rem;
    }

    /* Contenedor del Canvas de Dibujo */
    .canvas-card {
        background: #FFFDF7;
        border: 3px solid #2D2A26;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 8px 8px 0px #2D2A26;
    }

    /* Botones de acción principales */
    .stButton > button {
        background: #2D2A26 !important;
        color: #F7F4EA !important;
        border: 2px solid #2D2A26 !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        box-shadow: 3px 3px 0px #888 !important;
        transition: all 0.1s ease !important;
    }
    .stButton > button:hover {
        background: #F4C430 !important;
        color: #2D2A26 !important;
        transform: translate(-1px, -1px);
        box-shadow: 5px 5px 0px #2D2A26 !important;
    }

    /* Tarjetas de Stickers Interactivos */
    .sticker-box {
        background: #FFFDF7;
        border: 2px solid #2D2A26;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        box-shadow: 4px 4px 0px #2D2A26;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Inicializar estados de la sesión
if "active_section" not in st.session_state:
  st.session_state.active_section = "🎨 Paleta de Pintor"

if "current_theme" not in st.session_state:
  st.session_state.current_theme = "☀️ Playero"

if "selected_color" not in st.session_state:
  st.session_state.selected_color = "#2D2A26"

# Header / Portada de Diseñador
st.markdown(
    """
    <div class="art-hero">
        <h1>🎨 STUDIO ARTE INTERACTIVO</h1>
        <p>Espacio de creación libre de autor: mezcla tintas en tu paleta, selecciona texturas de papel y activa mundos animados.</p>
    </div>
""",
    unsafe_allow_html=True,
)

# =========================================================================
# BARRA LATERAL (AMARILLO CROMO Y AMPLIA) - Módulos Interactivos
# =========================================================================
with st.sidebar:
  st.markdown(
      "<h2 style='font-weight:900; margin-bottom:15px;'>🖌️ ESTUDIO CREATIVO</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='font-size:0.9rem; font-weight:700;'>Selecciona un módulo de"
      " trabajo:</p>",
      unsafe_allow_html=True,
  )

  sections = [
      ("🎨 Paleta de Pintor", "Óleos y tintas"),
      ("📐 Disposición", "Herramientas de trazo"),
      ("📏 Tamaño", "Lienzo y formato"),
      ("✨ Temática & Emojis", "Mundos animados"),
      ("📝 Renglones", "Guías de papel"),
  ]

  for sec_title, sec_desc in sections:
    is_active = st.session_state.active_section == sec_title
    label = f"✨ [{sec_title}]" if is_active else f"🔹 {sec_title}"
    if st.button(label, key=f"btn_sec_{sec_title}", use_container_width=True):
      st.session_state.active_section = sec_title
      st.rerun()

  st.markdown("---")

  # DESPLIEGUE SEGÚN LA SECCIÓN SELECCIONADA
  active = st.session_state.active_section
  st.markdown(
      f"<h3 style='font-weight:800; border-bottom: 2px solid"
      f" #2D2A26; padding-bottom:4px;'>⚙️ {active}</h3>",
      unsafe_allow_html=True,
  )

  if active == "🎨 Paleta de Pintor":
    st.markdown(
        "<p style='font-size:0.85rem; font-weight:700;'>Toca una gota de óleos"
        " de la paleta artística:</p>",
        unsafe_allow_html=True,
    )

    # Simulación visual de una paleta de pintura con botones distribuidos
    c1, c2, c3 = st.columns(3)
    painter_palette = {
        "Azul Ultramar": "#0047AB",
        "Rojo Carmín": "#960018",
        "Verde Olivo": "#556B2F",
        "Amarillo Ocre": "#CC7722",
        "Rosa Pastel": "#FFB6C1",
        "Negro Gráfito": "#2D2A26",
    }

    for name, hex_val in painter_palette.items():
      if st.button(
          name, key=f"paint_{hex_val}", use_container_width=True
      ):
        st.session_state.selected_color = hex_val

    st.markdown("<br><b>➕ Mezclador Personalizado (Libre):</b>", unsafe_allow_html=True)
    st.session_state.selected_color = st.color_picker(
        "Añadir tono exacto", st.session_state.selected_color
    )
    stroke_color = st.session_state.selected_color

  elif active == "📐 Disposición":
    drawing_mode = st.selectbox(
        "Herramienta de dibujo:",
        ("freedraw", "line", "rect", "circle", "transform"),
    )
    stroke_width = st.slider("Grosor del pincel", 1, 40, 6)

  elif active == "📏 Tamaño":
    formato_hoja = st.selectbox(
        "Formato del lienzo:",
        [
            "Apaisado Profesional (750x450)",
            "Cuadrado Estudio (550x550)",
            "Panorámico Ancho (900x500)",
        ],
    )
    if "750x450" in formato_hoja:
      canvas_width, canvas_height = 750, 450
    elif "550x550" in formato_hoja:
      canvas_width, canvas_height = 550, 550
    else:
      canvas_width, canvas_height = 900, 500

  elif active == "✨ Temática & Emojis":
    st.markdown(
        "Elige un sticker animado para poblar el fondo del cuaderno:"
    )
    if st.button("☀️ Sticker: Playero (Soles/Palmeras)", use_container_width=True):
      st.session_state.current_theme = "☀️ Playero"
    if st.button("💖 Sticker: Enamorados (Corazones)", use_container_width=True):
      st.session_state.current_theme = "💖 Enamorados"
    if st.button("🎵 Sticker: Vinilos (Discos/Retro)", use_container_width=True):
      st.session_state.current_theme = "🎵 Vinilos"
    if st.button("😊 Sticker: Caritas Felices (Pop)", use_container_width=True):
      st.session_state.current_theme = "😊 Caritas Felices"

  elif active == "📝 Renglones":
    tipo_guia = st.selectbox(
        "Patrón de papel:",
        [
            "Renglones de Cuaderno",
            "Cuadrícula Artística",
            "Puntos Minimalistas",
            "Lienzo Limpio",
        ],
    )

# Valores predeterminados de seguridad
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
# GESTIÓN DE TEMÁTICAS Y FONDOS CON EMOJIS ANIMADOS
# =========================================================================
current_theme = st.session_state.current_theme

if "Playero" in current_theme:
  default_bg = "#E0F7FA"
  theme_title = "Vibe Playero & Solecitos"
  emoji_list = ["☀️", "🌴", "🌊", "🏖️", "⭐"]
elif "Enamorados" in current_theme:
  default_bg = "#FCE4EC"
  theme_title = "Vibe Enamorados & Corazones"
  emoji_list = ["💖", "💌", "✨", "🌹", "💘"]
elif "Vinilos" in current_theme:
  default_bg = "#EFEBE9"
  theme_title = "Vibe Vintage & Discos"
  emoji_list = ["🎵", "🎧", "💿", "🎷", "🎶"]
else:
  default_bg = "#FFFDE7"
  theme_title = "Vibe Pop & Caritas Felices"
  emoji_list = ["😊", "⭐", "🚀", "🎨", "🔥"]


# Función generadora de fondos artísticos con emojis incrustados
def crear_fondo_creativo(width, height, bg_hex, guia, emojis):
  bg_rgb = tuple(int(bg_hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
  img = Image.new("RGB", (width, height), bg_rgb)
  draw = ImageDraw.Draw(img)

  # Margen y guías estéticas crema
  margen_color = (45, 42, 38)
  guia_color = (220, 212, 198)

  # Margen estilo cuaderno de diseño
  draw.line([(55, 0), (55, height)], fill=margen_color, width=3)

  if guia == "Renglones de Cuaderno":
    step = 42
    for y in range(step, height, step):
      draw.line([(0, y), (width, y)], fill=guia_color, width=1)
  elif guia == "Cuadrícula Artística":
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


bg_image = crear_fondo_creativo(
    canvas_width, canvas_height, default_bg, tipo_guia, emoji_list
)

# =========================================================================
# LAYOUT PRINCIPAL: Canvas de Dibujo + Panel de Stickers Interactivos Derecha
# =========================================================================
col_canvas, col_stickers = st.columns([3, 1], gap="medium")

with col_canvas:
  st.markdown('<div class="canvas-card">', unsafe_allow_html=True)

  canvas_result = st_canvas(
      fill_color="rgba(244, 196, 48, 0.25)",
      stroke_width=stroke_width,
      stroke_color=stroke_color,
      background_color=default_bg,
      background_image=bg_image,
      height=canvas_height,
      width=canvas_width,
      drawing_mode=drawing_mode,
      key=f"canvas_art_{canvas_width}_{canvas_height}_{current_theme}_{tipo_guia}",
  )

  st.markdown("<br>", unsafe_allow_html=True)
  b1, b2 = st.columns(2)

  with b1:
    if st.button("🗑️ Limpiar Lienzo", use_container_width=True):
      st.rerun()

  with b2:
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
          label="💾 Guardar Obra",
          data=byte_im,
          file_name="obra_estudio.png",
          mime="image/png",
          use_container_width=True,
      )
    else:
      st.button("💾 Guardar Obra", disabled=True, use_container_width=True)

  st.markdown("</div>", unsafe_allow_html=True)

with col_stickers:
  st.markdown(
      "<h3 style='font-weight:900;'>📌 Stickers Vivos</h3>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='font-size:0.85rem; color:#555;'>Selecciona un sticker para"
      " transformar el fondo y los emojis al instante:</p>",
      unsafe_allow_html=True,
  )

  if st.button("☀️ Sticker: Playero", use_container_width=True):
    st.session_state.current_theme = "☀️ Playero"
    st.rerun()

  if st.button("💖 Sticker: Enamorados", use_container_width=True):
    st.session_state.current_theme = "💖 Enamorados"
    st.rerun()

  if st.button("🎵 Sticker: Vinilos", use_container_width=True):
    st.session_state.current_theme = "🎵 Vinilos"
    st.rerun()

  if st.button("😊 Sticker: Carita Feliz", use_container_width=True):
    st.session_state.current_theme = "😊 Caritas Felices"
    st.rerun()

  st.markdown("---")
  st.markdown(
      f"""
    <div class="sticker-box">
        <p style="font-size:0.75rem; font-weight:800; margin:0; color:#888;">AMBIENTE ACTUAL</p>
        <p style="font-size:0.95rem; font-weight:900; margin:5px 0 0 0; color:#2D2A26;">{theme_title}</p>
        <p style="font-size:1.6rem; margin:8px 0 0 0;">{' '.join(emoji_list)}</p>
    </div>
    """,
      unsafe_allow_html=True,
  )
