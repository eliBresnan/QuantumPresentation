import streamlit as st
from PIL import Image

image_1 = Image.open("images/cool_basketball_photo.webp")
image_2 = Image.open("images/hq720.jpg")

st.title("Project Overview")
st.markdown("---")

placeholder = st.empty()

show_abstract = st.checkbox("Wishful Thinking", value=True)

with placeholder.container():
    if show_abstract:
        st.subheader("Abstract")
        st.write("This project will examine the prediction capabilities of quantum machine learning. Using a neural network built from simulated quantum circuits, the program will be trained, under supervision, with NBA statistics to predict the outcome of basketball games. This data will include player statistics and conditions as well as coaching staff, location, and time.")
        st.write("Traditional neural networks have been widely used for predictive modeling, but they struggle with the complexity and high-dimensionality of the data. Utilizing quantum principles like superposition and entanglement, a neural network can analyze data and recognize relationships that a classical computer cannot. The success of the QNN will be determined by comparing the results with that of an identically trained classical neural network.")
        st.image(image_1)
    else:
        st.subheader("How it Turned Out")
        st.image(image_2)
        st.markdown("---")
        st.subheader("What I Was Able To Do")
        st.write("""
            - Build a classical lstm cell
            - Build a functional quantum lstm system from scratch
            - Use a simulated quantum circuit to perform computations on NBA data
            - Theoretically make predictions on game outcomes using time series training

            """)

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    if st.button("<< Prev"):
        st.switch_page("Home.py")
with col2:    
    if st.button("Next >>"):
        st.switch_page("pages/2_What_is_an_LSTM.py")  


