import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Configuración de la página
st.set_page_config(
    page_title="Mi Pizarra a Mi Medida", page_icon="🎨", layout="centered"
)

st.title("🎨 Mi Pizarra a Mi Medida")
st.markdown(
    "Un tablero de tiza personalizable pensado para adaptarse a cómo ves, cómo dibujas y qué necesitas."
)

with st.sidebar:
  st.header("⚙️ Perfiles y Accesibilidad")

  # Perfiles listos para usar
  perfil = st.selectbox(
      "Perfiles listos para usar:",
      (
          "Personalizado",
          "Pizarra Clásica (Verde)",
          "Alto Contraste (Baja visión)",
          "Descanso Visual (Crema)",
          "Trazo Amplio (Motricidad)",
      ),
  )

  # Configuración predeterminada según el perfil elegido
  if perfil == "Pizarra Clásica (Verde)":
    default_bg = "#1b3b22"
    default_stroke = "#FFFFFF"
    default_width = 10
  elif perfil == "Alto Contraste (Baja visión)":
    default_bg = "#000000"
    default_stroke = "#FFFF00"
    default_width = 18
  elif perfil == "Descanso Visual (Crema)":
    default_bg = "#FDFBF7"
    default_stroke = "#2C2C2C"
    default_width = 12
  elif perfil == "Trazo Amplio (Motricidad)":
    default_bg = "#1b3b22"
    default_stroke = "#FFFFFF"
    default_width = 28
  else:
    default_bg = "#1b3b22"
    default_stroke = "#FFFFFF"
    default_width = 12

  st.subheader("📏 Dimensiones del Tablero")
  canvas_width = st.slider("Ancho del tablero", 300, 800, 600, 50)
  canvas_height = st.slider("Alto del tablero", 300, 700, 450, 50)

  st.subheader("✍️ Herramienta de Dibujo")
  drawing_mode = st.selectbox(
      "Herramienta:", ("freedraw", "line", "rect", "circle", "transform")
  )

  stroke_width = st.slider("Ancho de la tiza", 1, 40, default_width)

  # Paleta de tizas con nombres descriptivos
  st.subheader("🖍️ Tizas de Colores")
  colores_tiza = {
      "Blanco Tiza": "#FFFFFF",
      "Amarillo Tiza": "#FFF380",
      "Rosa Pastel": "#FFB3BA",
      "Celeste Pastel": "#BAE1FF",
      "Verde Menta": "#BAFFC9",
      "Naranja Suave": "#FFDFBA",
      "Personalizado...": "custom",
  }

  nombre_color = st.selectbox("Elige tu tiza:", list(colores_tiza.keys()))
  if nombre_color == "Personalizado...":
    stroke_color = st.color_picker("Color de trazo libre", default_stroke)
  else:
    stroke_color = colores_tiza[nombre_color]

  st.subheader("🎨 Fondo del Tablero")
  bg_color = st.color_picker("Color de fondo", default_bg)

  st.subheader("📐 Guías de Práctica")
  tipo_guia = st.selectbox(
      "Guía visual:",
      ("Ninguna", "Cuadrícula", "Renglones", "Calcar Letra / Número"),
  )

  letra_calcar = "A"
  if tipo_guia == "Calcar Letra / Número":
    letra_calcar = st.selectbox(
        "Carácter a practicar:",
        ["A", "B", "C", "D", "E", "1", "2", "3", "4", "5", "Ñ", "M"],
    )


# Función para generar fondos interactivos (guías o plantillas de caligrafía)
def crear_imagen_fondo(width, height, bg_hex, guia, caracter):
  # Convertir color hexadecimal a RGB
  bg_rgb = tuple(int(bg_hex[i : i + 2], 16) for i in (1, 3, 5))
  img = Image.new("RGB", (width, height), bg_rgb)
  draw = ImageDraw.Draw(img)

  # Determinar si el fondo es claro u oscuro para ajustar el contraste de la guía
  luminance = 0.299 * bg_rgb[0] + 0.587 * bg_rgb[1] + 0.114 * bg_rgb[2]
  guia_color = (255, 255, 255, 60) if luminance < 128 else (0, 0, 0, 50)

  if guia == "Cuadrícula":
    step = 40
    for x in range(0, width, step):
      draw.line([(x, 0), (x, height)], fill=guia_color[:3], width=1)
    for y in range(0, height, step):
      draw.line([(0, y), (width, y)], fill=guia_color[:3], width=1)

  elif guia == "Renglones":
    step = 60
    for y in range(step, height, step):
      draw.line([(30, y), (width - 30, y)], fill=guia_color[:3], width=1)

  elif guia == "Calcar Letra / Número":
    # Líneas de referencia para caligrafía
    line_y = height // 2 + 40
    draw.line(
        [(40, line_y), (width - 40, line_y)], fill=guia_color[:3], width=2
    )
    draw.line(
        [(40, line_y - 80), (width - 40, line_y - 80)],
        fill=guia_color[:3],
        width=1,
    )

    # Intentar cargar una fuente grande para calcar
    try:
      font = ImageFont.truetype("arial.ttf", 140)
    except IOError:
      try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 140
        )
      except:
        font = ImageFont.load_default()

    # Dibujar la letra guía tenue en el centro
    text_color = (255, 255, 255, 90) if luminance < 128 else (120, 120, 120, 90)
    bbox = draw.textbbox((0, 0), caracter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x_pos = (width - text_width) // 2
    y_pos = (height - text_height) // 2 - 20

    draw.text((x_pos, y_pos), caracter, fill=text_color[:3], font=font)

  return img


# Generar imagen de fondo basada en las selecciones
bg_image = crear_imagen_fondo(
    canvas_width, canvas_height, bg_color, tipo_guia, letra_calcar
)

# Lienzo principal
st.markdown("### Área de Práctica")
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=bg_image,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key=f"canvas_{canvas_width}_{canvas_height}_{perfil}_{tipo_guia}",
)

# Botones de acción grandes y claros (lejos de iconos confusos)
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
  if st.button("🗑️ Limpiar Tablero", use_container_width=True):
    st.rerun()

with col2:
  if canvas_result.image_data is not None:
    img_data = canvas_result.image_data
    img_pil = Image.fromarray(img_data.astype("uint8"), "RGBA")

    buf = io.BytesIO()
    img_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="💾 Descargar Creación",
        data=byte_im,
        file_name="mi_pizarra.png",
        mime="image/png",
        use_container_width=True,
    )
