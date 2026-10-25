import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Configuración de página (page_icon omitido para usar el ícono nativo de Streamlit)
st.set_page_config(
    page_title="Tablero de Trazos Urbano", layout="wide", initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para una estética Moderna / Urbana
st.markdown(
    """
    <style>
    /* Estilo general del fondo y la tipografía */
    .stApp {
        background-color: #0E1017;
        color: #E2E8F0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Principal */
    .urban-header {
        background: linear-gradient(135deg, #1E202E 0%, #11131F 100%);
        border: 1px solid #2A2D3E;
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .urban-header h1 {
        color: #FFFFFF;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }
    .urban-header p {
        color: #94A3B8;
        font-size: 0.98rem;
        margin: 0;
    }

    /* Cards de Perfiles / Temáticas */
    .theme-card {
        background: #181A26;
        border: 1px solid #2A2D3E;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: all 0.25s ease-in-out;
    }
    .theme-card:hover {
        border-color: #6366F1;
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.15);
    }
    .theme-card-title {
        font-weight: 700;
        color: #F8FAFC;
        font-size: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .theme-card-desc {
        color: #64748B;
        font-size: 0.85rem;
        margin-top: 4px;
    }

    /* Estilo de los Sliders y Selectbox en Sidebar */
    div[data-testid="stSidebar"] {
        background-color: #121420 !important;
        border-right: 1px solid #1E2030;
    }

    /* Botones Neón/Urbanos */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Encabezado con estética urbana
st.markdown(
    """
    <div class="urban-header">
        <h1>Tablero de Trazos & Caligrafía</h1>
        <p>Espacio de práctica adaptable, inclusivo y personalizable para dibujo, caligrafía o motricidad fina.</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Sidebar con propiedades
with st.sidebar:
  st.subheader("⚙️ Configuración del Tablero")

  perfil = st.selectbox(
      "Modo / Perfil:",
      (
          "Personalizado",
          "Pizarra Clásica",
          "Alto Contraste",
          "Descanso Visual",
          "Trazo Amplio",
      ),
  )

  if perfil == "Pizarra Clásica":
    default_bg = "#1B2A22"
    default_stroke = "#FFFFFF"
    default_width = 10
  elif perfil == "Alto Contraste":
    default_bg = "#000000"
    default_stroke = "#FFFF00"
    default_width = 18
  elif perfil == "Descanso Visual":
    default_bg = "#F4F1EA"
    default_stroke = "#1E293B"
    default_width = 10
  elif perfil == "Trazo Amplio":
    default_bg = "#111827"
    default_stroke = "#38BDF8"
    default_width = 26
  else:
    default_bg = "#111827"
    default_stroke = "#F43F5E"
    default_width = 12

  st.markdown("---")
  st.subheader("📐 Dimensiones")
  canvas_width = st.slider("Ancho", 400, 1000, 750, 50)
  canvas_height = st.slider("Alto", 300, 700, 480, 50)

  st.markdown("---")
  st.subheader("✏️ Herramientas")
  drawing_mode = st.selectbox(
      "Herramienta:", ("freedraw", "line", "rect", "circle", "transform")
  )
  stroke_width = st.slider("Grosor de trazo", 1, 40, default_width)

  colores_tiza = {
      "Blanco Tiza": "#FFFFFF",
      "Neón Rosa": "#FF2E93",
      "Neón Cyan": "#00F0FF",
      "Amarillo Tiza": "#FFE600",
      "Verde Menta": "#00FF66",
      "Naranja Urbano": "#FF6B00",
      "Personalizado": "custom",
  }

  nombre_color = st.selectbox("Color de trazo:", list(colores_tiza.keys()))
  if nombre_color == "Personalizado":
    stroke_color = st.color_picker("Color Libre", default_stroke)
  else:
    stroke_color = colores_tiza[nombre_color]

  bg_color = st.color_picker("Color de Fondo", default_bg)

  st.markdown("---")
  st.subheader("📝 Guías de Fondo")
  tipo_guia = st.selectbox(
      "Patrón de Guía:",
      ("Ninguna", "Cuadrícula", "Renglones", "Calcar Letra / Número"),
  )

  letra_calcar = "A"
  if tipo_guia == "Calcar Letra / Número":
    letra_calcar = st.selectbox(
        "Carácter a practicar:",
        ["A", "B", "C", "D", "E", "1", "2", "3", "4", "5", "Ñ", "M"],
    )


# Función para generar la guía de fondo con Pillow
def crear_imagen_fondo(width, height, bg_hex, guia, caracter):
  bg_rgb = tuple(int(bg_hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
  img = Image.new("RGB", (width, height), bg_rgb)
  draw = ImageDraw.Draw(img)

  luminance = 0.299 * bg_rgb[0] + 0.587 * bg_rgb[1] + 0.114 * bg_rgb[2]
  guia_color = (255, 255, 255, 50) if luminance < 128 else (0, 0, 0, 40)

  if guia == "Cuadrícula":
    step = 40
    for x in range(0, width, step):
      draw.line([(x, 0), (x, height)], fill=guia_color[:3], width=1)
    for y in range(0, height, step):
      draw.line([(0, y)], fill=guia_color[:3], width=1)

  elif guia == "Renglones":
    step = 50
    for y in range(step, height, step):
      draw.line([(30, y), (width - 30, y)], fill=guia_color[:3], width=1)

  elif guia == "Calcar Letra / Número":
    line_y = height // 2 + 30
    draw.line(
        [(40, line_y), (width - 40, line_y)], fill=guia_color[:3], width=2
    )

    try:
      font = ImageFont.truetype("arial.ttf", 130)
    except IOError:
      font = ImageFont.load_default()

    text_color = (255, 255, 255, 70) if luminance < 128 else (100, 100, 100, 70)
    bbox = draw.textbbox((0, 0), caracter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x_pos = (width - text_width) // 2
    y_pos = (height - text_height) // 2 - 20

    draw.text((x_pos, y_pos), caracter, fill=text_color[:3], font=font)

  return img


# Generar fondo
bg_image = crear_imagen_fondo(
    canvas_width, canvas_height, bg_color, tipo_guia, letra_calcar
)

# Layout Principal: Canvas a la izquierda, Cards descriptivas a la derecha
col_canvas, col_cards = st.columns([2.2, 1], gap="large")

with col_canvas:
  # Canvas con clave única para refresco correcto
  canvas_result = st_canvas(
      fill_color="rgba(255, 165, 0, 0.3)",
      stroke_width=stroke_width,
      stroke_color=stroke_color,
      background_color=bg_color,
      background_image=bg_image,
      height=canvas_height,
      width=canvas_width,
      drawing_mode=drawing_mode,
      key=f"canvas_{canvas_width}_{canvas_height}_{perfil}_{tipo_guia}_{bg_color}",
  )

  st.markdown("<br>", unsafe_allow_html=True)
  btn_col1, btn_col2 = st.columns(2)

  with btn_col1:
    if st.button("🗑️ Limpiar Tablero", use_container_width=True):
      st.rerun()

  with btn_col2:
    # Manejo seguro del estado para evitar el RuntimeError del canvas
    has_image = False
    img_pil = None

    try:
      if canvas_result is not None and canvas_result.image_data is not None:
        img_data = canvas_result.image_data
        if np.any(img_data):  # Verificar que no esté completamente vacío
          img_pil = Image.fromarray(img_data.astype("uint8"), "RGBA")
          has_image = True
    except Exception:
      has_image = False

    if has_image and img_pil is not None:
      buf = io.BytesIO()
      img_pil.save(buf, format="PNG")
      byte_im = buf.getvalue()

      st.download_button(
          label="💾 Descargar Guardado",
          data=byte_im,
          file_name="trazo_pizarra.png",
          mime="image/png",
          use_container_width=True,
      )
    else:
      st.button("💾 Descargar Guardado", disabled=True, use_container_width=True)

with col_cards:
  st.markdown("### 🎯 Modos & Enfoques")

  st.markdown(
      """
    <div class="theme-card">
        <div class="theme-card-title">👁️ Alto Contraste</div>
        <div class="theme-card-desc">Trazos amarillos Neón sobre fondos oscuros para máxima legibilidad y personas con baja visión.</div>
    </div>
    
    <div class="theme-card">
        <div class="theme-card-title">✍️ Caligrafía & Motricidad</div>
        <div class="theme-card-desc">Guías de letras y renglones ideales para niños, rehabilitación o aprendizaje de trazos.</div>
    </div>
    
    <div class="theme-card">
        <div class="theme-card-title">☕ Descanso Visual</div>
        <div class="theme-card-desc">Fondo tono papel/crema con tonos suaves para minimizar la fatiga en sesiones extensas.</div>
    </div>

    <div class="theme-card">
        <div class="theme-card-title">🎨 Tizas Neón Pastel</div>
        <div class="theme-card-desc">Colores seleccionados para simular el contraste de tiza sobre pizarras modernas.</div>
    </div>
    """,
      unsafe_allow_html=True,
  )
