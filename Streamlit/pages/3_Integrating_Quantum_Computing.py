import streamlit as st
from PIL import Image

from images import QLSTM_code

QLSTM_diagram = Image.open("Streamlit\images\Screenshot 2025-05-01 125905.png")
CLSTM_diagram = Image.open("Streamlit\images\Screenshot 2025-05-01 125854.png")
Circuit_diagram = Image.open("Streamlit\images\Screenshot 2025-05-01 130335.png")


st.title("Quantum Circuitry in an LSTM")
st.markdown("---")

show_qlstm = st.toggle("Integrate Quantum Circuits")

if show_qlstm:
    st.image(QLSTM_diagram)
else:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.image(CLSTM_diagram)

st.markdown("---")
st.subheader("What's the Difference?")
st.write("""
        - Instead of weighing the hidden state and input and adding them together at each gate, they are concatenated and encoded into a quantum circuit
            - The qubits are entangled, allowing the computations to find correlations between data that cannot be done classically
            - The weights are applied via rotations in 3 dimensions
        - Additionally, the output diverges to two different circuits for post-processing, allowing the new hidden state and the prediction to be independent
         """)
st.markdown("---")

st.subheader("The Circuit")
st.write("""
        - There are 6 quantum circuits in a QLSTM cell
            - One qubit is required for each data point in an input vector
        - The qubits are superposed, then the data is encoded via angle encoding (more on that later)
        - The variational layer (in the dotted box below), entangles the qubits and applies rotations in three dimensions as weights 
            - This layer can be repeated as desired to increase granularity and precision (circuit depth)
         """)
st.image(Circuit_diagram)

st.markdown("---")
st.subheader("My QLSTM Code")
st.write("I made my model from scratch, closely following the procedures described by scholars Samuel Yen-Chi Chen, Shinjae Yoo, and Yao-Lung L. Fang in their 2020 paper *Quantum Long Short-Term Memory*")
st.write("Here is the code for my cell and circuit objects.")

code_block = st.radio("Show Code Block",("QLSTM Cell","Variational Quantum Ciruit"))
if code_block == "QLSTM Cell":
    st.code(QLSTM_code.lstm_code)
else:
    st.code(QLSTM_code.circuit_code) 


col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    if st.button("<< Prev"):
        st.switch_page("pages/2_What_is_an_LSTM.py")
with col2:    
    if st.button("Next >>"):
        st.switch_page("pages/4_Data.py")
