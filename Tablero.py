import io

import streamlit as st
from PIL import Image, ImageDraw
from streamlit_drawable_canvas import st_canvas

st.set_page_config(
    page_title="Mi pizarra a mi medida",
    page_icon="🖍️",
    layout="wide",
)

# ============================================================
# PERFILES: cada uno define fondo, tizas, trazo y apariencia
# ============================================================
PERFILES = {
    "Pizarra clásica": {
        "desc": "Pizarra verde con tizas pastel. Para dibujar sin pensar en nada más.",
        "fondo": "#2F4F3E",
        "paleta": {
            "Blanco tiza": "#F7F5EE", "Amarillo limón": "#F6E27A",
            "Rosa chicle": "#F4A6C0", "Celeste cielo": "#9AD7F0",
            "Verde menta": "#A8E6C3", "Naranja durazno": "#F8B88B",
            "Lila": "#C9B1F0",
        },
        "grosor": 6, "guia": "Sin guía", "grande": False,
        "ui": {"bg": "#1D2B24", "panel": "#26382F", "texto": "#F3F1E7",
               "acento": "#F2D16B", "marco": "#8B5A2B"},
    },
    "Alto contraste": {
        "desc": "Colores muy fuertes sobre negro. Ayuda cuando cuesta ver los tonos suaves.",
        "fondo": "#000000",
        "paleta": {
            "Amarillo": "#FFE600", "Blanco": "#FFFFFF", "Cian": "#00E5FF",
            "Verde lima": "#39FF14", "Magenta": "#FF4DFF", "Naranja": "#FF9100",
        },
        "grosor": 10, "guia": "Sin guía", "grande": True,
        "ui": {"bg": "#000000", "panel": "#111111", "texto": "#FFFFFF",
               "acento": "#FFE600", "marco": "#FFFFFF"},
    },
    "Apto para daltonismo": {
        "desc": "Paleta de colores que se distinguen entre sí con daltonismo, sobre fondo claro.",
        "fondo": "#F4F4F0",
        "paleta": {
            "Negro": "#000000", "Naranja": "#E69F00", "Celeste": "#56B4E9",
            "Verde azulado": "#009E73", "Azul": "#0072B2",
            "Bermellón": "#D55E00", "Rosa": "#CC79A7",
        },
        "grosor": 8, "guia": "Sin guía", "grande": False,
        "ui": {"bg": "#EEF1F4", "panel": "#FFFFFF", "texto": "#12202E",
               "acento": "#0072B2", "marco": "#334155"},
    },
    "Descanso visual": {
        "desc": "Fondo crema y tonos suaves que cansan menos la vista en sesiones largas.",
        "fondo": "#F3E9D2",
        "paleta": {
            "Café": "#5B4636", "Azul pizarra": "#4C6A85",
            "Verde salvia": "#6E8B6B", "Terracota": "#B5654A",
            "Ciruela": "#7A5C7E", "Gris cálido": "#7B7468",
        },
        "grosor": 6, "guia": "Renglones", "grande": False,
        "ui": {"bg": "#EFE4CC", "panel": "#F7EFDD", "texto": "#3D3326",
               "acento": "#B5654A", "marco": "#8A7A5C"},
    },
    "Trazo grande": {
        "desc": "Trazo grueso y controles grandes. Pensado para quien tiene poca precisión al dibujar.",
        "fondo": "#2F4F3E",
        "paleta": {
            "Blanco tiza": "#F7F5EE", "Amarillo limón": "#F6E27A",
            "Rosa chicle": "#F4A6C0", "Celeste cielo": "#9AD7F0",
            "Verde menta": "#A8E6C3", "Naranja durazno": "#F8B88B",
        },
        "grosor": 22, "guia": "Sin guía", "grande": True,
        "ui": {"bg": "#1D2B24", "panel": "#26382F", "texto": "#F3F1E7",
               "acento": "#F2D16B", "marco": "#8B5A2B"},
    },
}

