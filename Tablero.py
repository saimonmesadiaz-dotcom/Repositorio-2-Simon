import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.title("Tablero para dibujo")

with st.sidebar:
  st. subheader("Propiedades del Tablero")
  
  # Canvas dimensions (moved to the top)
  st.subheader("Dimensiones del Tablero")
  
  # Drawing mode selector
drawing_mode = st. selectbox(
"Herramienta de Dibujo:",
