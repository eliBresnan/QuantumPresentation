import streamlit as st

st.title("Quantum Computing Final Presentation")
st.subheader("A Quantum Nueral Network for Time Series Prediction")
st.caption("By Elijah Bresnan")
st.markdown("---")
st.image("images\pbs-kids-gif-basketball.gif")

if st.button("Next >>"):
    st.switch_page("pages/1_Project_Overview.py")
