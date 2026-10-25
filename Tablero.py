import io
import random

import numpy as np
import streamlit as st
from PIL import Image, ImageDraw
from streamlit_drawable_canvas import st_canvas

# =========================================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================================
st.set_page_config(
    page_title="Mi Pizarra Personalizada",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================================
# DATOS DE CONFIGURACIÓN
# =========================================================================
CAFE = "#3B2108"        # texto café oscuro de alto contraste
CREMA = "#F7F4EA"       # fondo general
AMARILLO = "#E9C46A"    # barra lateral (amarillo más suave)
CARD_BG = "#FBEFC4"     # card desplegable (amarillo más claro)
BOTON = "#F0B03C"       # amarillo cromo suavizado para los botones
BOTON_HOVER = "#F7C867"

COLORES_TIZA = {
    "Azul Ultramar": "#0047AB",
    "Rojo Carmín": "#960018",
    "Verde Olivo": "#556B2F",
    "Amarillo Ocre": "#CC7722",
    "Rosa Pastel": "#FFB6C1",
    "Negro Grafito": "#2D2A26",
    "Naranja": "#F97316",
    "Morado": "#7E22CE",
    "Turquesa": "#14B8A6",
    "Marrón": "#7B4B2A",
    "Blanco Tiza": "#FFFFFF",
    "Gris Piedra": "#9CA3AF",
}

HERRAMIENTAS = {
    "✏️ Tiza libre": "freedraw",
    "📏 Línea recta": "line",
    "▭ Rectángulo": "rect",
    "⭕ Círculo": "circle",
    "✋ Mover figuras": "transform",
}

GROSORES = {
    "Muy fina · 2": 2,
    "Fina · 5": 5,
    "Media · 9": 9,
    "Gruesa · 15": 15,
    "Extra gruesa · 25": 25,
}

TAMANOS = {
    "Grande (780×430)": (780, 430),
    "Extra ancho (800×340)": (800, 340),
    "Cuadrado (500×500)": (500, 500),
}

TEMAS = {
    "☀️ Playero": {
        "bg": "#E0F7FA",
        "titulo": "Vibe Playero & Solecitos",
        "emojis": ["☀️", "🌴", "🌊", "🏖️", "⭐"],
    },
    "💖 Enamorados": {
        "bg": "#FCE4EC",
        "titulo": "Vibe Enamorados & Corazones",
        "emojis": ["💖", "💌", "✨", "🌹", "💘"],
    },
    "🎵 Vinilos": {
        "bg": "#EFEBE9",
        "titulo": "Vibe Vintage & Discos",
        "emojis": ["🎵", "🎧", "💿", "🎷", "🎶"],
    },
    "😊 Caritas Felices": {
        "bg": "#FFFDE7",
        "titulo": "Vibe Pop & Caritas Felices",
        "emojis": ["😊", "⭐", "🚀", "🎨", "🔥"],
    },
}

GUIAS = ["Renglones de Cuaderno", "Cuadrícula Artística", "Puntos Minimalistas", "Lienzo Limpio"]

# Stickers de estudio que siempre aparecen (números, letras, útiles)
STICKERS_ESTUDIO = [
    "A", "B", "C", "ñ", "a", "b", "1", "2", "3", "7", "+", "=", "abc", "123",
    "✏️", "📚", "🔢", "🔤", "📐", "🖍️", "🍎", "📓", "🖊️", "🧮", "🎒", "📏",
]

CATEGORIAS = [
    ("cat_color", "Color de tiza"),
    ("cat_grosor", "Grosor de tiza"),
    ("cat_dispo", "Disposición"),
    ("cat_tam", "Tamaño"),
    ("cat_tema", "Temática"),
    ("cat_guia", "Renglones"),
]

# =========================================================================
# ESTADO DE SESIÓN
# =========================================================================
defaults = {
    "open_cat": None,            # solo una categoría abierta a la vez
    "color": "#2D2A26",
    "herramienta": "freedraw",
    "grosor": 5,
    "tamano": "Grande (780×430)",
    "tema": "☀️ Playero",
    "guia": "Renglones de Cuaderno",
    "canvas_v": 0,               # sube cuando se limpia el lienzo
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# =========================================================================
# STICKERS ANIMADOS DE FONDO (escritorio de estudio)
# =========================================================================
def construir_stickers(emojis_tema):
    rnd = random.Random(7)  # semilla fija: las posiciones no saltan al recargar
    pool = emojis_tema * 3 + STICKERS_ESTUDIO
    cols, rows = 8, 5
    html = []
    for r in range(rows):
        for c in range(cols):
            left = (c + rnd.uniform(0.05, 0.75)) / cols * 100
            top = (r + rnd.uniform(0.05, 0.75)) / rows * 100
            size = rnd.randint(46, 76)
            rot = rnd.randint(-18, 18)
            dur = rnd.uniform(4, 8)
            delay = rnd.uniform(0, 5)
            txt = rnd.choice(pool)
            es_texto = txt.isalnum() or txt in "+="
            clase = "stk txt" if es_texto else "stk"
            html.append(
                f'<div class="{clase}" style="left:{left:.1f}vw;top:{top:.1f}vh;'
                f"--s:{size}px;--r:{rot}deg;--t:{dur:.1f}s;--d:{delay:.1f}s;"
                f'--t2:{dur * 0.9 + 2:.1f}s">{txt}</div>'
            )
    return '<div class="sticker-layer">' + "".join(html) + "</div>"


tema_actual = TEMAS[st.session_state.tema]

# =========================================================================
# CSS
# =========================================================================
css_swatches = ""
for hex_val in COLORES_TIZA.values():
    h = hex_val.lstrip("#")
    css_swatches += (
        f".st-key-sw_{h} button, .st-key-sw_{h} button:hover, "
        f".st-key-sw_{h} button:focus {{ background: {hex_val} !important; }}\n"
    )

PRIMARY = 'button[kind="primary"], button[data-testid="stBaseButton-primary"]'

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Caveat:wght@600;700&family=Pacifico&display=swap');

/* ---------- Fondo general crema ---------- */
.stApp {{
    background-color: {CREMA};
    color: #2D2A26;
    font-family: 'Fredoka', 'Trebuchet MS', sans-serif;
}}
[data-testid="stHeader"] {{ background: transparent; }}

/* Contenido por encima de los stickers */
.block-container, [data-testid="stMainBlockContainer"] {{
    position: relative;
    z-index: 0;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}}

/* ---------- Barra lateral amarilla y ANCHA ---------- */
[data-testid="stSidebar"][aria-expanded="true"] {{
    width: 36vw !important;
    min-width: 36vw !important;
    max-width: 36vw !important;
}}
[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {{
    width: 100% !important;
}}
[data-testid="stSidebar"] {{
    background-color: {AMARILLO} !important;
    border-right: 3px solid #2D2A26;
}}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {{
    color: #1F1308;
    font-family: 'Fredoka', sans-serif;
}}

/* ---------- Bienvenida ---------- */
.welcome {{
    background: #FFFDF7;
    border: 3px solid #2D2A26;
    border-radius: 16px;
    padding: 16px 18px;
    box-shadow: 5px 5px 0 #2D2A26;
    margin-bottom: 18px;
}}
.welcome h2 {{ margin: 0 0 6px 0; font-size: 1.7rem; font-weight: 700; color: #1F1308; font-family: 'Fredoka', sans-serif; }}
.welcome p  {{ margin: 0; font-size: 1.35rem; line-height: 1.2; color: {CAFE}; font-weight: 700; font-family: 'Caveat', cursive; }}

/* ---------- Botones base de la barra ---------- */
[data-testid="stSidebar"] .stButton button {{
    border-radius: 12px !important;
    font-weight: 800 !important;
    border: 2px solid #2D2A26 !important;
    transition: all .1s ease !important;
}}

/* Botones de categoría (el color se mantiene abierto o cerrado) */
[class*="st-key-cat_"] button {{
    background: {BOTON} !important;
    border: 2px solid {CAFE} !important;
    box-shadow: 4px 4px 0 {CAFE} !important;
    padding: .55rem 1rem !important;
}}
[class*="st-key-cat_"] button p {{ color: {CAFE} !important; font-size: 1.25rem; font-weight: 700; font-family: 'Fredoka', sans-serif; letter-spacing: .3px; }}
[class*="st-key-cat_"] button:hover {{
    background: {BOTON_HOVER} !important;
    transform: translate(-1px,-1px);
    box-shadow: 6px 6px 0 {CAFE} !important;
}}

/* Punto que muestra el tamaño de la tiza */
.dot-wrap {{
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.dot {{
    border-radius: 50%;
    border: 1.5px solid {CAFE};
    box-shadow: 1px 2px 0 rgba(91,58,31,.35);
}}

/* ---------- Card desplegable ---------- */
.st-key-card_open {{
    background: {CARD_BG};
    border: 2px solid {CAFE};
    border-radius: 14px;
    padding: 14px 14px 10px 14px;
    margin: -4px 0 14px 0;
    box-shadow: 3px 3px 0 {CAFE};
}}
.st-key-card_open p, .st-key-card_open label, .st-key-card_open span {{ color: {CAFE} !important; }}
.card-title {{
    font-family: 'Fredoka', sans-serif;
    font-weight: 700; font-size: 1.3rem; color: {CAFE};
    text-decoration: underline; text-underline-offset: 4px;
    margin-bottom: 10px;
}}

/* Opciones dentro de la card */
[class*="st-key-opt_"] button {{
    background: #FFFDF7 !important;
    box-shadow: 2px 2px 0 {CAFE} !important;
}}
[class*="st-key-opt_"] button p {{ color: {CAFE} !important; font-size: 1.05rem; font-weight: 600; font-family: 'Fredoka', sans-serif; }}
[class*="st-key-opt_"] button[kind="primary"] p,
[class*="st-key-opt_"] button[data-testid="stBaseButton-primary"] p {{ color: {CREMA} !important; }}
[class*="st-key-opt_"] button[kind="primary"],
[class*="st-key-opt_"] button[data-testid="stBaseButton-primary"] {{ background: {CAFE} !important; }}

/* Cuadraditos de color */
[class*="st-key-sw_"] button {{
    height: 52px !important;
    min-height: 52px !important;
    border: 2px solid {CAFE} !important;
    border-radius: 10px !important;
    box-shadow: 2px 2px 0 {CAFE} !important;
}}
[class*="st-key-sw_"] button p {{ color: #fff !important; font-size: 1.3rem; text-shadow: 0 0 3px #000; }}
[class*="st-key-sw_"] button[kind="primary"],
[class*="st-key-sw_"] button[data-testid="stBaseButton-primary"] {{
    outline: 4px solid {CAFE};
    outline-offset: 2px;
}}
{css_swatches}

/* ---------- Portada ---------- */
.art-hero {{
    background: #2D2A26;
    padding: 22px 30px;
    border-radius: 16px;
    box-shadow: 6px 6px 0 {AMARILLO};
    margin-bottom: 22px;
    border: 3px solid #1F1308;
    text-align: center;
}}
.art-hero h1 {{
    margin: 0;
    padding: .1em .3em .25em .3em;
    font-family: 'Pacifico', 'Dancing Script', cursive;
    font-weight: 400;
    font-size: 3.9rem;
    line-height: 1.3;
    letter-spacing: .5px;
    display: inline-block;
    background: linear-gradient(90deg,
        #FFF6E0, #F8DE95, #F0B03C, #FFE7A8, #F3E3C3, #FFF6E0);
    background-size: 300% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
    animation: titleflow 7s linear infinite, titleblur 4.5s ease-in-out infinite;
}}
@keyframes titleflow {{
    0%   {{ background-position: 0% 50%; }}
    100% {{ background-position: 300% 50%; }}
}}
@keyframes titleblur {{
    0%, 100% {{ filter: blur(0px) drop-shadow(0 0 6px rgba(240,176,60,.35)); }}
    50%      {{ filter: blur(.6px) drop-shadow(0 0 18px rgba(240,176,60,.7)); }}
}}
.art-hero p {{
    margin: 6px 0 0 0; color: #FFF8E1; font-size: 1.6rem; line-height: 1.1;
    font-family: 'Caveat', cursive; font-weight: 700;
}}

/* ---------- Canvas ---------- */
.st-key-canvas_card {{
    background: #FFFDF7;
    border: 3px solid #1F1308;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 8px 8px 0 #1F1308;
    width: fit-content !important;
    max-width: 100%;
    margin-left: auto;
    margin-right: auto;
    align-items: center;
}}
.stMain iframe {{ display: block; margin: 0 auto; max-width: 100%; }}

/* Botones del área principal */
.stMain .stButton button, .stMain .stDownloadButton button {{
    background: #2D2A26 !important;
    border: 2px solid #2D2A26 !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    box-shadow: 3px 3px 0 #888 !important;
}}
.stMain .stButton button p, .stMain .stDownloadButton button p {{ color: {CREMA} !important; font-family: 'Fredoka', sans-serif; font-size: 1.1rem; font-weight: 600; }}
.stMain .stButton button:hover, .stMain .stDownloadButton button:hover {{
    background: {AMARILLO} !important;
    transform: translate(-1px,-1px);
}}
.stMain .stButton button:hover p, .stMain .stDownloadButton button:hover p {{ color: #2D2A26 !important; }}

.sticker-box {{
    background: #FFFDF7;
    border: 2px solid #2D2A26;
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    box-shadow: 4px 4px 0 #2D2A26;
}}

/* =====================================================================
   STICKERS ANIMADOS DEL FONDO
   ===================================================================== */
.sticker-layer {{
    position: fixed;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    overflow: hidden;
    background: rgba(70, 50, 30, .42);   /* fondo oscuro para bajar la saturación */
}}
.stk {{
    position: absolute;
    width: var(--s);
    height: var(--s);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: calc(var(--s) * .55);
    background: #fff;
    border: 3px solid #fff;
    border-radius: 28%;
    box-shadow: 0 0 0 2px rgba(45,42,38,.28), 3px 4px 8px rgba(0,0,0,.18);
    opacity: .38;
    overflow: hidden;
    transform: rotate(var(--r));
    animation:
        floaty var(--t) ease-in-out var(--d) infinite,
        glow calc(var(--t) * .8) ease-in-out var(--d) infinite;
}}
.stk.txt {{
    font-family: 'Caveat', 'Segoe Print', cursive;
    font-weight: 700;
    color: {CAFE};
    font-size: calc(var(--s) * .72);
}}
/* Destello que cruza el sticker */
.stk::after {{
    content: "";
    position: absolute;
    top: -60%;
    left: -120%;
    width: 55%;
    height: 220%;
    background: linear-gradient(100deg, transparent, rgba(255,255,255,.6), transparent);
    transform: rotate(20deg);
    animation: shine var(--t2) linear var(--d) infinite;
}}
@keyframes floaty {{
    0%, 100% {{ transform: translateY(0) rotate(var(--r)) scale(1); }}
    50%      {{ transform: translateY(-12px) rotate(calc(var(--r) + 7deg)) scale(1.07); }}
}}
@keyframes glow {{
    0%, 100% {{ box-shadow: 0 0 0 2px rgba(45,42,38,.28), 3px 4px 8px rgba(0,0,0,.18); }}
    50%      {{ box-shadow: 0 0 0 2px rgba(244,196,48,.6), 0 0 12px 3px rgba(255,214,64,.45); }}
}}
@keyframes shine {{
    0%   {{ left: -120%; }}
    55%, 100% {{ left: 170%; }}
}}
</style>
""",
    unsafe_allow_html=True,
)

# Capa de stickers
st.markdown(construir_stickers(tema_actual["emojis"]), unsafe_allow_html=True)


# =========================================================================
# AYUDAS PARA LA BARRA LATERAL
# =========================================================================
def boton_opcion(etiqueta, estado, valor, key_extra=""):
    """Botón seleccionable: si es el valor activo se muestra resaltado con ✓."""
    activo = st.session_state[estado] == valor
    if st.button(
        f"✓ {etiqueta}" if activo else etiqueta,
        key=f"opt_{estado}_{key_extra or valor}",
        type="primary" if activo else "secondary",
        use_container_width=True,
    ):
        st.session_state[estado] = valor
        st.rerun()


def opciones_en_columnas(items, estado, n=2):
    """Reparte botones de opción en n columnas (la barra ahora es ancha)."""
    items = list(items)
    for i in range(0, len(items), n):
        cols = st.columns(n)
        for col, (nombre, valor) in zip(cols, items[i : i + n]):
            with col:
                boton_opcion(nombre, estado, valor, key_extra=nombre)


def contenido_categoria(cat):
    if cat == "cat_color":
        st.markdown('<div class="card-title">Color de tiza</div>', unsafe_allow_html=True)
        items = list(COLORES_TIZA.items())
        for i in range(0, len(items), 6):
            cols = st.columns(6)
            for col, (nombre, hex_val) in zip(cols, items[i : i + 6]):
                with col:
                    activo = st.session_state.color.lower() == hex_val.lower()
                    if st.button(
                        "✓" if activo else "\u00a0",
                        key=f"sw_{hex_val.lstrip('#')}",
                        help=nombre,
                        type="primary" if activo else "secondary",
                        use_container_width=True,
                    ):
                        st.session_state.color = hex_val
                        st.rerun()
        st.markdown("<b>➕ Mezclador libre:</b>", unsafe_allow_html=True)
        elegido = st.color_picker("Tono exacto", st.session_state.color)
        if elegido.lower() != st.session_state.color.lower():
            st.session_state.color = elegido
            st.rerun()

    elif cat == "cat_grosor":
        st.markdown('<div class="card-title">Grosor de tiza</div>', unsafe_allow_html=True)
        for nombre, valor in GROSORES.items():
            c_dot, c_btn = st.columns([1, 5], vertical_alignment="center")
            with c_dot:
                d = max(4, int(valor * 1.3))  # el punto refleja el grosor
                st.markdown(
                    f'<div class="dot-wrap"><div class="dot" style="width:{d}px;'
                    f'height:{d}px;background:{st.session_state.color};"></div></div>',
                    unsafe_allow_html=True,
                )
            with c_btn:
                boton_opcion(nombre, "grosor", valor)

    elif cat == "cat_dispo":
        st.markdown('<div class="card-title">Disposición / herramienta</div>', unsafe_allow_html=True)
        opciones_en_columnas(HERRAMIENTAS.items(), "herramienta")

    elif cat == "cat_tam":
        st.markdown('<div class="card-title">Tamaño del tablero</div>', unsafe_allow_html=True)
        opciones_en_columnas([(n, n) for n in TAMANOS], "tamano")

    elif cat == "cat_tema":
        st.markdown('<div class="card-title">Temática del tablero</div>', unsafe_allow_html=True)
        opciones_en_columnas([(n, n) for n in TEMAS], "tema")

    elif cat == "cat_guia":
        st.markdown('<div class="card-title">Patrón de papel</div>', unsafe_allow_html=True)
        opciones_en_columnas([(n, n) for n in GUIAS], "guia")


# =========================================================================
# BARRA LATERAL: BIENVENIDA + CATEGORÍAS DESPLEGABLES (UNA A LA VEZ)
# =========================================================================
with st.sidebar:
    st.markdown(
        """
        <div class="welcome">
            <h2>👋 ¡Bienvenido a tu tablero!</h2>
            <p>Elige una categoría para abrirla y ajusta tu pizarra a tu gusto,
            tu temática y tu objetivo de práctica.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for cat_key, cat_label in CATEGORIAS:
        abierta = st.session_state.open_cat == cat_key
        flecha = "▲" if abierta else "▼"
        if st.button(f"{cat_label}   {flecha}", key=cat_key, use_container_width=True):
            st.session_state.open_cat = None if abierta else cat_key
            st.rerun()

        if abierta:
            with st.container(key="card_open"):
                contenido_categoria(cat_key)

# =========================================================================
# PORTADA
# =========================================================================
st.markdown(
    """
    <div class="art-hero">
        <h1>Mi Pizarra de Práctica</h1>
        <p>Escribe números, letras y repasa caligrafía. Personaliza todo desde la barra amarilla.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================================
# FONDO DEL TABLERO (guías de papel)
# =========================================================================
def crear_fondo(width, height, bg_hex, guia):
    bg_rgb = tuple(int(bg_hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    img = Image.new("RGB", (width, height), bg_rgb)
    draw = ImageDraw.Draw(img)
    margen_color = (45, 42, 38)
    guia_color = (200, 190, 175)

    draw.line([(55, 0), (55, height)], fill=margen_color, width=3)

    if guia == "Renglones de Cuaderno":
        for y in range(42, height, 42):
            draw.line([(0, y), (width, y)], fill=guia_color, width=1)
    elif guia == "Cuadrícula Artística":
        for x in range(0, width, 35):
            draw.line([(x, 0), (x, height)], fill=guia_color, width=1)
        for y in range(0, height, 35):
            draw.line([(0, y), (width, y)], fill=guia_color, width=1)
    elif guia == "Puntos Minimalistas":
        for x in range(30, width, 30):
            for y in range(30, height, 30):
                draw.ellipse([(x - 1, y - 1), (x + 1, y + 1)], fill=margen_color)
    return img


canvas_width, canvas_height = TAMANOS[st.session_state.tamano]
bg_image = crear_fondo(canvas_width, canvas_height, tema_actual["bg"], st.session_state.guia)

# =========================================================================
# LAYOUT PRINCIPAL
# =========================================================================
with st.container(key="canvas_card"):

    canvas_result = st_canvas(
        fill_color="rgba(244, 196, 48, 0.25)",
        stroke_width=st.session_state.grosor,
        stroke_color=st.session_state.color,
        background_color=tema_actual["bg"],
        background_image=bg_image,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=st.session_state.herramienta,
        key=(
            f"canvas_{canvas_width}_{canvas_height}_{st.session_state.tema}"
            f"_{st.session_state.guia}_{st.session_state.canvas_v}"
        ),
    )

    st.markdown("<br>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)

    with b1:
        if st.button("🗑️ Limpiar Lienzo", use_container_width=True):
            st.session_state.canvas_v += 1  # cambia la key => lienzo nuevo
            st.rerun()

    with b2:
        png_bytes = None
        try:
            if canvas_result is not None and canvas_result.image_data is not None:
                data = canvas_result.image_data
                if np.any(data[:, :, 3]):  # hay trazos
                    capa = Image.fromarray(data.astype("uint8"), "RGBA")
                    base = bg_image.convert("RGBA")
                    if capa.size != base.size:
                        capa = capa.resize(base.size)
                    final = Image.alpha_composite(base, capa)  # fondo + trazos
                    buf = io.BytesIO()
                    final.save(buf, format="PNG")
                    png_bytes = buf.getvalue()
        except Exception:
            png_bytes = None

        if png_bytes:
            st.download_button(
                "💾 Guardar Obra",
                data=png_bytes,
                file_name="mi_pizarra.png",
                mime="image/png",
                use_container_width=True,
            )
        else:
            st.button("💾 Guardar Obra", disabled=True, use_container_width=True)