HERRAMIENTAS = {
    "✏️ Lápiz libre": "freedraw",
    "📏 Línea": "line",
    "▭ Rectángulo": "rect",
    "⭕ Círculo": "circle",
    "🔷 Polígono": "polygon",
    "📍 Punto": "point",
    "✋ Mover figuras": "transform",
}
FORMAS = {"line", "rect", "circle", "polygon"}
GUIAS = ["Sin guía", "Cuadrícula", "Renglones", "Puntos"]
OTRO = "🎨 Color propio"


def html(texto):
    """Markdown trata las líneas con sangría como código: se compacta el HTML."""
    st.markdown(
        " ".join(l.strip() for l in texto.splitlines() if l.strip()),
        unsafe_allow_html=True,
    )


# ============================================================
# AYUDAS DE COLOR E IMAGEN
# ============================================================
def a_rgb(hex_):
    h = hex_.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminancia(hex_):
    r, g, b = a_rgb(hex_)
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255


def texto_sobre(hex_):
    """Blanco u oscuro, según el fondo, para que siempre se lea."""
    return "#12202E" if luminancia(hex_) > 0.55 else "#FFFFFF"


@st.cache_data
def crear_fondo(ancho, alto, color, guia):
    """Fondo del tablero con su guía (cuadrícula, renglones o puntos)."""
    img = Image.new("RGBA", (ancho, alto), color)
    if guia == "Sin guía":
        return img

    base = a_rgb(color)
    extremo = (255, 255, 255) if luminancia(color) < 0.5 else (0, 0, 0)
    linea = tuple(int(b + (e - b) * 0.22) for b, e in zip(base, extremo))
    d = ImageDraw.Draw(img)
    paso = 32

    if guia == "Cuadrícula":
        for x in range(paso, ancho, paso):
            d.line([(x, 0), (x, alto)], fill=linea, width=1)
        for y in range(paso, alto, paso):
            d.line([(0, y), (ancho, y)], fill=linea, width=1)
    elif guia == "Renglones":
        for y in range(paso + 8, alto, paso + 8):
            d.line([(0, y), (ancho, y)], fill=linea, width=2)
    elif guia == "Puntos":
        for x in range(paso, ancho, paso):
            for y in range(paso, alto, paso):
                d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=linea)
    return img


# ============================================================
# ESTADO INICIAL Y CAMBIO DE PERFIL
# ============================================================
def aplicar_perfil():
    p = PERFILES[st.session_state.perfil]
    st.session_state.fondo_color = p["fondo"]
    st.session_state.tiza = next(iter(p["paleta"]))
    st.session_state.grosor = p["grosor"]
    st.session_state.guia = p["guia"]
    st.session_state.grande = p["grande"]


if "perfil" not in st.session_state:
    st.session_state.perfil = "Pizarra clásica"
    aplicar_perfil()
    st.session_state.herramienta = "✏️ Lápiz libre"
    st.session_state.ancho = 600
    st.session_state.alto = 450
    st.session_state.relleno = False
    st.session_state.hoja = 0

perfil = PERFILES[st.session_state.perfil]
ui = perfil["ui"]

