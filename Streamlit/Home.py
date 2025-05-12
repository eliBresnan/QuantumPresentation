import os
import streamlit as st

dir_path = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(dir_path, "images","pbs-kids-gif-basketball.gif")

st.title("Quantum Computing Final Presentation")
st.subheader("A Quantum Nueral Network for Time Series Prediction")
st.caption("By Elijah Bresnan")
st.markdown("---")
st.image(img_path)

if st.button("Next >>"):
    st.switch_page("pages/1_Project_Overview.py")
