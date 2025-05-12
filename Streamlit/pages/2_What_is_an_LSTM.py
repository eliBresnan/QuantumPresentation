import streamlit as st
from PIL import Image

from images import CLSTM_code

CLSTM_diagram = Image.open("Streamlit/images/Screenshot 2025-05-01 125746.png")
RNN_diagram = Image.open("Streamlit/images/Screenshot 2025-05-12 015717.png")

st.header("Long-Short Term Memory")
st.markdown("---")
st.subheader("Recurrent Neural Network")
st.write("""
        - LSTM is a model of Recurrent Neural Network that specializes in sequential, time series data
        - Contains a cell state (the long term memory) and a hidden state (short term memory)
         """)
st.image(CLSTM_diagram, caption="Here is an example of an LSTM cell")
st.write("""
        - The Forget Block (blue box above) decides how much of the cell state to get rid of
        - The Input Block (green and yellow) decides what to add to the cell state
        - The Output Block (purple and pink) generates a new hidden state and prediction for the next time step
        - The weights are optimized during training, meaning the model is learning to what extent the previous time step affects the next
         """)
st.markdown("---")
st.image(RNN_diagram)
st.markdown("---")
st.write("""
        - The cell repeats for every time step
        - This way, the model maintains memory from each previous input, using it to determine the next output, or prediction
         """)
st.markdown("---")

st.subheader("My Classical LSTM Cell")
st.write("I began my project by making a classical LSTM cell in order to integrate quantum circuitry later on.")
st.code(CLSTM_code.code)


col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    if st.button("<< Prev"):
        st.switch_page("pages/1_Project_Overview.py")
with col2:    
    if st.button("Next >>"):
        st.switch_page("pages/3_Integrating_Quantum_Computing.py")
