import streamlit as st
import time

st.title("Gedanken-Scanner")
st.write("Code eingeben und Karte wählen:")

if 'output' not in st.session_state:
    st.session_state.output = ''

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Pik-Ass wählen"):
        st.session_state.output = 'Scanne...'
        with st.spinner('Scanne Gedanken...'):
            time.sleep(1)
            st.session_state.output = "Signal-Resonanz 100%<br>Ergebnis: Pik-Ass"

with col2:
    if st.button("Dame Pik wählen"):
        st.session_state.output = 'Scanne...'
        with st.spinner('Scanne Gedanken...'):
            time.sleep(1)
            st.session_state.output = "Signal-Resonanz 98%<br>Abweichung: +1 Position<br>Resonanzkarte: Pik-Ass"

with col3:
    if st.button("6 Pik wählen"):
        st.session_state.output = 'Scanne...'
        with st.spinner('Scanne Gedanken...'):
            time.sleep(1)
            st.session_state.output = "Signal-Resonanz 95%<br>Abweichung: -1 Position<br>Resonanzkarte: Pik-Ass"

if st.session_state.output:
    st.markdown(st.session_state.output, unsafe_allow_html=True)