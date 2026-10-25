import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Configuración de página (mantiene el ícono nativo de Streamlit)
st.set_page_config(
    page_title="Pizarra de Estudio Pro", layout="wide", initial_sidebar_state="expanded"
)

# Estilos CSS personalizados: Estética Minimalista / Estudio Pro (Tonos claros, cálidos y focus)
st.markdown(
    """
    <style>
    /* Fondo general estilo papel de estudio limpio */
    .stApp {
        background-color: #F8F9FA;
        color: #1A1D20;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Principal */
    .study-header {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        padding: 24px;
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .study-header h1 {
        color: #111827;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 6px;
        font-size: 1.8rem;
    }
    .study-header p {
        color: #4B5563;
        font-size: 0.95rem;
        margin: 0;
    }

    /* Cards de Perfiles de Estudio */
    .study-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .study-card:hover {
        border-color: #3B82F6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
    }
    .study-card-title {
        font-weight: 700;
        color: #1F2937;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .study-card-desc {
        color: #6B7280;
        font-size: 0.83rem;
        margin-top: 4px;
    }

    /* Estilo de la barra lateral */
    div[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB;
    }

    /* Botones de acción limpios */
    .stButton > button {
        background: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: #1D4ED8 !important;
        transform: translateY(-1px) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Encabezado limpio
st.markdown(
    """
    <div class="study-header">
        <h1>📚 Pizarra de Estudio Pro</h1>
        <p>Diseñada para esquematizar conceptos, tomar apuntes visuales y estructurar tus sesiones de aprendizaje.</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Sidebar de configuración
with st.sidebar:
  st.subheader("🎯 Enfoque de Estudio")

  perfil_estudio = st.selectbox(
      "Modo de Pizarra:",
      (
          "Apunte Libre (Papel Limpio)",
          "Mapa Mental / Conceptual",
          "Resolución de Fórmulas",
          "Planificador / Kanban",
      ),
  )

  if perfil_estudio == "Apunte Libre (Papel Limpio)":
    default_bg = "#FFFFFF"
    default_stroke = "#1E293B"
    default_width = 4
  elif perfil_estudio == "Mapa Mental / Conceptual":
    default_bg = "#F8FAFC"
    default_stroke = "#3B82F6"
    default_width = 3
  elif perfil_estudio == "Resolución de Fórmulas":
    default_bg = "#FFFBEB"  # Tono papel marfil suave
    default_stroke = "#B45309"
    default_width = 3
  elif perfil_estudio == "Planificador / Kanban":
    default_bg = "#F1F5F9"
    default_stroke = "#0F172A"
    default_width = 4
  else:
    default_bg = "#FFFFFF"
    default_stroke = "#000000"
    default_width = 4

  st.markdown("---")
  st.subheader("📐 Dimensiones")
  canvas_width = st.slider("Ancho", 400, 1000, 750, 50)
  canvas_height = st.slider("Alto", 300, 700, 480, 50)

  st.markdown("---")
  st.subheader("✏️ Herramientas de Trazado")
  drawing_mode = st.selectbox(
      "Herramienta:", ("freedraw", "line", "rect", "circle", "transform")
  )
  stroke_width = st.slider("Grosor del lápiz", 1, 30, default_width)

  # Paleta de colores estilo 'Highlighter & Pen' académico
  colores_estudio = {
      "Negro Académico": "#1E293B",
      "Azul Apunte": "#2563EB",
      "Rojo Destacado": "#DC2626",
      "Verde Esquema": "#16A34A",
      "Morado Conceptual": "#7C3AED",
      "Gris Sutil": "#94A3B8",
      "Personalizado": "custom",
  }

  nombre_color = st.selectbox("Color de tinta:", list(colores_estudio.keys()))
  if nombre_color == "Personalizado":
    stroke_color = st.color_picker("Color Libre", default_stroke)
  else:
    stroke_color = colores_estudio[nombre_color]

  bg_color = st.color_picker("Fondo de Pizarra", default_bg)

  st.markdown("---")
  st.subheader("📋 Patrones de Fondo")
  tipo_guia = st.selectbox(
      "Estructura:",
      (
          "Ninguna",
          "Cuadrícula Matemáticas (Grid)",
          "Puntos (Bullet Journal)",
          "Líneas de Apunte",
      ),
  )


# Función para generar plantillas de estudio limpias con Pillow
def crear_imagen_fondo_estudio(width, height, bg_hex, guia):
  bg_rgb = tuple(int(bg_hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
  img = Image.new("RGB", (width, height), bg_rgb)
  draw = ImageDraw.Draw(img)

  # Color sutil y elegante para las guías académicas
  guia_color = (226, 232, 240)  # Gris muy suave

  if guia == "Cuadrícula Matemáticas (Grid)":
    step = 35
    for x in range(0, width, step):
      draw.line([(x, 0), (x, height)], fill=guia_color, width=1)
    for y in range(0, height, step):
      draw.line([(0, y), (width, y)], fill=guia_color, width=1)

  elif guia == "Puntos (Bullet Journal)":
    step = 30
    for x in range(20, width, step):
      for y in range(20, height, step):
        draw.ellipse(
            [(x - 1, y - 1), (x + 1, y + 1)], fill=(203, 213, 225)
        )  # Puntos delicados

  elif guia == "Líneas de Apunte":
    step = 45
    for y in range(step, height, step):
      draw.line([(40, y), (width - 40, y)], fill=guia_color, width=1)

  return img


# Generar fondo de estudio
bg_image = crear_imagen_fondo_estudio(
    canvas_width, canvas_height, bg_color, tipo_guia
)

# Layout Principal: Canvas y Panel explicativo lateral
col_canvas, col_info = st.columns([2.2, 1], gap="large")

with col_canvas:
  canvas_result = st_canvas(
      fill_color="rgba(37, 99, 235, 0.1)",  # Relleno de figuras translúcido y limpio
      stroke_width=stroke_width,
      stroke_color=stroke_color,
      background_color=bg_color,
      background_image=bg_image,
      height=canvas_height,
      width=canvas_width,
      drawing_mode=drawing_mode,
      key=f"canvas_estudio_{canvas_width}_{canvas_height}_{perfil_estudio}_{tipo_guia}_{bg_color}",
  )

  st.markdown("<br>", unsafe_allow_html=True)
  btn_col1, btn_col2 = st.columns(2)

  with btn_col1:
    if st.button("🗑️ Limpiar Pizarra", use_container_width=True):
      st.rerun()

  with btn_col2:
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
          label="💾 Descargar Apunte",
          data=byte_im,
          file_name="apunte_estudio.png",
          mime="image/png",
          use_container_width=True,
      )
    else:
      st.button("💾 Descargar Apunte", disabled=True, use_container_width=True)

with col_info:
  st.markdown("### 💡 Enfoques de la Pizarra")

  st.markdown(
      """
    <div class="study-card">
        <div class="study-card-title">🧠 Mapa Mental</div>
        <div class="study-card-desc">Usa figuras geométricas limpias con relleno suave para conectar ideas, conceptos y lluvias de ideas sin saturación visual.</div>
    </div>
    
    <div class="study-card">
        <div class="study-card-title">📐 Fórmulas & Ejercicios</div>
        <div class="study-card-desc">Fondo tipo papel marfil con cuadrícula matemática para despejar ecuaciones, trazar ejes o graficar funciones.</div>
    </div>
    
    <div class="study-card">
        <div class="study-card-title">📝 Bullet Journal</div>
        <div class="study-card-desc">Patrón de puntos discretos perfecto para estructurar listas de tareas, cronogramas de estudio o esquemas libres.</div>
    </div>

    <div class="study-card">
        <div class="study-card-title">🎨 Tinta Académica</div>
        <div class="study-card-desc">Paleta de colores optimizada para jerarquizar información (títulos, notas importantes, subrayados y conexiones).</div>
    </div>
    """,
      unsafe_allow_html=True,
  )