# ============================================================
# BARRA LATERAL: todo lo que se puede personalizar
# ============================================================
with st.sidebar:
    html('<div class="side-t">1. Elige un perfil</div>')
    st.radio(
        "Perfil",
        list(PERFILES),
        key="perfil",
        on_change=aplicar_perfil,
        label_visibility="collapsed",
    )
    st.caption(perfil["desc"])

    html('<div class="side-t">2. Elige tu tiza</div>')
    st.radio(
        "Tiza",
        list(perfil["paleta"]) + [OTRO],
        key="tiza",
        label_visibility="collapsed",
    )

    if st.session_state.tiza == OTRO:
        color_trazo = st.color_picker("Tu color", "#FFFFFF", key="color_propio")
    else:
        color_trazo = perfil["paleta"][st.session_state.tiza]

    st.slider("Grosor del trazo", 1, 40, key="grosor")

    html(
        f"""
<div class="vista" style="background:{st.session_state.fondo_color}">
<i style="background:{color_trazo};height:{st.session_state.grosor}px"></i>
</div>
<div class="vista-t">Así se verá tu trazo</div>
"""
    )

    html('<div class="side-t">3. Elige tu fondo</div>')
    st.color_picker("Color del tablero", key="fondo_color")
    st.radio("Guía de fondo", GUIAS, key="guia", horizontal=True)

    html('<div class="side-t">4. Elige tu herramienta</div>')
    st.radio(
        "Herramienta",
        list(HERRAMIENTAS),
        key="herramienta",
        label_visibility="collapsed",
    )
    modo = HERRAMIENTAS[st.session_state.herramienta]

    if modo in FORMAS:
        st.checkbox("Rellenar las figuras", key="relleno")

    with st.expander("📐 Tamaño del tablero y lectura"):
        st.slider("Ancho del tablero", 300, 900, step=50, key="ancho")
        st.slider("Alto del tablero", 300, 700, step=50, key="alto")
        st.checkbox("Interfaz grande (letras y botones)", key="grande")

    st.caption(
        "Al cambiar el perfil, el fondo, la guía o el tamaño se empieza una hoja nueva."
    )

# ============================================================
# ESTILOS SEGÚN EL PERFIL
# ============================================================
grande = st.session_state.grande
ancho = st.session_state.ancho
alto = st.session_state.alto
fondo = st.session_state.fondo_color

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Caveat:wght@600;700&display=swap');

html, body, .stApp, .stApp p, .stApp label, .stApp li, .stApp span, .stApp div {
    font-family:'Atkinson Hyperlegible',sans-serif;
}
.stApp {background:__BG__; color:__TEXTO__;}
.stApp p, .stApp label, .stApp li, .stApp span {color:__TEXTO__;}
[data-testid="stHeader"] {background:transparent;}
.block-container {max-width:1250px; padding-top:3.5rem;}

[data-testid="stSidebar"] {
    background:__PANEL__ !important;
    border-right:3px solid __ACENTO__;
}
[data-testid="stSidebar"] * {color:__TEXTO__;}
[data-testid="stSidebar"] .stApp, [data-testid="stSidebar"] input {color:inherit;}

.stApp p, .stApp label, [data-testid="stWidgetLabel"] p {font-size:__LETRA__;}

.titulo {
    font-family:'Caveat',cursive !important;
    font-size:clamp(2.6rem,6vw,4rem);
    font-weight:700;
    line-height:1.05;
    color:__ACENTO__;
}
.sub {font-size:__SUB__; margin:.2rem 0 .8rem; max-width:46rem;}

.side-t {
    margin:1.3rem 0 .4rem;
    padding-bottom:.3rem;
    border-bottom:2px solid __ACENTO__;
    font-size:1.2rem;
    font-weight:700;
    color:__ACENTO__;
}
[data-testid="stSidebar"] .side-t {color:__ACENTO__;}

.vista {
    display:flex;
    align-items:center;
    height:56px;
    padding:0 1rem;
    border-radius:12px;
    border:2px solid __ACENTO__;
}
.vista i {display:block; width:100%; border-radius:99px;}
.vista-t {font-size:.9rem; margin-top:.3rem; opacity:.85;}

iframe[title*="canvas"] {
    display:block;
    width:__ANCHO__px !important;
    max-width:calc(100% - 36px);
    margin:22px auto;
    border-radius:6px;
    box-shadow:0 0 0 14px __MARCO__,0 0 0 17px rgba(0,0,0,.35),0 18px 36px rgba(0,0,0,.35);
}

.stButton > button, .stDownloadButton > button {
    width:100%;
    min-height:__BOTON__;
    border-radius:14px;
    border:3px solid __ACENTO__;
    background:__ACENTO__;
    color:__TEXTOBOTON__;
    font-size:__LETRABOTON__;
    font-weight:700;
}
.stButton > button p, .stDownloadButton > button p {
    color:__TEXTOBOTON__ !important;
    font-size:__LETRABOTON__;
    font-weight:700;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background:__TEXTO__;
    border-color:__TEXTO__;
}
.stButton > button:hover p, .stDownloadButton > button:hover p {color:__BG__ !important;}

.stButton > button:focus-visible, .stDownloadButton > button:focus-visible,
input:focus-visible, [role="radio"]:focus-visible {
    outline:4px solid __TEXTO__ !important;
    outline-offset:3px;
}

.aviso {
    padding:.8rem 1.1rem;
    border-radius:12px;
    border:2px dashed __ACENTO__;
    font-size:1rem;
}

@media (prefers-reduced-motion:reduce) {
    *, *::before, *::after {animation:none !important; transition:none !important;}
}
</style>
"""

valores = {
    "__BG__": ui["bg"],
    "__PANEL__": ui["panel"],
    "__TEXTO__": ui["texto"],
    "__ACENTO__": ui["acento"],
    "__MARCO__": ui["marco"],
    "__TEXTOBOTON__": texto_sobre(ui["acento"]),
    "__ANCHO__": str(ancho),
    "__LETRA__": "1.25rem" if grande else "1rem",
    "__SUB__": "1.4rem" if grande else "1.15rem",
    "__BOTON__": "4rem" if grande else "3.2rem",
    "__LETRABOTON__": "1.4rem" if grande else "1.1rem",
}
for k, v in valores.items():
    CSS = CSS.replace(k, v)
html(CSS)

# ============================================================
# TABLERO
# ============================================================
html(
    """
<div class="titulo">Mi pizarra a mi medida</div>
<div class="sub">Elige un perfil, una tiza y un fondo en la barra de la izquierda
y dibuja como más cómodo te resulte.</div>
"""
)

fondo_img = crear_fondo(ancho, alto, fondo, st.session_state.guia)
relleno = (
    "rgba({}, {}, {}, 0.28)".format(*a_rgb(color_trazo))
    if st.session_state.relleno and modo in FORMAS
    else "rgba(0, 0, 0, 0)"
)

opciones = dict(
    fill_color=relleno,
    stroke_width=st.session_state.grosor,
    stroke_color=color_trazo,
    background_color=fondo,
    height=alto,
    width=ancho,
    drawing_mode=modo,
    display_toolbar=False,
    key=(
        f"hoja_{st.session_state.hoja}_{ancho}x{alto}_{fondo}"
        f"_{st.session_state.guia}"
    ),
)

guia_activa = st.session_state.guia != "Sin guía"
try:
    canvas_result = st_canvas(
        background_image=fondo_img if guia_activa else None, **opciones
    )
except Exception:
    # Algunas versiones de Streamlit no admiten imágenes de fondo en el lienzo.
    guia_activa = False
    canvas_result = st_canvas(**opciones)
    html(
        '<div class="aviso">Esta versión de Streamlit no permite guías de fondo. '
        "Se usa el fondo liso.</div>"
    )

# ============================================================
# ACCIONES: guardar y borrar, con botones grandes
# ============================================================
col_guardar, col_borrar = st.columns(2, gap="large")

with col_guardar:
    if canvas_result.image_data is not None:
        capa = Image.fromarray(canvas_result.image_data.astype("uint8")).convert("RGBA")
        base = (
            fondo_img if guia_activa else Image.new("RGBA", (ancho, alto), fondo)
        ).convert("RGBA")
        if capa.size != base.size:
            capa = capa.resize(base.size)

        buffer = io.BytesIO()
        Image.alpha_composite(base, capa).convert("RGB").save(buffer, format="PNG")

        st.download_button(
            "💾 Guardar mi dibujo",
            data=buffer.getvalue(),
            file_name="mi_pizarra.png",
            mime="image/png",
        )

with col_borrar:
    if st.button("🧹 Borrar todo y empezar de nuevo"):
        st.session_state.hoja += 1
        st.rerun()
